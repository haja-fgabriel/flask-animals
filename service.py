import ipdb

users = {}
animals = {}

class User:
    def __init__(self, username, animal_type):
        self.__username = username
        self.__animal = animal_type

    def get_username(self): return self.__username
    def set_username(self, username): self.__username = username

    def get_animal_type(self): return self.__animal
    def set_animal_type(self, animal): self.__animal = animal
    
    username = property(get_username, set_username)
    animal_type = property(get_animal_type, set_animal_type)


def confirm(username, animal_type):
    global users
    ipdb.set_trace()
    if users.get(username):
        raise Exception('The user is already confirmed. Please pick another username.')
    users[username] = User(username, animal_type)

def fetch_data():
    pass