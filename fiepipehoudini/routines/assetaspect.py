import os
import os.path
import pathlib
import typing

from fiepipehoudini.data.assetaspect import HoudiniAssetAspectConfiguration
from fiepipehoudini.data.installs import HoudiniInstall
from fiepipelib.applauncher.genericlauncher import listlauncher
from fiepipelib.assetaspect.routines.config import AspectConfigurationRoutines


class HoudiniAspectConfigurationRoutines(AspectConfigurationRoutines[HoudiniAssetAspectConfiguration]):
    _asset_path: str = None

    def __init__(self, asset_path: str):
        self._asset_path = asset_path
        super(HoudiniAspectConfigurationRoutines, self).__init__(HoudiniAssetAspectConfiguration(self._asset_path))

    def default_configuration(self):
        self.get_configuration().from_parameters([])

    async def reconfigure(self):
        pass

    def add_project(self, houdini_project_path: str):
        """Adds a project directory to the configuration and sets up git tracking"""
        path = pathlib.Path(houdini_project_path)
        if path.is_absolute():
            raise ValueError("Path should be relative to this asset.")
        project_files = self.get_configuration().get_project_dirs()
        if not houdini_project_path in project_files:
            project_files.append(houdini_project_path)

    def get_project_dirs(self) -> typing.List[str]:
        """Gets a list of project directories from the configuration."""
        project_dirs = self.get_configuration().get_project_dirs().copy()
        return project_dirs

    def remove_project_dir(self, houdini_project_dir: str):
        """Removes a project dir from the configuration and removes it from git tracking"""
        project_dirs = self.get_configuration().get_project_dirs()
        if houdini_project_dir in project_dirs:
            project_dirs.remove(houdini_project_dir)

    def open_houdini(self, houdini_install: HoudiniInstall, args: typing.List[str]):
        launch_args = []
        exec_path = os.path.join(houdini_install.get_path(), houdini_install.get_executable())
        launch_args.append(exec_path)
        launch_args.extend(args)
        launcher = listlauncher(launch_args)
        launcher.launch()
