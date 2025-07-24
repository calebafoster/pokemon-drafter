import pygame
import sys
import pokemon
import random
import json

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

        self.pokemon = pokemon.Pokemon(self.pick['name'])

    def run(self):
        while True:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.display_surface.fill('black')
            self.display_surface.blit(self.pokemon.image, self.pokemon.rect.topleft)

            pygame.display.update()

if __name__ == "__main__":
    game = Game()
    game.run()
