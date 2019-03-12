import typing

from fiepipelib.rootaspect.data.config import RootAsepctConfiguration


class MRProjectConfig(RootAsepctConfiguration):

    def get_config_name(self) -> str:
        return "mr_project"

    def from_json_data(self, data: typing.Dict):
        return

    def to_json_data(self) -> typing.Dict:
        return {}
