import fiepipelib.assetdata.data.items
import os
import os.path

import fiepipelib.assetdata.data.connection
import fiepipelib.assetdata.data.itemlist
import fiepipelib.filerepresentation.data.filerepresentation
import fiepipelib.fileversion.data.fileversion
from fiepipelib.gitstorage.data.git_working_asset import GitWorkingAsset


def GetFBXDir(workingAsset:GitWorkingAsset):
    return os.path.join(workingAsset.GetSubmodule().abspath,"fbx_lib")

def GetFBXFilesDir(workingAsset:GitWorkingAsset):
    return os.path.join(GetFBXDir(workingAsset),"file")


class FBXLibDatabase(fiepipelib.assetdata.data.items.AbstractItemsRelation):
    
    _fbxFileManager = None
    _fbxFileVersionManager = None
    _fbxFileRepresentationManager = None
    _fbxFileListManger = None
    _fbxFileListEntryManager = None
    
    def __init__(self, workingAsset:GitWorkingAsset):
        self._fbxFileManager = FBXFileManager()
        self._fbxFileVersionManager = FBXFileVersionManager()
        self._fbxFileRepresentationManager = FBXFileRepresentationManager()
        self._fbxFileListManger = FBXFileListManager()
        self._fbxFileListEntryManager = FBXFileListEntryManager(self._fbxFileListManger, self._fbxFileManager)
        
        dataManagers = [self._fbxFileManager,self._fbxFileVersionManager,self._fbxFileRepresentationManager, self._fbxFileListManger, self._fbxFileListEntryManager]
        super().__init__(workingAsset,dataManagers)
    
    def GetMultiManagedName(self):
        return "fbx_lib"
    
    def GetFileManager(self):
        return self._fbxFileManager
    
    def GetFileVersionManager(self):
        return self._fbxFileVersionManager
    
    def GetFileRepresentationManager(self):
        return self._fbxFileRepresentationManager
    
    def GetFileListManager(self):
        return self._fbxFileListManger
        
    def GetFileListEntryManager(self):
        return self._fbxFileListEntryManager
    
class FBXFile(object):
    
    _name = None
    _meta = None
    
    def __init__(self):
        self._meta = {}
       
    def GetName(self) -> str:
        return self._name
    
    def GetMeta(self) -> dict:
        return self._meta
    
    
def FBXFileFromJSON(data:dict) -> FBXFile:
    ret = FBXFile()
    ret._name = data['name']
    ret._meta = data['meta']
    return ret

def FBXFileToJSON(fbxfile:FBXFile) -> dict:
    ret = {}
    ret['name'] = fbxfile._name
    ret['meta'] = fbxfile._meta
    return ret

def FBXFileFromParameters(name:str,meta:dict) -> FBXFile:
    ret = FBXFile()
    ret._name = name
    ret._meta = meta
    return ret

class FBXFileManager(fiepipelib.assetdata.data.items.AbstractItemManager):
    
    def FromJSONData(self, data):
        return FBXFileFromJSON(data)
    
    def ToJSONData(self, item):
        return FBXFileToJSON(item)
    
    def GetColumns(self):
        ret = super().GetColumns()
        ret.append(('name','text'))
        return ret
    
    def GetManagedTypeName(self):
        return 'fbx_file'
    
    def GetPrimaryKeyColumns(self):
        return['name']
    
    def GetByName(self, name, connection: fiepipelib.assetdata.data.connection.Connection):
        return self._Get(colNamesAndValues=[('name',name)],conn=connection.GetDBConnection())
    
    def DeleteByName(self, name, connection: fiepipelib.assetdata.data.connection.Connection):
        self._Delete('name', name, connection.GetDBConnection())
    
class FBXFileList(fiepipelib.assetdata.data.itemlist.AbstractItemList):
    
    def __init__(self):
        pass

class FBXFileListManager(fiepipelib.assetdata.data.itemlist.AbstractItemListManager):
    
    def GetManagedTypeName(self):
        return "fbx_file_list"
    
    def NewList(self):
        return FBXFileList()

class FBXFileListEntry(fiepipelib.assetdata.data.itemlist.AbstractItemListEntry):
    
    
    def __init__(self, manager:'FBXFileListEntryManager'):
        super().__init__(manager)
        
    def GetFBXFile(self, conn: fiepipelib.assetdata.data.connection.Connection) -> FBXFile:
        return self.GetSecond(conn)
    
class FBXFileListEntryManager(fiepipelib.assetdata.data.itemlist.AbstractItemListEntryManager):
    
    def __init__(self, listManager:FBXFileListManager, 
                fileManager:FBXFileManager):
        super().__init__(listManager,fileManager)
        
    def GetManagedTypeName(self):
        return "fbx_file_list_entry"
    
    def NewLink(self):
        return FBXFileListEntry(self)    
    
class FBXFileVersion(fiepipelib.fileversion.data.fileversion.AbstractFileVersion):
    
    _fbxName = None
                
    def GetFBXName(self):
        return self._fbxName
    
    def GetFullName(self):
        return self._fbxName + "_" + self._version
    
    def GetFilename(self):
        return self.GetFullName() + ".fbx"
    
    def GetAbsolutePath(self):
        return os.path.join(GetFBXFilesDir(self.GetWorkingAsset()),self.GetFBXName(),self.GetFilename())

def FBXFileVersionFromJSON(data:dict,workingAsset:GitWorkingAsset) -> FBXFileVersion:
    ret = FBXFileVersion()
    ret._fbxName = data['fbx_name']
    fiepipelib.fileversion.data.fileversion.AbstractFileVersionFromJSON(ret, data, workingAsset)
    return ret

