from random import choice
import os

def random_headers():
    file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'agents.txt')

    with open(file_path, 'r') as file:
        headers = {"User-Agent": choice(file.readlines()).strip()}

    return headers


 