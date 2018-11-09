from fiepipelib.assetaspect.data.simpleapplication import AbstractSimpleApplicationInstall, \
    AbstractSimpleApplicationInstallsManager, T


class RPGMakerMVInstall(AbstractSimpleApplicationInstall):
    pass


class RPGMakerMVInstallManager(AbstractSimpleApplicationInstallsManager[RPGMakerMVInstall]):

    def get_application_name(self) -> str:
        return "rpg_maker_mv"

    def new_empty(self) -> T:
        return RPGMakerMVInstall()
