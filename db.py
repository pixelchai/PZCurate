import os
from sqlalchemy import create_engine, Column, Integer, String, Float, Enum, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
VERSION = 2

class InternalMeta(Base):
    __tablename__ = "InternalMeta"
    id = Column(Integer, primary_key=True)
    version = Column(Integer, default=VERSION)

class Tag(Base):
    __tablename__ = "Tags"
    id = Column(Integer, primary_key=True)
    name = Column(String, default="unnamed")

class Item(Base):
    __tablename__ = "Items"
    id = Column(Integer, primary_key=True)
    name = Column(String, default="unnamed")
    path = Column(String, nullable=False)
    timestamp = Column(Float)

if __name__ == '__main__':
    Session = sessionmaker()

    database_path = "data.db"
    engine = create_engine('sqlite:///' + database_path, echo=True)

    Session.configure(bind=engine)
    session = Session()

    if not os.path.isfile(database_path):
        Base.metadata.create_all(engine)
        session.merge(InternalMeta(id=1))
    else:
        from migrator import migrate
        migrate(session)

    session.commit()
