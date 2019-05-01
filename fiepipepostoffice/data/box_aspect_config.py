import typing

from fiepipelib.assetstructure.data.aspect_config import AssetDesktopStructureAspectConfiguration

class BoxAspectConfig(AssetDesktopStructureAspectConfiguration):

    def get_lfs_patterns(self) -> typing.List[str]:
        return []

    def get_git_ignores(self) -> typing.List[str]:
        return []

    def get_config_name(self) -> str:
        return "box"

    def from_json_data(self, data: typing.Dict):
        return

    def to_json_data(self) -> typing.Dict:
        return {}
