import fiepipelib.assetdata.shell
import fiepipe3dcoat.data.workfile
import fiepipe3dcoat.coat
import fiepipelib.assetdata.shell.item
import fiepipelib.fileversion.shell.assetdata
import fiepipelib.localplatform.routines.localplatform
import fiepipelib.localuser.routines.localuser
from fiepipelib.assetdata.data.connection import Connection, GetConnection
from fiepipelib.gitstorage.shells.gitasset import Shell
from fiepipelib.fileversion.data.fileversion import AbstractFileVersion

class WorkFilesCommand(fiepipelib.assetdata.shell.item.AbstractNamedItemCommand):
    
    def getPluginNamesV1(self):
        ret = super().getPluginNamesV1()
        ret.append("coat_workfiles_command")
        return ret
        
    def GetDataPromptCrumbText(self):
        return "workfiles"
    
    def GetShell(self, item:fiepipe3dcoat.data.workfile.WorkFile):
        return WorkFileShell(self.GetAssetShell(),item)
        
    def GetMultiManager(self):
        return fiepipe3dcoat.data.workfile.WorkFileDB(
            self.GetGitWorkingAsset())
    
    def GetManager(self, db:fiepipe3dcoat.data.workfile.WorkFileDB):
        return db.GetWorkFileManager()
    
    def DeleteItem(self, name:str, 
                  man:fiepipe3dcoat.data.workfile.WorkFileManager, 
                  conn:Connection):
        man.DeleteByName(name, conn)
        
    def do_create(self, args):
        """Creates a new 3dCoat workfile.
        
        Usage: create [name]
        
        arg name: A new name for the new workfile.
        
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
        
        item = man.NewFromParameters(args[0], {})
        man.Set([item],conn)
        conn.Commit()
        conn.Close()
    
    def ItemToName(self, item:fiepipe3dcoat.data.workfile.WorkFile):
        return item._name
    
    def GetAllItems(self, 
                   man:fiepipe3dcoat.data.workfile.WorkFileManager, 
                   conn:Connection):
        return man.GetAll( conn)
    
    def GetItemByName(self, name, 
                     man:fiepipe3dcoat.data.workfile.WorkFileManager, 
                     conn:Connection):
        return man.GetByName(name, conn)[0]
    

class WorkFileShell(fiepipelib.assetdata.shell.item.ItemShell):
    
    _workFile = None
    
    def GetWorkFile(self):
        return self._workFile
    
    def __init__(self, gitAssetShell:Shell, workFile:fiepipe3dcoat.data.workfile.WorkFile):
        self._workFile = workFile
        super().__init__(gitAssetShell)
        self.AddSubmenu(WorkFileVerionsCommand( gitAssetShell,self), "versions", [])
    
    def getPluginNamesV1(self):
        ret = super().getPluginNamesV1()
        ret.append("coat_workfile_version_shell")
        return ret
    
    def GetDataPromptCrumbText(self):
        return self._workFile._name
    

class WorkFileVerionsCommand(fiepipelib.fileversion.shell.assetdata.AbstractSingleFileVersionCommand):
    
    _workfileShell = None
    
    def GetWorkFileShell(self) -> WorkFileShell:
        return self._workfileShell
    
    def __init__(self, Shell, workFileShell:WorkFileShell):
        self._workfileShell = workFileShell
        super().__init__(gitAssetShell)
        
    def GetFileExtension(self):
        return "3b"
    
    def coat_complete(self, text, line, begidx, endidx):
        ret = []
        plat = fiepipelib.localplatform.routines.localplatform.get_local_platform_routines()
        user = fiepipelib.localuser.routines.localuser.LocalUserRoutines(plat)
        coatman = fiepipe3dcoat.coat.CoatLocalManager(user)
        allCoats = coatman.GetAll()
        for coat in allCoats:
            assert isinstance(coat, fiepipe3dcoat.coat.coat)
            if coat.GetName().startswith(text):
                ret.append(coat.GetName())
        return ret

    def GetVersionedUp(self, 
                      oldVer:fiepipe3dcoat.data.workfile.WorkFileVersion, 
                      newVerName:str):
        db = self.GetMultiManager()
        man = self.GetManager(db)
        return man.NewFromParameters(oldVer.GetWorkFileName(), newVerName)
    
    
    def complete_send_to_3dcoat(self, text, line, begidx, endidx):
        return self.index_based_complete(text, line, begidx, endidx,{1:self.type_complete})
            
    def do_send_to_3dcoat(self, args):
        """Sends this version to 3dCoat via AppLink
        
        Usage: send_to_3dcoat [version]
        
        arg version: the name of the version to send.
        """
        
        args = self.ParseArguments(args)
        
        if len(args) == 0:
            self.perror("No version specified.")
            return

        conn = GetConnection(self.GetGitWorkingAsset())
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
        
        models = [fiepipe3dcoat.applink.standard.Mesh(version.GetAbsolutePath())]
        outModel = fiepipe3dcoat.applink.standard.Mesh(version.GetAbsolutePath())
        mode = fiepipe3dcoat.applink.standard.Mode(fiepipe3dcoat.applink.standard.Mode.MODE_3B)
        
        fiepipe3dcoat.applink.standard.StartRoundTrip(
                                                     models, 
                                                     outModel, 
                                                     mode, 
                                                     [])
        #3B mode never creates an export.
        
    def getPluginNamesV1(self):
        ret = super().getPluginNamesV1()
        ret.append("coat_workfile_versions_command")
        return ret
    
    def GetDataPromptCrumbText(self):
        return self.GetWorkFileShell().GetWorkFile()._name + ":versions"
    
    def GetShell(self, item:fiepipe3dcoat.data.workfile.WorkFileVersion):
        return WorkFileVersionShell(self.GetGitWorkingAsset(), item)
        
    def GetMultiManager(self):
        return fiepipe3dcoat.data.workfile.WorkFileDB(
            self.GetGitWorkingAsset())
    
    def GetManager(self, db:fiepipe3dcoat.data.workfile.WorkFileDB) -> fiepipe3dcoat.data.workfile.WorkFileVersionManager:
        return db.GetWorkFileVersionManager()
    
    def DeleteItem(self, name:str, 
                  man:fiepipe3dcoat.data.workfile.WorkFileVersionManager, 
                  conn:Connection):
        man.DeleteByVersion(self.GetWorkFileShell().GetWorkFile()._name,
                            name, conn)

    def do_create(self, args):
        """Creates a new 3dcoat workfile version.
        
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
            man.NewFromParameters(self.GetWorkFileShell().GetWorkFile()._name,
                                  args[0])
        
        man.Set([item],conn)
        conn.Commit()
        conn.Close()
    
    def GetAllItems(self, 
                   manager:fiepipe3dcoat.data.workfile.WorkFileVersionManager, 
                   conn:Connection):
        return manager.GetByWorkFile(self.GetWorkFileShell().GetWorkFile()._name,
                              conn)
        
    def GetItemByName(self, name, 
                     manager:fiepipe3dcoat.data.workfile.WorkFileVersionManager, 
                     conn:Connection):
        return manager.GetByVersion(self.GetWorkFileShell().GetWorkFile()._name,
                                   name, conn)[0]
    
    
        

class WorkFileVersionShell(fiepipelib.fileversion.shell.assetdata.AbstractSingleFileVersionShell):
    
    _workfileShell = None
    
    def GetWorkFileShell(self) ->  WorkFileShell:
        return self._workfileShell
    
    def __init__(self, gitAssetShell:Shell,
                version:AbstractFileVersion, workFileShell:WorkFileShell):
        self._workfileShell = workFileShell
        super().__init__(gitAssetShell,version)
    
    def getPluginNamesV1(self):
        ret = super().getPluginNamesV1()
        ret.append("coat_workfile_version_shell")
        return ret
    
    def GetDataPromptCrumbText(self):
        return self.GetVersion().GetFullName()
