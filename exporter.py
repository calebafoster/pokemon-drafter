import random
import pyperclip


class Exporter:
    def __init__(self, box):
        self.team = box

    def create_text(self):
        text = ''

        for mon in self.team.sprites():
            name = mon.name
            stat = ''
            item = ''
            lines = []

            if mon.held_item:

                if hasattr(mon.held_item, "stat"):
                    stat = mon.held_item.stat

                else:
                    item = mon.held_item.name
                    lines.append(f'{name} @ {item}')

            else:
                lines.append(f'{name}')

            lines.append(f'Ability: {mon.ability['ability']['name']}')
            lines.append('Level: 50')
            lines.append(f'Tera Type: {mon.types[0]}')
            if stat:
                lines.append(f'EVs: 252 {stat}')

            lines.append(f'{self.random_nature()} Nature')

            for line in lines:
                concatonated_line = f'{line} \n'
                text = text + concatonated_line

            text = text + '\n'

        pyperclip.copy(text)

    def random_nature(self):
        natures = ['Hardy', 'Lonely', 'Adamant', 'Naughty', 'Brave', 
                   'Bold', 'Docile', 'Impish', 'Lax', 'Relaxed', 
                   'Modest', 'Mild', 'Bashful', 'Rash', 'Quiet', 
                   'Calm', 'Gentle', 'Careful', 'Quirky', 'Sassy',
                   'Timid', 'Hasty', 'Jolly', 'Naive', 'Serious']

        random.shuffle(natures)
        return natures[0]

    def export(self):
        with open('showdown-team.txt', 'w') as f:
            f.write(self.text)
