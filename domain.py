from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, LargeBinary
from sqlalchemy.sql.schema import ForeignKey

Base = declarative_base()


class Animal(Base):
    __tablename__ = "animals"

    animal_id = Column("animal_id", Integer, primary_key=True)
    name = Column("name", String, unique=True)
    kind = Column("kind", String)
    user = Column("user", String)
    image = Column("image", Integer, ForeignKey("images.image_id"))


class Image(Base):
    __tablename__ = "images"

    image_id = Column("image_id", Integer, primary_key=True)
    data = Column("data", LargeBinary)
    hash = Column("hash", LargeBinary, unique=True)


class User(Base):
    __tablename__ = "users"

    username = Column("username", String, primary_key=True)
    animal_type = Column("animal_type", String(10))
