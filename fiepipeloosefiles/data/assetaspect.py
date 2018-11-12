import typing

import pkg_resources

from fiepipelib.assetaspect.data.config import AspectConfiguration


class LooseFilesAspectConfiguration(AspectConfiguration):

    def __init__(self, asset_path: str):
        super().__init__(asset_path)

    def get_lfs_patterns(self) -> typing.List[str]:
        return self.lfs_patterns_from_plugins()

    def get_git_ignores(self) -> typing.List[str]:
        return self.ignore_patterns_from_plugins()

    def get_config_name(self) -> str:
        return "loose_files"

    def from_json_data(self, data: typing.Dict):
        pass

    def to_json_data(self) -> typing.Dict:
        ret = {}
        return ret

    def from_parameters(self):
        pass

    def lfs_patterns_from_plugins(self):

        lfs_extensions = []

        entrypoints = pkg_resources.iter_entry_points("fiepipe.plugin.loosefiles.lfs.extensions")
        for entrypoint in entrypoints:
            method = entrypoint.load()
            method(self, lfs_extensions)

        ret = []
        for extension in lfs_extensions:
            ret.append("*." + extension.lstrip('.'))

        return ret

    def ignore_patterns_from_plugins(self):

        ignore_extensions = []

        entrypoints = pkg_resources.iter_entry_points("fiepipe.plugin.loosefiles.ignore.extensions")
        for entrypoint in entrypoints:
            method = entrypoint.load()
            method(self, ignore_extensions)

        ret = []
        for extension in ignore_extensions:
            ret.append("*." + extension.lstrip('.'))

        return ret
