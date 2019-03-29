import abc
import typing

from fiellclib.mr_project.data.root_config import MRProjectConfig
from fiepipelib.assetaspect.routines.autoconf import AutoConfigurationResult
from fiepipelib.assetstructure.routines.desktop import AbstractDesktopProjectAssetBasePath, \
    AbstractDesktopProjectRootBasePath
from fiepipelib.assetstructure.routines.structure import AbstractDirPath, StaticSubDir, \
    AbstractAssetBasePath, GenericAssetBasePathsSubDir, AbstractPath, TABP
from fiepipelib.automanager.data.localconfig import LegalEntityConfig
from fiepipelib.container.local_config.data.automanager import ContainerAutomanagerConfigurationComponent
from fiepipelib.enum import get_worse_enum
from fiepipelib.gitstorage.routines.gitroot import GitRootRoutines
from fiepiperpgmakermv.routines.aspectconfig import RPGMakerMVAspectConfigurationRoutines, RPGMakerMVAspectConfiguration
from fieui.FeedbackUI import AbstractFeedbackUI


class DesignDocsTypeDir(
    GenericAssetBasePathsSubDir['MRProjectDesktopRootBasePath', 'DesignDocsDir', 'LooseFilesAssetBasePath']):
    """Design Documents Typed Asset Directory
    root/development/design_docs/[typename]

    where typename is a high level asset or idea.  e.g. "character.john_doe" e.g. env.john_doe_home"
    """

    def get_typename(self) -> str:
        return self.get_dirname()

    def __init__(self, typename: str, parent_path: AbstractDirPath):
        super().__init__(typename, parent_path)

    def get_asset_basepath_by_dirname(self, dirname: str) -> 'LooseFilesAssetBasePath':
        base_path = self.get_base_static_path()
        gitlab_server_name = base_path.get_gitlab_server_name()
        return LooseFilesAssetBasePath(gitlab_server_name, self.get_asset_routines_by_dirname(dirname))


class DesignDocsDir(StaticSubDir['MRProjectDesktopRootBasePath', 'DevelopmentPath']):
    """
    Design documents directory
    root/development/design_docs
    """
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


class StoryInteractivePath(
    GenericAssetBasePathsSubDir['MRProjectDesktopRootBasePath', 'StoryDir', 'MRStoryInteractiveAssetBasePath']):
    """
    Story Interactive assets directory path
    root/development/story/interactive
    """

    def __init__(self, parent_path: AbstractDirPath):
        super().__init__("interactive", parent_path)

    def get_asset_basepath_by_dirname(self, dirname: str) -> 'MRStoryInteractiveAssetBasePath':
        base_path = self.get_base_static_path()
        assert isinstance(base_path, MRProjectDesktopRootBasePath)
        gitlab_server_name = base_path.get_gitlab_server_name()
        return StoryInteractiveAssetBasePath(gitlab_server_name,
                                             self.get_asset_routines_by_dirname(dirname))


class StoryDir(StaticSubDir['MRProjectDesktopRootBasePath', 'DevelopmentPath']):
    """
    Story subdir
    root/development/story
    """
    _interactive: StoryInteractivePath = None

    def __init__(self, parent_path: AbstractDirPath):
        super().__init__("story", parent_path)

        self._interactive = StoryInteractivePath(self)
        self.add_subpath(self._interactive)

    @property
    def interactive(self):
        return self._interactive


class DevelopmentPath(StaticSubDir['MRProjectDesktopRootBasePath', 'MRProjectDesktopRootBasePath']):
    """developmoent subdir
    root/development"""
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


class DistributionPath(StaticSubDir['MRProjectDesktopRootBasePath', 'MRProjectDesktopRootBasePath']):
    """Distribution dir
    root/distribution"""

    def __init__(self, parent_path: AbstractDirPath):
        super().__init__("distribution", parent_path)


class ProductionTypeDir(GenericAssetBasePathsSubDir['MRProjectDesktopRootBasePath', 'ProductionPath', TABP],
                        typing.Generic[TABP], abc.ABC):
    """A production type asset directory.
    root/production/[typename]

    where typename is a type of production asset. e.g. 'characters' or 'rigs' or 'houdini_rigs'

    Generics TABP

    TABP: the asset base type for assets in this directory: AbstractAssetBasePath"""

    def get_typename(self) -> str:
        return self.get_dirname()

    def __init__(self, typename: str, parent_path: AbstractDirPath):
        super().__init__(typename, parent_path)

class ProductionHoudiniProjectsPath(ProductionTypeDir['HoudiniAssetBasePath']):
    """
    Production Houdini Projects Directory
    root/production/[name]

    where name is an asset type.  e.g. houdini_characters or houdini_environments""
    """

    def get_asset_basepath_by_dirname(self, dirname: str) -> 'HoudiniAssetBasePath':
        base_path = self.get_base_static_path()
        gitlab_server_name = base_path.get_gitlab_server_name()
        return HoudiniAssetBasePath(gitlab_server_name, self.get_asset_routines_by_dirname(dirname))


class ProductionUnrealProjectsPath(ProductionTypeDir['UnrealAssetBasePath']):
    """
    Production Unreal Projects Directory
    root/production/unreal_projects
    """

    def __init__(self, parent_path: AbstractDirPath):
        super().__init__("unreal_projects", parent_path)

    def get_asset_basepath_by_dirname(self, dirname: str) -> 'UnrealAssetBasePath':
        base_path = self.get_base_static_path()
        gitlab_server_name = base_path.get_gitlab_server_name()
        return UnrealAssetBasePath(gitlab_server_name, self.get_asset_routines_by_dirname(dirname))


