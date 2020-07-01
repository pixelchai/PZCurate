import os

import filesystem as fs
from utils import logger
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer


class FileImporter:
    def __init__(self, path):
        self.path = path

class FileImporterEventHandler(FileSystemEventHandler):
    def on_created(self, event):
        for file in os.listdir(fs.PATH_IMPORT):
            file_path = os.path.join(fs.PATH_IMPORT, file)
            pass

class FolderWatcher:
    def __init__(self):
        self._observer = Observer()
        self._handler = FileImporterEventHandler()
        self._observer.schedule(self._handler, fs.PATH_IMPORT)

        self._running = False

    def run(self):
        self._running = True
        self._observer.start()
        logger.debug("Folder watcher running")

        # initial poll
        self._handler.on_created(None)

        # keep thread alive
        while self._running:
            pass

    def stop(self):
        self._running = False
        logger.debug("Folder watcher stopped")
