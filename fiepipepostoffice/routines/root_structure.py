import typing

from fiepipelib.assetaspect.routines.autoconf import AutoConfigurationResult
from fiepipelib.assetstructure.routines.structure import AbstractSubPath, AbstractAssetBasePath, \
    GenericAssetBasePathsSubDir, AbstractRootBasePath, AutoManageResults, StaticSubDir, AutoCreateResults
from fiepipelib.automanager.data.localconfig import LegalEntityConfig, LegalEntityMode
from fiepipelib.container.local_config.data.automanager import ContainerAutomanagerConfigurationComponent
from fiepipelib.gitstorage.routines.gitasset import GitAssetRoutines
from fiepipelib.gitstorage.routines.gitroot import GitRootRoutines
from fieui.FeedbackUI import AbstractFeedbackUI
from fiepipelib.rootaspect.routines.config import RootAspectConfigurationRoutines
from fiepipelib.assetaspect.routines.config import AssetAspectConfigurationRoutines
from fiepipepostoffice.data.aspect_config import PostOfficeConfiguration, DeliveryNamingMethod
from fiepipelib.enum import get_worse_enum
from fiepipepostoffice.data.box_aspect_config import BoxAspectConfig
from fiepipepostoffice.data.delivery_aspect_config import DeliveryAspectConfig

class PostOfficeApsectRoutines(RootAspectConfigurationRoutines[PostOfficeConfiguration]):

    def default_configuration(self):
        self.get_configuration().set_delivery_naming_method(DeliveryNamingMethod.UTC_DATE_HASH)

    async def reconfigure_interactive_routine(self):
        #TODO: implement choice of delivery naming method.
        return


