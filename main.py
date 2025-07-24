import pygame
import sys
import pokemon

class Game:
    def __init__(self):
        _ = pygame.init()
        self.display_surface = pygame.display.set_mode((1280, 720))
        pygame.display.set_caption('Pokemon Drafter')
        self.clock = pygame.time.Clock()

        self.pokemon = pokemon.Pokemon('roaring-moon', 'pikachu')

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
