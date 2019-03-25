from fiepipedesktoplib.assetaspect.shell.simpleapplication import AbstractSimpleApplicationCommand
from fiepipedesktoplib.shells.ui.abspath_input_ui import AbspathInputDefaultUI
from fiepiperpgmakermv.data.installs import RPGMakerMVInstall
from fiepiperpgmakermv.routines.installs import RPGMakerMVInstallsRoutines


class RPGMakerMVInstallsCommand(AbstractSimpleApplicationCommand[RPGMakerMVInstall]):

    def get_routines(self) -> RPGMakerMVInstallsRoutines:
        return RPGMakerMVInstallsRoutines(self.get_feedback_ui(), AbspathInputDefaultUI(self))
