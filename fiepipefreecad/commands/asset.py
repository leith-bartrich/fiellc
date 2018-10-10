import fiepipelib.assetdata.shell.item
import fiepipelib.filerepresentation.shell.item
import fiepipelib.fileversion.shell.assetdata
import fiepipelib.gitstorage.shells.gitasset
import fiepipefreecad.data.partdesign
import pathlib
import os
import os.path
import fiepipefreecad.commands.manager
import fiepipelib.assetdata.shell
import fiepipefreecad.scripts.util
from fiepipelib.assetdata.data.items import AbstractItemsRelation,AbstractItemManager
from fiepipelib.assetdata.data.connection import Connection, GetConnection

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


class AbstractFreeCADFileVersionsCommand(fiepipelib.fileversion.shell.assetdata.AbstractSingleFileVersionCommand):
        
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
        freecads = fcman.get_by_name(args[1])

        if len(freecads) == 0:
            self.perror("No such freecad.")
            return
        
        freecad = freecads[0]
        assert isinstance(freecad, fiepipefreecad.freecad.FreeCAD)
        freecad.LaunchInteractive(filepaths=[version.GetAbsolutePath()])


class PartDesignsCommand(fiepipelib.assetdata.shell.item.AbstractNamedItemCommand):

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
                  man:AbstractItemManager,
                  conn:Connection):
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

        if len(man.get_by_name(args[0], conn)) != 0:
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
                   manager:AbstractItemManager,
                   conn:Connection):
        assert isinstance(manager, fiepipefreecad.data.partdesign.PartDesignManager)
        return manager.GetAll(conn)
        
    def GetItemByName(self, name, 
                     manager:AbstractItemManager,
                     conn:Connection):
        assert isinstance(manager, fiepipefreecad.data.partdesign.PartDesignManager)
        return manager.GetByName(name, conn)[0]
        

class PartDesignShell(fiepipelib.assetdata.shell.item.ItemShell):
    
    _partDesign = None
    
    def __init__(self, gitAssetShell: fiepipelib.gitstorage.shells.gitasset.Shell, partDesign:fiepipefreecad.data.partdesign.PartDesign):
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
    
    def __init__(self, gitAssetShell: fiepipelib.gitstorage.shells.gitasset.Shell, partDesignShell:PartDesignShell):
        self._partDesignShell = partDesignShell
        self._templates = {}
        super().__init__(gitAssetShell)

    def getPluginNameV1(self):
        return "freecad_part_design_versions_command"

    def GetDataPromptCrumbText(self):
        return ('part_design_versions')
     
    def GetShell(self, item):
        assert isinstance(item, fiepipefreecad.data.partdesign.PartDesignVersion)
        return PartDesignVersionShell(self._partDesignShell, item)
    
    def GetMultiManager(self):
        return fiepipefreecad.data.partdesign.PartDesignDB(
            self.GetGitWorkingAsset())
    
    def GetManager(self, db):
        assert isinstance(db, fiepipefreecad.data.partdesign.PartDesignDB)
        return db.GetPartDesignVersionManager()
    
    def DeleteItem(self, name:str, 
                  man:fiepipefreecad.data.partdesign.PartDesignVersionManager, 
                  conn:Connection):
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
    
    def GetAllItems(self, 
                   manager:AbstractItemManager,
                   conn:Connection):
        assert isinstance(manager, fiepipefreecad.data.partdesign.PartDesignVersionManager)
        return manager.GetByPart(self._partDesignShell._partDesign.GetName(), conn)
        
    def GetItemByName(self, name, 
                     manager:AbstractItemManager,
                     conn:Connection) -> fiepipefreecad.data.partdesign.PartDesignVersion:
        assert isinstance(manager, fiepipefreecad.data.partdesign.PartDesignVersionManager)
        return manager.GetByPartAndVersion(self._partDesignShell._partDesign.GetName(),
                                          name, conn)[0]
    
    def complete_dump_representation_obj_dir(self, text,line,begidx,endidx):
        return self.index_based_complete(text, line, begidx, endidx,
                                         {1:self.type_complete,2:self.freecad_complete})
    
    def do_dump_representation_obj_dir(self, args):
        """Dumps a representation of this version as a directory of named obj files
        to a represenation named 'obj_dir'
        
        Usage dump_representation_obj_dir [version] [freecad]
        
        arg version: The name of the version to dump.
        
        arg freecad: the name of the freecad to use.
        
        Will empty the directory of obj files and refill it, if it already exists.
        
        Will create and/or update the representation data.
        """
        args = self.ParseArguments(args)
        if len(args) == 0:
            self.perror("No version specified.")
            return
        
        if len(args) == 1:
            self.perror("No FreeCAD specified.")
            return
        
        conn = self.GetConnection()
        db = self.GetMultiManager()
        db.AttachToConnection(conn)
        man = self.GetManager(db)
        
        v = self.GetItemByName(args[0], man, conn)
        
        repman = db.GetPartRepresentationManager()
        
        r = fiepipefreecad.data.partdesign.RepresentationFromParameters(
            "obj_dir", 
            "obj_dir", 
            v.GetPartDesignName(), 
            v.GetVersion())
        
        absPath = r.GetAbsolutePath(v)
        
        if os.path.exists(absPath):
            for efname in os.listdir(absPath):
                p = pathlib.Path(os.path.join(absPath,efname))
                if p.suffix.lower() == ".obj":
                    p.unlink()
                
        fcadman = fiepipefreecad.freecad.FreeCADLocalManager(self._gitAssetShell._localUser)
        fcads = fcadman.get_by_name(args[1])
        
        if len(fcads) == 0:
            self.perror("No such FreeCAD.")
            return
        
        fcad = fcads[0]
        
        scriptPath = fiepipefreecad.scripts.util.GetScriptPath("partstoobj.py")
        
        assert isinstance(fcad, fiepipefreecad.freecad.FreeCAD)
        fcad.ExecuteInConsoleMode(filepaths=[v.GetAbsolutePath(),scriptPath])
        #fcad.LaunchInteractive(filepaths=[v.GetAbsolutePath(),scriptPath])
        
        repman.Set([r], conn)
        conn.Commit()
        conn.Close()
        
        

