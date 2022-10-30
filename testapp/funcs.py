from random import randint

def create_random_chars(nbr_of_chars):
    return "".join(chr(randint(97,122)) for i in range(nbr_of_chars))