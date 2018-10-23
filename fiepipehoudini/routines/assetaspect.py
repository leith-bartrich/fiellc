import os
import os.path
import pathlib
import typing

import git

from fiepipelib.assetaspect.routines.config import AspectConfigurationRoutines
from fiepipehoudini.data.assetaspect import HoudiniAssetAspectConfiguration
from fiepipehoudini.routines.git import add_project_tracking_metadata, remove_project_tracking_metadata


class HoudiniAspectConfigurationRoutines(AspectConfigurationRoutines[HoudiniAssetAspectConfiguration]):
    _asset_path: str = None

    def __init__(self, asset_path: str):
        self._asset_path = asset_path
        super(HoudiniAspectConfigurationRoutines, self).__init__(HoudiniAssetAspectConfiguration(self._asset_path))

    def default_configuration(self):
        self.get_configuration().from_parameters([])

    async def reconfigure(self):
        pass

    def _add_to_git_tracking(self, houdini_project_path: str):
        repo = git.Repo(self._asset_path)
        add_project_tracking_metadata(repo, houdini_project_path)

    def _remove_from_git_tracking(self, houdini_project_path: str):
        repo = git.Repo(self._asset_path)
        remove_project_tracking_metadata(repo, houdini_project_path)

    def add_project(self, houdini_project_path: str):
        """Adds a project directory to the configuration and sets up git tracking"""
        path = pathlib.Path(houdini_project_path)
        if path.is_absolute():
            raise ValueError("Path should be relative to this asset.")
        project_files = self.get_configuration().get_project_dirs()
        if not houdini_project_path in project_files:
            project_files.append(houdini_project_path)
        self._add_to_git_tracking(houdini_project_path)

    def get_project_dirs(self) -> typing.List[str]:
        """Gets a list of project directories from the configuration."""
        project_dirs = self.get_configuration().get_project_dirs().copy()
        return project_dirs

    def remove_project_dir(self, houdini_project_dir: str):
        """Removes a project dir from the configuration and removes it from git tracking"""
        project_dirs = self.get_configuration().get_project_dirs()
        if houdini_project_dir in project_dirs:
            project_dirs.remove(houdini_project_dir)
        self._remove_from_git_tracking(houdini_project_dir)
