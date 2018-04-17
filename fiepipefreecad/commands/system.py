import fiepipelib.applauncher.genericlauncher
import fiepipelib.shells.abstract
import pathlib
import fiepipefreecad.freecad
import fiepipelib.localplatform
import fiepipelib.localuser
import cmd2

class FreeCADSystemCommand(fiepipelib.shells.abstract.LocalManagedTypeCommand):
    
    def __init__(self, localUser:fiepipelib.localuser.localuser):
        super().__init__(localUser)
        
    def getPluginNameV1(self):
        return "freecad_system_command"
    
    def GetBreadCrumbsText(self):
        return self.breadcrumbs_separator.join(["pipe","freecad"])
    
    def GetManager(self):
        return fiepipefreecad.freecad.FreeCADLocalManager(self._localUser)
    
    def GetAllItems(self):
        return self.GetManager().GetAll()
    
    def GetItemByName(self, name):
        return self.GetManager().GetByName(name)[0]
    
    def GetShell(self, item):
        raise NotImplementedError("FreeCAD command does not support 'enter' at this time.")
    
    def ItemToName(self, item):
        assert isinstance(item, fiepipefreecad.freecad.FreeCAD)
        return item.GetName()
    
    def DeleteItem(self, name:str):
        self.GetManager().DeleteByName(name)
        
    complete_create = cmd2.Cmd.path_complete

    def do_create(self:fiepipelib.shells.abstract.Shell, args):
        """Adds a freecad instance to the User's FreeCAD preferences.
        
        usage: create [path]
        
        arg path: The path to a FreeCAD install directory.
        """
        args = cmd2.parse_quoted_string(args)
        if len(args) == 0:
            self.perror("No path specified.")
            return
        path = pathlib.Path(args[0])
        if not path.exists():
            self.perror("Does not exist.")
            return
        if not path.is_dir():
            self.perror("Is not a directory.")
            return
        
        name = self.AskStringQuestion("Name")
        
        freecad = fiepipefreecad.freecad.FromParameters(str(path.absolute()),name)
        manager = self.GetManager()
        manager.Set([freecad])
    
    complete_launch_interactive = fiepipelib.shells.abstract.LocalManagedTypeCommand.type_complete
    
    def do_launch_interactive(self:fiepipelib.shells.abstract.Shell, args, pythonPaths:list = [], modulePaths:list = [], filePaths:list = []):
        """Launches the named FreeCAD instance in interactive mode.
        
        Usage launch_interactive [name]
        arg name: The name of a previoiusly created FreeCAD install.
        """
        if args == None:
            self.perror("No install specified.")
            return
        if args == "":
            self.perror("No install specified.")
            return
        
        manager = self.GetManager()
        freecads = manager.GetByName(args)
        if len(freecads) == 0:
            self.perror("No FreeCAD Installs Found.  Try adding one.")
            return
        freecad = freecads[0]
        assert isinstance(freecad,fiepipefreecad.freecad.FreeCAD)
        freecad.LaunchInteractive(pythonPaths, modulePaths, filePaths)
        
            