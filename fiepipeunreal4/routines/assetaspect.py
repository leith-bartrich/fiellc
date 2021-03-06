import os
import os.path
import pathlib
import typing

from fiepipelib.assetaspect.routines.config import AssetAspectConfigurationRoutines
from fiepipelib.assetaspect.routines.autoconf import AutoConfigurationResult
from fiepipeunreal4.data.assetaspect import UnrealAssetAspectConfiguration
from fiepipeunreal4.data.installs import Unreal4Install
from fiepipedesktoplib.applauncher.genericlauncher import listlauncher
from fiepipelib.localplatform.routines.localplatform import get_local_platform_routines, LocalPlatformWindowsRoutines
from fiepipelib.gitstorage.routines.gitasset import GitAssetInteractiveRoutines
from fieui.FeedbackUI import AbstractFeedbackUI
from fiepipehoudini.routines.assetaspect import HoudiniAspectConfigurationRoutines

class UnrealAspectConfigurationRoutines(AssetAspectConfigurationRoutines[UnrealAssetAspectConfiguration]):

    def __init__(self, asset_routines:GitAssetInteractiveRoutines):
        asset_routines.load()
        asset_path = asset_routines.abs_path
        super(UnrealAspectConfigurationRoutines, self).__init__(UnrealAssetAspectConfiguration(asset_path),asset_routines)

    def default_configuration(self):
        self.get_configuration().from_parameters([])

    async def reconfigure_interactive_routine(self):
        pass

    async def auto_reconfigure_routine(self, feedback_ui: AbstractFeedbackUI) -> AutoConfigurationResult:
        pass

    def find_uproject_files(self) -> typing.List[str]:
        """Finds .uproject files in the asset on disk.  Return relative paths."""
        found = []
        for root, dirs, files in os.walk(self.get_asset_path()):
            for file in files:
                base, ext = os.path.splitext(file)
                if ext == ".uproject":
                    found.append(os.path.relpath(os.path.join(root, file), self.get_asset_path()))
        return found


    def add_uproject(self, uproject_files_path: str):
        """Adds a uproject file to the configuration and sets up git tracking"""
        path = pathlib.Path(uproject_files_path)
        if path.is_absolute():
            raise ValueError("Path should be relative to this asset.")
        project_files = self.get_configuration().get_project_files()
        if not uproject_files_path in project_files:
            project_files.append(uproject_files_path)

    def get_uproject_files(self) -> typing.List[str]:
        """Gets a list of .uproject files from the configuration."""
        project_files = self.get_configuration().get_project_files().copy()
        return project_files

    def remove_uproject_file(self, uproject_file_path: str):
        """Removes a .uproject file from the configuration and removes it from git tracking"""
        project_files = self.get_configuration().get_project_files()
        if uproject_file_path in project_files:
            project_files.remove(uproject_file_path)

    async def open_in_ueditor_routine(self, feedback_ui:AbstractFeedbackUI, uproject_file_path: str, unreal_install: Unreal4Install):
        """Opens the given uproject in ueditor"""
        args = []
        unreal_engine_path = unreal_install.get_path()
        plat = get_local_platform_routines()
        if isinstance(plat, LocalPlatformWindowsRoutines):
            exepath = os.path.join(unreal_engine_path,"Engine", "Binaries", "Win64","UE4Editor.exe")
        else:
            raise NotImplementedError("Not currently implremented for non-windows platforms.")
        args.append(exepath)

        uproject_abs_path = os.path.join(self.get_asset_path(),uproject_file_path)
        args.append(uproject_abs_path)

        houdini_aspect_routines = HoudiniAspectConfigurationRoutines(self.get_asset_routines())
        default_houdini = houdini_aspect_routines.get_default_houdini()
        houdini_env = await houdini_aspect_routines.get_houdini_env(default_houdini,feedback_ui)

        launcher = listlauncher(args,extra_env=houdini_env)
        launcher.launch()
