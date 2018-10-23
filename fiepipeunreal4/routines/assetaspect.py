import os
import os.path
import pathlib
import typing

import git

from fiepipelib.assetaspect.routines.config import AspectConfigurationRoutines
from fiepipeunreal4.data.assetaspect import UnrealAssetAspectConfiguration
from fiepipeunreal4.routines.git import add_project_tracking_metadata, remove_project_tracking_metadata


class UnrealAspectConfigurationRoutines(AspectConfigurationRoutines[UnrealAssetAspectConfiguration]):
    _asset_path: str = None

    def __init__(self, asset_path: str):
        self._asset_path = asset_path
        super(UnrealAspectConfigurationRoutines, self).__init__(UnrealAssetAspectConfiguration(self._asset_path))

    def default_configuration(self):
        self.get_configuration().from_parameters([])

    async def reconfigure(self):
        pass

    def find_uproject_files(self) -> typing.List[str]:
        """Finds .uproject files in the asset on disk.  Return relative paths."""
        found = []
        for root, dirs, files in os.walk(self._asset_path):
            for file in files:
                base, ext = os.path.splitext(file)
                if ext == ".uproject":
                    found.append(os.path.relpath(os.path.join(root, file), self._asset_path))
        return found

    def _add_to_git_tracking(self, uproject_file_path: str):
        repo = git.Repo(self._asset_path)
        add_project_tracking_metadata(repo, uproject_file_path)

    def _remove_from_git_tracking(self, uproject_file_path: str):
        repo = git.Repo(self._asset_path)
        remove_project_tracking_metadata(repo, uproject_file_path)

    def add_uproject(self, uproject_files_path: str):
        """Adds a uproject file to the configuration and sets up git tracking"""
        path = pathlib.Path(uproject_files_path)
        if path.is_absolute():
            raise ValueError("Path should be relative to this asset.")
        project_files = self.get_configuration().get_project_files()
        if not uproject_files_path in project_files:
            project_files.append(uproject_files_path)
        self._add_to_git_tracking(uproject_files_path)

    def get_uproject_files(self) -> typing.List[str]:
        """Gets a list of .uproject files from the configuration."""
        project_files = self.get_configuration().get_project_files().copy()
        return project_files

    def remove_uproject_file(self, uproject_file_path: str):
        """Removes a .uproject file from the configuration and removes it from git tracking"""
        project_files = self.get_configuration().get_project_files()
        if uproject_file_path in project_files:
            project_files.remove(uproject_file_path)
        self._remove_from_git_tracking(uproject_file_path)
