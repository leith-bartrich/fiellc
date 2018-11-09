from fiepipelib.assetaspect.routines.simpleapplication import AbstractSimpleApplicationRoutines
from fiepipelib.localplatform.routines.localplatform import get_local_platform_routines
from fiepipelib.localuser.routines.localuser import LocalUserRoutines
from fiepiperpgmakermv.data.installs import RPGMakerMVInstall, RPGMakerMVInstallManager


class RPGMakerMVInstallsRoutines(AbstractSimpleApplicationRoutines[RPGMakerMVInstall]):

    def GetManager(self) -> RPGMakerMVInstallManager:
        plat = get_local_platform_routines()
        user = LocalUserRoutines(plat)
        return RPGMakerMVInstallManager(user)
