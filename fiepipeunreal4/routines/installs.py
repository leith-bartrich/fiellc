import typing

from fiepipelib.locallymanagedtypes.routines.localmanaged import AbstractLocalManagedRoutines
from fiepipelib.localplatform.routines.localplatform import get_local_platform_routines
from fiepipelib.localuser.routines.localuser import LocalUserRoutines
from fiepipelib.ui.abspath_input_ui import AbstractAbspathDefaultInputUI
from fiepipeunreal4.data.installs import Unreal4Install, Unreal4InstallsManager
from fieui.FeedbackUI import AbstractFeedbackUI


class Unreal4InstallsRoutines(AbstractLocalManagedRoutines[Unreal4Install]):
    _path_input_ui: AbstractAbspathDefaultInputUI = None

    def __init__(self, feedback_ui: AbstractFeedbackUI, path_input_ui: AbstractAbspathDefaultInputUI):
        self._path_input_ui = path_input_ui
        super().__init__(feedback_ui)

    def GetManager(self) -> Unreal4InstallsManager:
        plat = get_local_platform_routines()
        user = LocalUserRoutines(plat)
        return Unreal4InstallsManager(user)

    def GetAllItems(self) -> typing.List[Unreal4Install]:
        man = self.GetManager()
        return man.GetAll()

    def ItemToName(self, item: Unreal4Install) -> str:
        return item.get_name()

    def GetItemByName(self, name: str) -> Unreal4Install:
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
            item = man.FromParameters(name, ".")
        path = await self._path_input_ui.execute("Path to Unreal4 Install Dir", item.get_path())
        item._path = path
        man.Set([item])
