from fiepipedesktoplib.assetaspect.shell.simpleapplication import AbstractSimpleApplicationCommand
from fiepipedesktoplib.shells.ui.abspath_input_ui import AbspathInputDefaultUI
from fiepipeunreal4.data.installs import Unreal4Install
from fiepipeunreal4.routines.installs import Unreal4InstallsRoutines


class Unreal4InstallsCommand(AbstractSimpleApplicationCommand[Unreal4Install]):

    def get_routines(self) -> Unreal4InstallsRoutines:
        return Unreal4InstallsRoutines(self.get_feedback_ui(), AbspathInputDefaultUI(self))
