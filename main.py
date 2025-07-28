import pygame
import sys
from pokemon import Pokemon
from biker import Biker
import random
import json
from pygame.math import Vector2 as vector

class Backgrounds(pygame.sprite.Group):
    def __init__(self):
        super().__init__()

    def change_image(self, path):
        for sprite in self.sprites():
            sprite.change_image(path)

class Background(pygame.sprite.Sprite):
    def __init__(self, path, pos, groups):
        super().__init__(groups)
        self.image = pygame.image.load(path)
        self.rect = self.image.get_rect(topleft = pos)

        self.default_pos = vector(self.rect.topleft)

        self.pos = vector(self.rect.topleft)
        self.speed = 100

    def move(self, dt):
        if self.pos.x < self.default_pos.x - self.image.get_width():
            self.pos.x = self.default_pos.x
        self.pos.x += -1 * self.speed * dt
        self.rect.x = round(self.pos.x)

    def change_image(self, path):
        self.image = pygame.image.load(path)

    def update(self, dt):
        self.move(dt)


class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((1280, 720))
        pygame.display.set_caption('Pokemon Drafter')
        self.clock = pygame.time.Clock()

        with open('pokelist.json', 'r') as f:
            self.pokelist = json.load(f)

        self.random = random.randint(1,len(self.pokelist) + 1)
        self.pick = self.pokelist[self.random]

        self.backgrounds = Backgrounds()

        self.background = Background('wallpaper.jpg', (1280, 0), self.backgrounds)
        self.background2 = Background('wallpaper.jpg', (1280 - self.background.image.get_width(), 0), self.backgrounds)

        self.pokemon = Pokemon('grovyle', (0,0))
        self.biker = Biker((100,360), self.backgrounds)

    def run(self):
        while True:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            dt = self.clock.tick() / 1000

            self.backgrounds.update(dt)

            self.backgrounds.draw(self.display_surface)
            self.display_surface.blit(self.pokemon.image, self.pokemon.rect.topleft)

            pygame.display.update()

if __name__ == "__main__":
    game = Game()
    game.run()
