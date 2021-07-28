from asyncio import futures
import ipdb
import animal_api
import utils
import animal_repository
import user_repository
import logging
import asyncio
from concurrent.futures import ThreadPoolExecutor, as_completed

def confirm(username, animal_type):
    global users
    ipdb.set_trace()
    if user_repository.get(username):
        raise Exception('The user is already confirmed. Please pick another username.')
    user_repository.add(user_repository.User(username, animal_type))

def fetch_data(username):
    user = user_repository.get(username)

    # insane measures to boost performance
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(animal_api.fetch_method[user.animal_type]) for i in range(200)]
        for future in as_completed(futures):
            image = future.result()
            name = utils.random_name()
            animal = animal_repository.Animal(name, user.animal_type, user.username, image)
            animal_repository.add(animal)


def get_animal_by_name(name):
    # TODO check if user is valid
    return animal_repository.get_by_name(name)

def get_animals_for_username(username):
    return animal_repository.get_all_for_username(username)