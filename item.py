import pygame
from pathlib import Path

## Notes for handling
## Logic for Item use will live here and the handler (Bag)
## Logic for holding items will live with the pokemon and the handler

class Item(pygame.sprite.Sprite):
    def __init__(self, item_dict, pos = (0,0)):
        super().__init__()

        self.name = item_dict['name']
        self.path = Path(item_dict['img'])

        self.import_assets()
        self.rect = self.images[0].get_rect(topleft = pos)

        self.held_by = None

        self.is_hidden = False

    def import_assets(self):
        self.images = []
        self.images.append(pygame.image.load(self.path).convert_alpha())
        self.images.append(pygame.image.load('images/items/poke-ball.png').convert_alpha())

    def hidden_logic(self):
        self.image = self.images[self.is_hidden]

    def update(self):
        self.hidden_logic()


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

    def hidden_logic(self):
        self.image = self.images[0]


class OptionExpander(Item):
    def __init__(self, item_dict):
        super().__init__(item_dict)

        self.name = item_dict['more_info']['alias']

    def on_pickup(self, item_effected_vars):
        item_effected_vars['choice_num'] += 1
        self.kill()
