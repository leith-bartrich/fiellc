from fiellclib.mr_project.data.root_config import MRProjectConfig
from fiepipelib.rootaspect.routines.config import RootAspectConfigurationRoutines


class MRProjectConfigRoutines(RootAspectConfigurationRoutines[MRProjectConfig]):

    def default_configuration(self):
        pass

    async def reconfigure_interactive_routine(self):
        pass
