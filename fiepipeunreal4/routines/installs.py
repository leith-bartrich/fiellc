from fiepipelib.assetaspect.routines.simpleapplication import AbstractSimpleApplicationInstallInteractiveRoutines
from fiepipelib.localplatform.routines.localplatform import get_local_platform_routines
from fiepipelib.localuser.routines.localuser import LocalUserRoutines
from fiepipeunreal4.data.installs import Unreal4Install, Unreal4InstallsManager


class Unreal4InstallsRoutines(AbstractSimpleApplicationInstallInteractiveRoutines[Unreal4Install]):

    def GetManager(self) -> Unreal4InstallsManager:
        plat = get_local_platform_routines()
        user = LocalUserRoutines(plat)
        return Unreal4InstallsManager(user)
