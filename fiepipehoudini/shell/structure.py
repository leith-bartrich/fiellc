import abc
import typing

from fiepipedesktoplib.assetstructure.shell.structure import StructureAssetConfigCommand
from fiepipehoudini.data.assetaspect import HoudiniAssetAspectConfiguration
from fiepipehoudini.routines.structure import HoudiniDesktopAssetBasePath
from fiepipehoudini.shell.assetaspect import HoudiniAssetAspectCommand

THA = typing.TypeVar("THA", bound=HoudiniDesktopAssetBasePath)


class HoudiniStructureAssetConfigCommand(HoudiniAssetAspectCommand,
                                         StructureAssetConfigCommand[HoudiniAssetAspectConfiguration, THA],
                                         typing.Generic[THA], abc.ABC):
    """Subclass this command in order to create project specific types of houdini commands."""

    @abc.abstractmethod
    def get_structure_routines(self) -> THA:
        raise NotImplementedError()
