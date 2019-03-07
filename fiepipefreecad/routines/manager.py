import pathlib
import typing

from fiepipefreecad.freecad import FreeCADLocalManager, FreeCAD, FromParameters
from fiepipelib.locallymanagedtypes.routines.localmanaged import AbstractLocalManagedInteractiveRoutines
from fiepipelib.localplatform.routines.localplatform import get_local_platform_routines
from fiepipelib.localuser.routines.localuser import LocalUserRoutines
from fiepipelib.ui.abspath_input_ui import AbstractAbspathInputUI
from fieui.FeedbackUI import AbstractFeedbackUI


class FreeCADLocalManagerInteractiveRoutines(AbstractLocalManagedInteractiveRoutines[FreeCAD]):
    _path_input_ui: AbstractAbspathInputUI = None

    def __init__(self, feedback_ui: AbstractFeedbackUI, path_input_ui: AbstractAbspathInputUI):
        self._path_input_ui = path_input_ui
        super().__init__(feedback_ui)

    def GetManager(self) -> FreeCADLocalManager:
        plat = get_local_platform_routines()
        user = LocalUserRoutines(plat)
        return FreeCADLocalManager(user)

    def GetAllItems(self) -> typing.List[FreeCAD]:
        return self.GetManager().GetAll()

    def ItemToName(self, item: FreeCAD) -> str:
        return item.GetName()

    def GetItemByName(self, name: str) -> FreeCAD:
        manager = self.GetManager()
        return manager.GetByName(name)[0]

    async def DeleteRoutine(self, name: str):
        manager = self.GetManager().DeleteByName(name)

    async def CreateUpdateRoutine(self, name: str):

        path = await self._path_input_ui.execute("Path to FreeCAD install dir.")
        path = pathlib.Path(path)
        if not path.exists():
            await self.get_feedback_ui().error("Does not exist: " + str(path))
            return
        if not path.is_dir():
            await self.get_feedback_ui().error("Is not a directory: " + str(path))
            return

        freecad = FromParameters(str(path.absolute()), name)
        manager = self.GetManager()
        manager.Set([freecad])
