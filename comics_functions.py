import random
from pathlib import Path

import requests


def download_image(image_url, download_path, params=None):
    response = requests.get(image_url, params=params)
    response.raise_for_status()
    with open(str(download_path), 'wb') as file:
        file.write(response.content)


def fetch_comics_by_id(img_id, img_dir):
    url = f'https://xkcd.com/{img_id}/info.0.json'
    response = requests.get(url)
    response.raise_for_status()
    comics_info = response.json()
    img_url = comics_info['img']
    img_path = Path(f"{img_dir}/{comics_info['title']}.png")
    download_image(img_url, img_path)
    return img_path, comics_info['alt']


def fetch_random_comics(img_dir):
    url = 'https://xkcd.com/info.0.json'
    response = requests.get(url)
    response.raise_for_status()
    last_comics_num = response.json()['num']
    comics_id = random.randint(1, last_comics_num)
    return fetch_comics_by_id(comics_id, img_dir)
