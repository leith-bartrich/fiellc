import typing

from fiepipe3dcoat.coat import CoatLocalManager,coat, FromParameters
from fiepipelib.locallymanagedtypes.data.abstractmanager import AbstractUserLocalTypeManager
from fiepipelib.locallymanagedtypes.routines.localmanaged import AbstractLocalManagedInteractiveRoutines

from fiepipelib.localplatform.routines.localplatform import get_local_platform_routines
from fiepipelib.localuser.routines.localuser import LocalUserRoutines

from fiepipelib.ui.abspath_input_ui import AbstractAbspathInputUI
from fieui.FeedbackUI import AbstractFeedbackUI


class CoatLocalManagerInteractiveRoutines(AbstractLocalManagedInteractiveRoutines[coat]):

    _abspath_input_ui:AbstractAbspathInputUI = None

    def __init__(self, feedback_ui: AbstractFeedbackUI, abspath_input_ui:AbstractAbspathInputUI):
        self._abspath_input_ui = abspath_input_ui
        super().__init__(feedback_ui)

    def GetManager(self) -> CoatLocalManager:
        plat = get_local_platform_routines()
        user = LocalUserRoutines(plat)
        return CoatLocalManager(user)

    def GetAllItems(self) -> typing.List[coat]:
        manager = self.GetManager()
        return manager.GetAll()

    def ItemToName(self, item: coat) -> str:
        return item.GetName()

    def GetItemByName(self, name: str) -> coat:
        manager = self.GetManager()
        return manager.GetByName(name)[0]

    async def DeleteRoutine(self, name: str):
        manager = self.GetManager()
        manager.DeleteByName(name)

    async def CreateUpdateRoutine(self, name: str):
        path = await self._abspath_input_ui.execute("Path to 3DCoat executable.")
        path = pathlib.Path(path)

        if not path.exists():
            await self.get_feedback_ui().error("Does not exist: " + str(path))
            return
        if not path.is_file():
            await self.get_feedback_ui().error("Is not a file: " + str(path))
            return

        c3d = FromParameters(str(path.absolute()), name)
        manager = self.GetManager()
        manager.Set([c3d])
