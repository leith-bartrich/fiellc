import fiepipelib.fileversion.data.fileversion
from fiepipe3dcoat.applink.standard import MeshFromParameters
import os
import os.path
import pathlib
import fiepipelib.assetdata.routines
from fiepipelib.assetdata.data.connection import Connection
from fieui.FeedbackUI import AbstractFeedbackUI
from fiepipelib.assetdata.data.items import AbstractItemsRelation
from fiepipelib.fileversion.data.fileversion import AbstractFileVersion
from fiepipelib.filerepresentation.data.filerepresentation import AbstractRepresentationManager
import typing
from fiepipelib.gitstorage.data.local_root_configuration import LocalRootConfiguration
from fiepipelib.gitstorage.data.git_working_asset import GitWorkingAsset
import asyncio
import tempfile
from fiepipefbxlib.data.common import FBXLibDatabase
from fiepipe3dcoat.applink.standard import Mesh, Mode, StartRoundTrip, ImportExists, ExportExists
from fiepipe3dcoat.data.workfile import WorkFileDB, WorkFileManager
import uuid
from .workfile import EnsureWorkfileAndMetaRoutine


def _getOBJMeshesInRepDir(dirPath:str) -> typing.List[Mesh]:
    meshes = []
    
    for fname in os.listdir(dirPath):
        base, ext = os.path.splitext(fname)
        if ext.lower() == ".obj":
            meshes.append(MeshFromParameters(os.path.join(str(dirPath),fname)))
    return meshes
    
async def _waitForApplinkExport(f:asyncio.Future):
    #while we're not done,
    while not f.done():
        #we check if there's an export.
        if ExportExists():
            #if there is, we complete
            return
        else:
            await asyncio.sleep(1.0)
            #if not, we go round again.
    
async def _waitForApplinkImportToComplete(f:asyncio.Future):
    while not f.done():
        if ImportExists():
            await asyncio.sleep(1.0)
        else:
            return

async def PushToApplinkMergedOBJDir(version:AbstractFileVersion, workingRoot:LocalRootConfiguration, workingAsset:GitWorkingAsset, db:AbstractItemsRelation, rman:AbstractRepresentationManager, mode:Mode, fb:AbstractFeedbackUI):
    """Sends an obj_dir representation to 3dcoat for merging and UVing.  Cancelable via future.
    Returns a context usable temmpdir for the output.  If you let it drop, the directory is deleted.
    Hold it until you're done with the output.
    """
        
    #check for a proper source representation    
    conn = fiepipelib.assetdata.assetdatabasemanager.GetConnection(workingAsset)
    db.AttachToConnection( conn)
    
    repDirPath = await fiepipelib.assetdata.routines.GetRepresentationDirectoryRoutine("obj_dir", version, rman, conn,fb)
    
    meshes = _getOBJMeshesInRepDir(repDirPath)
    
    localPlatform = fiepipelib.localplatform.GetLocalPlatform()
    localUser = fiepipelib.localuser.localuser(localPlatform)
    
    #get a temp folder on the working volume
    mapper = fiepipelib.gitstorage.localstoragemapper.localstoragemapper(localUser)
    volume = mapper.GetMountedWorkingStorageByName(workingRoot.GetVolumeName())
    assert isinstance(volume, fiepipelib.storage.localvolume.localvolume)
    volumePath = volume.GetPath()
    dirPath = tempfile.TemporaryDirectory(dir=volumePath)
    #path for 3dc to publish to
    outMeshFileName = str(uuid.uuid4()) + ".fbx"
    outMesh = MeshFromParameters(os.path.join(str(dirPath),outMeshFileName))
    #start the round trip
    StartRoundTrip(meshes, outMesh, mode, [])
    return dirPath

