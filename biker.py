import pygame

class Biker(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)

        self.images = []
        self.frame_index = 0
        self.import_assets()
        self.image = self.images[self.frame_index]
        self.rect = self.image.get_rect(topleft = pos)

    def import_assets(self):
        for i in range(4):
            img = pygame.image.load(f'biker/{i}.png').convert_alpha()
            img = pygame.transform.scale_by(img, 0.5)
            self.images.append(img)

    def animate(self, dt):

        self.frame_index += 7 * dt
        if self.frame_index >= len(self.images):
            self.frame_index = 0
        
        self.image = self.images[int(self.frame_index)]

    def update(self, dt):
        self.animate(dt)
