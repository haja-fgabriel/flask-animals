from domain import Animal, User, Image, Base
from database import Session, create_tables

create_tables(Base)


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
