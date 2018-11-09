import typing

from fiepipelib.assetaspect.data.config import AspectConfiguration


class UnrealAssetAspectConfiguration(AspectConfiguration):
    _project_files: typing.List[str] = None

    def __init__(self, asset_path: str):
        self._project_files = []
        super().__init__(asset_path)

    def get_config_name(self) -> str:
        return "unreal4"

    def from_json_data(self, data: typing.Dict):
        self._project_files = data['project_files']

    def to_json_data(self) -> typing.Dict:
        ret = {}
        ret['project_files'] = self._project_files
        return ret

    def from_parameters(self, project_files: typing.List[str]):
        self._project_files = project_files

    def get_project_files(self) -> typing.List[str]:
        return self._project_files
