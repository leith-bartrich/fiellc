import typing
import os
import os.path

from fiepipelib.assetaspect.routines.config import AutoConfigurationResult
from fiepipelib.localplatform.routines.localplatform import get_local_platform_routines, LocalPlatformWindowsRoutines,LocalPlatformUnixRoutines
from fiepipelib.localuser.routines.localuser import LocalUserRoutines
from fiepipelib.assetaspect.data.simpleapplication import AbstractSimpleApplicationInstallsManager
from fiepiperpgmakermv.data.aspectconfig import RPGMakerMVAspectConfiguration
from fiepiperpgmakermv.data.installs import RPGMakerMVInstallManager, RPGMakerMVInstall
from fiepipelib.assetaspect.routines.simpleapplication import AbstractSimpleFiletypeAspectConfigurationRoutines, T
from fieui.FeedbackUI import AbstractFeedbackUI


class RPGMakerMVAspectConfigurationRoutines(AbstractSimpleFiletypeAspectConfigurationRoutines[RPGMakerMVAspectConfiguration]):

    def get_filetype_extensions(self) -> typing.List[str]:
        return ["rpgproject"]

    def get_manager(self) -> RPGMakerMVInstallManager:
        plat = get_local_platform_routines()
        user = LocalUserRoutines(plat)
        return RPGMakerMVInstallManager(user)

    def get_executable_path(self, install: RPGMakerMVInstall) -> str:
        plat = get_local_platform_routines()
        if isinstance(plat, LocalPlatformWindowsRoutines):
            return os.path.join(install.get_path(),"RPGMV.exe")

    def default_configuration(self):
        self.get_configuration().from_parameters()

    async def reconfigure_interactive_routine(self):
        pass

    async def auto_reconfigure_routine(self, feedback_ui: AbstractFeedbackUI) -> AutoConfigurationResult:
        pass

