from watchdog.events import FileSystemEventHandler, FileSystemMovedEvent, DirMovedEvent, FileMovedEvent


class HoudiniSimpleGeometryWatchHandler(FileSystemEventHandler):

    def on_any_event(self, event):
        super().on_any_event(event)

    def on_moved(self, event: FileSystemMovedEvent):
        super().on_moved(event)
        if event.is_directory:
            assert isinstance(event, DirMovedEvent)

        else:
            assert isinstance(event, FileMovedEvent)

    def on_created(self, event):
        super().on_created(event)

    def on_deleted(self, event):
        super().on_deleted(event)

    def on_modified(self, event):
        super().on_modified(event)
