import datetime
import enum
import os.path
import typing
import uuid

from fiepipelib.assetstructure.data.aspect_config import RootDesktopStructureAspectConfiguration


class DeliveryNamingMethod(enum.Enum):
    UTC_DATE_HASH = 0
    UTC_DATE_INCREMENTAL = 1
    UTC_DATE_TIME = 2


def get_delivery_base_date() -> str:
    utcnow = datetime.datetime.utcnow()
    year_str = str(utcnow.year)
    month_str = str(utcnow.month)
    day_str = str(utcnow.day)
    return year_str + "_" + month_str + "_" + day_str


def get_delivery_name_date_hash(dir_path: str) -> str:
    base_name = get_delivery_base_date()
    hash = str(uuid.uuid4()).replace("-", "")[0:8]
    return base_name + "_" + hash


def get_delivery_name_date_incremental(dir_path: str) -> str:
    base_name = get_delivery_base_date()
    num = 0
    while True:
        num_str = str(num)
        ret = base_name + "_" + num_str
        abs_path = os.path.join(dir_path, ret)
        if not os.path.exists(abs_path):
            return ret
        num = num + 1


def get_delivery_name_date_time(dir_path: str) -> str:
    base_name = get_delivery_base_date()
    utcnow = datetime.datetime.utcnow()
    hour_str = str(utcnow.hour)
    minute_str = str(utcnow.minute)
    second_str = str(utcnow.second)
    ms_str = str(utcnow.microsecond)
    return base_name + "_" + hour_str + "_" + minute_str + "_" + second_str + "_" + ms_str


class PostOfficeConfiguration(RootDesktopStructureAspectConfiguration):
    _delivery_naming_method: DeliveryNamingMethod = None

    def get_delivery_naming_method(self) -> DeliveryNamingMethod:
        return self._delivery_naming_method

    def set_delivery_naming_method(self, delivery_naming_method: DeliveryNamingMethod):
        self._delivery_naming_method = delivery_naming_method

    def get_new_delivery_name(self, dir_path: str) -> str:
        if self._delivery_naming_method == DeliveryNamingMethod.UTC_DATE_HASH:
            return get_delivery_name_date_hash(dir_path)
        elif self._delivery_naming_method == DeliveryNamingMethod.UTC_DATE_INCREMENTAL:
            return get_delivery_name_date_incremental(dir_path)
        elif self._delivery_naming_method == DeliveryNamingMethod.UTC_DATE_TIME:
            return get_delivery_name_date_time(dir_path)
        else:
            raise TypeError("Unsupported delivery naming method.")

    def get_config_name(self) -> str:
        return "postoffice"

    def from_json_data(self, data: typing.Dict):
        self._delivery_naming_method = DeliveryNamingMethod[data["delivery_naming_method"]]

    def to_json_data(self) -> typing.Dict:
        ret = {}
        ret["delivery_naming_method"] = self._delivery_naming_method.name
        return ret
