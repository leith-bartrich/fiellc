import fiepipelib.gitstorage.workingasset
import os.path
import fiepipelib.assetdata.abstractassetdata
import pathlib
import abc
import typing

def GetFreeCADDir(workingAsset:fiepipelib.gitstorage.workingasset.workingasset):
    return os.path.join(workingAsset.GetSubmodule().abspath,"freecad")

def GetPartDesignsDir(workingAsset:fiepipelib.gitstorage.workingasset.workingasset):
    return os.path.join(GetFreeCADDir(workingAsset),"part_designs")


class PartDesignDB(fiepipelib.assetdata.abstractassetdata.abstractmultimanager):
    
    _partDesignManager = None
    _partDesignVersionManager = None
    
    def __init__(self, workingAsset:fiepipelib.gitstorage.workingasset.workingasset):
        self._partDesignManager = PartDesignManager()
        self._partDesignVersionManager = PartDesignVersionManager()
        super().__init__(workingAsset,[self._partDesignManager,self._partDesignVersionManager])
    
    def GetMultiManagedName(self):
        return "freecad_part_design"
    
    def GetPartDesignManager(self):
        return self._partDesignManager
    
    def GetPartDesignVersionManager(self):
        return self._partDesignVersionManager
    

class PartDesign(object):
    
    _name = None
    _workingAsset = None
    
    def GetName(self):
        return self._name
    
    def GetWorkingAsset(self):
        return self._workingAsset
    
    def GetVersions(self,db:PartDesignDB,connection:fiepipelib.assetdata.assetdatabasemanager.Connection):
        verman = db.GetPartDesignVersionManager()
        return verman.GetByPart(self.GetName(),connection)    


def PartDesignFromJSON(data,workingAsset:fiepipelib.gitstorage.workingasset.workingasset):
    ret = PartDesign()
    ret._name = data['name']
    ret._workingAsset = workingAsset
    return ret

def PartDesignToJSON(part:PartDesign):
    ret = {}
    ret['name'] = part._name
    return ret

def PartDesignFromParameters(name:str, workingAsset:fiepipelib.gitstorage.workingasset.workingasset):
    ret = PartDesign()
    ret._name = name
    ret._workingAsset = workingAsset
    return ret


class PartDesignManager(fiepipelib.assetdata.abstractassetdata.abstractdatamanager):
    
    def FromJSONData(self, data):
        return PartDesignFromJSON(data,self.GetMultiManager().GetWorkingAsset())
    
    def ToJSONData(self, item):
        return PartDesignToJSON(item)
    
    def GetColumns(self):
        ret = super().GetColumns()
        ret.append(('name','text'))
        return ret
    
    def GetManagedTypeName(self):
        return 'part_design'
    
    def GetPrimaryKeyColumns(self):
        return['name']
    
    def GetByName(self, name, connection:fiepipelib.assetdata.assetdatabasemanager.Connection):
        return self._Get(colNamesAndValues=[('name',name)],conn=connection.GetDBConnection())
    
    def DeleteByName(self, name, connection:fiepipelib.assetdata.assetdatabasemanager.Connection):
        self._Delete('name', name, connection.GetDBConnection())


class PartDesignVersion(fiepipelib.assetdata.abstractassetdata.AbstractFileVersion):
    
    _partDesignName = None
    
        
    def GetPartDesignName(self):
        return self._partDesignName
    
    def GetFullName(self):
        return self._partDesignName + "_" + self._version
    
    def GetFilename(self):
        return self.GetFullName() + ".FCStd" 
    
    def GetAbsolutePath(self):
        return os.path.join(GetPartDesignsDir(self.GetWorkingAsset()),self.GetPartDesignName(),self.GetFilename())


def PartDesignVersionToJSON(ver:PartDesignVersion):
    ret = {}
    fiepipelib.assetdata.abstractassetdata.AbstractFileVersionToJSON(ver, ret)
    ret['part_name'] = ver._partDesignName
    return ret

def PartDesignVersionFromJSON(data:typing.Dict,workingAsset:fiepipelib.gitstorage.workingasset.workingasset):
    ret = PartDesignVersion()
    fiepipelib.assetdata.abstractassetdata.AbstractFileVersionFromJSON(ret, data, workingAsset)
    ret._partDesignName = data['part_name']
    return ret

def PartDesignVersionFromParameters(partName:str,version:str,workingAsset:fiepipelib.gitstorage.workingasset.workingasset):
    ret = PartDesignVersion()
    fiepipelib.assetdata.abstractassetdata.AbstractFileVersionFromParameters(ret, version, workingAsset)
    ret._partDesignName = partName
    return ret

    

class PartDesignVersionManager(fiepipelib.assetdata.abstractassetdata.AbstractFileVersionManager):
        
    def FromJSONData(self, data):
        return PartDesignVersionFromJSON(data,self.GetMultiManager().GetWorkingAsset())
    
    def ToJSONData(self, item):
        return PartDesignVersionToJSON(item)
    
    def GetManagedTypeName(self):
        return 'part_design_version'
    
    def GetColumns(self):
        ret = super().GetColumns()
        ret.append(('part_name','text'))
        return ret
    
    def GetCompoundKeyColumns(self):
        return ['part_name']
    
    def GetByPart(self,partName, connection:fiepipelib.assetdata.assetdatabasemanager.Connection):
        return self._Get(colNamesAndValues=[('part_name',partName)],conn=connection.GetDBConnection())
        
    def GetByPartAndVersion(self, partName,version, connection:fiepipelib.assetdata.assetdatabasemanager.Connection):
        return self._Get(colNamesAndValues=[('part_name',partName),('version',version)],conn=connection.GetDBConnection())
    
    def DeleteByPart(self, partName, connection:fiepipelib.assetdata.assetdatabasemanager.Connection):
        self._Delete("part_name", partName, connection.GetDBConnection())
        
    def DeleteByPartAndVersion(self, partName,version,connection:fiepipelib.assetdata.assetdatabasemanager.Connection):
        self._DeleteByMultipleAND(colNamesAndValues=[("part_name",partName),("version",version)],conn=connection.GetDBConnection())