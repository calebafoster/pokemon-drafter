import pygame
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
