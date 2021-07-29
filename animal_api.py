import requests
import json
import random
import math

def fetch_cat():
    response = requests.get('https://cataas.com/cat/says/bws%20rocks?size=480')
    return response.content

def fetch_dog():
    def fetch_from_place_dog():
        randH = random.randint(64, 480)
        randW = random.randint(64, 480)
        response = requests.get(f'https://place.dog/{randW}/{randH}')
        return response.content
    
    def fetch_from_dog_ceo():
        response = requests.get(f'https://dog.ceo/api/breeds/image/random')
        info = json.loads(response.text)
        img_response = requests.get(info.get('message'))
        return img_response.content
    
    def fetch_from_shibe_online():
        response = requests.get('http://shibe.online/api/shibes')
        info = json.loads(response.text)
        img_response = requests.get(info[0])
        return img_response.content

    return random.choice([
        #fetch_from_dog_ceo,
        #fetch_from_shibe_online,
        fetch_from_place_dog
    ])()


def fetch_bear():
    # generate random height and width, because the API contains a single image for each resolution
    # we also want values in the [64, 480] interval
    randH = random.randint(64, 480)
    randW = random.randint(64, 480)
    response = requests.get(f'https://placebear.com/{randW}/{randH}')
    return response.content

def fetch_fox():
    response = requests.get('https://randomfox.ca/floof')
    info = json.loads(response.content)
    img_response = requests.get(info.get('image'))
    return img_response.content

fetch_method = {
    'bear': fetch_bear,
    'cat':  fetch_cat,
    'dog':  fetch_dog,
    'fox':  fetch_fox,
}