class Animal:
    def __init__(self, animal_id, name, kind, user, image):
        self.animal_id = animal_id
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
        if animals.get(animal.animal_id): animals.pop(animal.animal_id)

def get(animal_id):
    """
    Get animal by its given identifier.
    """
    global animals
    return animals.get(animal_id)

def add(animal):
    """
    Add an animal.
    """
    global animals
    animals[animal.animal_id] = animal