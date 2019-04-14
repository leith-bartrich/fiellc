import typing

from fiepipelib.assetstructure.data.aspect_config import RootDesktopStructureAspectConfiguration

class PostOfficeConfiguration(RootDesktopStructureAspectConfiguration):

    def get_config_name(self) -> str:
        return "postoffice"

    def from_json_data(self, data: typing.Dict):
        pass

    def to_json_data(self) -> typing.Dict:
        ret = {}
        return ret