class PostOfficeRootStructureRoutines(AbstractRootBasePath["PostOfficeRootStructureRoutines"]):
    _boxes:"Boxes" = None

    def get_boxes(self):
        return self._boxes

    def __init__(self, routines: GitRootRoutines):
        super().__init__(routines)
        self._boxes = Boxes("boxes", self)

    async def automanager_routine(self, feedback_ui: AbstractFeedbackUI, entity_config: LegalEntityConfig,
                                  container_config: ContainerAutomanagerConfigurationComponent) -> AutoManageResults:
        # We can assume we've (the root) just been updated by the automanager and that we're not conflicted.
        # But that is all.  This means we don't need to 'pull' from remote.

        # for a post office, this means we know which boxes exist out there.  But we don't neccesarily know what deliveries
        # exist because they are sub-assets of the boxes, which have not been updated themselves.

        # also, we may not have pushed up our latest boxes or their deliveries.

        # basic behavior is eventual consistency.  Therefore we want to push the boxes and their deliveries as fast
        # as possible to avoid conflicts in delivery naming.  Further, we want to pull them as early as possible to
        # avoid conflicts.

        # further, only highly privileged machines can actually publish changes to a post-office in a high security
        # environment.  And we expect security to be handled by github's permissions.

        # for delivery (content) internals, we don't automatically pull any new ones down.
        # Nor do we push them up.  We have explicit lock and archive commands for that kind of
        # behavior.  At some point, we may want to set a local configuration variable for auto-archive-locked.

        # behavior is:

        # we need to create, add and commit missing structure for ourselves (autocreate).
        # we need to report (and fail) dirt that's not handled by structure, and isn't just a submodule version update.
        # we should push those commits.

        # we need to then walk through the boxes and do the same.  That's:
        # pull, check for conflicts, auto-create, check for dirt, and then push.

        # and that's it.

        # return results. best possible status.  we degrade as we move along.

        ret = AutoManageResults.CLEAN

        if entity_config.get_mode() == LegalEntityMode.NONE:
            # for lack of a better respose, we don't know.
            return AutoManageResults.PENDING

        if entity_config.get_mode() == LegalEntityMode.USER_WORKSTATION:

            # first, create static structure.
            create_status = AutoCreateResults.NO_CHANGES

            for subpath in self.get_subpaths():
                if not subpath.exists():
                    # this is recursive....
                    subpath_ret = await subpath.automanager_create(feedback_ui, entity_config, container_config)
                    create_status = get_worse_enum(create_status, subpath_ret)
                    # catch a failure.

            if create_status == AutoCreateResults.CANNOT_COMPLETE:
                await feedback_ui.output(
                    "Canceling further auto-management of this post-office due to a subpath failing to create.")
                return AutoManageResults.CANNOT_COMPLETE

            # we need to check for working-copy dirt that's not in the index and fail based on it.
            is_dirty = self.is_dirty(False, True, True, False)
            if is_dirty:
                await feedback_ui.output("Root worktree is dirty.  Cannot auto-commit.  Canceling further auto-management.")
                await feedback_ui.output(self.get_path())
                return AutoManageResults.CANNOT_COMPLETE

            # Commit the index if it needs it.
            # this will be pushed next time through.
            index_dirty = self.is_dirty(True, False, False, False)
            if index_dirty:
                commit_output = self.get_routines().get_repo().git.commit(m="Auto-manager commit of post-office changed structure.")
                await feedback_ui.output(commit_output)

            # we move into our child box logic.

            boxes = self._boxes.get_asset_basepaths()
            for box in boxes:

                asset_routines = box.get_asset_routines()
                asset_routines.load()

                # check for conflicts
                if asset_routines.is_in_conflict():
                    await feedback_ui.error("Post-office Box is in conflict: " + asset_routines.abs_path)
                    await feedback_ui.error("Canceling further auto-management of this Box.")
                    ret = get_worse_enum(ret, AutoManageResults.CANNOT_COMPLETE)
                    #other boxes might get further...
                    continue

                asset_server_routines = box.get_gitlab_asset_routines()

                remote_exists = await asset_server_routines.remote_exists(feedback_ui)

                if not remote_exists:
                    success = await asset_server_routines.push_sub_routine(feedback_ui,"master",False)
                    #since we can't check ahead and behind on a non-existant, we return pending,
                    #hoping for the remote to come back and take teh push.
                    if not success:
                        await feedback_ui.warn("Push of new Post-Office Box failed: " + asset_routines.abs_path)
                        await feedback_ui.warn("Canceling further auto-management of this Box...")
                        ret = get_worse_enum(ret, AutoManageResults.PENDING)
                        #other boxes might get further...
                        continue

                #early push and pull for eventual consistency.

                is_behind_remote = await asset_server_routines.is_behind_remote(feedback_ui)
                is_ahead_of_remote = await asset_server_routines.is_aheadof_remote(feedback_ui)

                if is_behind_remote and not is_ahead_of_remote:
                    #we're behind and not ahead
                    #we pull but failure doesn't matter.
                    success = await asset_server_routines.pull_sub_routine(feedback_ui,"master")

                if is_ahead_of_remote and not is_behind_remote:
                    #we're ahead and not behidn.  we push and failure doesn't matter.
                    success = await asset_server_routines.push_sub_routine(feedback_ui,"master",False)

                if is_ahead_of_remote and is_behind_remote:
                    #we're both ahead and behind.  We pull, check for conflicts, then push.
                    #failure doesn't matter.
                    success = await asset_server_routines.pull_sub_routine(feedback_ui,"master")
                    if asset_routines.is_in_conflict():
                        await feedback_ui.error("Conflict detected while updating Post-Office Box: " + asset_routines.abs_path)
                        ret = get_worse_enum(ret, AutoManageResults.CANNOT_COMPLETE)
                        #other boxes might get further...
                        continue
                    success = await asset_server_routines.push_sub_routine(feedback_ui,"master",False)

                #now we auto_create and push (early) if needed.

                auto_create_results = await box.automanager_create(feedback_ui,entity_config,container_config)
                if auto_create_results == AutoCreateResults.CANNOT_COMPLETE:
                    await feedback_ui.error("Post-office Box couldn't auto-create: " + asset_routines.abs_path)
                    ret = get_worse_enum(ret, AutoManageResults.CANNOT_COMPLETE)
                    #other boxes might get further
                    continue
                else:
                    if asset_routines.get_repo().is_dirty(False,True,True,False):
                        #dirty and cannot auto-commit
                        await feedback_ui.error("Post-office Box is dirty and cannot auto-commit changes: " + asset_routines.abs_path)
                        ret = get_worse_enum(ret, AutoManageResults.CANNOT_COMPLETE)
                        #other boxes might get further...
                        continue
                    if asset_routines.get_repo().is_dirty(True,False,False,False):
                        #dirty index can be auto-commit
                        commit_output = asset_routines.get_repo().git.commit(m="Auto-commit of Post-Office Box Structure.")
                        await feedback_ui.output(commit_output)
                        push_success = await asset_server_routines.push_sub_routine(feedback_ui,"master",False)
                        if push_success:
                            ret = get_worse_enum(ret, AutoManageResults.CLEAN)
                        else:
                            ret = get_worse_enum(ret, AutoManageResults.UNPUBLISHED_COMMITS)
                    else:
                        ret = get_worse_enum(ret, AutoManageResults.CLEAN)

            if ret == AutoManageResults.CANNOT_COMPLETE or ret == AutoManageResults.PENDING:
                await feedback_ui.error(
                    "At least one child's auto-create and publish routine failed or is pending.  Canceling further auto-management.")
                return ret

            return ret


    def get_sub_basepaths(self) -> typing.List["AbstractAssetBasePath"]:
        return self._boxes.get_asset_basepaths()

    def get_subpaths(self) -> "typing.List[AbstractSubPath[PostOfficeRootStructureRoutines]]":
        return [self._boxes]

    def get_aspect_routines(self) -> PostOfficeApsectRoutines:
        config = PostOfficeConfiguration(self.get_path())
        return PostOfficeApsectRoutines(config)

    async def automanager_create_self(self, feedback_ui: AbstractFeedbackUI, entity_config: LegalEntityConfig,
                                      container_config: ContainerAutomanagerConfigurationComponent) -> 'AutoCreateResults':
        aspect_routines = self.get_aspect_routines()
        if not aspect_routines.is_configured():
            aspect_routines.default_configuration()
            aspect_routines.commit()
        return await super().automanager_create_self(feedback_ui, entity_config, container_config)


