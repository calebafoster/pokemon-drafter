import pygame
import json
from pathlib import Path
import requests

class Pokemon(pygame.sprite.Sprite):
    def __init__(self, name, nickname = ''):
        super().__init__()

        self.name = name
        self.nickname = nickname

        
        self.import_assets()
        self.rect = self.image.get_rect()
        self.rect.topleft = (0,0)

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
    pikachoo = Pokemon('chikorita')
    print(pikachoo.poke_dict['id'])
