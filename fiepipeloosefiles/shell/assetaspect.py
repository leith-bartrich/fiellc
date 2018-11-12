import typing

from fiepipelib.assetaspect.shell.config import ConfigCommand
from fiepipelib.git.routines.ignore import CheckCreateIgnore, AddIgnore
from fiepipelib.git.routines.lfs import Track, InstallLFSRepo, AddGitAttributes
from fiepipelib.shells.ui.fileext_input_ui import FileExtInputUI
from fiepipeloosefiles.data.assetaspect import LooseFilesAspectConfiguration
from fiepipeloosefiles.routines.assetaspect import LooseFilesAspectConfigurationRoutines


class LooseFilesAspectConfigCommand(ConfigCommand[LooseFilesAspectConfiguration]):

    def get_plugin_names_v1(self) -> typing.List[str]:
        ret = super(LooseFilesAspectConfigCommand, self).get_plugin_names_v1()
        ret.append("loose_files_aspect_command")
        return ret

    def get_configuration_data(self) -> LooseFilesAspectConfiguration:
        asset_routines = self.get_asset_shell().get_routines()
        asset_routines.load()
        asset_path = asset_routines.abs_path
        return LooseFilesAspectConfiguration(asset_path)

    def get_configuration_routines(self) -> LooseFilesAspectConfigurationRoutines:
        return LooseFilesAspectConfigurationRoutines(self.get_configuration_data())

    def do_add_ignore_extension(self, args):
        """Adds a file extension to ignore.

        Usage: add_ignore_extension"""
        args = self.parse_arguments(args)

        input_ui = FileExtInputUI(self)

        extension = self.do_coroutine(input_ui.execute("File extension to ignore"))
        extension = "*." + extension.lstrip('.')
        routines = self.get_configuration_routines()
        routines.load()
        repo = routines.get_asset_repo()
        CheckCreateIgnore(repo)
        AddIgnore(repo, extension)

    def do_add_lfs_track_extension(self, args):
        """Adds a file extension to track.

        Usage: add_lfs_track_extension"""
        args = self.parse_arguments(args)

        input_ui = FileExtInputUI(self)
        extension = self.do_coroutine(input_ui.execute("File extension for LFS to track"))
        extension = "*." + extension.lstrip('.')
        routines = self.get_configuration_routines()
        routines.load()
        repo = routines.get_asset_repo()
        InstallLFSRepo(repo)
        Track(repo, [extension])
        AddGitAttributes(repo)

