import requests
import json
import os
from time import sleep
from pathlib import Path

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
    with open('pokelist.json', 'r') as f:
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

def repair_pokemon(p_list):
    for pokemon in p_list:
        name = pokemon['name']

        file_path = Path(f'pokemon/{name}.json')
        species_path = Path(f'pokemon/species/{name}.json')
        
        if file_path.is_file():
            print(f'{name} already exists')
            continue
        else:
            try:
                r = requests.get(f'https://pokeapi.co/api/v2/pokemon/{name}')
                poke_dict = r.json()

                with open(file_path, 'w') as f:
                    json.dump(poke_dict, f, indent=4)

                print(f'imported {name}')
            except:
                print(f'failed to find {name}')

    for pokemon in p_list:
        name = pokemon['name']
        id = 0

        with open(f'pokemon/{name}.json', 'r') as f:
            j = json.load(f)
            id = j['id']

        file_path = Path(f'pokemon/{name}.json')
        species_path = Path(f'pokemon/species/{name}.json')

        if species_path.is_file():
            print(f'{name} already exists')
            continue
        else:
            try:
                r = requests.get(f'https://pokeapi.co/api/v2/pokemon-species/{name}')
                poke_dict = r.json()

                with open(species_path, 'w') as f:
                    json.dump(poke_dict, f, indent=4)

                print(f'imported {name}')
            except:
                print(f'failed to find {name}')
                try:
                    r = requests.get(f'https://pokeapi.co/api/v2/pokemon-species/{id}')
                    poke_dict = r.json()

                    with open(species_path, 'w') as f:
                        json.dump(poke_dict, f, indent=4)

                    print('imported via id')

                except:
                    break

if __name__ == "__main__":
    try:
        os.mkdir('pokemon')
    except:
        print('directory already exists')

    try:
        os.mkdir('items')
    except:
        print('directory already exists')

    try:
        os.mkdir('pokemon/species')
    except:
        print('directory already exists')

    create_list()

    repair_pokemon(get_list())
