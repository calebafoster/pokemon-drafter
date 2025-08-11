import pygame

class Button(pygame.sprite.Sprite):
    def __init__(self, text, groups, pos = (0,0), size=35):
        super().__init__(groups)

        self.text = text

        self.font = pygame.font.Font('pixel-font.ttf', size)
        self.image = self.font.render(self.text, False, 'white')
        self.rect = self.image.get_rect(topleft = pos)

    def is_clicked(self):
        pos = pygame.mouse.get_pos()
        action = False

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] and not self.clicked:
                self.clicked = True
                action = True

        if not pygame.mouse.get_pressed()[0]:
            self.clicked = False

        return action
