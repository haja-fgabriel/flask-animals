users = {}

class User:
    def __init__(self, username, animal_type):
        self.__username = username
        self.__animal = animal_type

    def get_username(self):             return self.__username
    def set_username(self, username):   self.__username = username

    def get_animal_type(self):          return self.__animal
    def set_animal_type(self, animal):  self.__animal = animal
    
    username = property(get_username, set_username)
    animal_type = property(get_animal_type, set_animal_type)

def add(user):
    """
    Adds an User instance to the users dictionary.
    """
    global users
    users[user.username] = user

def get(username):
    global users
    return users.get(username)