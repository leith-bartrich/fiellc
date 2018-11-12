import os
import os.path

from fiepipelib.assetaspect.data.simpleapplication import AbstractSimpleApplicationInstall, \
    AbstractSimpleApplicationInstallsManager


def get_application_name() -> str:
    return "unreal4"


class Unreal4Install(AbstractSimpleApplicationInstall):

    def path_instructions(self) -> str:
        return "Enter a path to an unreal engine directory.  e.g. C:\\Program Files\\Epic Games\\UE_4.20"

    def validate(self, path: str) -> (bool, str):
        if not os.path.exists(path):
            return False, "Path does not exist."
        if not os.path.isdir(path):
            return False, "Path s not a directory."
        return True, "ok"


class Unreal4InstallsManager(AbstractSimpleApplicationInstallsManager[Unreal4Install]):

    def get_application_name(self) -> str:
        return get_application_name()

    def new_empty(self) -> Unreal4Install:
        return Unreal4Install()
