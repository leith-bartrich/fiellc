from fiepipelib.assetaspect.routines.config import AspectConfigurationRoutines
from fiepipelib.assetaspect.routines.autoconf import AutoConfigurationResult
from fiepipeloosefiles.data.assetaspect import LooseFilesAspectConfiguration
from fieui.FeedbackUI import AbstractFeedbackUI


class LooseFilesAspectConfigurationRoutines(AspectConfigurationRoutines[LooseFilesAspectConfiguration]):

    def default_configuration(self):
        self.get_configuration().from_parameters(   )

    async def reconfigure_interactive_routine(self):
        pass

    async def auto_reconfigure_routine(self, feedback_ui: AbstractFeedbackUI) -> AutoConfigurationResult:
        pass


