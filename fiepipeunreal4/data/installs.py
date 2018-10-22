import typing

from fiepipelib.locallymanagedtypes.data.abstractmanager import AbstractUserLocalTypeManager


class Unreal4Install(object):
    _name: str = None
    _path: str = None

    def get_name(self) -> str:
        return self._name

    def get_path(self) -> str:
        return self._path


class Unreal4InstallsManager(AbstractUserLocalTypeManager[Unreal4Install]):
    def GetManagedTypeName(self) -> str:
        return "unreal4_installs"

    def GetColumns(self) -> typing.List[typing.Tuple[str, str]]:
        ret = super(Unreal4InstallsManager, self).GetColumns()
        ret.append(('name', 'text'))
        return ret

    def GetPrimaryKeyColumns(self) -> typing.List[str]:
        return ['name']

    def ToJSONData(self, item: Unreal4Install) -> dict:
        ret = {}
        ret['name'] = item.get_name()
        ret['path'] = item.get_path()
        return ret

    def FromJSONData(self, data: dict) -> Unreal4Install:
        ret = Unreal4Install()
        ret._name = data['name']
        ret._path = data['path']
        return ret

    def FromParameters(self, name: str, path: str) -> Unreal4Install:
        ret = Unreal4Install()
        ret._name = name
        ret._path = path
        return ret

    def get_by_name(self, name: str) -> Unreal4Install:
        return self._Get([('name', name)])[0]

    def delete_by_name(self, name: str):
        self._Delete('name', name)
