from fiepipelib.assetaspect.data.simpleapplication import AbstractSimpleApplicationInstall, \
    AbstractSimpleApplicationInstallsManager


def get_application_name() -> str:
    return "unreal4"


class Unreal4Install(AbstractSimpleApplicationInstall):
    pass


class Unreal4InstallsManager(AbstractSimpleApplicationInstallsManager[Unreal4Install]):

    def get_application_name(self) -> str:
        return get_application_name()

    def new_empty(self) -> Unreal4Install:
        return Unreal4Install()
