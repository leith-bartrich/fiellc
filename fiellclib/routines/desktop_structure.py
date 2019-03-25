import abc
import typing

from fiepipelib.assetstructure.routines.structure import BT, AbstractAssetBasePath, AbstractPath, AutoManageResults
from fiepipelib.assetstructure.routines.desktop import AbstractDesktopProjectAssetBasePath, AbstractDesktopProjectRootBasePath
from fiepipelib.automanager.data.localconfig import LegalEntityConfig
from fiepipelib.container.local_config.data.automanager import ContainerAutomanagerConfigurationComponent

from fiepipeloosefiles.routines.assetaspect import LooseFilesAspectConfigurationRoutines
from fiepipeloosefiles.data.assetaspect import LooseFilesAspectConfiguration
from fieui.FeedbackUI import AbstractFeedbackUI


class AbstractUnstructureDesktopAssetBasePath(AbstractDesktopProjectAssetBasePath[BT], abc.ABC):
    """An Asset that contains loose, unstructured files."""

    def get_sub_basepaths(self) -> typing.List["AbstractAssetBasePath"]:
        return []

    def get_subpaths(self) -> typing.List[AbstractPath]:
        return []

    def get_loose_files_aspect_config(self) -> LooseFilesAspectConfiguration:
        path = self.get_routines().abs_path
        return LooseFilesAspectConfiguration(path)

    def get_loose_files_aspect_routines(self) -> LooseFilesAspectConfigurationRoutines:
        return LooseFilesAspectConfigurationRoutines(self.get_loose_files_aspect_config(),self.get_routines())

    async def pre_children_automanage_routine(self, feedback_ui: AbstractFeedbackUI, entity_config: LegalEntityConfig,
                                              container_config: ContainerAutomanagerConfigurationComponent) -> AutoManageResults:
        ret = await super().pre_children_automanage_routine(feedback_ui, entity_config, container_config)
        loose_files_routines = self.get_loose_files_aspect_routines()
        loose_files_routines.load()
        #TODO: Do proper add/update
        loose_files_routines.update_git_meta()





