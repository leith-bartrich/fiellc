import typing

from fiepipelib.locallymanagedtypes.routines.localmanaged import AbstractLocalManagedRoutines
from fiepipelib.locallymanagedtypes.shells.AbstractLocalManagedTypeCommand import LocalManagedTypeCommand
from fiepipelib.shells.AbstractShell import AbstractShell
from fiepipeunreal4.data.installs import Unreal4Install
from fiepipeunreal4.routines.installs import Unreal4InstallsRoutines
from fiepipelib.shells.ui.abspath_input_ui import AbspathInputDefaultUI

class Unreal4InstallsCommand(LocalManagedTypeCommand[Unreal4Install]):

    def get_routines(self) -> Unreal4InstallsRoutines:
        return Unreal4InstallsRoutines(self.get_feedback_ui(),AbspathInputDefaultUI(self))

    def get_shell(self, item) -> AbstractShell:
        return super(Unreal4InstallsCommand, self).get_shell()

    def get_plugin_names_v1(self) -> typing.List[str]:
        ret = super(Unreal4InstallsCommand, self).get_plugin_names_v1()
        ret.append("unreal4_installs_command")
        return ret

    def get_prompt_text(self) -> str:
        return self.prompt_separator.join(['fiepipe','unreal4_installs'])
