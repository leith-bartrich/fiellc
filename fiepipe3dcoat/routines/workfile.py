import asyncio

from fiepipe3dcoat.data.workfile import WorkFile, WorkFileDB, WorkFileManager, WorkFileVersion, WorkFileVersionManager
from fiepipelib.fileversion.data.fileversion import LatestVersion
from fiepipelib.assetdata.data.connection import Connection
from fiepipelib.gitstorage.data.git_working_asset import GitWorkingAsset
from fiepipelib.versions.default import GetVersionDefaultManager
from fiepipelib.versions.incrementation import GetVersionIncrementationManager


async def EnsureWorkfileRoutine(workfileName:str, asset:GitWorkingAsset, db:WorkFileDB, man:WorkFileManager, conn:Connection) -> WorkFile:
    allWorkFiles = man.GetByName(workfileName, conn)
    if len(allWorkFiles) == 0:
        man.Set([man.NewFromParameters(workfileName)],conn)
        allWorkFiles = man.GetByName(workfileName,conn)
    workFile = allWorkFiles[0]
    return workFile

async def EnsureWorkfileAndMetaRoutine(workfileName:str, meta:dict, asset:GitWorkingAsset, db:WorkFileDB, man:WorkFileManager, conn:Connection) -> WorkFile:
    ret = await EnsureWorkfileRoutine(workfileName, asset, db, man, conn)
    for k in meta.keys():
        ret._meta[k] = meta[k]
    man.Set([ret], conn)
    return ret

async def NewTemplatedVersionRoutine(f:asyncio.Future, workFile:WorkFile, templatePath:str, asset:GitWorkingAsset, fqdn:str, db:WorkFileDB, man:WorkFileVersionManager, conn:Connection) -> WorkFileVersion:
    allVersions = man.GetByWorkFile(workFile._name, conn)
    ret = None
    if len(allVersions) == 0:
        #create default
        defMan = GetVersionDefaultManager()
        defVer = defMan.get_default(fqdn)
        ret = man.NewFromParameters(workFile._name, defVer)
    else:
        #create incredmented
        latestVer = LatestVersion(allVersions, fqdn)
        incMan = GetVersionIncrementationManager()
        incVer = incMan.Increment(latestVer.GetVersion(), fqdn)
        ret = man.NewFromParameters(workFile._name, incVer)
    man.Set([ret], connn)

    deployTemplateFuture = asyncio.Future
    await DeployTemplateRoutine(deployTemplateFuture,ret,templatePath)

    if deployTemplateFuture.cancelled():
        f.cancel()
        return
    
    deployTemplateFuture.result()
    
    f.set_result(ret)
    return
