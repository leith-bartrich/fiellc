from fiepipelib.assetaspect.routines.config import AspectConfigurationRoutines
from fiepipeloosefiles.data.assetaspect import LooseFilesAspectConfiguration


class LooseFilesAspectConfigurationRoutines(AspectConfigurationRoutines[LooseFilesAspectConfiguration]):

    def default_configuration(self):
        self.get_configuration().from_parameters(   )

    async def reconfigure(self):
        pass
