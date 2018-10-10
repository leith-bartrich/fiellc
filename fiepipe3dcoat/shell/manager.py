import typing

import fiepipelib.locallymanagedtypes.shells.AbstractLocalManagedTypeCommand
import fiepipelib.localuser.routines.localuser
from fiepipe3dcoat.routines.manager import CoatLocalManagerRoutines
from fiepipelib.shells.AbstractShell import AbstractShell
from fiepipelib.shells.ui.abspath_input_ui import AbspathInputUI


class CoatSystemCommand(fiepipelib.locallymanagedtypes.shells.AbstractLocalManagedTypeCommand.LocalManagedTypeCommand):

    def get_routines(self) -> CoatLocalManagerRoutines:
        return CoatLocalManagerRoutines(self.get_feedback_ui(), AbspathInputUI(self))

    def get_shell(self, item) -> AbstractShell:
        raise NotImplementedError("3DCoat command does not support 'enter' at this time.")

    def get_plugin_names_v1(self) -> typing.List[str]:
        ret = super(CoatSystemCommand, self).get_plugin_names_v1()
        ret.append("coat3d_system_command")
        return ret

    def get_prompt_text(self) -> str:
        return self.prompt_separator.join(["fiepipe", "3DCoat"])
