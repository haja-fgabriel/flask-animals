import random
import string
import math

def random_string():
    """
    Generate a random string having a length between 3 and 45.
    """
    length = random.randint(3, 32)
    return ''.join(random.choice(string.ascii_letters) for i in range(length))
