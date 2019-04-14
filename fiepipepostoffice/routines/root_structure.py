import typing

from fiepipelib.assetstructure.routines.structure import AbstractSubPath, AbstractAssetBasePath, \
    GenericAssetBasePathsSubDir, AbstractRootBasePath, AutoManageResults, StaticSubDir
from fiepipelib.automanager.data.localconfig import LegalEntityConfig
from fiepipelib.container.local_config.data.automanager import ContainerAutomanagerConfigurationComponent
from fiepipelib.gitstorage.routines.gitroot import GitRootRoutines
from fieui.FeedbackUI import AbstractFeedbackUI
from fiepipepostoffice.routines.box_structure import Box


class PostOfficeRootStructureRoutines(AbstractRootBasePath["PostOfficeRootStructureRoutines"]):
    _boxes:"Boxes" = None

    def get_boxes(self):
        return self._boxes

    def __init__(self, routines: GitRootRoutines):
        super().__init__(routines)
        self._boxes = Boxes("boxes", self)

    async def automanager_routine(self, feedback_ui: AbstractFeedbackUI, entity_config: LegalEntityConfig,
                                  container_config: ContainerAutomanagerConfigurationComponent) -> AutoManageResults:
        raise NotImplementedError()

    def get_sub_basepaths(self) -> typing.List["AbstractAssetBasePath"]:
        return self._boxes.get_asset_basepaths()

    def get_subpaths(self) -> "typing.List[AbstractSubPath[PostOfficeRootStructureRoutines]]":
        return [self._boxes]


class Boxes(GenericAssetBasePathsSubDir["PostOfficeRootStructureRoutines", "PostOfficeRootStructureRoutines", "Box"]):

    def get_asset_basepath_by_dirname(self, dirname: str) -> "Box":
        asset_routines = self.get_asset_routines_by_dirname(dirname)
        asset_routines.load()
        return Box(asset_routines)
