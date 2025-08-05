import requests
import json
from pathlib import Path
from item import Item, HeldItem, EvoCandy, Vitamin, SellItem

def determine_items():
    item_list = []
    with open('item-list.json', 'r') as f:
        item_list = json.load(f)

    destinations = []
    urls = []

    for item in item_list:
        path = Path(item['img'])
        
        if path.is_file():
            print('file already exists')
        else:

            destinations.append(item['img'])

            r = requests.get(f'https://pokeapi.co/api/v2/item/{item['name']}').json()

            urls.append(r['sprites']['default'])

    return urls, destinations

def download_images(urls, destinations):
    for i, url in enumerate(urls):

        r = requests.get(url)

        if r.status_code == 200:
            with open(destinations[i], 'wb') as f:
                print(f'{destinations[i]} downloaded')
                f.write(r.content)

        else:
            print(f'failed to download{i}')


if __name__ == "__main__":
    urls, destinations = determine_items()
    download_images(urls, destinations)
