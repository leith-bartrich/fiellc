from fiepipelib.assetaspect.routines.structure import AbstractDirPath, StaticSubDir, \
    AbstractDesktopProjectRootBasePath
from fiepipelib.gitlabserver.routines.gitlabserver import GitLabServerRoutines
from fiepipelib.gitstorage.routines.gitroot import GitRootRoutines
from fiepipelib.gitstorage.routines.gitlab_server import GitLabFQDNGitRootRoutines
from fieui.FeedbackUI import AbstractFeedbackUI




class DesignDocsTypeDir(StaticSubDir):

    def get_typename(self) -> str:
        return self.get_dirname()

    def __init__(self, typename: str, parent_path: AbstractDirPath):
        super().__init__(typename, parent_path)


class DesignDocsDir(StaticSubDir):
    _environments: DesignDocsTypeDir = None
    _characters: DesignDocsTypeDir = None
    _props: DesignDocsTypeDir = None
    _vehicles: DesignDocsTypeDir = None

    def __init__(self, parent_path: AbstractDirPath):
        super().__init__("design_docs", parent_path)

        self._environments = DesignDocsTypeDir("environments", self)
        self.add_subpath(self._environments)

        self._characters = DesignDocsTypeDir("characters", self)
        self.add_subpath(self._characters)

        self._props = DesignDocsTypeDir("props", self)
        self.add_subpath(self._props)

        self._vehicles = DesignDocsTypeDir("vehicles", self)
        self.add_subpath(self._vehicles)


class StoryInteractivePath(StaticSubDir):

    def __init__(self, parent_path: AbstractDirPath):
        super().__init__("interactive", parent_path)


class StoryDir(StaticSubDir):
    _interactive: StoryInteractivePath = None

    def __init__(self, parent_path: AbstractDirPath):
        super().__init__("story", parent_path)

        self._interactive = StoryInteractivePath(self)
        self.add_subpath(self._interactive)


class DevelopmentPath(StaticSubDir):
    _design_docs: DesignDocsDir = None
    _story: StoryDir = None

    def __init__(self, parent_path: AbstractDirPath):
        super().__init__("development", parent_path)

        self._design_docs = DesignDocsDir(self)
        self.add_subpath(self._design_docs)

        self._story = StoryDir(self)
        self.add_subpath(self._story)


class DistributionPath(StaticSubDir):

    def __init__(self, parent_path: AbstractDirPath):
        super().__init__("distribution", parent_path)


class ProductionTypeDir(StaticSubDir):

    def get_typename(self) -> str:
        return self.get_dirname()

    def __init__(self, typename: str, parent_path: AbstractDirPath):
        super().__init__(typename, parent_path)


class ProductionUnrealProjectsPath(ProductionTypeDir):

    def __init__(self, parent_path: AbstractDirPath):
        super().__init__("unreal_projects", parent_path)


class ProductionPath(StaticSubDir):
    _environments: ProductionTypeDir = None
    _characters: ProductionTypeDir = None
    _props: ProductionTypeDir = None
    _vehicles: ProductionTypeDir = None

    _unreal_projects: ProductionUnrealProjectsPath = None

    def __init__(self, parent_path: AbstractDirPath):
        super().__init__("production", parent_path)

        self._environments = ProductionTypeDir("environments", self)
        self.add_subpath(self._environments)

        self._characters = ProductionTypeDir("characters", self)
        self.add_subpath(self._characters)

        self._props = ProductionTypeDir("props", self)
        self.add_subpath(self._props)

        self._vehicles = ProductionTypeDir("vehicles", self)
        self.add_subpath(self._vehicles)

        self._unreal_projects = ProductionUnrealProjectsPath(self)
        self.add_subpath(self._unreal_projects)


class MRProjectDesktopRootBasePath(AbstractDesktopProjectRootBasePath):
    _development: DevelopmentPath = None
    _distribution: DistributionPath = None
    _production: ProductionPath = None

    def __init__(self, routines: GitRootRoutines, gitlab_server_name: str):
        super().__init__(gitlab_server_name, routines)

        self._development = DevelopmentPath(self)
        self.add_subpath(self._development)

        self._distribution = DistributionPath(self)
        self.add_subpath(self._distribution)

        self._production = ProductionPath(self)
        self.add_subpath(self._production)

    def get_gitlab_root_routines(self) -> GitLabFQDNGitRootRoutines:
        gitlab_server_routines = GitLabServerRoutines(self.get_gitlab_server_name())
        root_routines = self.get_routines()
        return GitLabFQDNGitRootRoutines(gitlab_server_routines,root_routines.root,root_routines.root_config)


    async def auto_update_routine(self, feedback_ui:AbstractFeedbackUI):
        """Root auto update behavior is as follows:

        auto_update all submodules/children first.

        If we're dirty(not_submodule) we tell the user to keep working and either commit or revert.  done.

        If we're ahead, we push.

        If we're behind or detached, we pull.

        If we're ahead and behind, we pull and check for success or failure.

            Upon failure, (due to conflict) we inform the user they'll need to merge. done.

            Upon success, done.


        """

        #TODO: update all children first.

        is_ahead = self.remote_is_behind()
        is_behind = self.remote_is_ahead()
        is_detached = self.is_detached()

        root_routines = self.get_routines()
        gitlab_root_routines = self.get_gitlab_root_routines()
        repo = root_routines.get_local_repo()

        is_dirty = repo.is_dirty(index=True,working_tree=True,untracked_files=True,submodules=False)

        unmerged_blobs = repo.index.unmerged_blobs()

        #checking for conflicts
        conflicted = False
        for path in unmerged_blobs:
            list_of_blobs = unmerged_blobs[path]
            for (stage, blob) in list_of_blobs:
                # Now we can check each stage to see whether there were any conflicts
                if stage != 0:
                    conflicted = True
        if conflicted:
            await feedback_ui.warn(self.get_path() + " is conflicted.")
            await feedback_ui.output("You will need to resolve conflicts or cancel the merge.")
            return


        #dirty disables auto upating until it's no longer dirty.
        if is_dirty:
            await feedback_ui.warn(self.get_path() + " is dirty.")
            await feedback_ui.output("Once you are done making changes, you'll want to either commit them, or revert them; to resume auto updating.")
            if is_behind:
                await feedback_ui.warn(self.get_path() + " has upstream changes.")
                await feedback_ui.output("You may wish to merge in the changes, or you could wait.")
            return

        #ahead and not behind or detached, is a push.
        if is_ahead and not (is_behind or is_detached):
            await gitlab_root_routines.push(feedback_ui)
            return

        #any pull could leave us conflicted.  If we are left conflicted, it's handled the next time we auto-update.

        #behind or detached, is a pull.
        if not is_ahead and (is_behind or is_detached):
            await gitlab_root_routines.pull(feedback_ui)
            return

        #ahead and behind is a pull.
        if is_ahead and (is_behind or is_detached):
            await gitlab_root_routines.pull(feedback_ui)
            return

        #most likely, we're up to date and clean.  with the exception of submodules, which may be even more up to date.
        return







