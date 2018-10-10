import fiepipelib.localplatform.routines.localplatform
import fiepipelib.localuser.routines.localuser
import fiepipelib.legalentity.registry.data.registered_entity
import fiepipelib.storage.localvolume
import os.path
import json

def is_registered():
    plat = fiepipelib.localplatform.routines.localplatform.get_local_platform_routines()
    user = fiepipelib.localuser.routines.localuser.LocalUserRoutines(plat)
    registry = fiepipelib.legalentity.registry.data.registered_entity.localregistry(user)
    entities = registry.GetByFQDN("fie.us")
    return len(entities) > 0


def register():
    moduleDir = os.path.dirname(__file__)
    regPath = os.path.join(moduleDir, "registration.fiepipe.fie.us.json")
    regFile = open(regPath,'r')
    data = json.load(regFile)
    regFile.close()

    registration = fiepipelib.legalentity.registry.data.registered_entity.FromJSONData(data)
    plat = fiepipelib.localplatform.routines.localplatform.get_local_platform_routines()
    user = fiepipelib.localuser.routines.localuser.LocalUserRoutines(plat)
    registry = fiepipelib.legalentity.registry.data.registered_entity.localregistry(user)
    registry.Set([registration])

def setup_standard_volumes():
    plat = fiepipelib.localplatform.routines.localplatform.get_local_platform_routines()
    user = fiepipelib.localuser.routines.localuser.LocalUserRoutines(plat)
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

    