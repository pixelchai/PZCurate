import os
from sqlalchemy import create_engine, Column, Integer, String, Float, Enum, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()
VERSION = 0

class InternalMeta(Base):
    __tablename__ = "InternalMeta"
    id = Column(Integer, primary_key=True)
    version = Column(Integer, default=VERSION)

# Item-Tag association table
item_tags = Table("ItemTagJoins", Base.metadata,
                  Column('item_id', Integer, ForeignKey('Items.id'), primary_key=True),
                  Column('tag_id', Integer, ForeignKey('Tags.id'), primary_key=True))

class Tag(Base):
    __tablename__ = "Tags"
    id = Column(Integer, primary_key=True)
    name = Column(String, default="unnamed")
    items = relationship("Item", secondary=item_tags, back_populates="tags")

class Item(Base):
    __tablename__ = "Items"
    id = Column(Integer, primary_key=True)
    name = Column(String, default="unnamed")
    path = Column(String, nullable=False)
    timestamp = Column(Float)
    file_timestamp = Column(Float)
    tags = relationship("Tag", secondary=item_tags, back_populates="items")

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
