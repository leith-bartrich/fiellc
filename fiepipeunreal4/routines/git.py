import os
import os.path

import git

from fiepipelib.git.routines.ignore import AddIgnore, CheckCreateIgnore, RemoveIgnore
from fiepipelib.git.routines.lfs import AddGitAttributes, Track, InstallLFSGlobal, Untrack


def add_project_tracking_metadata(repo: git.Repo, path: str):
    """
    Adds appropriate ignores, lfs, trakcs for an unreal project
    :param path: the path to a .uproject file.  All other paths are created relative to this.
    :return: None
    """
    (project_dir, project_filename) = os.path.split(path)

    root, ext = os.path.splitext(project_filename)
    if ext != ".uproject":
        raise ValueError("Passed path should have been to a .uproject file.")

    CheckCreateIgnore(repo)

    AddIgnore(repo=repo, pattern=os.path.join(project_dir, "Binaries"))
    AddIgnore(repo=repo, pattern=os.path.join(project_dir, "DerivedDataCache"))
    AddIgnore(repo=repo, pattern=os.path.join(project_dir, "Intermediate"))
    AddIgnore(repo=repo, pattern=os.path.join(project_dir, "Saved"))
    AddIgnore(repo=repo, pattern=".vscode")
    AddIgnore(repo=repo, pattern=".vs")
    AddIgnore(repo=repo, pattern="*.VC.db")
    AddIgnore(repo=repo, pattern="*.opensdf")
    AddIgnore(repo=repo, pattern="*.opendb")
    AddIgnore(repo=repo, pattern="*.sdf")
    AddIgnore(repo=repo, pattern="*.sln")
    AddIgnore(repo=repo, pattern="*.suo")
    AddIgnore(repo=repo, pattern="*.xcodeproj")
    AddIgnore(repo=repo, pattern="*.xcworkspace")

    InstallLFSGlobal()

    Track(repo, [os.path.join(project_dir, "Content/**")])
    AddGitAttributes(repo)


def remove_project_tracking_metadata(repo: git.Repo, path: str):
    """
    Removes appropriate ignores, lfs, trakcs for an unreal project
    :param path: the path to a .uproject file.  All other paths are created relative to this.
    :return: None
    """
    (project_dir, project_filename) = os.path.split(path)

    with os.path.splitext(project_filename) as (root, ext):
        if ext != ".uproject":
            raise ValueError("Passed path should have been to a .uproject file.")

    CheckCreateIgnore(repo)

    RemoveIgnore(repo, os.path.join(project_dir, "Binaries"))
    RemoveIgnore(repo, os.path.join(project_dir, "DerivedDataCache"))
    RemoveIgnore(repo, os.path.join(project_dir, "Intermediate"))
    RemoveIgnore(repo, os.path.join(project_dir, "Saved"))

    InstallLFSGlobal()

    Untrack(repo, [os.path.join(project_dir, "Content/**")])
    AddGitAttributes(repo)
