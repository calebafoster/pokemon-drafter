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
        self.default_pos = self.rect.midright
        
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

        self.gray_setup()

        self.pokemon_choices = pygame.sprite.Group()
        self.item_choices = pygame.sprite.Group()
        self.bag = pygame.sprite.Group()
        self.box = pygame.sprite.Group()
        self.buttons = pygame.sprite.Group()
        self.mart_choices = pygame.sprite.Group()

        self.item_effected_vars = {"choice_num": 4, 
                                   "points": 2500, 
                                   "revealed": False}

        self.point_tracker = Points(self.item_effected_vars['points'], (self.width, self.height / 2 + 30))

        self.main_button = Button("Main Menu", self.buttons)
        self.main_button.rect.midbottom = (int(self.width / 2), self.height - 10)
        self.main_button.default_pos = self.main_button.rect.topleft

        self.drafter_button = Button("Drafter", self.buttons)
        self.drafter_button.rect.bottomleft = (10, self.height - 10)
        self.drafter_button.default_pos = self.drafter_button.rect.topleft

        self.box_button = Button("Box", self.buttons, size=45)
        self.box_button.rect.bottomright = (self.width - 10, self.height - 10)
        self.box_button.default_pos = self.box_button.rect.topleft

        self.mart_button = Button("Mart", self.buttons)
        self.mart_button.rect.topright = self.point_tracker.rect.bottomright
        self.mart_button.default_pos = self.mart_button.rect.topleft

        self.biker = Biker((int(self.width / 3), 360), self.backgrounds)

        self.state = 'main_menu'

        self.can_choose = False

        self.items_picked = 0
        self.last_picked_item = None
        self.last_picked_pokemon = None

        self.item_using = None

    def main_menu(self):
        self.biker.target_x = self.width / 2

        self.main_button.rect.midtop = (int(self.width / 2), int(self.height / 5))
        prev_pos = self.main_button.rect.midbottom

        for sprite in self.buttons.sprites():
            sprite.rect.midtop = prev_pos
            prev_pos = sprite.rect.midbottom

        self.main_button.rect.bottomright = (0,0)
        self.point_tracker.rect.bottomright = (0,0)

    def pokemon_draft(self):
        self.biker.target_x = 150
        if not self.pokemon_choices:
            self.create_pokemon(Pokemon, self.item_effected_vars['choice_num'], self.pokelist)
            self.arrange_options(self.pokemon_choices)
            self.item_smuggling()

        self.buttons_default()

        self.pokemon_choices.update()
        self.pokemon_choices.draw(self.display_surface)

        self.display_last_picked()

        for sprite in self.pokemon_choices:

            self.display_text(self.pokemon_choices)
            sprite.display_item(self.display_surface)

            if sprite.bst > self.item_effected_vars['points']:
                sprite.set_cant_afford()

            if sprite.is_clicked() and self.can_choose and self.item_effected_vars['points'] >= sprite.bst:
                self.can_choose = False

                self.item_effected_vars['points'] -= sprite.bst
                self.point_tracker.update(self.item_effected_vars['points'])

                if sprite.held_item:
                    self.acquire_item(sprite.held_item)
                    sprite.held_item = None

                self.last_picked_pokemon = sprite
                self.box.add(sprite)

                self.pokemon_choices.empty()

    def item_draft(self):
        self.biker.target_x = 150
        if not self.item_choices:
            self.create_items(6)
            self.item_choices.update()
            self.arrange_options(self.item_choices)

        self.buttons_default()

        self.item_choices.update()
        self.item_choices.draw(self.display_surface)

        self.display_last_picked()

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

    def box_view(self):
        self.bag_box_setup()
        self.display_text(self.box)

        for sprite in self.bag.sprites():
            if sprite.is_hovering() and not self.item_using:
                sprite.text.rect.midtop = sprite.rect.midbottom
                self.display_surface.blit(sprite.text.image, sprite.text.rect.topleft)

            if sprite.is_clicked() and self.can_choose and not self.item_using:
                self.can_choose = False
                self.item_using = sprite
                self.bag.remove(sprite)

        for sprite in self.box.sprites():
            sprite.display_item(self.display_surface)

            if sprite.is_clicked() and self.item_using and self.can_choose:
                if hasattr(self.item_using, 'use_item'):
                    if self.item_using.check_evo(sprite):

                        self.item_using.use_item(sprite)
                        self.item_using = None
                    else:
                        self.bag.add(self.item_using)
                        self.item_using = None

                else:
                    sprite.held_item = self.item_using
                    self.item_using = None

        if self.item_using:
            self.item_using.rect.center = pygame.mouse.get_pos()
            self.display_surface.blit(self.item_using.image, self.item_using.rect.topleft)

            if pygame.mouse.get_pressed()[0] and self.can_choose:
                self.can_choose = False
                self.bag.add(self.item_using)
                self.item_using = None

    def mart(self):
        if not self.mart_choices:
            self.create_mart_choices(16)
            self.mart_choices.update()

        self.bag_box_setup()
        self.buttons_default()
        self.mart_button.rect.midbottom = self.gray_rect.midtop
        self.point_tracker.rect.midright = self.gray_rect.midright

        for sprite in self.mart_choices.sprites():
            if sprite.is_hovering():
                sprite.cost_text.rect.midtop = sprite.rect.midtop
                self.display_surface.blit(sprite.cost_text.image, sprite.cost_text.rect.topleft)
                sprite.text.rect.midtop = sprite.rect.midbottom
                self.display_surface.blit(sprite.text.image, sprite.text.rect.topleft)

            if sprite.is_clicked() and self.can_choose and sprite.cost <= self.item_effected_vars['points']:
                self.can_choose = False

                self.acquire_item(sprite)

                self.item_effected_vars['points'] -= sprite.cost

                self.mart_choices.remove(sprite)

    def gray_setup(self):
        self.gray_bg = pygame.surface.Surface((self.width / 1.25, self.height / 1.25))
        self.gray_bg.set_alpha(125)
        self.gray_bg.fill('gray')
        self.gray_rect = self.gray_bg.get_rect()
        self.gray_rect.center = (int(self.width / 2), int(self.height / 2))

        self.little_rect = self.gray_rect.inflate(0, -self.gray_rect.height + 40)
        self.little_rect.bottomleft = self.gray_rect.bottomleft

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

    def display_text(self, group):
        for sprite in group:
            sprite.display_text(self.display_surface)
            sprite.update()

    def item_smuggling(self):
        for mon in self.pokemon_choices:
            chance = mon.item_chance()
            if random.random() < chance:
                index = random.randint(0, len(self.item_list) - 1)
                new_item = eval(self.item_list[index]['class'])(self.item_list[index])
                new_item.is_hidden = not self.item_effected_vars['revealed']
                mon.hold_item(new_item)

    def state_sanity(self):

        if self.main_button.is_clicked() and self.can_choose:
            self.can_choose = False
            self.state = 'main_menu'
            self.item_using = None

        if self.drafter_button.is_clicked() and self.can_choose:
            self.can_choose = False
            self.state = 'pokemon_draft'
            self.item_using = None

        if self.box_button.is_clicked() and self.can_choose:
            self.can_choose = False
            self.state = 'box_view'

        if self.mart_button.is_clicked() and self.can_choose:
            self.can_choose = False
            self.state = 'mart'

        if self.state == 'pokemon_draft':
            if self.items_picked <= len(self.box) / 3:
                self.state = 'item_draft'

    def display_last_picked(self):
        if self.last_picked_item:
            self.last_picked_item.is_hidden = False
            self.last_picked_item.rect.midright = self.box_button.rect.midleft
            self.display_surface.blit(self.last_picked_item.image, self.last_picked_item.rect.topleft)

        if self.last_picked_pokemon:
            self.last_picked_pokemon.small_rect.midbottom = self.box_button.rect.midtop
            self.display_surface.blit(self.last_picked_pokemon.small_image, self.last_picked_pokemon.small_rect.topleft)

    def buttons_default(self):
        for sprite in self.buttons.sprites():
            sprite.rect.topleft = sprite.default_pos

        self.point_tracker.rect.midright = self.point_tracker.default_pos

    def place_on_gray(self, group):
        item_width = 0
        item_height = 0
        row_capacity = 0
        prev_pos = vector(self.gray_rect.topleft)

        for i, sprite in enumerate(group.sprites(), start=1):
            if i == 1:
                item_width = sprite.image.get_width()
                item_height = sprite.image.get_height()
                row_capacity = int(self.gray_bg.get_width() / item_width)

            sprite.rect.topleft = prev_pos
            prev_pos.x = sprite.rect.right
            self.display_surface.blit(sprite.image, sprite.rect.topleft)

            if i == row_capacity or i == row_capacity * 2:
                prev_pos.x = self.gray_rect.left
                prev_pos.y += item_height

    def bag_box_setup(self):
        self.display_surface.blit(self.gray_bg, self.gray_rect.topleft)
        self.buttons_default()
        self.biker.target_x = self.width - 150
        self.point_tracker.rect.bottomright = (0,0)

        if self.state == 'box_view':
            self.place_on_gray(self.box)

        if self.state == 'mart':
            self.place_on_gray(self.mart_choices)

        prev_pos = vector(self.little_rect.midleft)
        for sprite in self.bag.sprites():
            sprite.rects[0].midleft = prev_pos
            prev_pos.x = sprite.rects[0].right
            self.display_surface.blit(sprite.images[0], sprite.rects[0].topleft)

    def acquire_item(self, item):
        if hasattr(item, 'on_pickup'):
            item.on_pickup(self.item_effected_vars)

        else:
            item.is_hidden = False
            item.is_big = False
            item.update()
            self.last_picked_item = item
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

    def create_mart_choices(self, num):
        guarantees = ['rare-candy', 'burn-drive', 'reveal-glass']
        item_list = self.item_list

        for guarantee in guarantees:
            for item in item_list:
                if item['name'] == guarantee:
                    new_item = eval(item['class'])(item)
                    new_item.is_hidden = False
                    new_item.is_big = True
                    self.mart_choices.add(new_item)
                    break

        for i in range(num - len(guarantees)):
            random.shuffle(item_list)
            item_dict = item_list[0]
            new_item = eval(item_dict['class'])(item_dict)
            new_item.is_hidden = False
            new_item.is_big = True
            self.mart_choices.add(new_item)

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

            dt = self.clock.tick(120) / 1000

            self.backgrounds.update(dt)
            self.point_tracker.update(self.item_effected_vars['points'])

            self.left_click_sanity()
            self.backgrounds.draw(self.display_surface)

            self.state_sanity()

            if self.state == 'main_menu':
                self.main_menu()
            elif self.state == 'pokemon_draft':
                self.pokemon_draft()
            elif self.state == 'item_draft':
                self.item_draft()
            elif self.state == 'box_view':
                self.box_view()
            elif self.state == 'mart':
                self.mart()

            self.buttons.draw(self.display_surface)

            self.display_surface.blit(self.point_tracker.image, self.point_tracker.rect.topleft)

            pygame.display.update()

if __name__ == "__main__":
    game = Game()
    game.run()
