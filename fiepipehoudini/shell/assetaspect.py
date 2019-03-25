import os
import os.path
import typing

import cmd2

from fiepipehoudini.data.assetaspect import HoudiniAssetAspectConfiguration
from fiepipehoudini.data.filetypes import get_hip_extensions
from fiepipehoudini.data.installs import HoudiniInstallsManager
from fiepipehoudini.routines.assetaspect import HoudiniAspectConfigurationRoutines
from fiepipedesktoplib.assetaspect.shell.config import AssetConfigCommand
from fiepipelib.localplatform.routines.localplatform import get_local_platform_routines
from fiepipelib.localuser.routines.localuser import LocalUserRoutines


class HoudiniAssetAspectCommand(AssetConfigCommand[HoudiniAssetAspectConfiguration]):

    def get_plugin_names_v1(self) -> typing.List[str]:
        ret = super(HoudiniAssetAspectCommand, self).get_plugin_names_v1()
        ret.append('houdini_assetaspect_command')
        return ret

    def get_configuration_data(self) -> HoudiniAssetAspectConfiguration:
        asset_routines = self.get_asset_shell().get_routines()
        asset_routines.load()
        working_asset = asset_routines.working_asset
        path = working_asset.GetSubmodule().abspath
        return HoudiniAssetAspectConfiguration(path)

    def get_configuration_routines(self) -> HoudiniAspectConfigurationRoutines:
        asset_routines = self.get_asset_shell().get_routines()
        return HoudiniAspectConfigurationRoutines(asset_routines)

    complete_add_project = cmd2.Cmd.path_complete

    def do_add_project(self, args):
        """Adds a houdini project to the configuration for this asset and sets it up for GIT tracking.

        Usage: add_project [project_path]

        project_path:  A relative path to a houdini project directory.
        """
        args = self.parse_arguments(args)

        if len(args) == 0:
            self.perror("No project_path given.")
            return

        routines = self.get_configuration_routines()
        routines.load()
        routines.add_project(args[0])
        routines.commit()

    def configured_projects_complete(self, text, line, begidx, endidx):
        ret = []
        routines = self.get_configuration_routines()
        routines.load()
        project_files = routines.get_project_dirs()
        for project_file in project_files:
            if project_file.startswith(text):
                ret.append(project_file)
        return ret

    complete_remove_project = configured_projects_complete

    def do_remove_project(self, args):
        """Removes a houdini project from the configuration for this asset and removes it from GIT tracking.

        Usage: remove_project [project_path]

        project_path:  A registered project in the configuration.
        """
        args = self.parse_arguments(args)

        if len(args) == 0:
            self.perror("No project_path given.")
            return

        routines = self.get_configuration_routines()
        routines.load()
        routines.remove_project_dir(args[0])

    def do_list_projects(self, args):
        """Prints a list of projects in the configuration for this asset.

        Usage: list_projects
        """
        routines = self.get_configuration_routines()
        routines.load()
        all_projects = routines.get_project_dirs()
        for project_dir in all_projects:
            self.poutput(project_dir)

    def houdini_install_complete(self, text, line, begidx, endidx):
        ret = []
        plat = get_local_platform_routines()
        user = LocalUserRoutines(plat)
        man = HoudiniInstallsManager(user)
        for houdini in man.GetAll():
            if houdini.get_name().startswith(text):
                ret.append(houdini.get_name())
        return ret

    complete_open = houdini_install_complete

    def do_open(self, args):
        """Opens the given houdini version.

        Usage: open [houdini_install]

        houdini_install:  The name of the houdini install to open.
        """
        args = self.parse_arguments(args)
        if len(args) < 1:
            self.perror("No houdini_install specified.")
            return

        plat = get_local_platform_routines()
        user = LocalUserRoutines(plat)
        man = HoudiniInstallsManager(user)
        houdini = man.get_by_name(args[0])

        routines = self.get_configuration_routines()
        routines.load()

        self.do_coroutine(routines.open_houdini_routine(houdini, [], self.get_feedback_ui()))

    def hip_file_complete(self, text, line, begidx, endidx):
        ret = []
        hip_exts = get_hip_extensions(".")
        paths = self.path_complete(text, line, begidx, endidx)
        for p in paths:
            base, ext = os.path.splitext(p)
            if ext.lower() in hip_exts:
                ret.append(p)

    def complete_batch_render(self, text, line, begidx, endidx):
        return self.index_based_complete(text, line, begidx, endidx,
                                         {1: self.houdini_install_complete, 2: self.hip_file_complete, 3: None})

    def do_batch_render(self, args):
        """Batch renders the given hip file with the given rop path.

        batch_render [houdini_install] [file] [rop_path]

        houdini_install:  The name of the houdini install to use to render
        file: The path to the hip file.
        rop_path:  The path to the rop to render in the file."""
        args = self.parse_arguments(args)

        if len(args) < 1:
            self.perror("No houdini_install specified.")
            return

        if len(args) < 2:
            self.perror("No file specified.")
            return

        if len(args) < 3:
            self.perror("No rop_path specified.")
            return

        plat = get_local_platform_routines()
        user = LocalUserRoutines(plat)
        man = HoudiniInstallsManager(user)
        houdini = man.get_by_name(args[0])

        routines = self.get_configuration_routines()
        routines.load()

        self.do_coroutine(routines.batch_render_hip_files_routine(houdini, [args[1]], [args[2]], self.get_feedback_ui()))

    def complete_hython_module(self, text, line, begidx, endidx):
        return self.index_based_complete(text, line, begidx, endidx, {1: self.houdini_install_complete})

    def do_hython_module(self, args):
        """Runs the given module with the given arguments in houdini python (hython).

        Usage hython_module [houdini_install] [module] {[arg] ...}

        houdini_install: The houdini install to use
        module: The python module to run
        arg: Optional arguments to pass to python's sys.argv
        """
        args = self.parse_arguments(args)

        if len(args) < 1:
            self.perror("No houdini_install given.")
            return
        if len(args) < 2:
            self.perror("No module given.")
            return

        plat = get_local_platform_routines()
        user = LocalUserRoutines(plat)
        man = HoudiniInstallsManager(user)
        houdini = man.get_by_name(args[0])

        module_name = args[1]

        py_args = args[2:]

        routines = self.get_configuration_routines()
        routines.load()

        self.do_coroutine(routines.run_hython_script_routine(houdini,module_name,py_args,self.get_feedback_ui()))

