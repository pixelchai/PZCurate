import os
from sqlalchemy import create_engine, Column, Integer, String, Float, Enum, ForeignKey, Table, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

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

class TagDef(Base):
    __tablename__ = "TagDefs"
    id = Column(Integer, primary_key=True, autoincrement=True)
    library_id = Column(Integer, ForeignKey("Libraries.id", ondelete="CASCADE"))
    name = Column(String, default="unnamed")
    constraints = Column(JSON)
    items = relationship("TagAss")

class TagAss(Base):
    __tablename__ = "TagAsses"
    id = Column(Integer, primary_key=True, autoincrement=True)
    library_id = Column(Integer, ForeignKey("Libraries.id", ondelete="CASCADE"))
    def_id = Column(Integer, ForeignKey("TagDefs.id", ondelete="CASCADE"))
    item_id = Column(Integer, ForeignKey("Items.id", ondelete="CASCADE"))
    value = Column(String)
    item = relationship("Item")

class Item(Base):
    __tablename__ = "Items"
    id = Column(Integer, primary_key=True, autoincrement=True)
    library_id = Column(Integer, ForeignKey("Libraries.id", ondelete="CASCADE"))
    name = Column(String, default="unnamed")
    path = Column(String, nullable=False)
    timestamp = Column(Float)
    file_timestamp = Column(Float)

if __name__ == '__main__':
    Session = sessionmaker()

    database_path = "data.db"
    database_existed = os.path.isfile(database_path)
    engine = create_engine('sqlite:///' + database_path, echo=True)
    engine.execute("PRAGMA foreign_keys=ON")

    Session.configure(bind=engine)
    session = Session()

    if not database_existed:
        Base.metadata.create_all(engine)
        session.merge(InternalMeta(id=1))
    else:
        from migrator import migrate
        migrate(session)

    session.commit()
