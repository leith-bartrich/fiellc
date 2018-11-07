import typing

from fiepipelib.shells.ui.fileext_input_ui import FileExtInputUI

from fiepipelib.assetaspect.shell.config import ConfigCommand
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

    def ignore_extensions_complete(self, text, line, begidx, endidx):
        ret = []
        routines = self.get_configuration_routines()
        routines.load()
        ignores = routines.get_ignore_extensions_copy()
        for ignore in ignores:
            if ignore.startswith(text):
                ret.append(ignore)
        return ret

    def lfs_track_extensions_complete(self, text, line, begix, endidx):
        ret = []
        routines = self.get_configuration_routines()
        routines.load()
        tracks = routines.get_lfs_track_extensions_copy()
        for track in tracks:
            if track.startswith(text):
                ret.append(track)
        return ret

    def do_publish(self, args):
        """Publishes loose file tracking and ignore info to the asset.

        Usage: publish
        """
        routines = self.get_configuration_routines()
        routines.load()
        routines.add_from_plugins()
        routines.commit()
        routines.publish()

    def do_add_ignore_extension(self, args):
        """Adds a file extension to ignore.

        Usage: add_ignore_extension"""
        args = self.parse_arguments(args)

        routines = self.get_configuration_routines()
        routines.load()
        input_ui = FileExtInputUI(self)
        self.do_coroutine(routines.add_ignore_extension(input_ui))
        routines.commit()

    def do_add_lfs_track_extension(self, args):
        """Adds a file extension to track.

        Usage: add_lfs_track_extension"""
        args = self.parse_arguments(args)

        routines = self.get_configuration_routines()
        routines.load()
        input_ui = FileExtInputUI(self)
        self.do_coroutine(routines.add_lfs_track_extension(input_ui))
        routines.commit()

    complete_remove_ignore_extension = ignore_extensions_complete

    def do_remove_ignore_extension(self, args):
        """Removes a file extension to ignore

        Usage: remove_ignore_extension [ext]

        ext: The extension to remove e.g. '.bmp'
        """
        args = self.parse_arguments(args)
        if len(args) == 0:
            self.perror("No file extension given.")
            return
        routines = self.get_configuration_routines()
        routines.load()
        routines.remove_ignore_extension(args[0])
        routines.commit()

    def do_remove_lfs_track_extension(self, args):
        """Removes a file extension to track

        Usage: remove_lfs_track_extension [ext]

        ext: The extension to remove e.g. '.bmp'
        """
        args = self.parse_arguments(args)
        if len(args) == 0:
            self.perror("No file extension given.")
            return
        routines = self.get_configuration_routines()
        routines.load()
        routines.remove_lfs_track_extension(args[0])
        routines.commit()

    def do_list_ignore_extensions(self, args):
        """Lists file extensions for git to ignore.

        Usage: list_ignore_extensions
        """
        args = self.parse_arguments(args)
        routines = self.get_configuration_routines()
        routines.load()
        for ignore in routines.get_ignore_extensions_copy():
            self.poutput(ignore)

    def do_list_lfs_track_extensions(self, args):
        """Lists file extensions for lfs to track.

        Usage: list_lfs_track_extensions
        """
        args = self.parse_arguments(args)
        routines = self.get_configuration_routines()
        routines.load()
        for track in routines.get_lfs_track_extensions_copy():
            self.poutput(track)
