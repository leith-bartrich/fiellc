import typing

from fiepipelib.assetaspect.routines.config import AspectConfigurationRoutines
from fiepipelib.assetaspect.shell.config import ConfigCommand, T
from fiepipeunreal4.data.assetaspect import UnrealAssetAspectConfiguration
from fiepipeunreal4.routines.assetaspect import UnrealAspectConfigurationRoutines

class Unreal4AssetAspectCommand(ConfigCommand[UnrealAssetAspectConfiguration]):

    def get_plugin_names_v1(self) -> typing.List[str]:
        ret = super(Unreal4AssetAspectCommand, self).get_plugin_names_v1()
        ret.append('unreal4_assetaspect_command')
        return ret

    def get_configuration_data(self) -> UnrealAssetAspectConfiguration:
        asset_routines = self.get_asset_shell().get_routines()
        asset_routines.load()
        working_asset = asset_routines.working_asset
        path = working_asset.GetSubmodule().abspath
        return UnrealAssetAspectConfiguration(path)

    def get_configuration_routines(self) -> UnrealAspectConfigurationRoutines:
        asset_routines = self.get_asset_shell().get_routines()
        asset_routines.load()
        working_asset = asset_routines.working_asset
        path = working_asset.GetSubmodule().abspath
        return UnrealAspectConfigurationRoutines(path)

    def uproject_files_disk_complete(self, text, line, begidx, endidx):
        ret = []
        routines = self.get_configuration_routines()
        routines.load()
        project_files = routines.find_uproject_files()
        for project_file in project_files:
            if project_file.startswith(text):
                ret.append(project_file)
        return ret

    complete_add_project = uproject_files_disk_complete

    def do_add_project(self, args):
        """Adds a unreal project to the configuration for this asset and sets it up for GIT tracking.

        Usage: add_project [uproject_path]

        uproject_path:  A relative path to a .uproject file in the asset.
        """
        args = self.parse_arguments(args)

        if len(args) == 0:
            self.perror("No uproject_path given.")
            return

        routines = self.get_configuration_routines()
        routines.load()
        routines.add_uproject(args[0])
        routines.commit()

    def configured_projects_complete(self, text, line, begidx, endidx):
        ret = []
        routines = self.get_configuration_routines()
        routines.load()
        project_files = routines.get_uproject_files()
        for project_file in project_files:
            if project_file.startswith(text):
                ret.append(project_file)
        return ret

    complete_remove_project = configured_projects_complete

    def do_remove_project(self, args):
        """Removes an unreal projet from the configuration for this asset and removes it from GIT tracking.

        Usage: remove_project [uproject_path]

        uproject_path:  A registered project in the configuration.
        """
        args = self.parse_arguments(args)

        if len(args) == 0:
            self.perror("No uproject_path given.")
            return

        routines = self.get_configuration_routines()
        routines.load()
        routines.remove_uproject_file(args[0])

    def do_list_projects(self, args):
        """Prints a list of unreal projects from the configuration for this asset.

        Usage: list_projects
        """
        routines = self.get_configuration_routines()
        routines.load()
        project_files = routines.get_uproject_files()
        for project_file in project_files:
            self.poutput(project_file)



