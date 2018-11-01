import typing

from fiepipehoudini.data.installs import HoudiniInstall, HoudiniInstallsManager
from fiepipelib.locallymanagedtypes.routines.localmanaged import AbstractLocalManagedRoutines
from fiepipelib.localplatform.routines.localplatform import get_local_platform_routines
from fiepipelib.localuser.routines.localuser import LocalUserRoutines
from fiepipelib.ui.abspath_input_ui import AbstractAbspathDefaultInputUI
from fiepipelib.ui.subpath_input_ui import AbstractSubpathDefaultInputUI
from fieui.FeedbackUI import AbstractFeedbackUI


class HoudiniInstallsRoutines(AbstractLocalManagedRoutines[HoudiniInstall]):
    _path_input_ui: AbstractAbspathDefaultInputUI = None
    _executable_input_ui: AbstractSubpathDefaultInputUI

    def __init__(self, feedback_ui: AbstractFeedbackUI, path_input_ui: AbstractAbspathDefaultInputUI,
                 executable_input_ui: AbstractSubpathDefaultInputUI):
        self._path_input_ui = path_input_ui
        self._executable_input_ui = executable_input_ui
        super().__init__(feedback_ui)

    def GetManager(self) -> HoudiniInstallsManager:
        plat = get_local_platform_routines()
        user = LocalUserRoutines(plat)
        return HoudiniInstallsManager(user)

    def GetAllItems(self) -> typing.List[HoudiniInstall]:
        man = self.GetManager()
        return man.GetAll()

    def ItemToName(self, item: HoudiniInstall) -> str:
        return item.get_name()

    def GetItemByName(self, name: str) -> HoudiniInstall:
        man = self.GetManager()
        return man.get_by_name(name)

    async def DeleteRoutine(self, name: str):
        man = self.GetManager()
        man.delete_by_name(name)

    async def CreateUpdateRoutine(self, name: str):
        man = self.GetManager()
        try:
            item = man.get_by_name(name)
        except LookupError:
            item = man.FromParameters(name, ".","bin\\houdini.exe")
        path = await self._path_input_ui.execute("Path to Unreal4 Install Dir", item.get_path())
        executable = await self._executable_input_ui.execute("Executable sub-path", item.get_executable())
        item._path = path
        item._executable = executable
        man.Set([item])
