import typing

from fiellclib.mr_project.data.root_config import MRProjectConfig
from fiellclib.mr_project.routines.root_config import MRProjectConfigRoutines
from fiepipedesktoplib.rootaspect.shell.config import RootConfigCommand


class MRProjectConfigShell(RootConfigCommand[MRProjectConfig]):

    def get_configuration_routines(self) -> MRProjectConfigRoutines:
        return MRProjectConfigRoutines(self.get_configuration_data())

    def get_plugin_names_v1(self) -> typing.List[str]:
        ret = super(MRProjectConfigShell, self).get_plugin_names_v1()
        ret.append("fiellc.mr_project.configuration.command")
        return ret

    def get_configuration_data(self) -> MRProjectConfig:
        root_routines = self.get_root_shell().get_routines()
        root_routines.load()
        repo_path = root_routines.get_local_repo_path()
        return MRProjectConfig(repo_path)
