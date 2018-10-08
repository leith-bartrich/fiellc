import fiepipelib.assetdata.data.items
import os
import os.path
from fiepipelib.gitstorage.data.git_working_asset import GitWorkingAsset
from fiepipelib.assetdata.data.connection import Connection
import fiepipelib.fileversion.data.fileversion


class WorkFileDB(fiepipelib.assetdata.data.items.AbstractItemsRelation):
    
    _workFileManager = None
    _workFileVersionManager = None
    
    def GetWorkFileManager(self):
        return self._workFileManager
    
    def GetWorkFileVersionManager(self):
        return self._workFileVersionManager
    
    def __init__(self, 
                workingAsset:GitWorkingAsset):
        self._workFileManager = WorkFileManager()
        self._workFileVersionManager = WorkFileVersionManager()
        super().__init__(workingAsset,[self._workFileManager,self._workFileVersionManager])
    
    def GetMultiManagedName(self):
        return "coat_workfile"
    
    

class WorkFile(object):
    
    _name = None
    _meta = None
    
class WorkFileManager(fiepipelib.assetdata.data.items.AbstractItemManager):
    
    def FromJSONData(self, data) -> WorkFile:
        ret = WorkFile()
        ret._name = data['name']
        ret._meta = data['meta']
        return ret
    
    def ToJSONData(self, item:WorkFile):
        ret = {}
        ret['name'] = item._name
        ret['meta'] = item._meta
        return ret
        
    def NewFromParameters(self, name:str, meta:dict={}) -> WorkFile:
        ret = WorkFile()
        ret._name = name
        ret._meta = meta
        return ret
    
    def GetColumns(self):
        ret = super().GetColumns()
        ret.append(("name","text"))
        return ret
    
    def GetManagedTypeName(self):
        return "workfile"
    
    def GetPrimaryKeyColumns(self):
        return ["name"]
    
    def GetByName(self, name, conn:Connection):
        return self._Get(conn.GetDBConnection(), [("name",name)])
    
    def DeleteByName(self, name, conn:Connection):
        self._Delete("name", name, conn.GetDBConnection())

class WorkFileVersion(fiepipelib.fileversion.data.fileversion.AbstractFileVersion):
    
    _workFileName = None
    
    def GetWorkFileName(self):
        return self._workFileName
    
    def GetFullName(self):
        return self._workFileName + "_" + self.GetVersion()
    
    def GetFilename(self):
        return self.GetFullName() + ".3b"
    
    def GetAbsolutePath(self):
        return os.path.join(self.GetWorkingAsset().GetSubmodule().abspath,"3dcoat","work_files",self._workFileName,self.GetFilename())

class WorkFileVersionManager(fiepipelib.fileversion.data.fileversion.AbstractFileVersionManager):
    
    def FromJSONData(self, data):
        ret = WorkFileVersion()
        fiepipelib.fileversion.data.fileversion.AbstractFileVersionFromJSON(
            ret, data, self.GetMultiManager().GetWorkingAsset())
        ret._workFileName = data['work_file_name']
        return ret
    
    def ToJSONData(self, item:WorkFileVersion):
        ret = {}
        fiepipelib.fileversion.data.fileversion.AbstractFileVersionToJSON(
            item, ret)
        ret['work_file_name'] = item._workFileName
        return ret
    
    def NewFromParameters(self, workFileName, version):
        ret = WorkFileVersion()
        fiepipelib.fileversion.data.fileversion.AbstractFileVersionFromParameters(
            ret, version, self.GetMultiManager().GetWorkingAsset())
        ret._workFileName = workFileName
        return ret
    
    def GetColumns(self):
        ret = super().GetColumns()
        ret.append(('work_file_name',"text"))
        return ret
    
    def GetManagedTypeName(self):
        return "workfile_version"
    
    def GetCompoundKeyColumns(self):
        return ["work_file_name"]
    
    def GetByWorkFile(self, name, conn:Connection):
        return self._Get(conn.GetDBConnection(), [("work_file_name",name)])
    
    def GetByVersion(self, wf_name, version, conn:Connection):
        return self._Get(conn.GetDBConnection(), [("work_file_name",wf_name),("version",version)])
        
    def DeleteByWorkFile(self, name, conn:Connection):
        self._DeleteByMultipleAND(conn.GetDBConnection(), [("work_file_name",name)])
    
    def DeleteByVersion(self, wf_name, version, conn:Connection):
        self._DeleteByMultipleAND(conn.GetDBConnection(), [("work_file_name",wf_name),("version",version)])
    
    