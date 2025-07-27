import pygame
import sys
from pokemon import Pokemon
from biker import Biker
import random
import json
from background import Background, Backgrounds
from pygame.math import Vector2 as vector

class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((1280, 720))
        pygame.display.set_caption('Pokemon Drafter')
        self.clock = pygame.time.Clock()

        with open('pokelist.json', 'r') as f:
            self.pokelist = json.load(f)

        self.backgrounds = Backgrounds()

        self.background = Background('wallpaper.jpg', (1280, 0), self.backgrounds)
        self.background2 = Background('wallpaper.jpg', (1280 - self.background.image.get_width(), 0), self.backgrounds)
        self.choices = pygame.sprite.Group()

        self.pokemon = Pokemon('miraidon', (0,0))
        self.biker = Biker((100,360), self.backgrounds)

        self.state = 'pokemon_picker'

        self.create_choices(Pokemon, 4, self.pokelist)
        self.arrange_choices()

    def create_choices(self, Product, num, lis):
        self.choices.empty()

        for i in range(num):
            rand = random.randint(0, len(lis) - 1)
            current = lis[rand]
            name = current['name']
            self.choices.add(Product(name, (0,0)))

    def arrange_choices(self):
        current_pos = vector(0,0)
        right_x = 0
        iteration = 1280 / len(self.choices)

        for opt in self.choices.sprites():
            opt.rect.topleft = current_pos
            current_pos.x += iteration
            right_x = opt.rect.right

        offset = (1280 - right_x) / 2

        for opt in self.choices.sprites():
            opt.rect.x += offset

    def run(self):
        while True:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            dt = self.clock.tick() / 1000

            self.backgrounds.update(dt)

            self.backgrounds.draw(self.display_surface)
            self.choices.draw(self.display_surface)

            pygame.display.update()

if __name__ == "__main__":
    game = Game()
    game.run()
