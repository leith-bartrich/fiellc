import abc
from fiepipelib.assetstructure.routines.desktop import AbstractDesktopProjectAssetBasePath


class HoudiniDesktopAssetBasePath(AbstractDesktopProjectAssetBasePath['HoudiniDesktopAssetBasePath'], abc.ABC):
    """
    A houdini asset for holding a houdini project.
    Subclass this class to create project specific types of houdini assets.
    """

    pass
