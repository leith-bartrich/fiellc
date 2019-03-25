import fiepipe3dcoat.coat
import fiepipedesktoplib.assetdata.shell
import fiepipe3dcoat.applink.standard
import fiepipe3dcoat.shell.common
import fiepipedesktoplib.assetdata.shell.item
import fiepipedesktoplib.filerepresentation.shell.item
import fiepipe3dcoat.routines.applink

class CoatRepresentationsCommand(fiepipedesktoplib.assetdata.shell.item.ItemShell):
    
    _representationsCommand = None
    
    def GetVersion(self):
        return self._representationsCommand.GetVersion()
    
    def __init__(self, repCommand =fiepipedesktoplib.filerepresentation.shell.item.AbstractSingleFileRepresentationsCommand):
        self._representationsCommand = repCommand
        super().__init__(repCommand.GetAssetShell())
        
    def getPluginNamesV1(self):
        ret = super().getPluginNamesV1()
        ret.append("coat_representations_command")
        return ret
    
    def GetBreadCrumbsText(self):
        return self.breadcrumbs_separator.join([self._representationsCommand.GetBreadCrumbsText(),"coat"])

    def do_send_obj_dir_to_uv_merged(self, args):
        db = self._representationsCommand.GetMultiManager()
        rman = self._representationsCommand.GetManager(db)
        mode = fiepipe3dcoat.applink.standard.Mode(fiepipe3dcoat.applink.standard.Mode.MODE_UVMapping)
        workingRoot = self.GetAssetShell()._workingRoot
        self.DoCoroutine(fiepipe3dcoat.routines.applink.PushToApplinkMergedOBJDir( self.GetVersion(), workingRoot, self.GetGitWorkingAsset(), db, rman, mode, self.GetFeedbackUI(), self.GetCancelableModalUI()))
    
    def do_send_obj_dir_to_uv_sequentially(self, args):
        db = self._representationsCommand.GetMultiManager()
        rman = self._representationsCommand.GetManager(db)
        mode = fiepipe3dcoat.applink.standard.Mode(fiepipe3dcoat.applink.standard.Mode.MODE_UVMapping)
        workingRoot = self.GetAssetShell()._workingRoot
        self.DoCoroutine(fiepipe3dcoat.routines.applink.PushToApplinkSequentialOBJDir( self.GetVersion(), workingRoot, self.GetGitWorkingAsset(), db, rman, mode, self.GetFeedbackUI(), self.GetCancelableModalUI()))
        
    def do_pull_to_workfile_uv_merged(self, args):
        raise NotImplementedError()
    
    def do_pull_to_workfile_uv_sequentially(self, args):
        raise NotImplementedError()
        
    
    #def do_send_obj_dir_to_uv_sequentially(self, args):
        #"""Sends an obj_dir representation to 3dcoat for UVing, one obj at a time.  Waits for 3dcoat to send
        #it back.
        
        #Then, it creates a new file and version in the fbx library for the result.
        
        #Usage: send_obj_dir_to_uv_sequentially
        #"""
        #args = self.ParseArguments(args)
        
        
        ##check for a proper source representation    
        #conn = self._representationsCommand.GetConnection()
        #db = self._representationsCommand.GetMultiManager()
        #db.AttachToConnection( conn)
        #rman = self._representationsCommand.GetManager(db)
        #reps = self._representationsCommand.GetItemByName("obj_dir",rman,conn)
        #conn.Close()
        
        #del conn,db,rman
        
        #if len(reps) == 0:
            #self.perror("No such representation: obj_dir")
            #return
        
        #rep = reps[0]
        
        #assert isinstance(rep, fiepipelib.assetdata.abstractassetdata.AbstractRepresentation)
        
        ##put together list of obj meshes
        
        #repDirPath = pathlib.Path(rep.GetAbsolutePath(
            #self._representationsCommand._versionShell._version))
        
        #meshes = []
        
        #for fname in os.listdir(repDirPath):
            #base, ext = os.path.splitext(fname)
            #if ext.lower() == ".obj":
                #meshes.append(fiepipe3dcoat.applink.standard.Mesh(os.path.join(str(repDirPath),fname)))


        ##get a temp folder on the working volume
        #mapper = fiepipelib.gitstorage.localstoragemapper.localstoragemapper(self.GetAssetShell()._localUser)
        #volume = mapper.GetMountedWorkingStorageByName(self.GetAssetShell()._workingRoot.GetVolumeName())
        #assert isinstance(volume, fiepipelib.storage.localvolume.localvolume)
        #volumePath = volume.GetPath()
        #with tempfile.TemporaryDirectory(dir=volumePath) as dirPath:
            ##path for 3dc to publish to
            #outMeshFileName = str(uuid.uuid4()) + ".fbx"
            #outMesh = fiepipe3dcoat.applink.standard.Mesh(os.path.join(str(dirPath),outMeshFileName))
            ##UV mode
            #mode = fiepipe3dcoat.applink.standard.Mode(fiepipe3dcoat.applink.standard.Mode.MODE_UVMapping)
            ##start the round trip
            #for mesh in meshes:
                #fiepipe3dcoat.applink.standard.StartRoundTrip(
                                                             #[mesh], 
                                                             #outMesh, 
                                                             #mode, 
                                                             #[])
                #self.poutput("Waiting for 3DCoat to import...")
                #self.poutput("Press 'esc' to cancel")
                #canceled = False
                #while(fiepipe3dcoat.applink.standard.ImportExists()):
                    #time.sleep(0.5)
                    #if keyboard.is_pressed('esc'):
                        #canceled = True
                        #break
                #if canceled:
                    #self.poutput("User canceled.")
                    #return
                #self.poutput("imported.")
            #self.poutput("3DCoat done picking up imports.")
            
            #if fiepipe3dcoat.applink.standard.ExportExists():
                #self.poutput("Clearing existing export.")
                #fiepipe3dcoat.applink.standard.EndRountrip()
            
            ##event loop runs every second
            ##we look for esc to be pressed just incase.
            #self.poutput("Waiting for 3DCoat to export...")
            #self.poutput("Press 'esc' to cancel")
            
            #canceled = False
            
            #while not fiepipe3dcoat.applink.standard.ExportExists():
                #time.sleep(1.0)
                #if keyboard.is_pressed('esc'):
                    #canceled = True
                    #break
            
            ##if we canceled, we exit. the temp lib cleans up the directory for us.
            #if canceled:
                #self.poutput("User canceled.")
                #return
            
            ##an export exists
            #mesh, textures = fiepipe3dcoat.applink.standard.EndRountrip()
            #assert isinstance(mesh, fiepipe3dcoat.applink.standard.Mesh)
            #assert isinstance(textures, list)
            
            ##just incase
            #mpath = pathlib.Path(mesh._path)
            #if not mpath.exists():
                #self.perror("Mesh doesn't exist: " + str(mpath))
                #return
            
            ##no real reason to do this.  but okay.
            #for texture in textures:
                #assert isinstance(texture,
                                  #fiepipe3dcoat.applink.standard.Texture)
                #tpath = pathlib.Path(texture._path)
                ##we don't use texuteres for a uv export.
                ##if they exist, we delete them to clean up.
                #if tpath.exists():
                    #tpath.unlink()
                    
            ##now we move on to creating a proper fbx_lib entry
            #conn = self._representationsCommand.GetConnection()
            #db = fiepipefbxlib.data.common.FBXLibDatabase(self.GetGitWorkingAsset())
            #db.AttachToConnection( conn)
            #fbxman = db.GetFileManager()
            #fbxverman = db.GetFileVersionManager()
            
            #origFullName = rep.GetVersion().GetFullName()
            ##we name it after the 'department's work'
            #newFullName = origFullName + "_uvs"
            
            ##we look for such an existing file just incase
            #foundFBXFiles = fbxman.GetByName(newFullName, conn)
            #foundFBXFile = None
            #if len(foundFBXFiles) == 0:
                ##if there were none, we create it.
                #foundFBXFile = fiepipefbxlib.data.common.FBXFileFromParameters(newFullName,{})
            #else:
                #foundFBXFile = foundFBXFiles[0]
            ##we set meta-data to mark it as having uvs and set it.
            #foundFBXFile.GetMeta()['uvs'] = True
            #fbxman.Set([foundFBXFile], conn)
            
            ##we look for existing versions
            #foundFBXVersions = fbxverman.GetByName(newFullName,conn)
            #newFBXVersion = None
            
            #fqdn = self.GetAssetShell()._entity.GetFQDN()
            #workingAsset = self.GetGitWorkingAsset()
            
            #if len(foundFBXVersions) == 0:
                #defverman = fiepipelib.versions.default.GetVersionDefaultManager()
                #ver = defverman.GetDefault(fqdn)
                #newFBXVersion = fiepipefbxlib.data.common.FBXFileVersionFromParameters(
                    #ver, 
                    #newFullName, 
                    #workingAsset)
            #else:
                #incverman = fiepipelib.versions.incrementation.GetVersionIncrementationManager()
                #latestVer = fiepipelib.assetdata.abstractassetdata.LatestVersion(foundFBXVersions,fqdn)
                #incverman = fiepipelib.versions.incrementation.GetVersionIncrementationManager()
                #ver = incverman.Increment(latestVer.GetVersion(), fqdn)
                #newFBXVersion = fiepipefbxlib.data.common.FBXFileVersionFromParameters(
                    #ver, 
                    #newFullName, 
                    #workingAsset)
            
            #fbxverman.Set([newFBXVersion],conn)
            #conn.Commit()
            #conn.Close()
            
            #if newFBXVersion.FileExists():
                #self.perror("File already exists.")
                #self.perror("Moving work product to work volume root: " + str(target))
                #self.perror("You probably want to delete the existing version's file and ingest the one referened above.")
                #target = pathlib.Path(os.path.join(volumePath,outMeshFileName))
                #source = pathlib.Path(outMesh._path)
                #source.rename(target)
                #return
            
            #self.pfeedback("Moving work product to proper location.")
            #source = pathlib.Path(outMesh._path)
            #target = pathlib.Path(newFBXVersion.GetAbsolutePath())
            #source.rename(target)
            #self.pfeedback("done.")
        
    
    
    #def do_send_obj_dir_to_uv_merged(self, args):
        #"""Sends an obj_dir representation to 3dcoat for merging and UVing.  Waits for 3dcoat to send
        #it back.
        
        #Then, it creates a new file and version in the fbx library for the result.
        
        #Usage: send_obj_dir_to_uv_merged
        #"""
        
        #args = self.ParseArguments(args)
        
        
        ##check for a proper source representation    
        #conn = self._representationsCommand.GetConnection()
        #db = self._representationsCommand.GetMultiManager()
        #db.AttachToConnection( conn)
        #rman = self._representationsCommand.GetManager(db)
        #reps = self._representationsCommand.GetItemByName("obj_dir",rman,conn)
        #conn.Close()
        
        #del conn,db,rman
        
        #if len(reps) == 0:
            #self.perror("No such representation: obj_dir")
            #return
        
        #rep = reps[0]
        
        #assert isinstance(rep, fiepipelib.assetdata.abstractassetdata.AbstractRepresentation)
        
        ##put together list of obj meshes
        
        #repDirPath = pathlib.Path(rep.GetAbsolutePath(
            #self._representationsCommand._versionShell._version))
        
        #meshes = []
        
        #for fname in os.listdir(repDirPath):
            #base, ext = os.path.splitext(fname)
            #if ext.lower() == ".obj":
                #meshes.append(fiepipe3dcoat.applink.standard.Mesh(os.path.join(str(repDirPath),fname)))


        ##get a temp folder on the working volume
        #mapper = fiepipelib.gitstorage.localstoragemapper.localstoragemapper(self.GetAssetShell()._localUser)
        #volume = mapper.GetMountedWorkingStorageByName(self.GetAssetShell()._workingRoot.GetVolumeName())
        #assert isinstance(volume, fiepipelib.storage.localvolume.localvolume)
        #volumePath = volume.GetPath()
        #with tempfile.TemporaryDirectory(dir=volumePath) as dirPath:
            ##path for 3dc to publish to
            #outMeshFileName = str(uuid.uuid4()) + ".fbx"
            #outMesh = fiepipe3dcoat.applink.standard.Mesh(os.path.join(str(dirPath),outMeshFileName))
            ##UV mode
            #mode = fiepipe3dcoat.applink.standard.Mode(fiepipe3dcoat.applink.standard.Mode.MODE_UVMapping)
            ##start the round trip
            #fiepipe3dcoat.applink.standard.StartRoundTrip(
                                                         #meshes, 
                                                         #outMesh, 
                                                         #mode, 
                                                         #[])
            
            ##event loop runs every second
            ##we look for esc to be pressed just incase.
            #self.poutput("Waiting for 3DCoat to export...")
            #self.poutput("Press 'esc' to cancel")
            
            #canceled = False
            
            #while not fiepipe3dcoat.applink.standard.ExportExists():
                #time.sleep(1.0)
                #if keyboard.is_pressed('esc'):
                    #canceled = True
                    #break
            
            ##if we canceled, we exit. the temp lib cleans up the directory for us.
            #if canceled:
                #self.poutput("User canceled.")
                #return
            
            ##an export exists
            #mesh, textures = fiepipe3dcoat.applink.standard.EndRountrip()
            #assert isinstance(mesh, fiepipe3dcoat.applink.standard.Mesh)
            #assert isinstance(textures, list)
            
            ##just incase
            #mpath = pathlib.Path(mesh._path)
            #if not mpath.exists():
                #self.perror("Mesh doesn't exist: " + str(mpath))
                #return
            
            ##no real reason to do this.  but okay.
            #for texture in textures:
                #assert isinstance(texture,
                                  #fiepipe3dcoat.applink.standard.Texture)
                #tpath = pathlib.Path(texture._path)
                ##we don't use texuteres for a uv export.
                ##if they exist, we delete them to clean up.
                #if tpath.exists():
                    #tpath.unlink()
                    
            ##now we move on to creating a proper fbx_lib entry
            #conn = self._representationsCommand.GetConnection()
            #db = fiepipefbxlib.data.common.FBXLibDatabase(self.GetGitWorkingAsset())
            #db.AttachToConnection( conn)
            #fbxman = db.GetFileManager()
            #fbxverman = db.GetFileVersionManager()
            
            #origFullName = self.GetVersion().GetFullName()
            
            ##we name it after the 'department's work'
            #newFullName = origFullName + "_uvs"
            
            ##we look for such an existing file just incase
            #foundFBXFiles = fbxman.GetByName(newFullName, conn)
            #foundFBXFile = None
            #if len(foundFBXFiles) == 0:
                ##if there were none, we create it.
                #foundFBXFile = fiepipefbxlib.data.common.FBXFileFromParameters(newFullName,{})
            #else:
                #foundFBXFile = foundFBXFiles[0]
                
            ##we set meta-data to mark it as having uvs and set it.
            #foundFBXFile.GetMeta()['uvs'] = True
            #fbxman.Set([foundFBXFile], conn)
            
            ##we look for existing versions
            #foundFBXVersions = fbxverman.GetByName(newFullName,conn)
            #newFBXVersion = None
            
            #fqdn = self.GetAssetShell()._entity.GetFQDN()
            #workingAsset = self.GetGitWorkingAsset()
            
            #if len(foundFBXVersions) == 0:
                #defverman = fiepipelib.versions.default.GetVersionDefaultManager()
                #ver = defverman.GetDefault(fqdn)
                #newFBXVersion = fiepipefbxlib.data.common.FBXFileVersionFromParameters(
                    #ver, 
                    #newFullName, 
                    #workingAsset)
            #else:
                #incverman = fiepipelib.versions.incrementation.GetVersionIncrementationManager()
                #latestVer = fiepipelib.assetdata.abstractassetdata.LatestVersion(foundFBXVersions,fqdn)
                #incverman = fiepipelib.versions.incrementation.GetVersionIncrementationManager()
                #ver = incverman.Increment(latestVer.GetVersion(), fqdn)
                #newFBXVersion = fiepipefbxlib.data.common.FBXFileVersionFromParameters(
                    #ver, 
                    #newFullName, 
                    #workingAsset)
            
            #fbxverman.Set([newFBXVersion],conn)
            #conn.Commit()
            #conn.Close()
            
            #newFBXVersion.EnsureDirExists()
            
            #if newFBXVersion.FileExists():
                #self.perror("File already exists.")
                #self.perror("Moving work product to work volume root: " + str(target))
                #self.perror("You probably want to delete the existing version's file and ingest the one referened above.")
                #target = pathlib.Path(os.path.join(volumePath,outMeshFileName))
                #targetDir = pathlib.Path(target.parent())
                #source = pathlib.Path(outMesh._path)
                #source.rename(target)
                #return
            
            #self.pfeedback("Moving work product to proper location.")
            #source = pathlib.Path(outMesh._path)
            #target = pathlib.Path(newFBXVersion.GetAbsolutePath())
            #source.rename(target)
            #self.pfeedback("done.")