class Boxes(GenericAssetBasePathsSubDir["PostOfficeRootStructureRoutines", "PostOfficeRootStructureRoutines", "Box"]):

    def get_asset_basepath_by_dirname(self, dirname: str) -> "Box":
        asset_routines = self.get_asset_routines_by_dirname(dirname)
        asset_routines.load()
        po_root_struct = self.get_base_static_path()
        return Box(asset_routines,po_root_struct)


class BoxAspectRoutines(AssetAspectConfigurationRoutines[BoxAspectConfig]):

    async def auto_reconfigure_routine(self, feedback_ui: AbstractFeedbackUI) -> AutoConfigurationResult:
        pass

    def default_configuration(self):
        pass

    async def reconfigure_interactive_routine(self):
        pass


class Box(AbstractAssetBasePath["Box"]):

    _incoming: "Section" = None

    def get_incoming(self) -> "Section":
        return self._incoming

    _outgoing: "Section" = None

    def get_outgoing(self) -> "Section":
        return self._outgoing

    _post_office_root_structure: PostOfficeRootStructureRoutines = None

    def get_post_office_root_structure(self) -> PostOfficeRootStructureRoutines:
        return self._post_office_root_structure


    def __init__(self, routines: GitAssetRoutines, po_root_structure:PostOfficeRootStructureRoutines):
        self._post_office_root_structure = po_root_structure
        super().__init__(routines)
        self._incoming = Section("incoming", self)
        self._outgoing = Section("outgoing", self)

    def get_sub_basepaths(self) -> typing.List["AbstractAssetBasePath"]:
        return []

    def get_subpaths(self) -> "typing.List[AbstractSubPath[Box]]":
        return [self._incoming, self._outgoing]

    async def automanager_create_self(self, feedback_ui: AbstractFeedbackUI, entity_config: LegalEntityConfig,
                                      container_config: ContainerAutomanagerConfigurationComponent) -> 'AutoCreateResults':
        asset_routines = self.get_asset_routines()
        box_config = BoxAspectConfig(asset_routines.abs_path)
        aspect_routines = BoxAspectRoutines(box_config,asset_routines)
        if not aspect_routines.is_configured():
            aspect_routines.default_configuration()
            aspect_routines.commit()
        return await super().automanager_create_self(feedback_ui, entity_config, container_config)


