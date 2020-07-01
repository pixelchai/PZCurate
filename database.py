import enum
import os
import random
from typing import Optional, Any
from utils import logger
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, aliased
from sqlalchemy.sql.expression import and_, cast
from sqlalchemy import event
from sqlalchemy.engine import Engine
from sqlite3 import Connection as SQLite3Connection
import lang
import filesystem as fs

Base = declarative_base()
VERSION = 0

class InternalMeta(Base):
    __tablename__ = "InternalMeta"
    id = Column(Integer, primary_key=True, autoincrement=True)
    version = Column(Integer, default=VERSION)

class TagType(enum.Enum):
    LABEL = 0
    STR = 1
    INT = 2
    FLOAT = 3

class TagDef(Base):
    __tablename__ = "TagDefs"
    name = Column(String, default="unnamed", primary_key=True, unique=True)
    tag_type: TagType = Column(Enum(TagType))
    source = Column(String, default="user")
    assignments = relationship("TagAss")

class TagAss(Base):
    __tablename__ = "TagAsses"
    id = Column(Integer, primary_key=True, autoincrement=True)
    def_name = Column(String, ForeignKey("TagDefs.name", ondelete="CASCADE"))
    item_id = Column(Integer, ForeignKey("Items.id", ondelete="CASCADE"))
    value = Column(String)
    source = Column(String, default="user")
    item = relationship("Item")

class Item(Base):
    __tablename__ = "Items"
    id = Column(Integer, primary_key=True, autoincrement=True)
    path = Column(String, nullable=False, unique=True)

@event.listens_for(Engine, "connect")
def _set_sqlite_pragma(dbapi_connection, connection_record):
    # https://stackoverflow.com/a/15542046/5013267
    if isinstance(dbapi_connection, SQLite3Connection):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON;")
        cursor.close()

Session = sessionmaker()
engine = None
session: Any = None

def _def_system_tags():
    session.add(TagDef(name="timestamp", tag_type=TagType.FLOAT, source="system"))
    session.add(TagDef(name="media", tag_type=TagType.STR, source="system"))
    session.commit()

def _setup_session():
    global engine
    global session

    database_existed = os.path.isfile(fs.PATH_DATABASE)
    engine = create_engine('sqlite:///' + fs.PATH_DATABASE, echo=False)

    Session.configure(bind=engine)
    session = Session()

    if not database_existed:
        Base.metadata.create_all(engine)
        session.merge(InternalMeta(id=1))
        _def_system_tags()
        logger.info("Database did not exist. Created new one.")
    else:
        from migrator import migrate
        migrate(session)

    session.commit()

# set up session (will be globally accessible through `session`)
_setup_session()

if __name__ == '__main__':
    if False:
        # items
        for i in range(20):
            item = Item(path="bruh_{:03d}".format(i))
            session.add(item)
            session.flush()

        # TagDefs
        d = TagDef(name="art", tag_type=TagType.LABEL)
        session.add(d)

        d = TagDef(name="genre", tag_type=TagType.STR)
        session.add(d)

        d = TagDef(name="rating", tag_type=TagType.INT)
        session.add(d)

        d = TagDef(name="ratio", tag_type=TagType.FLOAT)
        session.add(d)
        session.flush()

        # TagAsses
        # ratings
        ratings = [1, 2, 3, 4, 5]*(20//5)
        for i, val in enumerate(ratings):
            a = TagAss(def_name="rating", item_id=i+1, value=str(val))
            session.add(a)
        session.flush()

        # arts
        sel = list(range(1, 20+1))
        random.shuffle(sel)
        for i in sel[:8]:
            a = TagAss(def_name="art", item_id=i)
            session.add(a)
        session.flush()

        # ratios
        random.shuffle(sel)
        for i in sel[:5]:
            a = TagAss(def_name="ratio", item_id=i, value=str(random.random()))
            session.add(a)
        session.flush()

        genres = ["rock", "block", "jazz", "blues", "wow"]
        random.shuffle(sel)
        for i in sel[:10]:
            a = TagAss(def_name="genre", item_id=i, value=random.choice(genres))
            session.add(a)
        session.commit()
