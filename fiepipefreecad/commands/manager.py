import typing

import fiepipelib.locallymanagedtypes.shells.AbstractLocalManagedTypeCommand
import fiepipelib.shells.AbstractShell
from fiepipefreecad.routines.manager import FreeCADLocalManagerInteractiveRoutines
from fiepipelib.shells.AbstractShell import AbstractShell
from fiepipelib.shells.ui.abspath_input_ui import AbspathInputUI


class FreeCADSystemCommand(fiepipelib.locallymanagedtypes.shells.AbstractLocalManagedTypeCommand.LocalManagedTypeCommand):

    def get_routines(self) -> FreeCADLocalManagerInteractiveRoutines:
        return FreeCADLocalManagerInteractiveRoutines(self.get_feedback_ui(), AbspathInputUI(self))

    def get_shell(self, item) -> AbstractShell:
        self.poutput("Entering a FreeCAD instance is currently not supported.")
        raise NotImplementedError()

    def get_plugin_names_v1(self) -> typing.List[str]:
        ret = super(FreeCADSystemCommand, self).get_plugin_names_v1()
        ret.append("freecad_system_command")
        return ret

    def get_prompt_text(self) -> str:
        return self.prompt_separator.join(["fiepipe", "freecad"])