class Section(GenericAssetBasePathsSubDir[Box, Box, "Delivery"]):

    def get_asset_basepath_by_dirname(self, dirname: str) -> "Delivery":
        asset_routines = self.get_asset_routines_by_dirname(dirname)
        asset_routines.load()
        return Delivery(asset_routines,self.get_parent_path())

    async def create_new_delivery_routine(self, feedback_ui:AbstractFeedbackUI):
        post_office = self.get_parent_path().get_post_office_root_structure()
        aspect_routines = post_office.get_aspect_routines()
        aspect_routines.load()
        dirname = aspect_routines.get_configuration().get_new_delivery_name(self.get_path())
        await feedback_ui.output("Creating new delivery: " + dirname)
        self.create_new_empty_asset(dirname)
        await feedback_ui.output("Auto-creating delivery: " + dirname)
        await self.autocreate_asset_by_dirname(dirname,feedback_ui)
        await feedback_ui.output("Done creating new delivery.")


class DeliveryAspectRoutines(AssetAspectConfigurationRoutines[DeliveryAspectConfig]):

    async def auto_reconfigure_routine(self, feedback_ui: AbstractFeedbackUI) -> AutoConfigurationResult:
        self.update_git_meta()
        return AutoConfigurationResult.UNCLEAR

    def default_configuration(self):
        config = self.get_configuration()
        config.set_locked(False)

    async def reconfigure_interactive_routine(self):
        pass

    async def lock_routine(self):
        """Lock the delivery.  Changes to the delivery will not be allowed going forward."""
        self.load()
        config = self.get_configuration()
        config.set_locked(True)
        self.commit()

    async def unlock_routine(self):
        """Unlock the delivery.  Changes to the delivery will be allowed again."""
        self.load()
        config = self.get_configuration()
        config.set_locked(False)
        self.commit()


