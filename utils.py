import random
import string
import math

def random_name():
    """
    Generate a random name having a length between 3 and 45.
    """
    length = random.randint(3, 45)
    return ''.join(random.choice(string.ascii_lowercase) for i in range(length))
