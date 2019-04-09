from fiellclib.mr_project.data.root_config import MRProjectConfig
from fiepipelib.rootaspect.routines.config import RootAspectConfigurationRoutines
from fieui.InputDefaultModalUI import AbstractInputDefaultModalUI


class MRProjectConfigRoutines(RootAspectConfigurationRoutines[MRProjectConfig]):

    _gitlab_server_name_inputui: AbstractInputDefaultModalUI = None

    def __init__(self, config: MRProjectConfig, gitlab_server_nameui:AbstractInputDefaultModalUI):
        self._gitlab_server_name_inputui = gitlab_server_nameui
        super().__init__(config)

    def default_configuration(self):
        self.get_configuration().set_gitlab_server_name("gitlab")

    async def reconfigure_interactive_routine(self):
        server_name = await self._gitlab_server_name_inputui.execute("GitLab server name?", self.get_configuration()._gitlab_server_name)
        self.get_configuration().set_gitlab_server_name(server_name)
