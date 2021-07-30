from asyncio import futures
import random
import ipdb
import animal_api
import repository
import utils
import logging
import asyncio
import re
import hashlib
from repository import AnimalRepository, UserRepository, ImageRepository
from repository import Animal, User, Image
from concurrent.futures import ThreadPoolExecutor, as_completed, wait
from names import names
from dtos import ImageDTO, AnimalDTO

def confirm(username, animal_type):
    if not UserRepository.get(username):
        UserRepository.add(User(username=username, animal_type=animal_type))

def get_user(username):
    return UserRepository.get(username)

def fetch_data(username, count=200):
    user = UserRepository.get(username)
    print(AnimalRepository.get_all_images_for_username(username))
    try:
        for image in AnimalRepository.get_all_images_for_username(username):
            if image: ImageRepository.remove(image)
        AnimalRepository.remove_all_for_username(username)
    except Exception as e:
        print(e)

    def random_image():
        data = animal_api.fetch_method[user.animal_type]()
        hash = hashlib.sha256(data).digest()
        return ImageDTO(data, hash)

    def random_animal():
        name = random.choice(names)
        return AnimalDTO(name, user.animal_type, username)
    
    image_ids = []
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(random_image) for i in range(count)] + \
            [executor.submit(random_animal) for i in range(count)]
        all_fetched = False
        while not all_fetched:
            all_fetched = True
            done, not_done = wait(futures, timeout=0.45)
            if len(not_done): all_fetched = False
            new_futures = []
            for future in done:
                data = future.result()
                if type(data) is ImageDTO:
                    try: 
                        print(data.data[0:60])
                        ImageRepository.add(Image(data=data.data, hash=data.hash))
                        image = ImageRepository.get_by_hash(data.hash)
                        image_ids.append(image.image_id)
                    except Exception as e: 
                        print(e)
                        new_futures.append(executor.submit(random_image))
                elif type(data) is AnimalDTO:
                    try:
                        AnimalRepository.add(Animal(name=data.name, kind=data.kind, user=data.user))
                    except Exception as e: 
                        print(e)
                        new_futures.append(executor.submit(random_animal))
            futures = [*not_done] + new_futures

    try:
        animals = get_animals_for_username(username)
        # Lazily add the newly fetched images to each animal
        for animal, image_id in zip(animals, image_ids):
            pass
            animal.image = image_id
            AnimalRepository.update(animal)
    except Exception as e:
        print(e)

def get_image(image_id):
    return ImageRepository.get(image_id)


# TODO move these methods to animal_service.py

def update_animal(username, animal_id, name):
    animal = AnimalRepository.get(animal_id)
    if animal.user != username:
        raise Exception('The given animal does not belong to the logged username!')
    if len(name) < 3 or len(name) > 45:
        raise Exception('The given name must have the length between 3 and 45!')
    animal.name = name
    AnimalRepository.update(animal)

def get_animal(animal_id):
    return AnimalRepository.get(animal_id)

def get_animals_for_username(username):
    return AnimalRepository.get_all_for_username(username)

def get_animals_by_name(username, animal_name, page):
    """
    Returns a list containing all the animals that match the given name.
    """
    # TODO please fetch just the needed elements
    records = [animal for animal in AnimalRepository.get_all_for_username(username) if re.match(animal_name.lower(), animal.name.lower())]
    first = 10*(page-1)
    last = min(first+10, len(records))
    return records[first:last]

def count_animals_by_name(username, animal_name):
    return len([animal for animal in AnimalRepository.get_all_for_username(username) if re.match(animal_name.lower(), animal.name.lower())])

def add_image(data):
    ImageRepository.add(Image(data=data))