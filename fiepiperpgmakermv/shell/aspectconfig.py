from fiepipelib.assetaspect.shell.simpleapplication import AbstractSimpleFiletypeConfigCommand
from fiepiperpgmakermv.data.aspectconfig import RPGMakerMVAspectConfiguration
from fiepiperpgmakermv.routines.aspectconfig import RPGMakerMVAspectConfigurationRoutines


class RPGMakerMVAspectConfigurationCommand(AbstractSimpleFiletypeConfigCommand[RPGMakerMVAspectConfiguration]):

    def get_configuration_routines(self) -> RPGMakerMVAspectConfigurationRoutines:
        return RPGMakerMVAspectConfigurationRoutines(self.get_configuration_data())

    def get_configuration_data(self) -> RPGMakerMVAspectConfiguration:
        asset_routines = self.get_asset_shell().get_routines()
        asset_routines.load()
        asset_path = asset_routines.abs_path
        return RPGMakerMVAspectConfiguration(asset_path)
