import os
from typing import Any, Optional, Iterable
import database as db
from utils import logger
from abc import abstractmethod

class Tagger:
    def __init__(self, tagger_name, item: "db.Item"):
        self.item = item

    def get_tag_def(self, name: str, tag_type: "db.TagType"):
        pass

    @abstractmethod
    def _get_tags(self) -> "Iterable":
        pass

    def _tag(self):
        for tag in self._get_tags():
            tag.item_id = self.item.id
            db.session.add(tag)

class FileTagger(Tagger):
    def __init__(self, item: "db.Item", path: str):
        super().__init__("file_tagger", item)
        self.path = path

    @staticmethod
    def tag(item: "db.Item", path: str):
        tagger: Optional["Tagger"] = None
        ext = os.path.splitext(path)[1][1:]

        if tagger is None:
            logger.info("NB: No file tagger for file with ext: {}".format(ext))
        else:
            tagger._tag()
