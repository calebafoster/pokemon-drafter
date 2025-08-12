import pygame
from pygame import Vector2 as vector

class Biker(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)

        self.images = []
        self.frame_index = 0
        self.import_assets()
        self.image = self.images[self.frame_index]
        self.rect = self.image.get_rect(topleft = pos)
        self.animation_speed = 7
        self.speed = 500
        self.target_x = self.rect.centerx

    def import_assets(self):
        for i in range(4):
            img = pygame.image.load(f'biker/{i}.png').convert_alpha()
            img = pygame.transform.scale_by(img, 0.5)
            self.images.append(img)

    def move(self, dt):
        difference = self.target_x - self.rect.centerx
        self.pos = vector(self.rect.center)
        if difference < 0:
            direction = -1
            self.speed = 400
            self.animation_speed = 5
        elif difference > 0:
            direction = 1
            self.speed = 600
            self.animation_speed = 9
        else:
            direction = 0
            self.speed = 500
            self.animation_speed = 7

        if difference != 0:
            self.pos.x += self.speed * direction * dt
            self.rect.centerx = round(self.pos.x)

    def animate(self, dt):

        self.frame_index += self.animation_speed * dt
        if self.frame_index >= len(self.images):
            self.frame_index = 0
        
        self.image = self.images[int(self.frame_index)]

    def update(self, dt):
        self.animate(dt)
        self.move(dt)
