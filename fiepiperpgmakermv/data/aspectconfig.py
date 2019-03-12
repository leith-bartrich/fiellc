import typing

from fiepipelib.assetaspect.data.config import AssetAspectConfiguration


class RPGMakerMVAspectConfiguration(AssetAspectConfiguration):

    def get_config_name(self) -> str:
        return "rpg_maker_mv"

    def from_json_data(self, data: typing.Dict):
        pass

    def to_json_data(self) -> typing.Dict:
        ret = {}
        return ret

    def from_parameters(self):
        pass

    def get_lfs_patterns(self) -> typing.List[str]:
        ret = []
        ret.append("*.png")
        ret.append("*.ogg")
        ret.append("*.m4a")
        ret.append("*.ttf")
        return ret

    def get_git_ignores(self) -> typing.List[str]:
        ret = []
        return ret

