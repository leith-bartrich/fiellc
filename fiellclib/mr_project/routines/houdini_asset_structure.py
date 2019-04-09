import typing

from fiepipehoudini.routines.structure import HoudiniDesktopAssetBasePath
from fiepipelib.assetstructure.routines.structure import AbstractAssetBasePath, AbstractSubPath, BT, AutoCreateResults
from fiepipelib.automanager.data.localconfig import LegalEntityConfig
from fiepipelib.container.local_config.data.automanager import ContainerAutomanagerConfigurationComponent
from fieui.FeedbackUI import AbstractFeedbackUI
from fiepipelib.enum import get_worse_enum
from fiepipehoudini.routines.assetaspect import HoudiniAspectConfigurationRoutines

class HoudiniAssetBasePath(HoudiniDesktopAssetBasePath):

    def get_sub_basepaths(self) -> typing.List["AbstractAssetBasePath"]:
        return []

    def get_subpaths(self) -> "typing.List[AbstractSubPath[BT]]":
        return []

    async def automanager_create_self(self, feedback_ui: AbstractFeedbackUI, entity_config: LegalEntityConfig,
                                      container_config: ContainerAutomanagerConfigurationComponent) -> AutoCreateResults:

        ret = await super().automanager_create_self(feedback_ui, entity_config, container_config)
        asset_routines = self.get_routines()
        houdini_routines = HoudiniAspectConfigurationRoutines(asset_routines)

        if not houdini_routines.is_configured():
            houdini_routines.default_configuration()
            houdini_routines.commit()
            houdini_routines.update_git_meta()
            ret = get_worse_enum(ret, AutoCreateResults.CHANGES_MADE)
        else:
            houdini_routines.update_git_meta()
            ret = get_worse_enum(ret, AutoCreateResults.NO_CHANGES)

        return ret





