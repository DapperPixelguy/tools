import os
from io import BytesIO

import requests
from PIL import Image
import musicbrainzngs
musicbrainzngs.set_useragent("Album cover to text", "1.0", 'https://dapperpixelguy.wtf')

CACHE = os.path.join(os.path.dirname(__file__), "cache")

def get_artwork(album, artist, size) -> Image:

    ALBUM_CACHE_FOLDER = f'{album.title} - {album.artist}'
    ALBUM_CACHE_FOLDER_LOC = os.path.join(CACHE, ALBUM_CACHE_FOLDER)
    os.makedirs(ALBUM_CACHE_FOLDER_LOC, exist_ok=True)


    for ext in ('jpg', 'png'):
        CACHE_FILE = f'{album.title} - {album.artist}.{ext}'
        CACHE_FILE_LOC = os.path.join(ALBUM_CACHE_FOLDER_LOC, CACHE_FILE)
        if os.path.exists(CACHE_FILE_LOC):
            image = Image.open(CACHE_FILE_LOC).convert('RGB')
            break
    else:
        releases = musicbrainzngs.search_releases(artist=artist, release=album.title, limit=10, format='Digital Media')['release-list']

        url = None
        for release in releases:
            caa = requests.get(
                f'https://coverartarchive.org/release/{release["id"]}',
                headers={'Accept': 'application/json'}
            )
            if caa.status_code == 200 and caa.json().get('images'):
                url = caa.json()['images'][0]['image']
                break

        if not url:
            print('Unable to grab album cover')
            exit()

        ext = 'png' if url.endswith('.png') else 'jpg'
        CACHE_FILE = f'{album.title} - {album.artist}.{ext}'
        CACHE_FILE_LOC = os.path.join(ALBUM_CACHE_FOLDER_LOC, CACHE_FILE)
        image = Image.open(BytesIO(requests.get(url).content)).convert('RGB')
        image.save(CACHE_FILE_LOC)


    ratio = image.height / image.width

    height = int(size * ratio * 0.5)

    image = image.resize((size, height))

    return image