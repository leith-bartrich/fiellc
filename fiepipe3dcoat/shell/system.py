import fiepipelib.locallymanagedtypes.shells.AbstractLocalManagedTypeCommand
import fiepipelib.shells.AbstractShell
import pathlib
import fiepipe3dcoat.coat
import fiepipelib.localuser.routines.localuser
import cmd2

class CoatSystemCommand(fiepipelib.locallymanagedtypes.shells.AbstractLocalManagedTypeCommand.LocalManagedTypeCommand):
    
    def __init__(self, localUser: fiepipelib.localuser.routines.localuser.LocalUserRoutines):
        super().__init__(localUser)
        
    def getPluginNameV1(self):
        return "coat_system_command"
    
    def GetBreadCrumbsText(self):
        return self.prompt_separator.join(["pipe", "3dcoat"])
    
    def GetManager(self):
        return fiepipe3dcoat.coat.CoatLocalManager(self.get_user())
    
    def GetAllItems(self):
        return self.GetManager().GetAll()
    
    def GetItemByName(self, name):
        return self.GetManager().GetByName(name)[0]
    
    def GetShell(self, item):
        raise NotImplementedError("3DCoat command does not support 'enter' at this time.")
    
    def ItemToName(self, item):
        assert isinstance(item, fiepipe3dcoat.coat.coat)
        return item.GetName()
    
    def DeleteItem(self, name:str):
        self.GetManager().DeleteByName(name)
        
    complete_create = cmd2.Cmd.path_complete

    def do_create(self: fiepipelib.shells.AbstractShell.AbstractShell, args):
        """Adds a 3dcoat instance to the User's 3dCoat preferences.
        
        usage: create [path]
        
        arg path: The path to a 3DCoat executable.
        """
        args = cmd2.parse_quoted_string(args)
        if len(args) == 0:
            self.perror("No path specified.")
            return
        path = pathlib.Path(args[0])
        if not path.exists():
            self.perror("Does not exist.")
            return
        if not path.is_file():
            self.perror("Is not a file.")
            return
        
        name = self.AskStringQuestion("Name")
        
        c3d = fiepipe3dcoat.coat.FromParameters(str(path.absolute()),name)
        manager = self.GetManager()
        manager.Set([c3d])
        
    
    complete_launch_interactive = fiepipelib.locallymanagedtypes.shells.AbstractLocalManagedTypeCommand.LocalManagedTypeCommand.type_complete
    
    def do_launch_interactive(self: fiepipelib.shells.AbstractShell.AbstractShell, args, pythonPaths:list = [], modulePaths:list = [], filePaths:list = []):
        """Launches the named 3DCoat instance in interactive mode.
        
        Usage launch_interactive [name]
        arg name: The name of a previoiusly created 3DCoat install.
        """
        if args == None:
            self.perror("No install specified.")
            return
        if args == "":
            self.perror("No install specified.")
            return
        
        manager = self.GetManager()
        coats = manager.get_by_name(args)
        if len(coats) == 0:
            self.perror("No 3DCoat Installs Found.  Try adding one.")
            return
        c3d = coats[0]
        assert isinstance(c3d,fiepipe3dcoat.coat.coat)
        c3d.LaunchInteractive()
        
