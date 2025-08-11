import pygame
from pathlib import Path

## Notes for handling
## Logic for Item use will live here and the handler (Bag)
## Logic for holding items will live with the pokemon and the handler

class Text(pygame.sprite.Sprite):
    def __init__(self, text, size=22):
        super().__init__()

        if '-' in text:
            self.text = text.split('-')
            self.text = ' '.join(self.text)
            self.text = self.text.upper()
        else:
            self.text = text.upper()

        self.font = pygame.font.Font('pixel-font.ttf', size)

        self.image = self.font.render(self.text, True, 'black')
        self.rect = self.image.get_rect()


class Item(pygame.sprite.Sprite):
    def __init__(self, item_dict, pos = (0,0)):
        super().__init__()

        self.name = item_dict['name']
        self.path = Path(item_dict['img'])
        self.cost = item_dict['cost']

        self.import_assets()
        self.rect = self.images[0].get_rect(topleft = pos)

        self.held_by = None

        self.is_hidden = False
        self.is_big = False

        self.text = Text(self.name)
        
        self.clicked = False

    def import_assets(self):
        self.images = []
        self.rects = []

        self.images.append(pygame.image.load(self.path).convert_alpha())
        self.rects.append(self.images[0].get_rect(topleft = (0,0)))

        self.images.append(pygame.image.load('images/items/poke-ball.png').convert_alpha())
        self.rects.append(self.images[1].get_rect(topleft = (0,0)))

        self.images.append(pygame.transform.scale_by(self.images[0], 3))
        self.rects.append(self.images[2].get_rect(topleft = (0,0)))

    def image_logic(self):
        self.image = self.images[self.is_hidden]
        if self.is_hidden:
            self.image = self.images[1]
            self.rect = self.rects[1]
        elif self.is_big:
            self.image = self.images[2]
            self.rect = self.rects[2]
        else:
            self.image = self.images[0]
            self.rect = self.rects[0]

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

    def is_right_clicked(self):
        pos = pygame.mouse.get_pos()
        action = False

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[2] and not self.right_clicked:
                self.right_clicked = True
                action = True

        if not pygame.mouse.get_pressed()[2]:
            self.right_clicked = False
            self.can_right_click = True

        return action

    def is_hovering(self):
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            return True

    def update(self):
        self.image_logic()


class HeldItem(Item):
    def __init__(self, item_dict):
        super().__init__(item_dict)


class Vitamin(Item):
    def __init__(self, item_dict):
        super().__init__(item_dict)

        self.stat = item_dict['more_info']['stat']


class EvoCandy(Item):
    def __init__(self, item_dict):
        super().__init__(item_dict)

        self.name = item_dict['more_info']['alias']
        self.text = Text(self.name)


class SellItem(Item):
    def __init__(self, item_dict):
        super().__init__(item_dict)

        self.value = item_dict['more_info']['value']

    def on_pickup(self, item_effected_vars):
        item_effected_vars['points'] += self.value
        self.kill()


class RevealGlass(Item):
    def __init__(self, item_dict):
        super().__init__(item_dict)

    def on_pickup(self, item_effected_vars):
        item_effected_vars['revealed'] = True
        self.kill()

    def hidden_logic(self):
        self.image = self.images[0]


class OptionExpander(Item):
    def __init__(self, item_dict):
        super().__init__(item_dict)

        self.name = item_dict['more_info']['alias']
        self.text = Text(self.name)

    def on_pickup(self, item_effected_vars):
        item_effected_vars['choice_num'] += 1
        self.kill()
