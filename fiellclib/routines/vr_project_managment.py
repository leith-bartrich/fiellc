import os
import os.path
import shutil
import pathlib
import asyncio
import typing
import abc

from fiepipelib.gitstorage.routines.gitroot import GitRootRoutines
from fiepipelib.gitstorage.routines.gitasset import GitAssetRoutines
from fiepipelib.gitlabserver.data.gitlab_server import GitLabServer


class AbstractPath(abc.ABC):

    @abc.abstractmethod
    def get_path(self) -> str:
        raise NotImplementedError


class AbstractDirPath(AbstractPath, abc.ABC):

    @abc.abstractmethod
    def get_subpaths(self) -> typing.List[AbstractPath]:
        raise NotImplementedError


class AbstractSubPath(AbstractPath, abc.ABC):
    _parent_path: AbstractDirPath = None

    def get_parent_path(self) -> AbstractDirPath:
        return self._parent_path

    def __init__(self, parent_path: AbstractDirPath):
        self._parent_path = parent_path


class AbstractGitStorageBasePath(AbstractDirPath):
    _subpaths: typing.List[AbstractSubPath] = None

    def get_subpaths(self) -> typing.List[AbstractSubPath]:
        return self._subpaths.copy()

    def add_subpath(self, subpath: AbstractSubPath):
        subpath._parent_path = self
        self._subpaths.append(subpath)


class AbstractRootBasePath(AbstractGitStorageBasePath):
    _root_routines: GitRootRoutines = None

    def get_routines(self):
        return self._root_routines

    def __init__(self, routines: GitRootRoutines):
        self._root_routines = routines

    def get_path(self) -> str:
        return self._root_routines.get_local_repo_path()


class AbstractAssetBasePath(AbstractGitStorageBasePath):
    _asset_routines: GitAssetRoutines

    def get_routines(self):
        return self._asset_routines

    def __init__(self, routines: GitAssetRoutines):
        self._asset_routines = routines

    def get_path(self) -> str:
        return self._asset_routines.abs_path


class StaticSubDir(AbstractSubPath, AbstractDirPath):
    _dirname: str = None
    _subpaths: typing.List[AbstractSubPath] = None

    def get_dirname(self) -> str:
        return self._dirname

    def get_subpaths(self) -> typing.List[AbstractSubPath]:
        return self._subpaths.copy()

    def __init__(self, dirname: str, parent_path: AbstractDirPath):
        self._subpaths = []
        self._dirname = dirname
        super().__init__(parent_path)

    def add_subpath(self, subpath: AbstractSubPath):
        subpath._parent_path = self
        self._subpaths.append(subpath)

    def get_path(self) -> str:
        return os.path.join(self.get_parent_path().get_path(), self._dirname)


class AbstractSubAsset(AbstractSubPath):

    @abc.abstractmethod
    def get_asset_id(self) -> str:
        raise NotImplementedError

    @abc.abstractmethod
    def get_asset_name(self) -> str:
        raise NotImplementedError

    def get_path(self) -> str:
        return os.path.join(self.get_parent_path().get_path(), self.get_asset_name())


class StaticSubAsset(AbstractSubAsset):
    _asset_id: str = None
    _asset_name: str = None

    def get_asset_id(self):
        return self._asset_id

    def get_asset_name(self):
        return self._asset_name

    def __init__(self, parent_path: AbstractDirPath, asset_id: str, asset_name: str):
        self._asset_id = asset_id
        self._asset_name = asset_name
        super().__init__(parent_path)


class AbstractGitLabSubmodule(AbstractSubPath):

    @abc.abstractmethod
    def get_submod_dir_name(self) -> str:
        raise NotImplementedError()

    @abc.abstractmethod
    def get_submod_url(self) -> str:
        raise NotImplementedError()


class FIEPipeGitLabSubmodule(AbstractGitLabSubmodule):
    _server: GitLabServer = None

    def get_server(self):
        return self._server

    def set_server(self, server: GitLabServer):
        self._server = server

    def __init__(self, default_server: GitLabServer, parent_path: AbstractDirPath):
        super().__init__(parent_path)
        self._server = default_server

    def get_path(self) -> str:
        return os.path.join(self.get_parent_path().get_path(), self.get_submod_dir_name())


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


class ProductionUnrealProjectsPath(StaticSubDir):

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

        self._characters = ProductionTypeDir("characters"), self)
        self.add_subpath(self._characters)

        self._props = ProductionTypeDir("props", self)
        self.add_subpath(self._props)

        self._vehicles = ProductionTypeDir("vehicles", self)
        self.add_subpath(self._vehicles)

        self._unreal_projects = ProductionUnrealProjectsPath(self)
        self.add_subpath(self._unreal_projects


class HoudiniToolsPath(FIEPipeGitLabSubmodule):

    def get_submod_dir_name(self) -> str:
        return "houdini_tools"

    def get_submod_url(self) -> str:
        return self.get_server().get_ssh_url("leith", "houdini_tools.git")

    def __init__(self, default_server: GitLabServer, parent_path: AbstractDirPath):
        super().__init__(default_server, parent_path)


class MRProjectDesktopRootBasePath(AbstractRootBasePath):
    _development: DevelopmentPath = None
    _distribution: DistributionPath = None
    _production: ProductionPath = None
    _houdini_tools: HoudiniToolsPath = None

    def __init__(self, routines: GitRootRoutines, gitlab_server: GitLabServer):
        super().__init__(routines)

        self._development = DevelopmentPath(self)
        self.add_subpath(self._development)

        self._distribution = DistributionPath(self)
        self.add_subpath(self._distribution)

        self._production = ProductionPath(self)
        self.add_subpath(self._production)

        self._houdini_tools = HoudiniToolsPath(gitlab_server, self)
        self.add_subpath(self._houdini_tools)
