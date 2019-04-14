import typing

from fiepipelib.assetstructure.routines.structure import AbstractAssetBasePath, BT, StaticSubDir, AbstractSubPath, \
    AutoCreateResults
from fiepipelib.automanager.data.localconfig import LegalEntityConfig
from fiepipelib.container.local_config.data.automanager import ContainerAutomanagerConfigurationComponent
from fiepipelib.gitstorage.routines.gitasset import GitAssetRoutines
from fieui.FeedbackUI import AbstractFeedbackUI
from fiepipelib.enum import get_worse_enum

from fiepipeloosefiles.routines.assetaspect import LooseFilesAspectConfigurationRoutines
from fiepipeloosefiles.data.assetaspect import LooseFilesAspectConfiguration
from fieui.FeedbackUI import AbstractFeedbackUI

class AbstractDelivery(AbstractAssetBasePath[BT]):
    _content: "Content" = None
    _CONTENT_DIR_NAME = "content"

    def get_content(self):
        return self._content

    def __init__(self, routines: GitAssetRoutines):
        super().__init__(routines)
        self._content = Content(self._CONTENT_DIR_NAME, self)

    def get_sub_basepaths(self) -> typing.List["AbstractAssetBasePath"]:
        return []

    def get_subpaths(self) -> "typing.List[AbstractSubPath[BT]]":
        return [self._content]

    def get_loose_files_aspect(self) -> LooseFilesAspectConfigurationRoutines:
        asset_routines = self.get_routines()
        asset_routines.load()
        asset_path = asset_routines.abs_path
        config = LooseFilesAspectConfiguration(asset_path)
        return LooseFilesAspectConfigurationRoutines(config,asset_routines)

    async def automanager_create_self(self, feedback_ui: AbstractFeedbackUI, entity_config: LegalEntityConfig,
                                      container_config: ContainerAutomanagerConfigurationComponent) -> 'AutoCreateResults':
        ret = await super().automanager_create_self(feedback_ui, entity_config, container_config)

        #first we handle the loose files aspect

        loose_files_aspect = self.get_loose_files_aspect()

        #configure if not configured
        if not loose_files_aspect.is_configured():
            await loose_files_aspect.auto_configure_routine(feedback_ui)
            ret = get_worse_enum(ret, AutoCreateResults.CHANGES_MADE)

        #add a lfs track for the concent directory.
        loose_files_aspect.load()
        loose_files_config = loose_files_aspect.get_configuration()
        lfs_patterns = loose_files_config.get_lfs_patterns()

        content_pattern = self._CONTENT_DIR_NAME + "//**"

        if content_pattern not in lfs_patterns:
            lfs_patterns.append(content_pattern)
            loose_files_aspect.commit()
            ret = get_worse_enum(ret, AutoCreateResults.CHANGES_MADE)

        #done
        return ret

    async def commit_all_content(self, feedback_ui:AbstractFeedbackUI, message:str):
        asset_routines = self.get_routines()
        working_asset = asset_routines.working_asset
        repo = working_asset.GetRepo()
        add_output = repo.git.add(".")
        await feedback_ui.output(add_output)
        commit_output = repo.git.commit(m=message)
        await feedback_ui.output(commit_output)

    async def archive_and_remove(self,feedback_ui:AbstractFeedbackUI) -> (bool, str):
        asset_routines = self.get_routines()
        working_asset = asset_routines.working_asset
        repo = working_asset.GetRepo()

        #fail on dirty
        if repo.is_dirty(index=True,working_tree=True,untracked_files=True,submodules=True):
            return False, "Delivery is dirty.  Cannot archive and remove it: " + asset_routines.abs_path
        #fail on conflict
        if asset_routines.is_in_conflict():
            return False, "Delivery is in conflict.  Cannot archive and remove it: " + asset_routines.abs_path
        #fail on detached head
        if self.is_detached():
            return False, "Detached head.  Cannot archive and remove it: " + asset_routines.abs_path

        #check if remote exists
        remote_exists = self.remote_exists()
        gitlab_asset_routines = self.get_gitlab_asset_routines()
        if not remote_exists:
            #push a new one if it doesn't exist
            push_success = gitlab_asset_routines.push_sub_routine(feedback_ui,"master",True)
            if not push_success:
                return False, "Failed to push to remote: " + asset_routines.abs_path + " -> " + gitlab_asset_routines.get_remote_url()
        else:
            #check if we need to push

            is_ahead_of_remote = await gitlab_asset_routines.is_aheadof_remote(feedback_ui)
            is_behind_remote = await gitlab_asset_routines.is_behind_remote(feedback_ui)

            #fail if we're behind
            if is_behind_remote:
                return False, "Delivery isn't up to date.  Cannot archive and remove it: " + asset_routines.abs_path

            #push if need to
            if is_behind_remote:
                push_success = gitlab_asset_routines.push_sub_routine(feedback_ui,"master",True)
                if not push_success:
                    return False, "Failed to push to remote: " +  + asset_routines.abs_path + " -> " + gitlab_asset_routines.get_remote_url()

        #if we get here, the remote exists and is up to date.  It is not ahead.  And it's not detached.
        #so, we can delete.
        asset_routines.deinit()
        return True, "Archived and deleted."







class Content(StaticSubDir[AbstractDelivery, AbstractDelivery]):
    pass
