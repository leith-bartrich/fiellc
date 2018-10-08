import fiepipelib.localplatform.routines.localplatform
import fiepipelib.localuser.routines.localuser
import fiepipe3dcoat.coat
import fiepipelib.assetdata.shell
import fiepipelib.assetdata.data.items
import fiepipe3dcoat.applink.standard

def coat_complete(text, line, begidx, endidx):
    ret = []
    plat = fiepipelib.localplatform.routines.localplatform.get_local_platform_routines()
    user = fiepipelib.localuser.routines.localuser.LocalUserRoutines(plat)
    coatman = fiepipe3dcoat.coat.CoatLocalManager(user)
    allcoats = coatman.GetAll()
    for coat in allcoats:
        assert isinstance(coat, fiepipe3dcoat.coat.coat)
        if coat.GetName().startswith(text):
            ret.append(coat.GetName())
    return ret
