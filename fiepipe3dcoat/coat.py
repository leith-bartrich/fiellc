import os.path

import fiepipelib.locallymanagedtypes.data.abstractmanager
import fiepipelib.applauncher
import fiepipelib.localplatform.routines.localplatform
import fiepipelib.localuser.routines.localuser


def GetAppLinkExchangeDir():
    plat = fiepipelib.localplatform.routines.localplatform.get_local_platform_routines()
    user = fiepipelib.localuser.routines.localuser.LocalUserRoutines(plat)
    if isinstance(plat, fiepipelib.localplatform.routines.localplatform.LocalPlatformWindowsRoutines):
        return os.path.join(user.get_home_dir(), "Documents", "AppLinks", "3D-Coat", "Exchange")
    else:
        return os.path.join(user.get_home_dir(), "AppLinks", "3D-Coat", "Exchange")


class coat(object):
    _path = None
    _name = None

    def GetName(self) -> str:
        return self._name

    def GetPath(self) -> str:
        return self._path

    def LaunchInteractive(self):
        """Launches an interactive version of this 3dcoat install.
        """
        args = []
        args.append(self._path)

        launcher = fiepipelib.applauncher.genericlauncher.listlauncher(args)
        launcher.launch(echo=True)


def FromParameters(path: str, name: str):
    ret = coat()
    ret._path = path
    ret._name = name
    return ret


def FromJSON(data: dict):
    ret = coat()
    ret._path = data['path']
    ret._name = data['name']
    return ret


def ToJSON(c: coat):
    assert isinstance(c, coat)
    ret = {}
    ret['path'] = c._path
    ret['name'] = c._name
    return ret




class CoatLocalManager(fiepipelib.locallymanagedtypes.data.abstractmanager.AbstractUserLocalTypeManager[coat]):

    def FromJSONData(self, data):
        return FromJSON(data)

    def ToJSONData(self, item):
        return ToJSON(item)

    def GetPrimaryKeyColumns(self):
        return ['name']

    def GetColumns(self):
        ret = super().GetColumns()
        ret.append(("name", "text"))
        ret.append(("path", "text"))
        return ret

    def GetManagedTypeName(self):
        return "coat"

    def GetByName(self, name):
        return self._Get(colNamesAndValues=[("name", name)])

    def DeleteByName(self, name):
        self._Delete("name", name)
