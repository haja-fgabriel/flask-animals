class Animal:
    def __init__(self, name, kind, user, image):
        self.name = name
        self.kind = kind
        self.user = user
        self.image = image

animals = {}

def get_all_for_username(username):
    """
    Retrieves all animals fetched for the given username.
    """
    global animals
    return [animal for name, animal in animals.items() if animal.user == username]

def remove_all_for_username(username):
    """
    Removes all animals for the username.
    """
    global animals
    for animal in get_all_for_username(username):
        animals.pop(animal.name)

def get_by_name(name):
    """
    Get animal by its given name.
    """
    global animals
    return animals.get(name)

def add(animal):
    """
    Add an animal.
    """
    global animals
    animals[animal.name] = animal