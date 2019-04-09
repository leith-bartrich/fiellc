import typing

from fiellclib.mr_project.data.root_config import MRProjectConfig
from fiellclib.mr_project.routines.root_config import MRProjectConfigRoutines
from fiellclib.mr_project.routines.root_structure import ProductionPath, MRProjectDesktopRootBasePath
from fiellclib.mr_project.routines.houdini_asset_structure import HoudiniAssetBasePath
from fiellclib.mr_project.shell.houdini_asset_structure import HoudiniAssetConfigShell
from fiellclib.mr_project.shell.houdini_asset_structure import HoudiniAssetConfigShell
from fiepipedesktoplib.assetstructure.shell.structure import StaticSubdirCommand, \
    GenericTypedAssetsSubdirCommandCommand, StructureRootConfigCommand
from fiepipedesktoplib.gitstorage.shells.gitroot import Shell as GitRootShell
from fiepipehoudini.routines.structure import HoudiniDesktopAssetBasePath
from fieuishell.ModalInputDefaultUI import InputDefaultModalShellUI


class MRProjectConfigShell(StructureRootConfigCommand[MRProjectConfig, MRProjectDesktopRootBasePath]):


    def __init__(self, root_shell: GitRootShell):
        super().__init__(root_shell)
        self.add_submenu(ProductionCommand(self),"production",[])

    def get_structure_routines(self) -> MRProjectDesktopRootBasePath:
        root_shell = self.get_root_shell()
        root_routines = root_shell.get_routines()
        root_routines.load()
        return MRProjectDesktopRootBasePath(root_routines)

    def get_configuration_routines(self) -> MRProjectConfigRoutines:
        return MRProjectConfigRoutines(self.get_configuration_data(), GitLibServerInputUI(self))

    def get_plugin_names_v1(self) -> typing.List[str]:
        ret = super(MRProjectConfigShell, self).get_plugin_names_v1()
        ret.append("fiellc.mr_project.configuration.command")
        return ret

    def get_configuration_data(self) -> MRProjectConfig:
        root_routines = self.get_root_shell().get_routines()
        root_routines.load()
        repo_path = root_routines.get_local_repo_path()
        return MRProjectConfig(repo_path)


class ProductionCommand(
    StaticSubdirCommand[MRProjectDesktopRootBasePath, MRProjectDesktopRootBasePath, MRProjectConfigShell]):
    _mr_shell: MRProjectConfigShell = None

    def get_structure_routines(self) -> ProductionPath:
        return self._mr_shell.get_structure_routines().get_production()

    def get_parent_shell(self) -> MRProjectConfigShell:
        return self._mr_shell

    def __init__(self, mr_shell: MRProjectConfigShell):
        self._mr_shell = mr_shell
        super().__init__()
        self.add_submenu(HoudiniProductionCommand(self, ProductionPath.HOUDINI_CHARS_DIR_NAME),
                         ProductionPath.HOUDINI_CHARS_DIR_NAME, [])
        self.add_submenu(HoudiniProductionCommand(self, ProductionPath.HOUDINI_ENVS_DIR_NAME),
                         ProductionPath.HOUDINI_ENVS_DIR_NAME, [])
        self.add_submenu(HoudiniProductionCommand(self, ProductionPath.HOUDINI_VEHS_DIR_NAME),
                         ProductionPath.HOUDINI_VEHS_DIR_NAME, [])
        self.add_submenu(HoudiniProductionCommand(self, ProductionPath.HOUDINI_PROPS_DIR_NAME),
                         ProductionPath.HOUDINI_PROPS_DIR_NAME, [])
        # self.add_submenu(UnrealProductionCommand(self, ProductionPath.UNREAL_PROJS_DIR_NAME), ProductionPath.UNREAL_PROJS_DIR_NAME,[])

    def get_plugin_names_v1(self) -> typing.List[str]:
        ret = super(ProductionCommand, self).get_plugin_names_v1()
        ret.append("mr_project.production.command")
        return ret


# class UnrealProductionCommand(GenericTypedAssetsSubdirCommandCommand[MRProjectDesktopRootBasePath,ProductionPath,MRProjectConfigShell,UnrealDesktopAssetBasePath,]):
#
#     _production_command: ProductionCommand = None
#     _name: str = None
#
#     def __init__(self, production_command:ProductionCommand, name:str):
#         self._production_command = production_command
#         self._name = name
#         super().__init__()
#
#     def get_name(self) -> str:
#         return self._name
#
#     def get_asset_base_path_routines(self, name: str) -> UnrealDesktopAssetBasePath:
#         gitlab_sever_name = self.get_structure_routines().get_parent_path().get_parent_path().get_gitlab_server_name()
#         asset_routines = self.get_structure_routines().get_asset_routines_by_dirname(name,self.get_feedback_ui())
#         return UnrealDesktopAssetBasePath(gitlab_sever_name,asset_routines)
#
#     def get_parent_shell(self) -> ProductionCommand:
#         return self._production_command
#
#     def get_plugin_names_v1(self) -> typing.List[str]:
#         ret = super(UnrealProductionCommand, self).get_plugin_names_v1()
#         ret.append("fiellc.mr_project.production.unreal.command")
#         return ret


class HoudiniProductionCommand(
    GenericTypedAssetsSubdirCommandCommand[
        MRProjectDesktopRootBasePath, ProductionPath, MRProjectConfigShell, HoudiniAssetBasePath, HoudiniAssetConfigShell]):
    _prod_shell: ProductionCommand = None
    _name: str = None

    def __init__(self, prod_shell: ProductionCommand, name: str):
        self._prod_shell = prod_shell
        self._name = name
        super().__init__()

    def get_parent_routines(self) -> ProductionPath:
        return self._prod_shell.get_structure_routines()

    def get_parent_shell(self) -> ProductionCommand:
        return self._prod_shell

    def get_plugin_names_v1(self) -> typing.List[str]:
        ret = super(HoudiniProductionCommand, self).get_plugin_names_v1()
        ret.append(("mr_project.production.houdini.command"))
        return ret

    def get_name(self) -> str:
        return self._name

    def get_asset_base_path_command(self, name: str) -> HoudiniAssetConfigShell:
        asset_routines = self.get_structure_routines().get_asset_interactive_routines_by_dirname(name)
        return HoudiniAssetConfigShell(asset_routines)

    def get_asset_base_path_routines(self, name: str) -> HoudiniAssetBasePath:
        asset_routines = self.get_structure_routines().get_asset_routines_by_dirname(name)
        return HoudiniAssetBasePath(asset_routines)


class GitLibServerInputUI(InputDefaultModalShellUI[str]):

    def validate(self, v: str) -> typing.Tuple[bool, str]:
        v = v.strip()
        if len(v) == 0:
            return False, ""
        else:
            return True, v