class ProductionPath(StaticSubDir['MRProjectDesktopRootBasePath', 'MRProjectDesktopRootBasePath']):
    """AR/VR/MR Production Directory
    root/production"""

    _houdini_environments: ProductionHoudiniProjectsPath = None
    _houdini_characters: ProductionHoudiniProjectsPath = None
    _houdini_props: ProductionHoudiniProjectsPath = None
    _houdini_vehicles: ProductionHoudiniProjectsPath = None

    _unreal_projects: ProductionUnrealProjectsPath = None

    def __init__(self, parent_path: AbstractDirPath):
        super().__init__("production", parent_path)

        self._houdini_environments = ProductionHoudiniProjectsPath("houdini_environments", self)
        self.add_subpath(self._houdini_environments)

        self._houdini_characters = ProductionHoudiniProjectsPath("houdini_characters", self)
        self.add_subpath(self._houdini_characters)

        self._houdini_props = ProductionHoudiniProjectsPath("houdini_props", self)
        self.add_subpath(self._houdini_props)

        self._houdini_vehicles = ProductionHoudiniProjectsPath("houdini_vehicles", self)
        self.add_subpath(self._houdini_vehicles)

        self._unreal_projects = ProductionUnrealProjectsPath(self)
        self.add_subpath(self._unreal_projects)

    @property
    def environments(self):
        return self._houdini_environments

    @property
    def characters(self):
        return self._houdini_characters

    @property
    def props(self):
        return self._houdini_props

    @property
    def vehicles(self):
        return self._houdini_vehicles

    @property
    def unreal_projects(self):
        return self._unreal_projects


class MRProjectDesktopRootBasePath(AbstractDesktopProjectRootBasePath):
    """Root base path for a MR/VR/AR project."""

    _development: DevelopmentPath = None
    _distribution: DistributionPath = None
    _production: ProductionPath = None

    _subpaths = None

    def __init__(self, routines: GitRootRoutines, gitlab_server_name: str):
        super().__init__(gitlab_server_name, routines)

        self._development = DevelopmentPath(self)
        self._distribution = DistributionPath(self)
        self._production = ProductionPath(self)

        self._subpaths = [self._development, self._distribution, self._production]

    def get_subpaths(self) -> typing.List[AbstractPath]:
        return self._subpaths.copy()

    def get_sub_basepaths(self) -> typing.List["AbstractDesktopProjectAssetBasePath"]:

        # for now, all asset providers are of type GenericAssetBasePathsSubDir

        ret = []

        all_subpaths = self.get_subpaths_recursive()
        for subpath in all_subpaths:
            if isinstance(subpath, GenericAssetBasePathsSubDir):
                ret.extend(subpath.get_asset_basepaths())
        return ret


class LooseFilesAssetBasePath(AbstractDesktopProjectAssetBasePath['LooseFilesAssetBasePath']):
    """
    A loose files asset for holding unstructured loose files.
    """
    pass


class UnrealAssetBasePath(AbstractDesktopProjectAssetBasePath['UnrealAssetBasePath']):
    """
    An unreal asset for holding an unreal project
    """
    pass


class HoudiniAssetBasePath(AbstractDesktopProjectAssetBasePath['HoudiniAssetBasePath']):
    """
    A houdini asset for holding a houdini project.
    """
    pass


class StoryInteractiveAssetBasePath(AbstractDesktopProjectAssetBasePath['MRStoryInteractiveAssetBasePath']):
    """
    An asset for an interactive story design.

    In practice this is either a RPGMaker or Unreal project.

    root/development/story/interactive/[name]

    Where name is an interactive story section/element/world/name e.g. "pirate_island" or "home_town_act_1"
    """

    def get_sub_basepaths(self) -> typing.List["AbstractAssetBasePath"]:
        return []

    def get_rpgmaker_aspect(self) -> RPGMakerMVAspectConfigurationRoutines:
        asset_routines = self.get_routines()
        asset_abs_path = asset_routines.abs_path
        rpgmaker_conf = RPGMakerMVAspectConfiguration(asset_abs_path)
        rpgmaker_aspect = RPGMakerMVAspectConfigurationRoutines(rpgmaker_conf, asset_routines)
        return rpgmaker_aspect

    async def auto_configure_routine(self, feedback_ui: AbstractFeedbackUI) -> AutoConfigurationResult:
        ret = AutoConfigurationResult.NO_CHANGES

        rpgmaker_aspect = self.get_rpgmaker_aspect()
        rpgmaker_resutls = await rpgmaker_aspect.auto_configure_routine(feedback_ui)

        ret = get_worse_enum(ret, rpgmaker_resutls)

        return ret


def automanage_structure(feedback_ui: AbstractFeedbackUI, root_id: str, container_id: str,
                         container_config: ContainerAutomanagerConfigurationComponent,
                         legal_entity_config: LegalEntityConfig, gitlab_server: str):
    root_routines = GitRootRoutines(container_id, root_id, feedback_ui)
    root_routines.load()
    mr_project_config = MRProjectConfig(root_routines.get_local_repo_path())
    if not mr_project_config.exists():
        return
    mr_project_config.load()
    mr_project_structure = MRProjectDesktopRootBasePath(root_routines, gitlab_server)
    print("MR PROJECT!")
    # TODO: Do management!
