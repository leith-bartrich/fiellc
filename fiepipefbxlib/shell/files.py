import fiepipedesktoplib.assetdata.shell
import fiepipefbxlib.data.common
import fiepipedesktoplib.assetdata.shell.item


class ListShell(fiepipedesktoplib.assetdata.shell.item.ItemShell):
    
    _list = None
    
    def GetList(self) -> fiepipefbxlib.data.common.FBXFileList:
        return _list
    
    def __init__(self, gitAssetShell:fiepipedesktoplib.shells.gitasset.Shell, lst:fiepipefbxlib.data.common.FBXFileList):
        self._list = lst
        super().__init__(gitAssetShell)
        
    def getPluginNamesV1(self):
        return "fbx_file_list_shell"
    
    def GetDataPromptCrumbText(self):
        return self.GetList().GetName()

class ListsCommand(fiepipedesktoplib.assetdata.shell.item.AbstractNamedItemCommand):
    
    def getPluginNameV1(self):
        return "fbx_file_lists_command"

    def GetDataPromptCrumbText(self):
        return ('lists')
    
    def GetShell(self, item):
        assert isinstance(item, fiepipefbxlib.data.common.FBXFileList)
        return ListShell(self.GetAssetShell(), item)
    
    def GetMultiManager(self):
        return fiepipefbxlib.data.common.FBXLibDatabase(
            self.GetGitWorkingAsset())
    
    def GetManager(self, db) -> fiepipefbxlib.data.common.FBXFileListManager:
        assert isinstance(db, fiepipefbxlib.data.common.FBXLibDatabase)
        return db.GetFileListManager()
    
    def DeleteItem(self, name:str, 
                  man:fiepipelib.assetdata.abstractassetdata.abstractdatamanager, 
                  conn:fiepipelib.assetdata.assetdatabasemanager.Connection):
        assert isinstance(man,fiepipefbxlib.data.common.FBXFileListManager)
        man.DeleteByName(name, conn)
        
    def do_create(self, args):
        """Creates a new FBX File List.
        
        Usage: create [name]
        
        arg name: A new name for the new list.
        
        Errors if the name already exists.
        """
        
        args = self.ParseArguments(args)
        
        if len(args) == 0:
            self.perror("No name given.")
            return

        desc = self.AskStringQuestion("List Description")
        
        conn = self.GetConnection()
        db = self.GetMultiManager()
        man = self.GetManager(db)
        db.AttachToConnection( conn)
        
        if len(man.GetByName(args[0], conn)) != 0:
            self.perror("Already exists.")
            return
        
        item = man.NewListFromParameters(args[0], desc)
        
        man.Set([item],conn)
        conn.Commit()
        conn.Close()
    
    def ItemToName(self, item:fiepipefbxlib.data.common.FBXFileList):
        return item.GetName()
    
    def GetAllItems(self, 
                   manager:fiepipefbxlib.data.common.FBXFileManager, 
                   conn:fiepipelib.assetdata.assetdatabasemanager.Connection):
        return manager.GetAll(conn)
        
    def GetItemByName(self, name,
                      manager:fiepipefbxlib.data.common.FBXFileManager,
                      conn:fiepipelib.assetdata.assetdatabasemanager.Connection):
        return manager.GetByName(name, conn)[0]


    def complete_print(self, text, line, begidx, endidx):
        return self.index_based_complete(text, line, begidx, endidx,
                                         {1,self.type_complete})
    def do_print(self, args):
        """Prints the list.
        Usage: print [listName]
        arg listName:  The name of the list to print.
        """
        args = self.ParseArguments(args)
        if len(args) < 1:
            self.perror("No list specified.")
            return
            
        conn = fiepipelib.assetdata.assetdatabasemanager.GetConnection(self.GetGitWorkingAsset())
        db = fiepipefbxlib.data.common.FBXLibDatabase(self.GetGitWorkingAsset())
        db.AttachToConnection( conn)
        listman = db.GetFileListManager()
        
        assert isinstance(listman, fiepipefbxlib.data.common.FBXFileListManager)
        lsts = listman.GetByName(args[0], conn)
        
        if len(lsts) == 0:
            self.perror("No such list: " + args[0])
            return
        
        lst = lsts[0]
        assert isinstance(lst, fiepipefbxlib.data.common.FBXFileList)
        self.poutput("FBX File List: " + lst.GetName())
        self.poutput("Description: ")
        self.ppaged(lst.GetDescription())
        
        listentryman = db.GetFileListEntryManager()
        assert isinstance(listentryman,fiepipefbxlib.data.common.FBXFileListEntryManager)
        
        entries = listentryman.GetByFirst(lst, conn)
        for e in entries:
            assert isinstance(e, fiepipefbxlib.data.common.FBXFileListEntry)
            fbxfile = e.GetFBXFile( conn)[0]
            assert isinstance(fbxfile,fiepipefbxlib.data.common.FBXFile)
            self.poutput(fbxfile.GetName())

        conn.Close()
        
        