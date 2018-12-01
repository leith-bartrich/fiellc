import typing
from fiepipehoudini.data.filetypes import get_all_extensions

def get_asset_ignores() -> typing.List[str]:
    ret = []

    houdini_filetype_postpends = ['', 'lc', 'nc']

    houdini_ignore_backup_patterns = ["**/backup/*.hda", "**/backup/*.hip"]

    for postpend in houdini_filetype_postpends:
        for pattern in houdini_ignore_backup_patterns:
            ret.append(pattern + postpend)

    return ret


def get_project_ignores(project_path: str) -> typing.List[str]:
    ret = []

    return ret


def get_asset_lfs_tracks() -> typing.List[str]:
    return get_all_extensions("*.")


def get_project_lfs_tracks(project_path: str) -> typing.List[str]:
    ret = []

    return ret
