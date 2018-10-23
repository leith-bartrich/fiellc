import typing

from fiepipelib.locallymanagedtypes.routines.localmanaged import AbstractLocalManagedRoutines
from fiepipelib.locallymanagedtypes.shells.AbstractLocalManagedTypeCommand import LocalManagedTypeCommand
from fiepipelib.shells.AbstractShell import AbstractShell
from fiepipehoudini.data.installs import HoudiniInstall
from fiepipehoudini.routines.installs import HoudiniInstallsRoutines
from fiepipelib.shells.ui.abspath_input_ui import AbspathInputDefaultUI
from fiepipelib.shells.ui.subpath_input_ui import SubpathInputDefaultUI

class HoudiniInstallsCommand(LocalManagedTypeCommand[HoudiniInstall]):

    def get_routines(self) -> HoudiniInstallsRoutines:
        return HoudiniInstallsRoutines(self.get_feedback_ui(),AbspathInputDefaultUI(self),SubpathInputDefaultUI(self))

    def get_shell(self, item) -> AbstractShell:
        return super(HoudiniInstallsCommand, self).get_shell()

    def get_plugin_names_v1(self) -> typing.List[str]:
        ret = super(HoudiniInstallsCommand, self).get_plugin_names_v1()
        ret.append("houdini_installs_command")
        return ret

    def get_prompt_text(self) -> str:
        return self.prompt_separator.join(['fiepipe','houdini_installs'])
