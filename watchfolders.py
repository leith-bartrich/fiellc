from fiepipedesktoplib.gitstorage.shells import Shell as AssetShell, ContainerIDVariableCommand, AssetIDVarCommand, \
    RootIDVarCommand
from fiepipedesktoplib.watchfolder.shell.watchfolder import WatchFolderShellApplication as WatcherShell

_CONTAINER_ID = "9341cf7f-5f48-4971-aece-a5f203c23076"
_ROOT_ID = "e00a2013-9041-4570-bc88-ac31bcd3e36e"
_ASSET_ID = "aadc8b52-afa1-4525-a182-40841d2baa54"


def _get_asset_shell() -> AssetShell:
    cont_var = ContainerIDVariableCommand(_CONTAINER_ID)
    root_var = RootIDVarCommand(_ROOT_ID)
    asset_var = AssetIDVarCommand(_ASSET_ID)
    return AssetShell(cont_var, root_var, asset_var)


def get_watcher_shell() -> WatcherShell:
    return WatcherShell(_get_asset_shell())


def docs():
    shell = get_watcher_shell()
    shell.onecmd("start_documents")


def icloud():
    shell = get_watcher_shell()
    shell.onecmd("start_icloud")
