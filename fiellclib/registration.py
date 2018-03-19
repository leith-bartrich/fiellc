import fiepipelib.localplatform
import fiepipelib.localuser
import fiepipelib.registeredlegalentity
import fiepipelib.storage.localvolume
import os.path
import json

def IsRegistered():
    plat = fiepipelib.localplatform.GetLocalPlatform()
    user = fiepipelib.localuser.localuser(plat)
    registry = fiepipelib.registeredlegalentity.localregistry(user)
    entities = registry.GetByFQDN("fie.us")
    return len(entities) > 0


def Register():
    moduleDir = os.path.dirname(__file__)
    regPath = os.path.join(moduleDir, "registration.fiepipe.fie.us.json")
    regFile = open(regPath)
    data = json.load(regFile)
    regFile.close()
    registration = fiepipelib.registeredlegalentity.FromJSONData(data)
    plat = fiepipelib.localplatform.GetLocalPlatform()
    user = fiepipelib.localuser.localuser(plat)
    registry = fiepipelib.registeredlegalentity.localregistry(user)
    registry.Set([registration])

def SetupStandardVolumes():
    plat = fiepipelib.localplatform.GetLocalPlatform()
    user = fiepipelib.localuser.localuser(plat)
    registry = fiepipelib.storage.localvolume.localvolumeregistry(user)
    docsentries = registry.GetByName("docs")
    docsvolume = None
    if len(docsentries) == 0:
        homevolume = fiepipelib.storage.localvolume.GetHomeVolume(user)
        docsvolume = fiepipelib.storage.localvolume.FromParameters("docs",os.path.join(homevolume.GetPath(),"Documents"))
    else:
        docsvolume = docsentries[0]
    if not docsvolume.HasAdjective(fiepipelib.storage.localvolume.CommonAdjectives.containerrole.WORKING_VOLUME):
        docsvolume.AddAdjective(fiepipelib.storage.localvolume.CommonAdjectives.containerrole.WORKING_VOLUME)
    if not docsvolume.HasAdjective(fiepipelib.storage.localvolume.CommonAdjectives.containerrole.WORKING_VOLUME):
        docsvolume.AddAdjective(fiepipelib.storage.localvolume.CommonAdjectives.containerrole.WORKING_VOLUME)
    registry.Set([docsvolume])

    