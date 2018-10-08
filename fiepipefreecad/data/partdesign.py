import fiepipelib.filerepresentation.data.filerepresentation
import fiepipelib.fileversion.data.fileversion
import fiepipelib.gitstorage.data.git_working_asset
import os.path
import fiepipelib.assetdata.data.items
import typing
from fiepipelib.assetdata.data.connection import Connection, GetConnection


def GetFreeCADDir(workingAsset: fiepipelib.gitstorage.data.git_working_asset.GitWorkingAsset):
    return os.path.join(workingAsset.GetSubmodule().abspath,"freecad")

def GetPartDesignsDir(workingAsset: fiepipelib.gitstorage.data.git_working_asset.GitWorkingAsset):
    return os.path.join(GetFreeCADDir(workingAsset),"part_designs")


class PartDesignDB(fiepipelib.assetdata.data.items.AbstractItemsRelation):
    
    _partDesignManager = None
    _partDesignVersionManager = None
    _partRepresentationManager = None
    
    def __init__(self, workingAsset: fiepipelib.gitstorage.data.git_working_asset.GitWorkingAsset):
        self._partDesignManager = PartDesignManager()
        self._partDesignVersionManager = PartDesignVersionManager()
        self._partRepresentationManager = RepresentationManager()
        super().__init__(workingAsset,[self._partDesignManager,self._partDesignVersionManager,self._partRepresentationManager])
    
    def GetMultiManagedName(self):
        return "freecad_part_design"
    
    def GetPartDesignManager(self):
        return self._partDesignManager
    
    def GetPartDesignVersionManager(self):
        return self._partDesignVersionManager
    
    def GetPartRepresentationManager(self):
        return self._partRepresentationManager

class PartDesign(object):
    
    _name = None
    _workingAsset = None
    
    def GetName(self):
        return self._name
    
    def GetWorkingAsset(self):
        return self._workingAsset
    
    def GetVersions(self,db:PartDesignDB,connection:Connection):
        verman = db.GetPartDesignVersionManager()
        return verman.GetByPart(self.GetName(),connection)    


def PartDesignFromJSON(data, workingAsset: fiepipelib.gitstorage.data.git_working_asset.GitWorkingAsset):
    ret = PartDesign()
    ret._name = data['name']
    ret._workingAsset = workingAsset
    return ret

def PartDesignToJSON(part:PartDesign):
    ret = {}
    ret['name'] = part._name
    return ret

def PartDesignFromParameters(name:str, workingAsset: fiepipelib.gitstorage.data.git_working_asset.GitWorkingAsset):
    ret = PartDesign()
    ret._name = name
    ret._workingAsset = workingAsset
    return ret


class PartDesignManager(fiepipelib.assetdata.data.items.AbstractItemManager):
    
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
    
    def GetByName(self, name, connection:Connection):
        return self._Get(colNamesAndValues=[('name',name)],conn=connection.GetDBConnection())
    
    def DeleteByName(self, name, connection:Connection):
        self._Delete('name', name, connection.GetDBConnection())


class PartDesignVersion(fiepipelib.fileversion.data.fileversion.AbstractFileVersion):
    
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
    fiepipelib.fileversion.data.fileversion.AbstractFileVersionToJSON(ver, ret)
    ret['part_name'] = ver._partDesignName
    return ret

def PartDesignVersionFromJSON(data:typing.Dict, workingAsset: fiepipelib.gitstorage.data.git_working_asset.GitWorkingAsset):
    ret = PartDesignVersion()
    fiepipelib.fileversion.data.fileversion.AbstractFileVersionFromJSON(ret, data, workingAsset)
    ret._partDesignName = data['part_name']
    return ret

def PartDesignVersionFromParameters(partName:str, version:str, workingAsset: fiepipelib.gitstorage.data.git_working_asset.GitWorkingAsset):
    ret = PartDesignVersion()
    fiepipelib.fileversion.data.fileversion.AbstractFileVersionFromParameters(ret, version, workingAsset)
    ret._partDesignName = partName
    return ret

    

class PartDesignVersionManager(fiepipelib.fileversion.data.fileversion.AbstractFileVersionManager):
        
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
    
    def GetByPart(self,partName, connection:Connection):
        return self._Get(colNamesAndValues=[('part_name',partName)],conn=connection.GetDBConnection())
        
    def GetByPartAndVersion(self, partName,version, connection:Connection):
        return self._Get(colNamesAndValues=[('part_name',partName),('version',version)],conn=connection.GetDBConnection())
    
    def DeleteByPart(self, partName, connection:Connection):
        self._Delete("part_name", partName, connection.GetDBConnection())
        
    def DeleteByPartAndVersion(self, partName,version,connection:Connection):
        self._DeleteByMultipleAND(colNamesAndValues=[("part_name",partName),("version",version)],conn=connection.GetDBConnection())
        


class Representation(fiepipelib.filerepresentation.data.filerepresentation.AbstractRepresentation):
    
    _partDesignName = None        
    
    
def RepresentationFromJSON(data:dict) -> Representation:
    ret = Representation()
    fiepipelib.filerepresentation.data.filerepresentation.AbstractRepresentationFromJSON(data, ret)
    ret._partDesignName = data['part_design_name']
    return ret
    
def RepresentationToJSON(rep:Representation) -> dict:
    ret = {}
    fiepipelib.filerepresentation.data.filerepresentation.AbstractRepresentationToJSON(rep, ret)
    ret['part_design_name'] = rep._partDesignName
    return ret
    
def RepresentationFromParameters(name:str,path:str,partDesignName:str,version:str):
    ret = Representation()
    fiepipelib.filerepresentation.data.filerepresentation.AbstractRepresentationFromParameters(
        name, path, version, ret)
    ret._partDesignName = partDesignName
    return ret
    
class RepresentationManager(fiepipelib.filerepresentation.data.filerepresentation.AbstractRepresentationManager):
    
    def FromJSONData(self, data):
        return RepresentationFromJSON(data)
    
    def ToJSONData(self, item):
        return RepresentationToJSON(item)
    
    def GetManagedTypeName(self):
        return 'part_design_representation'
    
    def GetRepresentationColumns(self):
        ret = []
        ret.append(('part_design_name','text'))
        return ret

    def GetRepresentationPrimaryKeyColumns(self):
        return ['part_design_name']

    def GetByVersion(self, 
                    version:PartDesignVersion, 
                    connection:Connection):
        return self._Get(conn=connection,colNamesAndValues=[('part_design_name',version.GetPartDesignName()),('version',version.GetVersion())])
            
    def GetByName(self, name:str, 
                 version:PartDesignVersion, 
                 connection:Connection):
        return self._Get(colNamesAndValues=[('part_design_name',version.GetPartDesignName()),('version',version.GetVersion()),("name",name)],conn=connection.GetDBConnection())
        
    
    def DeleteByName(self, name:str, 
                    version:PartDesignVersion, 
                    connection:Connection):
        self._DeleteByMultipleAND(colNamesAndValues=[("part_design_name",version.GetPartDesignName()),("version",version.GetVersion()),("name",name)],conn=connection.GetDBConnection())
    
        
        