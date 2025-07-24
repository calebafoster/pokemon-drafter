import requests
import json
import os
from time import sleep

def create_list():
    r = requests.get('https://pokeapi.co/api/v2/pokemon/?limit=10000')
    my_dict = r.json()
    m = requests.get('https://pokeapi.co/api/v2/move/?limit=10000')
    move_dict = m.json()

    with open('pokelist.json', 'w') as f:
        json.dump(my_dict['results'], f, indent=4)

    with open('movelist.json', 'w') as f:
        json.dump(move_dict['results'], f, indent=4)

def get_list():
    with open('pokelist', 'r') as f:
        return json.load(f)

def do_the_pokemon(path, p_list):
    for pokemon in p_list:

        name = pokemon['name']
        r = requests.get(f'https://pokeapi.co/api/v2/pokemon/{name}')
        poke_dict = r.json()

        with open(f'{path}/{name}.json', 'w') as f:
            json.dump(poke_dict, f, indent=4)

        print(f'imported {name}')
        sleep(50 / 1000)

if __name__ == "__main__":
    try:
        os.mkdir('pokemon')
    except:
        print('directory already exists')

    create_list()

    do_the_pokemon('pokemon', get_list())
