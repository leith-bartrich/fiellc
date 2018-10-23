import typing
import cmd2

from fiepipelib.assetaspect.routines.config import AspectConfigurationRoutines
from fiepipelib.assetaspect.shell.config import ConfigCommand, T
from fiepipehoudini.data.assetaspect import HoudiniAssetAspectConfiguration
from fiepipehoudini.routines.assetaspect import HoudiniAspectConfigurationRoutines

class HoudiniAssetAspectCommand(ConfigCommand[HoudiniAssetAspectConfiguration]):

    def get_plugin_names_v1(self) -> typing.List[str]:
        ret = super(HoudiniAssetAspectCommand, self).get_plugin_names_v1()
        ret.append('houdini_assetaspect_command')
        return ret

    def get_configuration_data(self) -> HoudiniAssetAspectConfiguration:
        asset_routines = self.get_asset_shell().get_routines()
        asset_routines.load()
        working_asset = asset_routines.working_asset
        path = working_asset.GetSubmodule().abspath
        return HoudiniAssetAspectConfiguration(path)

    def get_configuration_routines(self) -> HoudiniAspectConfigurationRoutines:
        asset_routines = self.get_asset_shell().get_routines()
        asset_routines.load()
        working_asset = asset_routines.working_asset
        path = working_asset.GetSubmodule().abspath
        return HoudiniAspectConfigurationRoutines(path)

    complete_add_project = cmd2.Cmd.path_complete

    def do_add_project(self, args):
        """Adds a houdini project to the configuration for this asset and sets it up for GIT tracking.

        Usage: add_project [project_path]

        project_path:  A relative path to a houdini project directory.
        """
        args = self.parse_arguments(args)

        if len(args) == 0:
            self.perror("No project_path given.")
            return

        routines = self.get_configuration_routines()
        routines.load()
        routines.add_project(args[0])
        routines.commit()

    def configured_projects_complete(self, text, line, begidx, endidx):
        ret = []
        routines = self.get_configuration_routines()
        routines.load()
        project_files = routines.get_project_dirs()
        for project_file in project_files:
            if project_file.startswith(text):
                ret.append(project_file)
        return ret

    complete_remove_project = configured_projects_complete

    def do_remove_project(self, args):
        """Removes a houdini project from the configuration for this asset and removes it from GIT tracking.

        Usage: remove_project [project_path]

        project_path:  A registered project in the configuration.
        """
        args = self.parse_arguments(args)

        if len(args) == 0:
            self.perror("No project_path given.")
            return

        routines = self.get_configuration_routines()
        routines.load()
        routines.remove_project_dir(args[0])

    def do_list_projects(self, args):
        """Prints a list of projects in the configuration for this asset.

        Usage: list_projects
        """
        routines = self.get_configuration_routines()
        routines.load()
        all_projects = routines.get_project_dirs()
        for project_dir in all_projects:
            self.poutput(project_dir)


