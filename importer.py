import hashlib
import os
import database as db
import filesystem as fs
from utils import logger
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
from taggers import FileTagger

_HASH_BUF_SIZE = 65536

def get_file_hash(path: str):
    # https://stackoverflow.com/a/22058673/5013267
    hasher = hashlib.md5()  # md5 because fast (+ not too interested in security)

    with open(path, 'rb') as f:
        while True:
            data = f.read(_HASH_BUF_SIZE)
            if not data:
                break
            hasher.update(data)

    return hasher.hexdigest()

class FileImporterEventHandler(FileSystemEventHandler):
    def on_created(self, event):
        for file in os.listdir(fs.PATH_IMPORT):
            logger.debug("Importing: {}".format(file))
            file_path = os.path.join(fs.PATH_IMPORT, file)
            item = db.Item(path="files/" + get_file_hash(file_path) + os.path.splitext(file)[1])
            db.session.add(item)
            db.session.flush()

            FileTagger.tag(item, file_path)

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
