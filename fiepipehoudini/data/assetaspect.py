import typing

from fiepipelib.assetaspect.data.config import AspectConfiguration


class HoudiniAssetAspectConfiguration(AspectConfiguration):

    _project_dirs: typing.List[str] = None

    def __init__(self, asset_path: str):
        self._project_dirs = []
        super().__init__(asset_path)

    def get_config_name(self) -> str:
        return "houdini"

    def from_json_data(self, data: typing.Dict):
        self._project_dirs = data['project_dirs']

    def to_json_data(self) -> typing.Dict:
        ret = {}
        ret['project_dirs'] = self._project_dirs
        return ret

    def from_parameters(self, project_dirs:typing.List[str]):
        self._project_dirs = project_dirs

    def get_project_dirs(self) -> typing.List[str]:
        return self._project_dirs