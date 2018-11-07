import typing

from fiepipelib.assetaspect.data.config import AspectConfiguration


class LooseFilesAspectConfiguration(AspectConfiguration):
    _lfs_extensions = typing.List[str]
    _ignore_extensions = typing.List[str]

    def __init__(self, asset_path: str):
        self._lfs_extensions = []
        self._ignore_extensions = []
        super().__init__(asset_path)

    def get_lfs_extensions(self) -> typing.List[str]:
        """Returns the actual list of lfs extensions.  Modify it to modify the list in this object.
        Example entry: '.bmp'
        """
        return self._lfs_extensions

    def get_ignore_extensions(self) -> typing.List[str]:
        """Returns the actual list of git ignore extensions.  Modify it to modify the list in this object.
        Example entry: '.bmp'
        """
        return self._ignore_extensions

    def get_config_name(self) -> str:
        return "loose_files"

    def from_json_data(self, data: typing.Dict):
        self._lfs_extensions = data['lfs_extensions']
        self._ignore_extensions = data['ignore_extensions']

    def to_json_data(self) -> typing.Dict:
        ret = {}
        ret['lfs_extensions'] = self._lfs_extensions
        ret['ignore_extensions'] = self._ignore_extensions
        return ret

    def from_parameters(self, lfs_extensions: typing.List[str], ignore_extensions: typing.List[str]):
        self._lfs_extensions = lfs_extensions
        self._ignore_extensions = ignore_extensions
