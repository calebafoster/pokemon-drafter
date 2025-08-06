import pygame
import sys
from pokemon import Pokemon
from biker import Biker
import random
import json
from background import Background, Backgrounds
from pygame.math import Vector2 as vector
from item import *

class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((1280, 720))
        pygame.display.set_caption('Pokemon Drafter')
        self.clock = pygame.time.Clock()

        with open('pokelist.json', 'r') as f:
            self.pokelist = json.load(f)
        with open('item-list.json', 'r') as f:
            self.item_list = json.load(f)

        self.backgrounds = Backgrounds()

        self.background = Background('wallpaper.jpg', (1280, 0), self.backgrounds)
        self.background2 = Background('wallpaper.jpg', (1280 - self.background.image.get_width(), 0), self.backgrounds)
        self.pokemon_choices = pygame.sprite.Group()
        self.item_choices = pygame.sprite.Group()
        self.bag = pygame.sprite.Group()
        self.box = pygame.sprite.Group()

        self.biker = Biker((100,360), self.backgrounds)

        self.state = 'main_menu'

        self.can_choose = False

        self.choice_num = 4
        self.points = 1500
        self.items_revealed = True

        self.item_effected_vars = {"choice_num": self.choice_num, 
                                   "points": self.points, 
                                   "revealed": self.items_revealed}

    def dex_sanity(self):
        for i, poke in enumerate(self.pokelist):
            name = poke['name']
            current = None
            id_num = 0

            with open(f'pokemon/{name}.json', 'r') as f:
                current = json.load(f)
                id_num = current['id']

            if id_num >= 10000:
                self.dex_num = i - 1
                break

    def display_text(self):
        for sprite in self.pokemon_choices:
            sprite.display_text(self.display_surface)

    def item_smuggling(self):
        for mon in self.pokemon_choices:
            chance = mon.item_chance()
            if random.random() < chance:
                index = random.randint(1, len(self.item_list) - 1)
                new_item = eval(self.item_list[index]['class'])(self.item_list[index])
                new_item.is_hidden = not self.items_revealed
                mon.hold_item(new_item)

    def pokemon_draft(self, dt):
        if not self.pokemon_choices:
            self.create_choices(Pokemon, self.choice_num, self.pokelist)
            self.arrange_choices()
            self.item_smuggling()

        self.pokemon_choices.update(dt)
        self.pokemon_choices.draw(self.display_surface)

        for sprite in self.pokemon_choices:

            self.display_text()

            if sprite.is_clicked() and self.can_choose:
                self.can_choose = False

                if sprite.held_item:
                    self.acquire_item(sprite.held_item)
                    sprite.held_item = None

                self.box.add(sprite)

                for mon in self.box.sprites():
                    print(mon.name)

                self.pokemon_choices.empty()

    def items_draft(self):
        pass

    def acquire_item(self, item):
        if hasattr(item, 'on_pickup'):
            item.on_pickup(self.item_effected_vars)
            print(self.item_effected_vars)
            self.choice_num = self.item_effected_vars['choice_num']
            self.points = self.item_effected_vars['points']
            self.items_revealed = self.item_effected_vars['revealed']

        else:
            self.bag.add(item)

    def left_click_sanity(self):
        if not pygame.mouse.get_pressed()[0]:
            self.can_choose = True

    def create_choices(self, Product, num, lis):
        self.pokemon_choices.empty()

        for i in range(num):
            rand = random.randint(0, len(self.pokelist) - 1)
            current = lis[rand]
            name = current['name']
            self.pokemon_choices.add(Product(name, (0,0)))

    def arrange_choices(self):
        current_pos = vector(0,0)
        right_x = 0
        iteration = 1280 / len(self.pokemon_choices)

        for opt in self.pokemon_choices.sprites():
            opt.rect.topleft = current_pos
            current_pos.x += iteration
            right_x = opt.rect.right

        offset = (1280 - right_x) / 2

        for opt in self.pokemon_choices.sprites():
            opt.rect.x += offset

    def run(self):
        while True:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            dt = self.clock.tick() / 1000

            self.backgrounds.update(dt)

            self.left_click_sanity()
            self.backgrounds.draw(self.display_surface)

            if self.state == 'main_menu':
                pass
            elif self.state == 'pokemon_draft':
                self.pokemon_draft(dt)

            pygame.display.update()

if __name__ == "__main__":
    game = Game()
    game.run()
