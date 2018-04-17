import fiepipelib.shells.gitasset
import fiepipefreecad.data.partdesign
import cmd2
import pathlib
import os
import os.path
import shutil
import fiepipefreecad.commands.system
import fiepipelib.shells.abstract
import abc
import fiepipelib.assetdata.shell

def GetFreeCADFileExtension():
    return "FCStd"

def freecad_complete(text, line, begidx, endidx):
    ret = []
    plat = fiepipelib.localplatform.GetLocalPlatform()
    user = fiepipelib.localuser.localuser(plat)
    fcman = fiepipefreecad.freecad.FreeCADLocalManager(user)
    allfcads = fcman.GetAll()
    for fcad in allfcads:
        assert isinstance(fcad, fiepipefreecad.freecad.FreeCAD)
        if fcad.GetName().startswith(text):
            ret.append(fcad.GetName())
    return ret


class AbstractFreeCADFileVersionsCommand(fiepipelib.assetdata.shell.AbstractSingleFileVersionCommand):
    
    def GetFileExtension(self):
        return GetFreeCADFileExtension()

    def freecad_complete(self, text, line, begidx, endidx):
        return freecad_complete(text, line, begidx, endidx)
            
    def GetVersionedUp(self,
                       oldVer:fiepipefreecad.data.partdesign.PartDesignVersion,
                       newVerName:str):
        ret = fiepipefreecad.data.partdesign.PartDesignVersionFromParameters(
            oldVer.GetPartDesignName(), 
            newVerName, 
            self._gitAssetShell._workingAsset)
        return ret
            
    def complete_open(self, text, line, begidx, endidx):
        return self.index_based_complete(text, line, begidx, endidx,{1:self.type_complete,2:self.freecad_complete})
            
    def do_open(self, args):
        """Opens this version in FreeCAD
        
        Usage: open [version] [freecad]
        
        arg version: the name of the version to open.
        arg freecad: The name of the freecad to open this part design version with.
        """
        
        args = self.ParseArguments(args)
        
        if len(args) == 0:
            self.perror("No version specified.")
            return
        if len(args) == 1:
            self.perror("No freecad specified.")
            return

        conn = fiepipelib.assetdata.assetdatabasemanager.GetConnection(self.GetGitWorkingAsset())
        db = self.GetMultiManager()
        man = self.GetManager(db)
        db.AttachToConnection(conn)
            
        version = self.GetItemByName(args[0], man, conn)
        
        if version == None:
            self.perror("Version does not exist.")
            return
                        
        if not version.FileExists():
            self.perror("File does not exist.")
            return
        
        fcman = fiepipefreecad.freecad.FreeCADLocalManager(self.GetAssetShell()._localUser)
        freecads = fcman.GetByName(args[1])

        if len(freecads) == 0:
            self.perror("No such freecad.")
            return
        
        freecad = freecads[0]
        assert isinstance(freecad, fiepipefreecad.freecad.FreeCAD)
        freecad.LaunchInteractive(filepaths=[version.GetAbsolutePath()])


class PartDesignsCommand(fiepipelib.assetdata.shell.AbstractNamedTypeCommand):

    def getPluginNameV1(self):
        return "freecad_part_designs_command"

    def GetDataPromptCrumbText(self):
        return ('part_designs')
    
    def GetShell(self, item):
        assert isinstance(item, fiepipefreecad.data.partdesign.PartDesign)
        return PartDesignShell(self.GetAssetShell(), item)
    
    def GetMultiManager(self):
        return fiepipefreecad.data.partdesign.PartDesignDB(
            self.GetGitWorkingAsset())
    
    def GetManager(self, db):
        assert isinstance(db, fiepipefreecad.data.partdesign.PartDesignDB)
        return db.GetPartDesignManager()
    
    def DeleteItem(self, name:str, 
                  man:fiepipelib.assetdata.abstractassetdata.abstractdatamanager, 
                  conn:fiepipelib.assetdata.assetdatabasemanager.Connection):
        assert isinstance(man, fiepipefreecad.data.partdesign.PartDesignManager)
        man.DeleteByName(name, conn)
        
    def do_create(self, args):
        """Creates a new Part Design.
        
        Usage: create [name]
        
        arg name: A new name for the new part.
        
        Errors if the name already exists.
        """
        
        args = self.ParseArguments(args)
        
        if len(args) == 0:
            self.perror("No name given.")
            return
        
        conn = self.GetConnection()
        db = self.GetMultiManager()
        man = self.GetManager(db)
        db.AttachToConnection( conn)

        if len(man.GetByName(args[0], conn)) != 0:
            self.perror("Already exists.")
            return
        
        item = fiepipefreecad.data.partdesign.PartDesignFromParameters( args[0], self.GetGitWorkingAsset())
        man.Set([item],conn)
        conn.Commit()
        conn.Close()
    
    def ItemToName(self, item):
        assert isinstance(item, fiepipefreecad.data.partdesign.PartDesign)
        return item.GetName()
    
    def GetAllItems(self, 
                   manager:fiepipelib.assetdata.abstractassetdata.abstractdatamanager, 
                   conn:fiepipelib.assetdata.assetdatabasemanager.Connection):
        assert isinstance(manager, fiepipefreecad.data.partdesign.PartDesignManager)
        return manager.GetAll(conn)
        
    def GetItemByName(self, name, 
                     manager:fiepipelib.assetdata.abstractassetdata.abstractdatamanager, 
                     conn:fiepipelib.assetdata.assetdatabasemanager.Connection):
        assert isinstance(manager, fiepipefreecad.data.partdesign.PartDesignManager)
        return manager.GetByName(name, conn)[0]
        

