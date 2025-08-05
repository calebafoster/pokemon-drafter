import pygame
import json
from pathlib import Path
from pygame import Vector2 as vector
import requests
import random

class Text(pygame.sprite.Sprite):
    def __init__(self, name, bst, types, size = 25):
        super().__init__()

        self.font = pygame.font.Font('pixel-font.ttf', size)
        self.name = name.upper()
        self.bst = f'BST: {bst}'
        self.types = ' '.join(types).upper()
        self.text_list = [self.name, self.bst, self.types]

        self.generate_surfs()

    def draw_text(self, surface, index, pos):
        self.rect_list[index].topleft = pos

        self.bg_surfs[index].fill('black')
        self.bg_surfs[index].set_alpha(25)

        surface.blit(self.bg_surfs[index], self.rect_list[index].topleft)
        surface.blit(self.text_surfs[index], self.rect_list[index].topleft)

    def generate_surfs(self):
        self.text_surfs = []
        self.bg_surfs = []
        self.rect_list = []

        for txt in self.text_list:
            print(txt)
            img = self.font.render(txt, True, 'white')
            rect = img.get_rect()
            self.text_surfs.append(img)
            self.rect_list.append(rect)
            bg = pygame.surface.Surface((img.get_width(), img.get_height()))

            self.bg_surfs.append(bg)


class Pokemon(pygame.sprite.Sprite):
    def __init__(self, name, pos, nickname = ''):
        super().__init__()

        self.name = name   ## evo
        self.nickname = nickname
        
        self.import_assets()
        self.image = pygame.transform.scale_by(self.image, 2)   ## evo
        self.rect = self.image.get_rect(topleft = pos)

        self.pos = vector(self.rect.topleft)

        self.types = []   ## evo
        self.bst = 0   ## evo
        self.stage = 0   ## evo
        self.can_evolve = False   ## evo
        self.held_item = None

        self.move_list = self.poke_dict['moves']   ## evo
        self.ability_list = self.poke_dict['abilities']   ## evo
        self.evo_chain = self.get_evo_chain()

        self.ability = None   ## evo

        self.get_types()   ## evo
        self.get_bst()   ## evo
        self.set_ability()   ## evo

        self.moves = []   ## evo

        self.clicked = False
        self.right_clicked = False

        self.text = Text(self.name, self.bst, self.types)   ## evo
        self.cycle_count = 0
        self.cycle_index = 0
        self.can_right_click = True

        self.determine_evolution()   ## evo

    def force_evolve(self):
        self.name = self.next_evo
        self.import_assets()
        self.image = pygame.transform.scale_by(self.image, 2)

        self.ability_list = self.poke_dict['abilities']

        self.get_types()
        self.get_bst()
        self.set_ability()

        self.text = Text(self.name, self.bst, self.types)

        self.determine_evolution()

    def item_chance(self):
        floor = 200
        ceiling = 625 - floor
        temp_bst = self.bst - floor if self.bst - floor > 0 else 0
        chance_not = temp_bst / ceiling
        chance = 1 - chance_not
        return chance

    def hold_item(self, item_obj):
        self.held_item = item_obj

    def determine_evolution(self):
        chain_link = self.find_link()

        if chain_link:
            random.shuffle(chain_link)
            self.next_evo = chain_link[0]['species']['name']
            self.can_evolve = True
            print(self.next_evo)

    def find_link(self):
        
        if self.name == self.evo_chain['species']['name'] and self.evo_chain['evolves_to']:
            return self.evo_chain['evolves_to']

        if not self.evo_chain['evolves_to']:
            return []

        for mon in self.evo_chain['evolves_to']:
            if mon['species']['name'] == self.name:
                return mon['evolves_to']

        return []

    def display_text(self, surface):
        if self.is_hovering():
            self.text.draw_text(surface, self.cycle_index, self.rect.topleft)

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

    def cycle_logic(self):
        if self.is_right_clicked() and self.can_right_click:
            self.cycle_count += 1
            self.cycle_index = self.cycle_count % len(self.text.text_list)
            self.can_right_click = False

    def test_evo(self):
        if self.is_right_clicked() and self.can_right_click:
            self.force_evolve()
            self.can_right_click = False

    def set_ability(self):
        index = random.randint(0, len(self.ability_list)) - 1
        self.ability = self.ability_list[index]

    def get_types(self):
        for poke_type in self.poke_dict['types']:
            self.types.append(poke_type['type']['name'])

    def get_bst(self):
        count = 0

        for stat in self.poke_dict['stats']:
            count += stat['base_stat']

        self.bst = count

    def get_evo_chain(self):
        r = requests.get(self.species_dict['evolution_chain']['url'])
        evo_chain = r.json()
        return evo_chain['chain']

    def import_assets(self):
        with open(f'pokemon/{self.name}.json', 'r') as f:
            self.poke_dict = json.load(f)

        with open(f'pokemon/species/{self.name}.json', 'r') as f:
            self.species_dict = json.load(f)

        self.image_path = Path(f'images/pokemon/{self.name}.png')

        if self.image_path.is_file():
            self.image = pygame.image.load(self.image_path).convert_alpha()
        else:
            self.download_image()

    def download_image(self):
        image_url = self.poke_dict['sprites']['front_default']
        r = requests.get(image_url)

        if r.status_code == 200:
            with open(self.image_path, 'wb') as f:
                f.write(r.content)
            print(f'image download successful: {self.name}')
        else:
            self.image_path = Path('images/pokemon/missing.png')
            print('image download unsuccesful, replacing with missingno')

        self.image = pygame.image.load(self.image_path).convert_alpha()

    def display_item(self):
        if self.held_item:
            self.held_item.update()
            self.held_item.rect.bottomright = (self.image.get_width(), self.image.get_height())
            self.image.blit(self.held_item.image, self.held_item.rect.topleft)

    def update(self, dt):
        self.display_item()
        self.test_evo()
        ##self.cycle_logic()

if __name__ == '__main__':
    pikachoo = Pokemon('chikorita', (0,0))
    print(pikachoo.poke_dict['id'])
