import typing

from fiepipelib.locallymanagedtypes.data.abstractmanager import AbstractUserLocalTypeManager


class HoudiniInstall(object):
    _name: str = None
    _path: str = None
    _executable: str = None

    def get_name(self) -> str:
        return self._name

    def get_path(self) -> str:
        return self._path

    def get_executable(self) -> str:
        return self._executable


class HoudiniInstallsManager(AbstractUserLocalTypeManager[HoudiniInstall]):
    def GetManagedTypeName(self) -> str:
        return "houdini_installs"

    def GetColumns(self) -> typing.List[typing.Tuple[str, str]]:
        ret = super(HoudiniInstallsManager, self).GetColumns()
        ret.append(('name', 'text'))
        return ret

    def GetPrimaryKeyColumns(self) -> typing.List[str]:
        return ['name']

    def ToJSONData(self, item: HoudiniInstall) -> dict:
        ret = {}
        ret['name'] = item.get_name()
        ret['path'] = item.get_path()
        ret['executable'] = item.get_executable()
        return ret

    def FromJSONData(self, data: dict) -> HoudiniInstall:
        ret = HoudiniInstall()
        ret._name = data['name']
        ret._path = data['path']
        ret._executable = data['executable']
        return ret

    def FromParameters(self, name: str, path: str, executable:str) -> HoudiniInstall:
        ret = HoudiniInstall()
        ret._name = name
        ret._path = path
        ret._executable = executable
        return ret

    def get_by_name(self, name: str) -> HoudiniInstall:
        return self._Get([('name', name)])[0]

    def delete_by_name(self, name: str):
        self._Delete('name', name)
