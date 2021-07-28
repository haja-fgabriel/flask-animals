import requests
import json
import random
import math

def fetch_cat():
    response = requests.get('https://cataas.com/cat/says/bws%20rocks?size=640')
    return response.text

def fetch_dog():
    response = requests.get(f'https://place.dog/640/640')
    return response.text

def fetch_bear():
    # generate random height and width, because the API contains a single image for each resolution
    # we also want values in the [64, 640] interval
    randH = random.randint(64, 640)
    randW = random.randint(64, 640)
    response = requests.get(f'https://placebear.com/{randW}/{randH}')
    return response.text

def fetch_fox():
    response = requests.get('https://randomfox.ca/floof')
    info = json.loads(response.text)
    img_response = requests.get(info.image)
    return img_response.text

fetch_method = {
    'bear': fetch_bear,
    'cat':  fetch_cat,
    'dog':  fetch_dog,
    'fox':  fetch_fox,
}