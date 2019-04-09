import typing

from fiepipehoudini.data.git import get_asset_ignores, get_asset_lfs_tracks
from fiepipelib.assetaspect.data.config import AssetAspectConfiguration
from fiepipecommonfiletypes.data.lfs_tracked_patterns import get_image_extensions, get_3d_extensions, get_video_extensions,get_audio_extensions, extensions_to_lfs_patterns

class HoudiniAssetAspectConfiguration(AssetAspectConfiguration):

    def __init__(self, asset_path: str):
        super().__init__(asset_path)

    def get_config_name(self) -> str:
        return "houdini"

    def from_json_data(self, data: typing.Dict):
        pass

    def to_json_data(self) -> typing.Dict:
        ret = {}
        return ret

    def from_parameters(self):
        pass

    def get_lfs_patterns(self) -> typing.List[str]:

        ret = []

        get_video_extensions(ret)
        get_audio_extensions(ret)
        get_3d_extensions(ret)
        get_image_extensions(ret)

        ret = extensions_to_lfs_patterns(ret)

        ret.extend(get_asset_lfs_tracks())



        return ret

    def get_git_ignores(self) -> typing.List[str]:

        ret = []
        ret.extend(get_asset_ignores())

        return ret