class PartDesignVersionShell(fiepipelib.fileversion.shell.assetdata.AbstractSingleFileVersionShell):
    
    _partDesignShell = None

    def __init__(self, partDesignShell:PartDesignShell, version:fiepipefreecad.data.partdesign.PartDesignVersion):
        self._partDesignShell = partDesignShell
        super().__init__(partDesignShell.GetAssetShell(), version)
        self.AddSubmenu(RepresentationsCommand( partDesignShell.GetAssetShell(), self),
                        "representations", [])
        
    def getPluginNamesV1(self):
        ret = super().getPluginNamesV1()
        ret.append("freecad_part_design_version_shell")
        return ret
        
    def GetBreadCrumbsText(self):
        return self.breadcrumbs_separator.join([self.GetAssetShell().get_prompt_text(), "fc_pd", self._version.GetFullName()])

class RepresentationsCommand(fiepipelib.filerepresentation.shell.item.AbstractSingleFileRepresentationsCommand):
    
    def getPluginNamesV1(self):
        ret = super().getPluginNamesV1()
        ret.append("freecad_part_design_representations_command")
        return ret

    def GetShell(self, item):
        assert isinstance(item, fiepipefreecad.data.partdesign.Representation)
        return RepresentationShell(self.GetAssetShell(), item)
    
    def GetMultiManager(self):
        return fiepipefreecad.data.partdesign.PartDesignDB(
            self.GetGitWorkingAsset())
    
    def GetManager(self, db):
        assert isinstance(db, fiepipefreecad.data.partdesign.PartDesignDB)
        return db.GetPartRepresentationManager()
    
    def DeleteItem(self, name:str, 
                  man:AbstractItemManager,
                  conn:Connection):
        assert isinstance(man, fiepipefreecad.data.partdesign.RepresentationManager)
        i = self.GetItemByName(name, man,conn)
        i.DeleteFiles(self._versionShell._version)
        man.DeleteByName(self._versionShell._version.GetPartDesignName(),self._versionShell._version.GetVersion(),name, conn)
    
    
    def GetAllItems(self, 
                   manager:AbstractItemManager,
                   conn:Connection):
        assert isinstance(manager, fiepipefreecad.data.partdesign.RepresentationManager)
        return manager.GetByPartAndVersion(self._versionShell._version.GetPartDesignName(),
                                    self._versionShell._version.GetVersion(), conn)
        
        
class RepresentationShell(fiepipelib.filerepresentation.shell.item.AbstractRepresentationShell):
    
    def __init__(self, partDesignVersionShell:PartDesignVersionShell, representation:fiepipefreecad.data.partdesign.Representation):
        super().__init__(partDesignVersionShell,representation)
        
    def getPluginNameV1(self):
        return "freecad_part_design_representation_shell"
        
    def GetBreadCrumbsText(self):
        return self.breadcrumbs_separator.join([self._partDesignVersionShell.get_prompt_text(), self._representation._name])
