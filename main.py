import pygame
import sys 
from pokemon import Pokemon
from biker import Biker
from button import Button
import random
import json
from background import Background, Backgrounds
from pygame.math import Vector2 as vector
from item import *
class Points(pygame.sprite.Sprite):
    def __init__(self, points, pos, size=35):
        self.font = pygame.font.Font('pixel-font.ttf', size=size)
        self.image = self.font.render(f'Points: {points}', False, 'white')
        self.rect = self.image.get_rect(midright=pos)
        
    def update(self, points):
        self.image = self.font.render(f'Points: {points}', False, 'white')
        self.rect = self.image.get_rect(midright=self.rect.midright)


class Game:
    def __init__(self):
        pygame.init()
        self.width = 1280
        self.height = 720
        self.display_surface = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Pokemon Drafter')
        self.clock = pygame.time.Clock()

        with open('pokelist.json', 'r') as f:
            self.pokelist = json.load(f)
        with open('item-list.json', 'r') as f:
            self.item_list = json.load(f)

        self.backgrounds = Backgrounds()

        self.background = Background('wallpaper.jpg', (self.width, 0), self.backgrounds)
        self.background2 = Background('wallpaper.jpg', (self.width - self.background.image.get_width(), 0), self.backgrounds)
        self.pokemon_choices = pygame.sprite.Group()
        self.item_choices = pygame.sprite.Group()
        self.bag = pygame.sprite.Group()
        self.box = pygame.sprite.Group()
        self.buttons = pygame.sprite.Group()

        self.main_button = Button("Main Menu", self.buttons)
        self.main_button.rect.midbottom = (int(self.width / 2), self.height - 10)
        self.mb_pos = self.main_button.rect.topleft

        self.item_effected_vars = {"choice_num": 4, 
                                   "points": 500, 
                                   "revealed": False}

        self.drafter_button = Button("Drafter", self.buttons)
        self.drafter_button.rect.bottomleft = (10, self.height - 10)
        self.db_pos = self.drafter_button.rect.topleft


        self.biker = Biker((100,360), self.backgrounds)

        self.state = 'pokemon_draft'

        self.can_choose = False

        self.point_tracker = Points(self.item_effected_vars['points'], (self.width, self.height / 2))

        self.items_picked = 0


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
                index = random.randint(0, len(self.item_list) - 1)
                new_item = eval(self.item_list[index]['class'])(self.item_list[index])
                new_item.is_hidden = not self.item_effected_vars['revealed']
                mon.hold_item(new_item)

    def state_sanity(self):
        if self.state == 'pokemon_draft':
            if self.items_picked <= len(self.box) / 3:
                self.state = 'item_draft'

        if self.main_button.is_clicked() and self.can_choose:
            self.can_choose = False
            self.state = 'main_menu'
        if self.drafter_button.is_clicked() and self.can_choose:
            self.can_choose = False
            self.state = 'pokemon_draft'


    def pokemon_draft(self, dt):
        if not self.pokemon_choices:
            self.create_pokemon(Pokemon, self.item_effected_vars['choice_num'], self.pokelist)
            self.arrange_options(self.pokemon_choices)
            self.item_smuggling()

        self.pokemon_choices.update(dt)
        self.pokemon_choices.draw(self.display_surface)


        for sprite in self.pokemon_choices:

            self.display_text()

            if sprite.bst > self.item_effected_vars['points']:
                sprite.set_cant_afford()

            if sprite.is_clicked() and self.can_choose and self.item_effected_vars['points'] > sprite.bst:
                self.can_choose = False

                self.item_effected_vars['points'] -= sprite.bst
                self.point_tracker.update(self.item_effected_vars['points'])

                if sprite.held_item:
                    self.acquire_item(sprite.held_item)
                    sprite.held_item = None

                self.box.add(sprite)

                for mon in self.box.sprites():
                    print(mon.name)

                self.pokemon_choices.empty()

    def item_draft(self):
        if not self.item_choices:
            self.create_items(6)
            self.item_choices.update()
            self.arrange_options(self.item_choices)

        self.item_choices.update()
        self.item_choices.draw(self.display_surface)

        for sprite in self.item_choices.sprites():

            if sprite.is_hovering():
                sprite.text.rect.midtop = sprite.rect.midbottom
                self.display_surface.blit(sprite.text.image, sprite.text.rect.topleft)
            
            if sprite.is_clicked() and self.can_choose:
                self.can_choose = False

                self.acquire_item(sprite)

                self.item_choices.empty()

                self.items_picked += 1

                self.state = 'pokemon_draft'

    def bag_view(self):
        pass

    def box_view(self):
        pass

    def mart(self):
        pass

    def acquire_item(self, item):
        if hasattr(item, 'on_pickup'):
            item.on_pickup(self.item_effected_vars)
            print(self.item_effected_vars)

        else:
            self.bag.add(item)

    def left_click_sanity(self):
        if not pygame.mouse.get_pressed()[0]:
            self.can_choose = True

    def create_pokemon(self, Product, num, lis):
        self.pokemon_choices.empty()

        for i in range(num):
            rand = random.randint(0, len(self.pokelist) - 1)
            current = lis[rand]
            name = current['name']
            self.pokemon_choices.add(Product(name, (0,0)))

    def create_items(self, num):
        self.item_choices.empty()
        item_list = self.item_list

        random.shuffle(item_list)

        for i in range(num):
            item_dict = item_list[i]
            new_item = eval(item_dict['class'])(item_dict)
            new_item.is_hidden = False
            new_item.is_big = True
            self.item_choices.add(new_item)

    def arrange_options(self, group):
        current_pos = vector(0,0)
        right_x = 0
        iteration = self.width / len(group)

        for opt in group.sprites():
            opt.rect.topleft = current_pos
            current_pos.x += iteration
            right_x = opt.rect.right

        offset = (self.width - right_x) / 2

        for opt in group.sprites():
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
            self.buttons.draw(self.display_surface)

            self.point_tracker.update(self.item_effected_vars['points'])
            self.display_surface.blit(self.point_tracker.image, self.point_tracker.rect.topleft)
            
            self.state_sanity()

            if self.state == 'main_menu':
                pass
            elif self.state == 'pokemon_draft':
                self.pokemon_draft(dt)
            elif self.state == 'item_draft':
                self.item_draft()

            pygame.display.update()

if __name__ == "__main__":
    game = Game()
    game.run()
