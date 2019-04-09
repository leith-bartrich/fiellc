import typing

from fiepipelib.assetstructure.routines.desktop import AbstractDesktopProjectAssetBasePath
from fiepipelib.assetstructure.routines.structure import AbstractAssetBasePath, AbstractSubPath, BT

#in theory, one could create a subclass that has actual subpaths and such.  But that seems
#somewhat antithetical to the idea of structures.  You'd almost always want
#to create a new structure routine from something else.

class LooseFilesDesktopAssetBasePath(AbstractDesktopProjectAssetBasePath['LooseFilesDesktopAssetBasePath']):
    """
    A loose files asset for holding unstructured loose files.
    """

    def get_sub_basepaths(self) -> typing.List["AbstractAssetBasePath"]:
        return []

    def get_subpaths(self) -> "typing.List[AbstractSubPath[BT]]":
        return []

