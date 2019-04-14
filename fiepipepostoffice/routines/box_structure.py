import typing

from fiepipelib.assetstructure.routines.desktop import AbstractDesktopProjectAssetBasePath
from fiepipepostoffice.routines.root_structure import PostOfficeRootStructureRoutines
from fiepipelib.assetstructure.routines.structure import AbstractAssetBasePath, AbstractSubPath, StaticSubDir, \
    GenericAssetBasePathsSubDir, AbstractAssetBasePath, TABP


class Box(AbstractAssetBasePath["Box"]):

    def get_sub_basepaths(self) -> typing.List["AbstractAssetBasePath"]:
        raise NotImplementedError()

    def get_subpaths(self) -> "typing.List[AbstractSubPath[Box]]":
        raise NotImplementedError()

class Incoming(GenericAssetBasePathsSubDir[Box,Box,"IncomingDelivery"]):

    def get_asset_basepath_by_dirname(self, dirname: str) -> "IncomingDelivery":
        raise NotImplementedError()

class Outgoing(GenericAssetBasePathsSubDir[Box,Box,"OutgoingDelivery"]):

    def get_asset_basepath_by_dirname(self, dirname: str) -> "OutgoingDelivery":
        raise NotImplementedError()
