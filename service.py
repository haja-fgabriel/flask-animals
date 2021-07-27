users = {}

def login(username, animal):
    global users
    if users.get(username):
        raise Exception('The given username is already taken.')