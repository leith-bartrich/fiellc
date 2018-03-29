import fiepipelib.abstractmanager
import types
import fiepipelib.applauncher
import os.path
import subprocess

def FromParameters(path:str,name:str):
    ret = FreeCAD()
    ret._path = path
    ret._name = name
    return ret

def FromJSON(data:dict):
    ret = FreeCAD()
    ret._path = data['path']
    ret._name = data['name']
    return ret

def ToJSON(freecad):
    assert isinstance(freecad, FreeCAD)
    ret = {}
    ret['path'] = freecad._path
    ret['name'] = freecad._name
    return ret
    

class FreeCAD(object):
    
    _name = None
    _path = None
        
    def GetName(self) -> str:
        return self._name
    
    def GetPath(self) -> str:
        return self._path
    
    def LaunchInteractive(self, pythonPaths:list = [], modulepaths:list = [], filepaths:list = []):
        """Launches an interactive version of this FreeCAD install.
        @arg pythonPaths: list of python paths
        @arg modulepaths: list of FreeCAD module paths
        @arg filepaths: list of files/scripts to open
        """
        args = []
        args.append(os.path.join(self._path,"bin","FreeCAD"))
        for ppath in pythonPaths:
            args.append("-P")
            args.append(ppath)
            
        for mpath in modulepaths:
            args.append("-M")
            args.append(mpath)
            
        for fpath in filepaths:
            args.append(fpath)
            
        launcher = fiepipelib.applauncher.genericlauncher.listlauncher(args)
        launcher.launch(echo=True)
        
    def ExecuteInConsoleMode(self, pythonPaths:list = [], modulesPaths:list = [], filepaths:list = []):
        """Executes a console mode version of this FreeCAD install.
        @arg pythonPaths: list of python paths
        @arg modulepaths: list of FreeCAD module paths
        @arg filepaths: list of files/scripts to open
        """
        args = []
        args.append(os.path.join(self._path,"bin","FreeCADCmd"))
        for ppath in pythonPaths:
            args.append("-P")
            args.append(ppath)
            
        for mpath in modulepaths:
            args.append("-M")
            args.append(mpath)
            
        for fpath in filepaths:
            args.append(fpath)
            
        print(" ".join(args))
        subprocess.Popen(args)

class FreeCADLocalManager(fiepipelib.abstractmanager.abstractlocalmanager):
    
    
    def FromJSONData(self, data):
        return FromJSON(data)
    
    def ToJSONData(self, item):
        return ToJSON(item)
    
    def GetPrimaryKeyColumns(self):
        return ['name']
    
    def GetColumns(self):
        ret = super().GetColumns()
        ret.append(("name","text"))
        ret.append(("path","text"))
        return ret
    
    def GetManagedTypeName(self):
        return "freecad"
    
    def GetByName(self, name):
        return self._Get(colNamesAndValues=[("name",name)])
    
    def DeleteByName(self, name):
        self._Delete("name", name)