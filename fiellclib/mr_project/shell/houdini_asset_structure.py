import typing

from fiellclib.mr_project.routines.houdini_asset_structure import HoudiniAssetBasePath
from fiepipehoudini.shell.structure import HoudiniStructureAssetConfigCommand, THA


class HoudiniAssetConfigShell(HoudiniStructureAssetConfigCommand[HoudiniAssetBasePath]):

    def get_structure_routines(self) -> HoudiniAssetBasePath:
        return HoudiniAssetBasePath(self.get_asset_routines())
