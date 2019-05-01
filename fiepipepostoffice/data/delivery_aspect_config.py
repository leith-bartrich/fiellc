import typing

from fiepipelib.assetstructure.data.aspect_config import AssetDesktopStructureAspectConfiguration

class DeliveryAspectConfig(AssetDesktopStructureAspectConfiguration):

    _locked: bool = None

    def get_locked(self) -> bool:
        return self._locked

    def set_locked(self, locked:bool):
        self._locked = locked


    def get_lfs_patterns(self) -> typing.List[str]:
        ret = []
        ret.append("content/**")
        return ret

    def get_git_ignores(self) -> typing.List[str]:
        return []

    def get_config_name(self) -> str:
        return "delivery"

    def from_json_data(self, data: typing.Dict):
        self._locked = data['locked']

    def to_json_data(self) -> typing.Dict:
        ret = {}
        ret['locked'] = self._locked
        return ret

    def from_params(self, locked:bool):
        self._locked = locked