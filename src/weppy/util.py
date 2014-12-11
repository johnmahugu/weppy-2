import random

def random_string(length=64, allowed_chars='abcdefghijklmnopqrstuvwxyz'
                  'ABCDEFGHIJKLMNOPQRSTUVWXYZ'):
    """
    Returns a random string with the specified length and the allowed
    characters.

    length -- int that specifies the length of the random string. 64 by default.
    allowed_chars -- str that specifies the allowed chars for the random string.
    """
    return ''.join([random.choice(allowed_chars) for i in range(length)])
