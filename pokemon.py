import pygame
import json

class Pokemon(pygame.sprite.Sprite):
    def __init__(self, name, nickname = ''):
        super().__init__()

        self.name = name
        self.nickname = nickname
        with open(f'pokemon/{self.name}.json', 'r') as f:
            self.poke_dict = json.load(f)

if __name__ == '__main__':
    pikachoo = Pokemon('chikorita')
    print(pikachoo.poke_dict['id'])