def FBXFileVersionToJSON(fbxver:FBXFileVersion) -> dict:
    ret = {}
    ret['fbx_name'] = fbxver._fbxName
    fiepipelib.fileversion.data.fileversion.AbstractFileVersionToJSON(fbxver, ret)
    return ret

def FBXFileVersionFromParameters(ver:str,fbxname:str,workingAsset:GitWorkingAsset) -> FBXFileVersion:
    ret = FBXFileVersion()
    ret._fbxName = fbxname
    fiepipelib.fileversion.data.fileversion.AbstractFileVersionFromParameters(ret, ver, workingAsset)
    return ret


class FBXFileVersionManager(fiepipelib.fileversion.data.fileversion.AbstractFileVersionManager):
        
    def FromJSONData(self, data):
        return FBXFileVersionFromJSON(data,self.GetMultiManager().GetWorkingAsset())
    
    def ToJSONData(self, item):
        return FBXFileVersionToJSON(item)
    
    def GetManagedTypeName(self):
        return 'fbx_file_version'
    
    def GetColumns(self):
        ret = super().GetColumns()
        ret.append(('fbx_name','text'))
        return ret
    
    def GetCompoundKeyColumns(self):
        return ['fbx_name']
    
    def GetByName(self, fbxName, connection: fiepipelib.assetdata.data.connection.Connection):
        return self._Get(colNamesAndValues=[('fbx_name',fbxName)],conn=connection.GetDBConnection())
        
    def GetByNameAndVersion(self, fbxName, version, connection: fiepipelib.assetdata.data.connection.Connection):
        return self._Get(colNamesAndValues=[('fbx_name',fbxName),('version',version)],conn=connection.GetDBConnection())
    
    def DeleteByName(self, fbxName, connection: fiepipelib.assetdata.data.connection.Connection):
        self._Delete("fbx_name", fbxName, connection.GetDBConnection())
        
    def DeleteByNameAndVersion(self, fbxName, version, connection: fiepipelib.assetdata.data.connection.Connection):
        self._DeleteByMultipleAND(colNamesAndValues=[("fbx_name",fbxName),("version",version)],conn=connection.GetDBConnection())
        
class FBXFileVersionList(fiepipelib.assetdata.data.itemlist.AbstractItemList):
    pass

class FBXFileVersionListManager(fiepipelib.assetdata.data.itemlist.AbstractItemListManager):
    
    def GetManagedTypeName(self):
        return "fbx_file_version_list"
    
    def NewList(self):
        return FBXFileVersionList()

class FBXFileVersionListEntry(fiepipelib.assetdata.data.itemlist.AbstractItemListEntry):
    
    def GetVersion(self, conn: fiepipelib.assetdata.data.connection.Connection) -> FBXFileVersion:
        return self.GetSecond( conn)
    
class FBXFileVersionListEntryManager(fiepipelib.assetdata.data.itemlist.AbstractItemListEntryManager):
    
    def GetManagedTypeName(self):
        return "fbx_file_version_list_entry"
    
    def NewLink(self):
        return FBXFileVersionListEntry(self)
    
    
class FBXFileRepresentation(fiepipelib.filerepresentation.data.filerepresentation.AbstractRepresentation):
    
    _fbxName = None        
    
    
def FBXFileRepresentationFromJSON(data:dict) -> FBXFileRepresentation:
    ret = FBXFileRepresentation()
    fiepipelib.filerepresentation.data.filerepresentation.AbstractRepresentationFromJSON(data, ret)
    ret._fbxName = data['fbx_name']
    return ret
    
def FBXFileRepresentationToJSON(rep:FBXFileRepresentation) -> dict:
    ret = {}
    fiepipelib.filerepresentation.data.filerepresentation.AbstractRepresentationToJSON(rep, ret)
    ret['fbx_name'] = rep._fbxName
    return ret
    
def FBXFileRepresentationFromParameters(name:str,path:str,fbxName:str,version:str):
    ret = FBXFileRepresentation()
    fiepipelib.filerepresentation.data.filerepresentation.AbstractRepresentationFromParameters(
        name, path, version, ret)
    ret._fbxName = fbxName
    return ret
    
class FBXFileRepresentationManager(fiepipelib.filerepresentation.data.filerepresentation.AbstractRepresentationManager):
    
    def FromJSONData(self, data):
        return FBXFileRepresentationFromJSON(data)
    
    def ToJSONData(self, item):
        return FBXFileRepresentationToJSON(item)
    
    def GetManagedTypeName(self):
        return 'fbx_file_representation'
    
    def GetRepresentationColumns(self):
        ret = []
        ret.append(('fbx_name','text'))
        return ret

    def GetRepresentationPrimaryKeyColumns(self):
        return ['fbx_name']

    def GetByVersion(self,
                     version:FBXFileVersion,
                     connection: fiepipelib.assetdata.data.connection.Connection):
        return self._Get(conn=connection,colNamesAndValues=[('fbx_name',version.GetPartDesignName()),('version',version.GetVersion())])
            
    def GetByName(self, name:str,
                  version:FBXFileVersion,
                  connection: fiepipelib.assetdata.data.connection.Connection):
        return self._Get(colNamesAndValues=[('fbx_name',version.GetPartDesignName()),('version',version.GetVersion()),("name",name)],conn=connection.GetDBConnection())
        
    
    def DeleteByName(self, name:str,
                     version:FBXFileVersion,
                     connection: fiepipelib.assetdata.data.connection.Connection):
        self._DeleteByMultipleAND(colNamesAndValues=[("fbx_name",version.GetPartDesignName()),("version",version.GetVersion()),("name",name)],conn=connection.GetDBConnection())
    
        
