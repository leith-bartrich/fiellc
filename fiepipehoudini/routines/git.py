import os
import os.path

import git

from fiepipelib.git.routines.ignore import AddIgnore, CheckCreateIgnore
from fiepipelib.git.routines.lfs import AddGitAttributes, Track, InstallLFSGlobal


def add_project_tracking_metadata(repo: git.Repo, path: str):
    """
    Adds appropriate ignores, lfs, trakcs for a houdini project
    :param path: the path to a houdini project directory.  All other paths are created relative to this.
    :return: None
    """
    project_dir = path
    if not os.path.isdir(project_dir):
        raise ValueError("The given path is not a directory.")

    CheckCreateIgnore(repo)

    houdini_filetype_postpends = ['','lc', 'nc']

    houdini_ignore_backup_patterns = ["**/backup/*.hda","**/backup/*.hip"]

    for postpend in houdini_filetype_postpends:
        for pattern in houdini_ignore_backup_patterns:
            AddIgnore(repo=repo,pattern=pattern + postpend)

    InstallLFSGlobal()

    houdini_filetype_patterns = ['*.hda', '*.hip', '*.bgeo', '*.geo']

    houdini_patterns = []
    for postpend in houdini_filetype_postpends:
        for pattern in houdini_filetype_patterns:
            houdini_patterns.append(pattern + postpend)
    Track(repo, houdini_patterns)

    AddGitAttributes(repo)


def remove_project_tracking_metadata(repo: git.Repo, path: str):
    """
    Removes appropriate ignores, lfs, tracks for a houdini project
    :param path: the path to a houdini project directory.  All other paths are created relative to this.
    :return: None
    """

    CheckCreateIgnore(repo)

    InstallLFSGlobal()

    AddGitAttributes(repo)
