import os
import os.path

from fiepipelib.assetaspect.data.simpleapplication import AbstractSimpleApplicationInstall, \
    AbstractSimpleApplicationInstallsManager, T


class RPGMakerMVInstall(AbstractSimpleApplicationInstall):

    def path_instructions(self) -> str:
        return "Enter a path to a RPGMakerMV Install directory.\n" \
               "e.g. C:\\Program Files (x86)\\Steam\\steamapps\\common\\RPG Maker MV"

    def validate(self, path: str) -> (bool, str):
        if not os.path.exists(path):
            return False, "Path does not exist."
        if not os.path.isdir(path):
            return False, "Path is not a directory."
        return True, "ok"


class RPGMakerMVInstallManager(AbstractSimpleApplicationInstallsManager[RPGMakerMVInstall]):

    def get_application_name(self) -> str:
        return "rpg_maker_mv"

    def new_empty(self) -> T:
        return RPGMakerMVInstall()
