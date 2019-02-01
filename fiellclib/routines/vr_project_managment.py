import typing

from fiepipelib.assetaspect.routines.config import AutoConfigurationResult
from fiepipelib.assetaspect.routines.structure import AbstractDirPath, StaticSubDir, \
    AbstractDesktopProjectRootBasePath, AssetsStaticSubDir, AbstractAssetBasePath, AutoUpdateResults, \
    AbstractDesktopProjectAssetBasePath, GenericAssetBasePathsSubDir, AutoCreateResults, AutoConfigureResults
from fiepipelib.gitlabserver.routines.gitlabserver import GitLabServerRoutines
from fiepipelib.gitstorage.routines.gitroot import GitRootRoutines
from fiepipelib.gitstorage.routines.gitlab_server import GitLabFQDNGitRootRoutines
from fieui.FeedbackUI import AbstractFeedbackUI
from fiepiperpgmakermv.routines.aspectconfig import RPGMakerMVAspectConfigurationRoutines, RPGMakerMVAspectConfiguration
from fiepipelib.enum import WorseEnum
from fiepipelib.enum import get_worse_enum

class MRDesignDocsAssetBasePath(AbstractDesktopProjectAssetBasePath):

    def get_sub_basepaths(self, feedback_ui:AbstractFeedbackUI) -> typing.List["AbstractAssetBasePath"]:
        return []

class MRProductionAssetBasePath(AbstractDesktopProjectAssetBasePath):

    def get_sub_basepaths(self, feedback_ui:AbstractFeedbackUI) -> typing.List["AbstractAssetBasePath"]:
        return []

class MRStoryInteractiveAssetBasePath(AbstractDesktopProjectAssetBasePath):

    def get_sub_basepaths(self, feedback_ui:AbstractFeedbackUI) -> typing.List["AbstractAssetBasePath"]:
        return []

    async def auto_configure_routine(self, feedback_ui: AbstractFeedbackUI) -> AutoConfigurationResult:
        ret = AutoConfigurationResult.NO_CHANGES

        asset_routines = self.get_routines()
        asset_abs_path = asset_routines.abs_path
        rpgmaker_conf = RPGMakerMVAspectConfiguration(asset_abs_path)
        rpgmaker_aspect = RPGMakerMVAspectConfigurationRoutines(rpgmaker_conf,asset_routines)
        rpgmaker_resutls = await rpgmaker_aspect.auto_configure_routine(feedback_ui)

        ret = get_worse_enum(ret, rpgmaker_resutls)

        return ret



class DesignDocsTypeDir(GenericAssetBasePathsSubDir[MRDesignDocsAssetBasePath]):

    def get_typename(self) -> str:
        return self.get_dirname()

    def __init__(self, typename: str, parent_path: AbstractDirPath):
        super().__init__(typename, parent_path)

    def get_asset_basepath_by_dirname(self, dirname:str, feedback_ui:AbstractFeedbackUI) -> MRDesignDocsAssetBasePath:
        base_path = self.get_base_static_path()
        assert isinstance(base_path, MRProjectDesktopRootBasePath)
        gitlab_server_name = base_path.get_gitlab_server_name()
        return MRDesignDocsAssetBasePath(gitlab_server_name, self.get_asset_routines_by_dirname(feedback_ui,dirname))


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

    @property
    def environments(self):
        return self._environments

    @property
    def characters(self):
        return self._characters

    @property
    def props(self):
        return self._props

    @property
    def vehicles(self):
        return self._vehicles


class StoryInteractivePath(GenericAssetBasePathsSubDir[MRStoryInteractiveAssetBasePath]):

    def __init__(self, parent_path: AbstractDirPath):
        super().__init__("interactive", parent_path)

    def get_asset_basepath_by_dirname(self, dirname:str, feedback_ui:AbstractFeedbackUI) -> MRStoryInteractiveAssetBasePath:
        base_path = self.get_base_static_path()
        assert isinstance(base_path, MRProjectDesktopRootBasePath)
        gitlab_server_name = base_path.get_gitlab_server_name()
        return MRStoryInteractiveAssetBasePath(gitlab_server_name, self.get_asset_routines_by_dirname(feedback_ui,dirname))


class StoryDir(StaticSubDir):
    _interactive: StoryInteractivePath = None

    def __init__(self, parent_path: AbstractDirPath):
        super().__init__("story", parent_path)

        self._interactive = StoryInteractivePath(self)
        self.add_subpath(self._interactive)

    @property
    def interactive(self):
        return self._interactive


class DevelopmentPath(StaticSubDir):
    _design_docs: DesignDocsDir = None
    _story: StoryDir = None

    def __init__(self, parent_path: AbstractDirPath):
        super().__init__("development", parent_path)

        self._design_docs = DesignDocsDir(self)
        self.add_subpath(self._design_docs)

        self._story = StoryDir(self)
        self.add_subpath(self._story)

    @property
    def story(self):
        return self._story

    @property
    def design_docs(self):
        return self._design_docs


class DistributionPath(StaticSubDir):

    def __init__(self, parent_path: AbstractDirPath):
        super().__init__("distribution", parent_path)


class ProductionTypeDir(GenericAssetBasePathsSubDir[MRProductionAssetBasePath]):

    def get_typename(self) -> str:
        return self.get_dirname()

    def __init__(self, typename: str, parent_path: AbstractDirPath):
        super().__init__(typename, parent_path)

    def get_asset_basepath_by_dirname(self, dirname:str, feedback_ui:AbstractFeedbackUI) -> MRProductionAssetBasePath:
        base_path = self.get_base_static_path()
        assert isinstance(base_path, MRProjectDesktopRootBasePath)
        gitlab_server_name = base_path.get_gitlab_server_name()
        return MRProductionAssetBasePath(gitlab_server_name, self.get_asset_routines_by_dirname(feedback_ui,dirname))


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

    @property
    def environments(self):
        return self._environments

    @property
    def characters(self):
        return self._characters

    @property
    def props(self):
        return self._props

    @property
    def vehicles(self):
        return self._vehicles

    @property
    def unreal_projects(self):
        return self._unreal_projects




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

    def get_sub_basepaths(self, feedback_ui:AbstractFeedbackUI) -> typing.List["AbstractAssetBasePath"]:
        ret = []

        ret.extend(self._development.story.interactive.get_asset_basepaths(feedback_ui))
        ret.extend(self._development.design_docs.environments.get_asset_basepaths(feedback_ui))
        ret.extend( self._development.design_docs.characters.get_asset_basepaths(feedback_ui))
        ret.extend(self._development.design_docs.props.get_asset_basepaths(feedback_ui))
        ret.extend(self._development.design_docs.vehicles.get_asset_basepaths(feedback_ui))
        ret.extend(self._production.environments.get_asset_basepaths(feedback_ui))
        ret.extend(self._production.characters.get_asset_basepaths(feedback_ui))
        ret.extend( self._production.props.get_asset_basepaths(feedback_ui))
        ret.extend( self._production.vehicles.get_asset_basepaths(feedback_ui))
        ret.extend( self._production.unreal_projects.get_asset_basepaths(feedback_ui))

        return ret

    async def auto_configure_routine(self, feedback_ui: AbstractFeedbackUI) -> AutoConfigurationResult:
        return AutoConfigurationResult.NO_CHANGES










