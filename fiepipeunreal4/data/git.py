import os
import os.path
import typing


def get_asset_ignore_patterns() -> typing.List[str]:
    ret = []

    ret.append(".vscode")
    ret.append(".vs")
    ret.append("*.VC.db")
    ret.append("*.opensdf")
    ret.append("*.opendb")
    ret.append("*.sdf")
    ret.append("*.sln")
    ret.append("*.suo")
    ret.append("*.xcodeproj")
    ret.append("*.xcworkspace")

    return ret


def get_project_ignore_patterns(uproject_path: str) -> typing.List[str]:
    ret = []

    (project_dir, project_filename) = os.path.split(path)

    root, ext = os.path.splitext(project_filename)
    if ext != ".uproject":
        raise ValueError("Passed path should have been to a .uproject file.")

    ret.append(os.path.join(project_dir, "Binaries"))
    ret.append(os.path.join(project_dir, "DerivedDataCache"))
    ret.append(os.path.join(project_dir, "Intermediate"))
    ret.append(os.path.join(project_dir, "Saved"))

    return ret


def get_asset_lfs_track_patterns() -> typing.List[str]:
    ret = []
    return ret


def get_project_lfs_track_patterns(uproject_path: str) -> typing.List[str]:
    ret = []

    (project_dir, project_filename) = os.path.split(path)

    root, ext = os.path.splitext(project_filename)
    if ext != ".uproject":
        raise ValueError("Passed path should have been to a .uproject file.")

    ret.append(os.path.join(project_dir, "Content/**"))

    return ret

# def remove_project_tracking_metadata(repo: git.Repo, path: str):
#     """
#     Removes appropriate ignores, lfs, trakcs for an unreal project
#     :param path: the path to a .uproject file.  All other paths are created relative to this.
#     :return: None
#     """
#     (project_dir, project_filename) = os.path.split(path)
#
#     with os.path.splitext(project_filename) as (root, ext):
#         if ext != ".uproject":
#             raise ValueError("Passed path should have been to a .uproject file.")
#
#     CheckCreateIgnore(repo)
#
#     RemoveIgnore(repo, os.path.join(project_dir, "Binaries"))
#     RemoveIgnore(repo, os.path.join(project_dir, "DerivedDataCache"))
#     RemoveIgnore(repo, os.path.join(project_dir, "Intermediate"))
#     RemoveIgnore(repo, os.path.join(project_dir, "Saved"))
#
#     InstallLFSGlobal()
#
#     Untrack(repo, [os.path.join(project_dir, "Content/**")])
#     AddGitAttributes(repo)