async def PushToApplinkSequentialOBJDir(version:AbstractFileVersion, workingRoot:LocalRootConfiguration, workingAsset:GitWorkingAsset, db:AbstractItemsRelation, rman:AbstractRepresentationManager, mode:Mode, fb:AbstractFeedbackUI):
    """Sends an obj_dir representation to 3dcoat for UVing one obj at a time.  Cancelable via future.
    Returns a context usable temmpdir for the output.  If you let it drop, the directory is deleted.
    Hold it until you're done with the output.
    """
        
    #check for a proper source representation    
    conn = fiepipelib.assetdata.assetdatabasemanager.GetConnection(workingAsset)
    db.AttachToConnection( conn)
    
    repDirPath = await fiepipelib.assetdata.routines.GetRepresentationDirectoryRoutine("obj_dir", version, rman, conn,fb)
    
    meshes = _getOBJMeshesInRepDir(repDirPath)
    
    localPlatform = fiepipelib.localplatform.GetLocalPlatform()
    localUser = fiepipelib.localuser.localuser(localPlatform)
    
    #get a temp folder on the working volume
    mapper = fiepipelib.gitstorage.localstoragemapper.localstoragemapper(localUser)
    volume = mapper.GetMountedWorkingStorageByName(workingRoot.GetVolumeName())
    assert isinstance(volume, fiepipelib.storage.localvolume.localvolume)
    volumePath = volume.GetPath()
    dirPath = tempfile.TemporaryDirectory(dir=volumePath)
    #path for 3dc to publish to
    outMeshFileName = str(uuid.uuid4()) + ".fbx"
    outMesh = MeshFromParameters(os.path.join(str(dirPath),outMeshFileName))
    #start the round trips
    for mesh in meshes:
        fiepipe3dcoat.applink.standard.StartRoundTrip([mesh], outMesh, mode, [])
        await mf.execute(_waitForApplinkImportToComplete)
        if mf.get_future().cancelled():
            fb.error("User canceled the AppLink push.")
            return
    return dirPath

async def PushToApplinkNew3BWorkFileVersion(template:str, workfileName:str, blankTemplateName:str, asset:GitWorkingAsset, db:WorkFileDB, man:WorkFileManager, conn:Connection, fb:AbstractFeedbackUI, fromPreviousVerion=False):
    workFile = await EnsureWorkfileAndMetaRoutine(workfileName, {}, asset, db, man, conn)
    raise NotImplementedError()
    

async def PullFromApplink(workingRoot:LocalRootConfiguration, mode:Mode, fb:AbstractFeedbackUI):
    """Sends a dummy push to applink, which in turn, really works as a 'pull.'
    3dCoat imports 'nothing' but sets up the 'return to app' as per the 'mode.'
    """
        
    #check for a proper source representation    
    
    localPlatform = fiepipelib.localplatform.GetLocalPlatform()
    localUser = fiepipelib.localuser.localuser(localPlatform)
    
    #get a temp folder on the working volume
    mapper = fiepipelib.gitstorage.localstoragemapper.localstoragemapper(localUser)
    volume = mapper.GetMountedWorkingStorageByName(workingRoot.GetVolumeName())
    assert isinstance(volume, fiepipelib.storage.localvolume.localvolume)
    volumePath = volume.GetPath()
    dirPath = tempfile.TemporaryDirectory(dir=volumePath)
    #path for 3dc to publish to
    outMeshFileName = str(uuid.uuid4()) + ".fbx"
    outMesh = MeshFromParameters(os.path.join(str(dirPath),outMeshFileName))
    #start the round trips
    StartRoundTrip([], outMesh, mode, [])
    await mf.execute(_waitForApplinkImportToComplete)
    if mf.get_future().cancelled():
        fb.error("User canceled the AppLink push.")
        return
    return dirPath

        
async def WaitForApplinkExportRoutine(f:asyncio.Future,fb:AbstractFeedbackUI):
    #modal cancelable future call.
    fb.output("Waiting for 3DCoat to export.")
    mf.execute(_waitForApplinkExport)
    
    #if we canceled, we exit. the temp lib cleans up the directory for us.
    if mf.get_future().cancelled():
        f.cancel()
        return
    
    f.set_result(fiepipe3dcoat.applink.standard.EndRountrip())
    return

async def WaitForApplinkImportRoutine(f:asyncio.Future,fb:AbstractFeedbackUI):
    #modal cancelable future call.
    fb.output("Waiting for 3DCoat to import.")
    mf.execute(_waitForApplinkImportToComplete)
    
    #if we canceled, we exit.
    if mf.get_future().cancelled():
        f.cancel()
        return
    
    return

    
