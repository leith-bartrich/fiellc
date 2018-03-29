import fiepipelib.applauncher.genericlauncher
import fiepipelib.shells.abstract
import pathlib
import fiepipefreecad.freecad
import fiepipelib.localplatform
import fiepipelib.localuser

def AddFreeCAD(self:fiepipelib.shells.abstract.Shell, args):
    """Adds a freecad instance to the User's FreeCAD preferences.
    """
    
    path = pathlib.Path(args)
    if not path.exists():
        self.perror("Does not exist.")
        return
    if not path.is_dir():
        self.perror("Is not a directory.")
        return
    
    name = self.AskStringQuestion("Name?")
    
    platform = fiepipelib.localplatform.GetLocalPlatform()
    user = fiepipelib.localuser.localuser(platform)
    
    freecad = fiepipefreecad.freecad.FromParameters(str(path.absolute()),name)
    manager = fiepipefreecad.freecad.FreeCADLocalManager(user)
    manager.Set([freecad])

def freecad_installs_complete(self:fiepipelib.shells.abstract.Shell,text,line,begidx,endidx):
    platform = fiepipelib.localplatform.GetLocalPlatform()
    user = fiepipelib.localuser.localuser(platform)
    manager = fiepipefreecad.freecad.FreeCADLocalManager(user)
    allFreeCADs = manager.GetAll()
    ret = []
    for freeCAD in allFreeCADs:
        assert isinstance(freeCAD,fiepipefreecad.freecad.FreeCAD)
        if freeCAD.GetName().lower().startswith(text.lower()):
            ret.append(freeCAD.GetName())
    return ret    

def DeleteFreeCAD(self:fiepipelib.shells.abstract, args):
    platform = fiepipelib.localplatform.GetLocalPlatform()
    user = fiepipelib.localuser.localuser(platform)
    manager = fiepipefreecad.freecad.FreeCADLocalManager(user)
    manager.DeleteByName(args)
    
    
def LaunchInteractive(self:fiepipelib.shells.abstract.Shell, args, pythonPaths:list = [], modulePaths:list = [], filePaths:list = []):
    """Launches the named FreeCAD instance in interactive mode.
    
    Usage LaunchFreeCAD [name]
    arg name: The name of a previoiusly added FreeCAD install.
    """
    if args == None:
        self.perror("No install specified.")
        return
    if args == "":
        self.perror("No install specified.")
        return
    
    platform = fiepipelib.localplatform.GetLocalPlatform()
    user = fiepipelib.localuser.localuser(platform)
    manager = fiepipefreecad.freecad.FreeCADLocalManager(user)
    freecads = manager.GetByName(args)
    if len(freecads) == 0:
        self.perror("No FreeCAD Installs Found.  Try adding one.")
        return
    freecad = freecads[0]
    assert isinstance(freecad,fiepipefreecad.freecad.FreeCAD)
    freecad.LaunchInteractive(pythonPaths, modulePaths, filePaths)
    
        