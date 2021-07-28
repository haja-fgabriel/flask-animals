from asyncio import futures
import random
import ipdb
import animal_api
import utils
import animal_repository
import user_repository
import logging
import asyncio
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from names import names

def confirm(username, animal_type):
    if not user_repository.get(username):
        user_repository.add(user_repository.User(username, animal_type))

def get_user(username):
    return user_repository.get(username)

def fetch_data(username, count=200):
    user = user_repository.get(username)
    animal_repository.remove_all_for_username(username)

    def random_animal():
        image = animal_api.fetch_method[user.animal_type]()
        animal_id = utils.random_string()
        name = random.choice(names)
        return animal_repository.Animal(animal_id, name, user.animal_type, username, image)

    # insane measures to boost performance
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(random_animal) for i in range(count)]
        for future in as_completed(futures):
            animal_repository.add(future.result())


def get_animal(animal_id):
    return animal_repository.get(animal_id)

def get_animals_for_username(username):
    return animal_repository.get_all_for_username(username)

def get_animals_by_name(username, animal_name, page):
    """
    Returns a list containing all the animals that match the given name.
    """
    records = [animal for animal in animal_repository.get_all_for_username(username) if re.match(animal_name.lower(), animal.name.lower())]
    first = 10*(page-1)
    last = min(first+10, len(records))
    return records[first:last]

def count_animals_by_name(username, animal_name):
    return len([animal for animal in animal_repository.get_all_for_username(username) if re.match(animal_name.lower(), animal.name.lower())])
