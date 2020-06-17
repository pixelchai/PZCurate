import enum
import os
import random

from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import event
from sqlalchemy.engine import Engine
from sqlite3 import Connection as SQLite3Connection
import lang

Base = declarative_base()
VERSION = 0

class InternalMeta(Base):
    __tablename__ = "InternalMeta"
    id = Column(Integer, primary_key=True, autoincrement=True)
    version = Column(Integer, default=VERSION)

class Library(Base):
    __tablename__ = "Libraries"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, default="unnamed")
    # path, etc

class TagType(enum.Enum):
    LABEL = 0
    STR = 1
    INT = 2
    FLOAT = 3

class TagDef(Base):
    __tablename__ = "TagDefs"
    id = Column(Integer, primary_key=True, autoincrement=True)
    library_id = Column(Integer, ForeignKey("Libraries.id", ondelete="CASCADE"))
    name = Column(String, default="unnamed")
    tag_type = Column(Enum(TagType))
    assignments = relationship("TagAss")

class TagAss(Base):
    __tablename__ = "TagAsses"
    id = Column(Integer, primary_key=True, autoincrement=True)
    library_id = Column(Integer, ForeignKey("Libraries.id", ondelete="CASCADE"))
    def_id = Column(Integer, ForeignKey("TagDefs.id", ondelete="CASCADE"))
    item_id = Column(Integer, ForeignKey("Items.id", ondelete="CASCADE"))
    value = Column(String)
    source = Column(String, default="user")
    item = relationship("Item")

class Item(Base):
    __tablename__ = "Items"
    id = Column(Integer, primary_key=True, autoincrement=True)
    library_id = Column(Integer, ForeignKey("Libraries.id", ondelete="CASCADE"))
    path = Column(String, nullable=False, unique=True)
    timestamp = Column(Float)
    file_timestamp = Column(Float)
    source = Column(String, default="user")

@event.listens_for(Engine, "connect")
def _set_sqlite_pragma(dbapi_connection, connection_record):
    # https://stackoverflow.com/a/15542046/5013267
    if isinstance(dbapi_connection, SQLite3Connection):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON;")
        cursor.close()

if __name__ == '__main__':
    Session = sessionmaker()

    database_path = "data.db"
    database_existed = os.path.isfile(database_path)
    engine = create_engine('sqlite:///' + database_path, echo=True)

    Session.configure(bind=engine)
    session = Session()

    if not database_existed:
        Base.metadata.create_all(engine)
        session.merge(InternalMeta(id=1))
    else:
        from migrator import migrate
        migrate(session)

    session.commit()

    if False:
        # test objects set up
        l = Library()
        session.add(l)
        session.flush()

        # items
        for i in range(20):
            item = Item(library_id=l.id, path="bruh_{:03d}".format(i))
            session.add(item)
            session.flush()

        # TagDefs
        d = TagDef(library_id=l.id, name="art", tag_type=TagType.LABEL)
        session.add(d)

        d = TagDef(library_id=l.id, name="genre", tag_type=TagType.STR)
        session.add(d)

        d = TagDef(library_id=l.id, name="rating", tag_type=TagType.INT)
        session.add(d)

        d = TagDef(library_id=l.id, name="ratio", tag_type=TagType.FLOAT)
        session.add(d)
        session.flush()

        # TagAsses
        # ratings
        ratings = [1, 2, 3, 4, 5]*(20//5)
        for i, val in enumerate(ratings):
            a = TagAss(library_id=l.id, def_id=3, item_id=i+1, value=str(val))
            session.add(a)
        session.flush()

        # arts
        sel = list(range(1, 20+1))
        random.shuffle(sel)
        for i in sel[:8]:
            a = TagAss(library_id=1, def_id=1, item_id=i)
            session.add(a)
        session.flush()

        # ratios
        random.shuffle(sel)
        for i in sel[:5]:
            a = TagAss(library_id=1, def_id=4, item_id=i, value=str(random.random()))
            session.add(a)
        session.flush()

        genres = ["rock", "block", "jazz", "blues", "wow"]
        random.shuffle(sel)
        for i in sel[:10]:
            a = TagAss(library_id=1, def_id=2, item_id=i, value=random.choice(genres))
            session.add(a)
        session.commit()



    q = lang.Querier(session, 1).query("")
    print(str(q))
