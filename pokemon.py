import pygame
import json
from pathlib import Path
from pygame import Vector2 as vector
import requests
import random

class Pokemon(pygame.sprite.Sprite):
    def __init__(self, name, pos, nickname = ''):
        super().__init__()

        self.name = name
        self.nickname = nickname

        print(self.name)
        
        self.import_assets()
        self.image = pygame.transform.scale_by(self.image, 2)
        self.rect = self.image.get_rect(topleft = pos)

        self.pos = vector(self.rect.topleft)

        self.types = []
        self.bst = 0
        self.stage = 0
        self.can_evolve = False

        self.move_list = self.poke_dict['moves']
        self.ability_list = self.poke_dict['abilities']

        self.ability = ''

        self.get_types()
        self.get_bst()
        self.set_ability()

        self.moves = []

        print(f'ability = {self.ability}')

    def set_ability(self):
        index = random.randint(0, len(self.ability_list)) - 1
        self.ability = self.ability_list[index]

    def get_types(self):
        for poke_type in self.poke_dict['types']:
            self.types.append(poke_type['type']['name'])

    def get_bst(self):
        count = 0

        for stat in self.poke_dict['stats']:
            count += stat['base_stat']

        self.bst = count

    def import_assets(self):
        with open(f'pokemon/{self.name}.json', 'r') as f:
            self.poke_dict = json.load(f)

        self.image_path = Path(f'images/{self.name}.png')

        if self.image_path.is_file():
            self.image = pygame.image.load(self.image_path).convert_alpha()
        else:
            self.download_image()

    def download_image(self):
        image_url = self.poke_dict['sprites']['front_default']
        r = requests.get(image_url)

        if r.status_code == 200:
            with open(self.image_path, 'wb') as f:
                f.write(r.content)
            print(f'image download successful: {self.name}')
        else:
            self.image_path = Path('images/missing.png')
            print('image download unsuccesful, replacing with missingno')

        self.image = pygame.image.load(self.image_path).convert_alpha()

if __name__ == '__main__':
    pikachoo = Pokemon('chikorita', (0,0))
    print(pikachoo.poke_dict['id'])
