import pygame
import sys
import pokemon
import random
import json
from pygame.math import Vector2 as vector

class Background(pygame.sprite.Sprite):
    def __init__(self, path, pos):
        self.image = pygame.image.load(path)
        self.rect = self.image.get_rect(topleft = pos)

        self.default_pos = vector(self.rect.topleft)

        self.pos = vector(self.rect.topleft)
        self.speed = 200

    def move(self, dt):
        if self.pos.x < self.default_pos.x - self.image.get_width():
            self.pos.x = self.default_pos.x
        self.pos.x += -1 * self.speed * dt
        self.rect.x = round(self.pos.x)

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

        self.random = random.randint(0,len(self.pokelist))
        self.pick = self.pokelist[self.random]
        self.background = Background('wallpaper.jpg', (1280, 0))
        self.background2 = Background('wallpaper.jpg', (1280 - self.background.image.get_width(), 0))

        self.pokemon = pokemon.Pokemon(self.pick['name'])

    def run(self):
        while True:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            dt = self.clock.tick() / 1000

            self.background.update(dt)
            self.background2.update(dt)

            self.display_surface.fill('aqua')
            self.display_surface.blit(self.background.image, self.background.rect.topleft)
            self.display_surface.blit(self.background2.image, self.background2.rect.topleft)
            self.display_surface.blit(self.pokemon.image, self.pokemon.rect.topleft)

            pygame.display.update()

if __name__ == "__main__":
    game = Game()
    game.run()