class Delivery(AbstractAssetBasePath["Delivery"]):
    _CONTENT_DIR_NAME = "content"

    _content: "Content" = None

    def get_content(self) -> "Content":
        return self._content

    _box_routines: "Box" = None

    def get_box_routines(self) -> "Box":
        return self._box_routines


    def __init__(self, routines: GitAssetRoutines, box:"Box"):
        self._box_routines = box
        super().__init__(routines)
        self._content = Content(self._CONTENT_DIR_NAME, self)

    def get_sub_basepaths(self) -> typing.List["AbstractAssetBasePath"]:
        return []

    def get_subpaths(self) -> "typing.List[AbstractSubPath[Delivery]]":
        return [self._content]

    def get_aspect_routines(self) -> DeliveryAspectRoutines:
        asset_routines = self.get_asset_routines()
        asset_routines.load()
        asset_path = asset_routines.abs_path
        config = DeliveryAspectConfig(asset_path)
        return DeliveryAspectRoutines(config, asset_routines)

    async def commit_and_lock_routine(self, feedback_ui: AbstractFeedbackUI) -> bool:
        aspect_routines = self.get_aspect_routines()
        aspect_routines.load()
        asset_routines = aspect_routines.get_asset_routines()
        working_asset = asset_routines.working_asset

        locked = aspect_routines.get_configuration().get_locked()

        if locked:
            await feedback_ui.error("Delivery is locked.  It should not be modified.")
            return False

        repo = working_asset.GetRepo()
        add_output = repo.git.add("content")
        await feedback_ui.output(add_output)
        aspect_routines.get_configuration().set_locked(True)
        aspect_routines.commit()
        commit_output = repo.git.commit(m="Adding and locking delivery content.")
        await feedback_ui.output(commit_output)

    async def unlock_routine(self, feedback_ui: AbstractFeedbackUI):
        aspect_routines = self.get_aspect_routines()
        aspect_routines.load()
        asset_routines = aspect_routines.get_asset_routines()
        working_asset = asset_routines.working_asset

        aspect_routines.get_configuration().set_locked(False)
        aspect_routines.commit()

    async def archive_and_remove(self, feedback_ui: AbstractFeedbackUI) -> (bool, str):
        aspect_routines = self.get_aspect_routines()
        aspect_routines.load()
        asset_routines = aspect_routines.get_asset_routines()
        working_asset = asset_routines.working_asset

        locked = aspect_routines.get_configuration().get_locked()

        if not locked:
            return False, "Delivery isn't locked.  Cannot archive and remove it: " + asset_routines.abs_path

        repo = working_asset.GetRepo()

        # fail on dirty
        if repo.is_dirty(index=True, working_tree=True, untracked_files=True, submodules=True):
            return False, "Delivery is dirty.  Cannot archive and remove it: " + asset_routines.abs_path

        # fail on conflict
        if asset_routines.is_in_conflict():
            return False, "Delivery is in conflict.  Cannot archive and remove it: " + asset_routines.abs_path

        # fail on detached head
        if self.is_detached():
            return False, "Detached head.  Cannot archive and remove it: " + asset_routines.abs_path

        # check if remote exists
        remote_exists = self.remote_exists()
        gitlab_asset_routines = self.get_gitlab_asset_routines()
        if not remote_exists:
            # push a new one if it doesn't exist
            push_success = await gitlab_asset_routines.push_sub_routine(feedback_ui, "master", True)
            if not push_success:
                return False, "Failed to push to remote: " + asset_routines.abs_path + " -> " + gitlab_asset_routines.get_remote_url()
        else:
            # check if we need to push

            is_ahead_of_remote = await gitlab_asset_routines.is_aheadof_remote(feedback_ui)
            is_behind_remote = await gitlab_asset_routines.is_behind_remote(feedback_ui)

            # fail if we're behind
            if is_behind_remote:
                return False, "Delivery isn't up to date.  Cannot archive and remove it: " + asset_routines.abs_path

            # push if need to
            if is_ahead_of_remote:
                push_success = await gitlab_asset_routines.push_sub_routine(feedback_ui, "master", True)
                if not push_success:
                    return False, "Failed to push to remote: " + + asset_routines.abs_path + " -> " + gitlab_asset_routines.get_remote_url()

            # it's possible the commit exists on remote, but the lfs objects do not. (prior run of standard push fails
            # after commit but before lfs push is complete)
            # we can't check this.  But we can do a git lfs push which is pretty well optimized.

            await gitlab_asset_routines.push_lfs_objects_subroutine(feedback_ui,"master")

        # if we get here, the remote exists and is up to date.  It is not ahead.  And it's not detached.  And it is not
        # missing local LFS objects.
        # so, we can delete.
        await asset_routines.delete_lfs_object_cache(feedback_ui)
        await asset_routines.deinit(feedback_ui, force=True)
        return True, "Archived and deleted."

    async def automanager_create_self(self, feedback_ui: AbstractFeedbackUI, entity_config: LegalEntityConfig,
                                      container_config: ContainerAutomanagerConfigurationComponent) -> 'AutoCreateResults':
        asset_routines = self.get_asset_routines()
        delivery_config = DeliveryAspectConfig(asset_routines.abs_path)
        delivery_aspect_routines = DeliveryAspectRoutines(delivery_config,asset_routines)
        if not delivery_aspect_routines.is_configured():
            delivery_aspect_routines.default_configuration()
            delivery_aspect_routines.commit()
        return await super().automanager_create_self(feedback_ui, entity_config, container_config)


class Content(StaticSubDir[Delivery, Delivery]):
    pass

async def automanage_structure(feedback_ui: AbstractFeedbackUI, root_id: str, container_id: str,
                               container_config: ContainerAutomanagerConfigurationComponent,
                               legal_entity_config: LegalEntityConfig, gitlab_server: str):
    root_routines = GitRootRoutines(container_id, root_id)
    root_routines.load()
    post_office_config = PostOfficeConfiguration(root_routines.get_local_repo_path())
    if not post_office_config.exists():
        return
    post_office_config.load()
    post_office_structure = PostOfficeRootStructureRoutines(root_routines)
    await feedback_ui.output("Starting Post Office structure automanagement...")
    results = await post_office_structure.automanager_routine(feedback_ui, legal_entity_config, container_config)
    await feedback_ui.output("Post Office structure automanagement results: " + results.name)
