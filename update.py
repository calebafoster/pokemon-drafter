import requests
import json
import os
from time import sleep
from pathlib import Path

def create_list():
    r = requests.get('https://pokeapi.co/api/v2/pokemon-species/?limit=10000')
    print(r)
    my_dict = r.json()
    m = requests.get('https://pokeapi.co/api/v2/move/?limit=10000')
    move_dict = m.json()

    with open('pokelist.json', 'w') as f:
        json.dump(my_dict['results'], f, indent=4)

    with open('movelist.json', 'w') as f:
        json.dump(move_dict['results'], f, indent=4)

def get_json(path):
    with open(path, 'r') as f:
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
        print(name)
        species_url = pokemon['url']

        file_path = Path(f'pokemon/{name}.json')
        species_path = Path(f'pokemon/species/{name}.json')

        if species_path.is_file() and file_path.is_file():
            print(f'{name} already exists')

        else:
            if not species_path.is_file():
                species_dict = requests.get(species_url).json()
                id = species_dict['id']
                mon = requests.get(f'https://pokeapi.co/api/v2/pokemon/{id}')
                poke_dict = mon.json()

                with open(species_path, 'w') as f:
                    json.dump(species_dict, f, indent=4)

                with open(file_path, 'w') as f:
                    json.dump(poke_dict, f, indent=4)

            else:
                species_dict = get_json(species_path)
                id = species_dict['id']
                mon = requests.get(f'https//pokeapi.co/api/v2/pokemon/{id}')
                poke_dict = mon.json()

                with open(file_path, 'w') as f:
                    json.dump(poke_dict, f, indent=4)

def get_evo_chains(p_list):
    
    for mon in p_list:
        name = mon['name']

        file_path = Path(f'pokemon/species/{name}.json')
        dest_path = Path(f'pokemon/evos/{name}.json')

        if not dest_path.is_file():


            mon_dict = {}

            with open(file_path, 'r') as f:
                mon_dict = json.load(f)

            chain_url = mon_dict['evolution_chain']['url']

            r = requests.get(chain_url)
            evo_chain = r.json()

            with open(dest_path, 'w') as f:
                json.dump(evo_chain, f, indent=4)

            print(f'{name} evo chain dumped')

        else:
            print('evo already exists')

            
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

    repair_pokemon(get_json('pokelist.json'))

    get_evo_chains(get_json('pokelist.json'))