class PartDesignShell(fiepipelib.assetdata.shell.AssetShell):
    
    _partDesign = None
    
    def __init__(self, gitAssetShell:fiepipelib.shells.gitasset.Shell, partDesign:fiepipefreecad.data.partdesign.PartDesign):
        self._partDesign = partDesign
        super().__init__(gitAssetShell)
        self.AddSubmenu(PartDesignVersionsCommand( gitAssetShell, self),
                        "versions", [])

    def getPluginNameV1(self):
        return "freecad_part_design_shell"
        
    def GetDataPromptCrumbText(self):
        return (self._partDesign.GetName())
    


class PartDesignVersionsCommand(AbstractFreeCADFileVersionsCommand):

        
    _partDesignShell = None
    
    def __init__(self, gitAssetShell:fiepipelib.shells.gitasset.Shell, partDesignShell:PartDesignShell):
        self._partDesignShell = partDesignShell
        self._templates = {}
        super().__init__(gitAssetShell)

    def getPluginNameV1(self):
        return "freecad_part_design_versions_command"

    def GetDataPromptCrumbText(self):
        return ('part_design_versions')
     
    def GetShell(self, item):
        assert isinstance(item, fiepipefreecad.data.partdesign.PartDesignVersion)
        return PartDesignVersionShell(self.GetAssetShell(), self._partDesignShell, item)
    
    def GetMultiManager(self):
        return fiepipefreecad.data.partdesign.PartDesignDB(
            self.GetGitWorkingAsset())
    
    def GetManager(self, db):
        assert isinstance(db, fiepipefreecad.data.partdesign.PartDesignDB)
        return db.GetPartDesignVersionManager()
    
    def DeleteItem(self, name:str, 
                  man:fiepipelib.assetdata.abstractassetdata.abstractdatamanager, 
                  conn:fiepipelib.assetdata.assetdatabasemanager.Connection):
        assert isinstance(man, fiepipefreecad.data.partdesign.PartDesignVersionManager)
        i = self.GetItemByName(name, man,conn)
        p = pathlib.Path(i.GetAbsolutePath())
        if p.exists():
            p.unlink()
        man.DeleteByPartAndVersion(self._partDesignShell._partDesign.GetName(), name, conn)
        
        
        
    def do_create(self, args):
        """Creates a new Part Design Version.
        
        Usage: create [ver]
        
        arg ver: A new version name for the version. e.g. 01, v01, 1.0, beta, 1.0.0a
        
        Errors if the name already exists.
        """
        
        args = self.ParseArguments(args)
        
        if len(args) == 0:
            self.perror("No version given.")
            return
        
        conn = self.GetConnection()
        db = self.GetMultiManager()
        man = self.GetManager(db)
        db.AttachToConnection( conn)
        
        
        try:
            self.GetItemByName(args[0], man, conn)
            self.perror("Already exists")
            return
        except LookupError:
            pass
        
        item =\
            fiepipefreecad.data.partdesign.PartDesignVersionFromParameters(
                self._partDesignShell._partDesign.GetName(), args[0],
                self.GetGitWorkingAsset())
        man.Set([item],conn)
        conn.Commit()
        conn.Close()
    
    def ItemToName(self, item):
        assert isinstance(item, fiepipefreecad.data.partdesign.PartDesignVersion)
        return item.GetVersion()
    
    def GetAllItems(self, 
                   manager:fiepipelib.assetdata.abstractassetdata.abstractdatamanager, 
                   conn:fiepipelib.assetdata.assetdatabasemanager.Connection):
        assert isinstance(manager, fiepipefreecad.data.partdesign.PartDesignVersionManager)
        return manager.GetByPart(self._partDesignShell._partDesign.GetName(), conn)
        
    def GetItemByName(self, name, 
                     manager:fiepipelib.assetdata.abstractassetdata.abstractdatamanager, 
                     conn:fiepipelib.assetdata.assetdatabasemanager.Connection) -> fiepipefreecad.data.partdesign.PartDesignVersion:
        assert isinstance(manager, fiepipefreecad.data.partdesign.PartDesignVersionManager)
        return manager.GetByPartAndVersion(self._partDesignShell._partDesign.GetName(),
                                          name, conn)[0]
    
            
        

class PartDesignVersionShell(fiepipelib.assetdata.shell.AssetShell):
    
    _partDesignShell = None
    _version = None

    def __init__(self, gitAssetShell:fiepipelib.shells.gitasset.Shell, partDesignShell:PartDesignShell, version:fiepipefreecad.data.partdesign.PartDesignVersion):
        self._version = version
        self._partDesignShell = partDesignShell
        super().__init__(gitAssetShell)
        
    def getPluginNameV1(self):
        return "freecad_part_design_version_shell"
        
    def GetBreadCrumbsText(self):
        return self.breadcrumbs_separator.join([self._gitAssetShell.GetBreadCrumbsText(),"fc_pd",self._version.GetFullName()])

    
        
        
