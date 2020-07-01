import os
import time
from typing import Any, Optional, Iterable
import database as db
from utils import logger

class Tagger:
    def __init__(self, tagger_name, item: "db.Item"):
        self.tagger_name = tagger_name
        self.item = item

    def get_tag_def(self, name: str, tag_type: "db.TagType"):
        tag_def = db.TagDef(name=name,
                            tag_type=tag_type,
                            source=self.tagger_name)
        db.session.merge(tag_def)
        return tag_def

    def get_tag_ass(self, name: str, tag_type: "db.TagType", value):
        tag_def = self.get_tag_def(name, tag_type)
        return db.TagAss(def_name=tag_def.name,
                         item_id=self.item.id,
                         value=str(value),
                         source=self.tagger_name)

    def _get_tags(self) -> "Iterable":
        yield self.get_tag_ass("timestamp", db.TagType.FLOAT, time.time())

    def _tag(self):
        for tag in self._get_tags():
            tag.item_id = self.item.id
            db.session.add(tag)
        db.session.flush()

class FileTagger(Tagger):
    def __init__(self, item: "db.Item", path: str):
        super().__init__("file_tagger", item)
        self.path = path

    @staticmethod
    def tag(item: "db.Item", path: str):
        tagger: Optional["Tagger"] = None
        ext = os.path.splitext(path)[1][1:]

        if ext in ["png", "jpeg", "jpg", "bmp", "gif"]:
            tagger = ImageTagger(item, path)

        if tagger is None:
            logger.debug("NB: No specific file tagger for file with ext: {}".format(ext))
            tagger = FileTagger(item, path)

        tagger._tag()

    def _get_tags(self) -> "Iterable":
        yield from super()._get_tags()
        yield self.get_tag_ass("modified", db.TagType.FLOAT, os.path.getmtime(self.path))

class ImageTagger(FileTagger):
    def __init__(self, item: "db.Item", path: str):
        super().__init__(item, path)
        self.tagger_name += ":image"

    def _get_tags(self) -> "Iterable":
        yield from super()._get_tags()

        from PIL import Image
        im = Image.open(self.path)

        # size tags
        yield self.get_tag_ass("width", db.TagType.INT, im.width)
        yield self.get_tag_ass("height", db.TagType.INT, im.height)
