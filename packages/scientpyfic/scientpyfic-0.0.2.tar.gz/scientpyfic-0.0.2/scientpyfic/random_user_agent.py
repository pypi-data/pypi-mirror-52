from random import choice
import os
import pkg_resources

def random_headers():
    user_agents = pkg_resources.resource_string(__name__, 'agents.txt') \
                               .decode('utf-8') \
                               .strip() \
                               .split('\n')
    headers = {"User-Agent": choice(user_agents).strip()}

    return headers


 