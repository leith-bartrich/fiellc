import typing

from fiepipedesktoplib.assetaspect.shell.config import AssetConfigCommand
from fiepipelib.git.routines.ignore import CheckCreateIgnore, AddIgnore
from fiepipelib.git.routines.lfs import Track, InstallLFSRepo, AddGitAttributes
from fiepipedesktoplib.shells.ui.fileext_input_ui import FileExtInputUI
from fiepipeloosefiles.data.assetaspect import LooseFilesAspectConfiguration
from fiepipeloosefiles.routines.assetaspect import LooseFilesAspectConfigurationRoutines


class LooseFilesAspectConfigCommand(AssetConfigCommand[LooseFilesAspectConfiguration]):

    def get_plugin_names_v1(self) -> typing.List[str]:
        ret = super(LooseFilesAspectConfigCommand, self).get_plugin_names_v1()
        ret.append("loose_files_aspect_command")
        return ret

    def get_configuration_data(self) -> LooseFilesAspectConfiguration:
        asset_routines = self.get_asset_routines()
        asset_routines.load()
        asset_path = asset_routines.abs_path
        return LooseFilesAspectConfiguration(asset_path)

    def get_configuration_routines(self) -> LooseFilesAspectConfigurationRoutines:
        asset_routines = self.get_asset_shell().get_asset_routines()
        asset_routines.load()
        return LooseFilesAspectConfigurationRoutines(self.get_configuration_data(),asset_routines)

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

