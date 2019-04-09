import typing

from fiepipelib.rootaspect.data.config import RootAsepctConfiguration


class MRProjectConfig(RootAsepctConfiguration):

    _gitlab_server_name: str = None

    def get_gitlab_server_name(self) -> str:
        return self._gitlab_server_name

    def set_gitlab_server_name(self, gitlab_server_name:str):
        self._gitlab_server_name = gitlab_server_name


    def get_config_name(self) -> str:
        return "mr_project"

    def from_json_data(self, data: typing.Dict):
        self._gitlab_server_name = data['gitlab_server_name']
        return

    def to_json_data(self) -> typing.Dict:
        ret = {}
        ret['gitlab_server_name'] = self._gitlab_server_name
        return ret


