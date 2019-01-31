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