async def AppLinkExportToFBXLibRoutine(applinkexport, fname:str, metaDataToAdd:dict, asset:GitWorkingAsset, fqdn:str, fb:AbstractFeedbackUI):
    """Given an applink export object, this routine will import the results to the FBX Library.
    It will create the FBXFile if it doesn't exist.  It will create a new FileVersion via standard version incrementation.
    """
        
    mesh, textures = applinkexport
    assert isinstance(mesh, fiepipe3dcoat.applink.standard.Mesh)
    assert isinstance(textures, list)
    
    #just incase
    mpath = pathlib.Path(mesh._path)
    if not mpath.exists():
        fb.error("Mesh doesn't exist: " + str(mpath))
        return
            
    #now we create a proper fbx_lib entry
    conn = fiepipelib.assetdata.assetdatabasemanager.GetConnection(db.GetWorkingAsset())
    db = FBXLibDatabase(asset)
    fbxman = db.GetFileManager()
    fbxverman = db.GetFileVersionManager()
    db.AttachToConnection( conn)
    
    newFullName = fname
    
    #we look for such an existing file
    foundFBXFiles = fbxman.get_by_name(newFullName, conn)
    foundFBXFile = None
    if len(foundFBXFiles) == 0:
        #if there were none, we create it.
        foundFBXFile = fiepipefbxlib.data.common.FBXFileFromParameters(newFullName,{})
    else:
        foundFBXFile = foundFBXFiles[0]
        
    #we set the passed meta-data.
    for key in metaDataToAdd.keys():
        foundFBXFile.GetMeta()[key] = metaDataToAdd[key]
    #set data
    fbxman.Set([foundFBXFile], conn)
    
    #that's the file. now its new version.
    
    #we look for existing versions
    foundFBXVersions = fbxverman.get_by_name(newFullName, conn)
    newFBXVersion = None
            
    if len(foundFBXVersions) == 0:
        defverman = fiepipelib.versions.default.GetVersionDefaultManager()
        ver = defverman.get_default(fqdn)
        newFBXVersion = fiepipefbxlib.data.common.FBXFileVersionFromParameters(
            ver, 
            newFullName, 
            workingAsset)
    else:
        incverman = fiepipelib.versions.incrementation.GetVersionIncrementationManager()
        latestVer = fiepipelib.fileversion.data.fileversion.LatestVersion(foundFBXVersions, fqdn)
        incverman = fiepipelib.versions.incrementation.GetVersionIncrementationManager()
        ver = incverman.Increment(latestVer.GetVersion(), fqdn)
        newFBXVersion = fiepipefbxlib.data.common.FBXFileVersionFromParameters(
            ver, 
            newFullName, 
            workingAsset)
    
    #set data
    fbxverman.Set([newFBXVersion],conn)
    
    #commit all data
    conn.Commit()
    conn.Close()
    
    
    #now we move on to the files themselves.
    newFBXVersion.EnsureDirExists()
    
    #TODO: make this interactive via async modals.
    if newFBXVersion.FileExists():
        fb.error("File already exists.")
        fb.warn("Moving work product to work volume root: " + str(target))
        target = pathlib.Path(os.path.join(volumePath,outMeshFileName))
        targetDir = pathlib.Path(target.parent())
        source = pathlib.Path(outMesh._path)
        source.rename(target)
        fb.warn("You probably want to delete the existing version's file and ingest the one referenced prior.")
        return
    
    fb.output("Moving work product to proper location...")
    source = pathlib.Path(outMesh._path)
    target = pathlib.Path(newFBXVersion.GetAbsolutePath())
    source.rename(target)
    
    #now the textures.
    for texture in textures:
        assert isinstance(texture,
                          fiepipe3dcoat.applink.standard.Texture)
        tpath = pathlib.Path(texture._path)
        ttargetdir = pathlib.Path(newFBXVersion.GetDirPath())
        ttarget = pathlib.Path(os.path.join(ttargetdir,tpath.parts[-1]))
        if ttarget.exists():
            #this is rough handling.  better to do interactive via async modals.
            ttarget.unlink()
        tpath.rename(ttarget)
    
    fb.output("done.")
