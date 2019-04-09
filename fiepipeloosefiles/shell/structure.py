from fiepipedesktoplib.assetstructure.shell.structure import StructureAssetConfigCommand
from fiepipeloosefiles.data.assetaspect import LooseFilesAspectConfiguration
from fiepipeloosefiles.routines.structure import LooseFilesDesktopAssetBasePath
from fiepipeloosefiles.shell.assetaspect import LooseFilesAspectConfigCommand

#we don't do much here because LooseFilesStrucure inherits from the stand-alone aspect command.
#the only things we'd add to this shell are things that a loose-files structure could do that
#a aspect could not.
#but the nature of loose files, are that they're not structured.  So this will be very minimal.

class LooseFilesStructureAssetCommand(LooseFilesAspectConfigCommand, StructureAssetConfigCommand[
    LooseFilesAspectConfiguration, LooseFilesDesktopAssetBasePath]):

    def get_structure_routines(self) -> LooseFilesDesktopAssetBasePath:
        config_routines = self.get_configuration_routines()
        if not config_routines.is_configured():
            raise FileNotFoundError("This Loose Files aspect isn't configured: " + config_routines.get_asset_path())
        return LooseFilesDesktopAssetBasePath(config_routines.get_asset_routines())
