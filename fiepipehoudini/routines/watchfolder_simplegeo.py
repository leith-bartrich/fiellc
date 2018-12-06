import os
import os.path
import shutil
import tempfile
import typing

from watchdog.events import DirModifiedEvent, FileModifiedEvent, DirDeletedEvent, FileDeletedEvent, DirCreatedEvent, \
    FileCreatedEvent, DirMovedEvent, FileMovedEvent

from fiepipehoudini.data.filetypes import get_hip_extensions
from fiepipehoudini.routines.assetaspect import HoudiniAspectConfigurationRoutines
from fiepipelib.watchfolder.routines.Folder import FolderRoutines
from fiepipelib.watchfolder.routines.aspect_config import WatcherRoutines


def get_service_subpath() -> str:
    return os.path.join("houdini_watch", "simple_geo")


def get_hip_files_subpath() -> str:
    return os.path.join(get_service_subpath(), "hip_files")


def get_in_subpath() -> str:
    return os.path.join(get_service_subpath(), "in")


def get_out_subpath() -> str:
    return os.path.join(get_service_subpath(), "out")


def get_proc_subpath() -> str:
    return os.path.join(get_service_subpath(), "proc")


def get_in_subpath_for_hip(hip_file_name: str) -> str:
    base, ext = os.path.splitext(hip_file_name)
    return os.path.join(get_in_subpath(), base)


def get_out_subpath_for_hip(hip_file_name: str) -> str:
    base, ext = os.path.splitext(hip_file_name)
    return os.path.join(get_out_subpath(), base)


class HIPProcessThread(object):
    _hip_file_path: str = None
    _geo_file_path: str = None
    _dest_dir_path: str = None
    _proc_dir_path: str = None
    _watcher_routines: WatcherRoutines = None

    def __init__(self, hip_file_path: str, geo_file_path: str, dest_dir_path: str, proc_dir_path: str,
                 watcher_routines: WatcherRoutines):
        super(HIPProcessThread, self).__init__()
        self._hip_file_path = hip_file_path
        self._geo_file_path = geo_file_path
        self._dest_dir_path = dest_dir_path
        self._proc_dir_path = proc_dir_path
        self._watcher_routines = watcher_routines

    async def run(self) -> None:
        asset_routines = self._watcher_routines.get_asset_routines()
        asset_routines.load()
        asset_path = asset_routines.abs_path
        working_dir_path = tempfile.mkdtemp(dir=asset_path)
        blah, hip_filename = os.path.split(self._hip_file_path)
        hip_file_path = os.path.join(working_dir_path, hip_filename)
        shutil.copy(self._hip_file_path, hip_file_path)
        blah, geo_filename = os.path.split(self._geo_file_path)
        geo_basename, geo_ext = os.path.splitext(geo_filename)
        geo_file_path = os.path.join(working_dir_path, "in" + geo_ext)
        shutil.move(self._geo_file_path, geo_file_path)

        hou_routines = HoudiniAspectConfigurationRoutines(asset_routines)
        app = hou_routines.batch_render_hip_files(hou_routines.get_default_houdini(), [hip_file_path], ['simple_geo'],
                                                  self._watcher_routines.feedback_ui,skip_quit=False)
        # communiacte is safer than wait
        app.communicate()
        out_dir_path = os.path.join(self._dest_dir_path, geo_filename)
        if os.path.exists(out_dir_path):
            shutil.rmtree(out_dir_path, ignore_errors=True)
        shutil.move(working_dir_path, out_dir_path)


class HIPProcessorRoutines(FolderRoutines):
    _hip_file_path: str = None
    _out_dir_path: str = None
    _proc_dir_path: str = None

    def __init__(self, watcher: WatcherRoutines, in_dir_path: str, hip_file_path: str, out_dir_path: str,
                 proc_dir_path: str):
        self._hip_file_path = hip_file_path
        self._out_dir_path = out_dir_path
        self._proc_dir_path = proc_dir_path
        super().__init__(watcher, in_dir_path)

    def is_geo_file(self, path: str) -> bool:
        base, ext = os.path.splitext(path)
        geo_formats = ['.obj', '.iges']
        if ext.lower() in geo_formats:
            return True
        return False

    def do_file(self, path: str):
        t = HIPProcessThread(self._hip_file_path, path, self._out_dir_path, self._proc_dir_path, self.watcher)
        self.watcher.queue_task(t.run)

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
        shutil.rmtree(self.path, True)


class HIPFilesRoutines(FolderRoutines):
    _watchers: typing.Dict[str, HIPProcessorRoutines] = None

    _watch_dir_path: str = None
    _proc_dir_path: str = None

    def __init__(self, watcher: WatcherRoutines, hip_dir_path: str, proc_dir_path: str, watch_dir_path: str):
        self._watchers = {}
        self._watch_dir_path = watch_dir_path
        self._proc_dir_path = proc_dir_path
        super().__init__(watcher, hip_dir_path)

    def is_hip_file(self, path: str) -> bool:
        base, ext = os.path.splitext(path)
        if ext.lower() in get_hip_extensions("."):
            return True
        return False

    def add_hip_watcher(self, path: str):
        head, tail = os.path.split(path)
        base, ext = os.path.splitext(tail)
        in_dir_path = os.path.join(self._watch_dir_path, get_in_subpath_for_hip(tail))
        out_dir_path = os.path.join(self._watch_dir_path, get_out_subpath_for_hip(tail))
        self._watchers[tail] = HIPProcessorRoutines(self.watcher, in_dir_path, path, out_dir_path, self._proc_dir_path)

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


def watch(routines: WatcherRoutines, asset_dir_path: str, watch_dir_path: str):
    hip_dir_path = os.path.join(asset_dir_path, get_hip_files_subpath())
    proc_dir_path = os.path.join(asset_dir_path, get_proc_subpath())
    HIPFilesRoutines(routines, hip_dir_path, proc_dir_path, watch_dir_path)
