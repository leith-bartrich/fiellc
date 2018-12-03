import os
import os.path
import shutil
import typing

from watchdog.events import DirModifiedEvent, FileModifiedEvent, DirDeletedEvent, FileDeletedEvent, DirCreatedEvent, \
    FileCreatedEvent, DirMovedEvent, FileMovedEvent

from fiepipehoudini.data.filetypes import get_hip_extensions
from fiepipelib.watchfolder.routines.Folder import FolderRoutines
from fiepipelib.watchfolder.routines.Watcher import WatcherRoutines


def get_service_subpath() -> str:
    return os.path.join("houdini", "simple_geo")


def get_hip_files_subpath() -> str:
    return os.path.join(get_service_subpath(), "hip_files")


def get_in_subpath() -> str:
    return os.path.join(get_service_subpath(), "in")


def get_in_subpath_for_hip(hip_file_name: str) -> str:
    base, ext = os.path.splitext(hip_file_name)
    return os.path.join(get_in_subpath(), base)


class HIPProcessorRoutines(FolderRoutines):
    _hip_file_path: str = None

    def __init__(self, watcher: WatcherRoutines, subpath: str, hip_file_path: str):
        self._hip_file_path = hip_file_path
        super().__init__(watcher, subpath)

    def is_geo_file(self, path: str) -> bool:
        base, ext = os.path.splitext(path)
        geo_formats = ['.obj', '.iges']
        if ext.lower() in geo_formats:
            return True
        return False

    def do_file(self, path: str):
        raise NotImplementedError()

    def on_existing_file(self, path: str):
        if self.is_geo_file(path):
            self.do_file(path)

    def on_existing_dir(self, path: str):
        pass

    def on_file_moved(self, event: FileMovedEvent):
        pass

    def on_dir_moved(self, event: DirMovedEvent):
        pass

    def on_file_created(self, event: FileCreatedEvent):
        if self.is_geo_file(event.src_path):
            self.do_file(event.src_path)

    def on_dir_created(self, event: DirCreatedEvent):
        pass

    def on_file_deleted(self, event: FileDeletedEvent):
        pass

    def on_dir_deleted(self, event: DirDeletedEvent):
        pass

    def on_file_modified(self, event: FileModifiedEvent):
        if self.is_geo_file(event.src_path):
            self.do_file(event.src_path)

    def on_dir_modified(self, event: DirModifiedEvent):
        pass

    def stop(self):
        super().stop()
        dir_path = os.path.join(self._watcher.path, self.subpath)
        shutil.rmtree(dir_path, True)


class HIPFilesRoutines(FolderRoutines):
    _watchers: typing.Dict[str, HIPProcessorRoutines] = None

    def __init__(self, watcher: WatcherRoutines, subpath: str):
        self._watchers = {}
        super().__init__(watcher, subpath)

    def is_hip_file(self, path: str) -> bool:
        base, ext = os.path.splitext(path)
        if ext.lower() in get_hip_extensions("."):
            return True
        return False

    def add_hip_watcher(self, path: str):
        head, tail = os.path.split(path)
        base, ext = os.path.splitext(tail)
        subpath = get_in_subpath_for_hip(tail)
        self._watchers[tail] = HIPProcessorRoutines(self.watcher, subpath, path)

    def remove_hip_watcher(self, path: str):
        head, tail = os.path.split(path)
        if tail in self._watchers.keys():
            hip_watcher = self._watchers.pop(tail)
            hip_watcher.stop()

    def on_existing_file(self, path: str):
        if self.is_hip_file(path):
            self.add_hip_watcher(path)

    def on_existing_dir(self, path: str):
        pass

    def on_file_moved(self, event: FileMovedEvent):
        if self.is_hip_file(event.dest_path):
            self.add_hip_watcher(event.dest_path)

    def on_dir_moved(self, event: DirMovedEvent):
        pass

    def on_file_created(self, event: FileCreatedEvent):
        if self.is_hip_file(event.src_path):
            self.add_hip_watcher(event.src_path)

    def on_dir_created(self, event: DirCreatedEvent):
        pass

    def on_file_deleted(self, event: FileDeletedEvent):
        if self.is_hip_file(event.src_path):
            self.remove_hip_watcher(event.src_path)

    def on_dir_deleted(self, event: DirDeletedEvent):
        pass

    def on_file_modified(self, event: FileModifiedEvent):
        pass

    def on_dir_modified(self, event: DirModifiedEvent):
        pass


def watch(routines: WatcherRoutines):
    HIPFilesRoutines(routines, get_hip_files_subpath())
