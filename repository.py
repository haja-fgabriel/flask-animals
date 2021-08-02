from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, LargeBinary
from sqlalchemy.sql.schema import ForeignKey


engine = create_engine("sqlite:///app.db", echo=True)
Base = declarative_base()
Session = sessionmaker(engine)


class Animal(Base):
    __tablename__ = "animals"

    animal_id = Column("animal_id", Integer, primary_key=True)
    name = Column("name", String, unique=True)
    kind = Column("kind", String)
    user = Column("user", String)
    image = Column("image", Integer, ForeignKey("images.image_id"))


class AnimalRepository:
    def get_all_for_username(username):
        """
        Retrieves all animals fetched for the given username.
        """
        with Session.begin() as session:
            animals = [*session.query(Animal).filter_by(user=username).all()]
            session.expunge_all()
            return animals

    def get_all_images_for_username(username):
        with Session.begin() as session:
            image_ids = [row[0] for row in session.query(Animal.image).filter_by(user=username).all()]
            return image_ids

    def remove_all_for_username(username):
        """
        Removes all animals for the username.
        """
        with Session.begin() as session:
            session.query(Animal).filter_by(user=username).delete(synchronize_session="fetch")

    def get(animal_id):
        """
        Get animal by its given identifier.
        """
        with Session.begin() as session:
            animal = session.query(Animal).filter_by(animal_id=animal_id).first()
            session.expunge_all()
            return animal

    def add(animal):
        """
        Add an animal.
        """
        with Session.begin() as session:
            session.add(animal)

    def update(animal):
        """
        Updates the given animal.
        """
        with Session.begin() as session:
            session.query(Animal).filter_by(animal_id=animal.animal_id).update(
                {"name": animal.name, "image": animal.image}, synchronize_session="fetch"
            )


class Image(Base):
    __tablename__ = "images"

    image_id = Column("image_id", Integer, primary_key=True)
    data = Column("data", LargeBinary)
    hash = Column("hash", LargeBinary, unique=True)


class ImageRepository:
    def add(image):
        with Session.begin() as session:
            session.add(image)

    def get(image_id):
        with Session.begin() as session:
            image = session.query(Image).filter_by(image_id=image_id).first()
            session.expunge_all()
            return image

    def get_by_hash(hash):
        with Session.begin() as session:
            image = session.query(Image).filter_by(hash=hash).first()
            session.expunge_all()
            return image

    def remove(image_id):
        with Session.begin() as session:
            session.query(Image).filter_by(image_id=image_id).delete(synchronize_session="fetch")


class User(Base):
    __tablename__ = "users"

    username = Column("username", String, primary_key=True)
    animal_type = Column("animal_type", String(10))


class UserRepository:
    def add(user):
        """
        Adds an User instance to the users dictionary.
        """
        with Session.begin() as session:
            session.add(user)

    def get(username):
        with Session.begin() as session:
            user = session.query(User).filter_by(username=username).first()
            session.expunge_all()
            return user


Base.metadata.create_all(bind=engine)
