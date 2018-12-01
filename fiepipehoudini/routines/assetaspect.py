import os
import os.path
import pathlib
import shlex
import typing

from fiepipehoudini.data.assetaspect import HoudiniAssetAspectConfiguration
from fiepipehoudini.data.installs import HoudiniInstall
from fiepipehoudini.routines.houdini_paths import get_houdini_site_paths, get_houdini_job_paths
from fiepipelib.applauncher.genericlauncher import listlauncher
from fiepipelib.assetaspect.routines.config import AspectConfigurationRoutines
from fiepipelib.gitstorage.routines.gitasset import GitAssetRoutines
from fieui.FeedbackUI import AbstractFeedbackUI


class HoudiniAspectConfigurationRoutines(AspectConfigurationRoutines[HoudiniAssetAspectConfiguration]):

    def __init__(self, asset_routines: GitAssetRoutines):
        asset_routines.load()
        asset_path = asset_routines.abs_path
        super(HoudiniAspectConfigurationRoutines, self).__init__(HoudiniAssetAspectConfiguration(asset_path),
                                                                 asset_routines)

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

    def open_houdini(self, houdini_install: HoudiniInstall, args: typing.List[str], feedback_ui:AbstractFeedbackUI):
        launch_args = []
        exec_path = os.path.join(houdini_install.get_path(), houdini_install.get_executable())
        launch_args.append(exec_path)
        launch_args.extend(args)
        #houdini_env = {}
        houdini_env = self._get_houdini_env(houdini_install,feedback_ui)
        #houdini_env["HOUDINI_PATH"] = os.pathsep.join(self._get_houdini_paths(houdini_install,feedback_ui))
        launcher = listlauncher(launch_args, houdini_env)
        launcher.launch()

    def _run_hbatch(self, houdini_install: HoudiniInstall, non_graphic_license: bool = False,
                    file_list: typing.List[str] = [],
                    commands: typing.List[str] = [], env_vars: typing.Dict[str, str] = {}):
        launch_args = []
        exec_path = os.path.join(houdini_install.get_path(), "bin", "hbatch")
        launch_args.append(exec_path)
        for k, v in env_vars.items():
            launch_args.append("-e")
            launch_args.append(k + "=" + v)
        for c in commands:
            launch_args.append("-c")
            launch_args.append(shlex.quote(c))
        if non_graphic_license:
            launch_args.append("-R")
        for f in file_list:
            launch_args.append(shlex.quote(f))
        launcher = listlauncher(launch_args, env_vars)
        launcher.launch()

    def batch_render_hip_files(self, houdini_install: HoudiniInstall, hip_files: typing.List[str],
                               rop_node_paths: typing.List[str],
                               feedback_ui:AbstractFeedbackUI,
                               non_graphic_license: bool = False
                               ):
        commands = []
        for rop_node_path in rop_node_paths:
            commands.append("render " + rop_node_path)
        #env_vars = {}
        env_vars = self._get_houdini_env(houdini_install,feedback_ui)
        #env_vars["HOUDINI_PATH"] = os.pathsep.join(self._get_houdini_paths(houdini_install,feedback_ui))
        self._run_hbatch(houdini_install, non_graphic_license, hip_files, commands, env_vars)

    def _get_houdini_env(self, install:HoudiniInstall, feedback_ui:AbstractFeedbackUI) -> typing.Dict[str,str]:
        ret = {}

        ret['HSITE'] = self._get_houdini_site_path(install,feedback_ui)
        ret['JOB'] = self._get_houdini_job_path(install,feedback_ui)

        return ret

    def _get_houdini_job_path(self, install:HoudiniInstall, feedback_ui: AbstractFeedbackUI) -> str:
        asset_routines = self.get_asset_routines()
        asset_routines.load()
        fqdn = asset_routines.container.GetFQDN()
        container_id = asset_routines._container_id
        root_id = asset_routines._root_id
        asset_id = asset_routines._asset_id
        job_paths = get_houdini_job_paths(fqdn, container_id, root_id, asset_id, feedback_ui)
        if len(job_paths) >= 1:
            return job_paths[0]
        else:
            return ""

    def _get_houdini_site_path(self, install:HoudiniInstall, feedback_ui: AbstractFeedbackUI) -> str:
        asset_routines = self.get_asset_routines()
        asset_routines.load()
        fqdn = asset_routines.container.GetFQDN()
        container_id = asset_routines._container_id
        root_id = asset_routines._root_id
        asset_id = asset_routines._asset_id
        site_paths = get_houdini_site_paths(fqdn, container_id, root_id, asset_id, feedback_ui)
        if len(site_paths) >= 1:
            return site_paths[0]
        else:
            return ""


