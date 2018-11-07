import git
import asyncio
import typing
import pkg_resources

from fiepipelib.assetaspect.routines.config import AspectConfigurationRoutines
from fiepipelib.git.routines.ignore import AddIgnore
from fiepipelib.git.routines.lfs import Track, InstallLFSRepo
from fiepipeloosefiles.data.assetaspect import LooseFilesAspectConfiguration
from fiepipelib.ui.fileext_input_ui import AbstractFileExtInputUI

class LooseFilesAspectConfigurationRoutines(AspectConfigurationRoutines[LooseFilesAspectConfiguration]):

    def default_configuration(self):
        self.get_configuration().from_parameters([], [])

    async def reconfigure(self):
        pass

    def publish_ignores(self):
        """Adds the ignores from the config to the actual ignore file.
        Skips ignores that exist.
        """
        repo = git.Repo(self.get_configuration().asset_path)
        for ignore_ext in self.get_configuration().get_ignore_extensions():
            AddIgnore(repo, "*" + ignore_ext)

    def publish_lfs_tracks(self):
        """Adds tracked files to .gitattributes file.  Ignores those that are already added."""
        repo = git.Repo(self.get_configuration().asset_path)
        InstallLFSRepo(repo)
        patterns = []
        for track_ext in self.get_configuration().get_lfs_extensions():
            patterns.append("*" + track_ext)
        return Track(repo, patterns)

    def publish(self):
        self.publish_ignores()
        self.publish_lfs_tracks()

    def get_ignore_extensions_copy(self) -> typing.List[str]:
        return self.get_configuration().get_ignore_extensions().copy()

    async def add_ignore_extension(self, input_ui:AbstractFileExtInputUI):
        extension = await input_ui.execute("Extension to add (ex: .bmp)")
        if extension not in self.get_configuration().get_ignore_extensions():
            self.get_configuration().get_ignore_extensions().append(extension)

    def remove_ignore_extension(self, ignore_ext:str):
        self.get_configuration().get_ignore_extensions().remove(ignore_ext)

    def get_lfs_track_extensions_copy(self) -> typing.List[str]:
        return self.get_configuration().get_lfs_extensions().copy()

    async def add_lfs_track_extension(self, input_ui:AbstractFileExtInputUI):
        extension = await input_ui.execute("Extension to add (ex: .bmp)")
        if extension not in self.get_configuration().get_lfs_extensions():
            self.get_configuration().get_lfs_extensions().append(extension)

    def remove_lfs_track_extension(self, lfs_ext:str):
        self.get_configuration().get_lfs_extensions().remove(lfs_ext)

    def add_from_plugins(self):

        lfs_extensions = []

        entrypoints = pkg_resources.iter_entry_points("fiepipe.plugin.loosefiles.lfs.extensions")
        for entrypoint in entrypoints:
            method = entrypoint.load()
            method(self, lfs_extensions)

        for lfs_ext in lfs_extensions:
            if lfs_ext not in self.get_configuration().get_lfs_extensions():
                self.get_configuration().get_lfs_extensions().append(lfs_ext)

        ignore_extensions = []

        entrypoints = pkg_resources.iter_entry_points("fiepipe.plugin.loosefiles.ignore.extensions")
        for entrypoint in entrypoints:
            method = entrypoint.load()
            method(self, ignore_extensions)

        for ignore_ext in ignore_extensions:
            if ignore_ext not in self.get_configuration().get_ignore_extensions():
                self.get_configuration().get_ignore_extensions().append(ignore_ext)
