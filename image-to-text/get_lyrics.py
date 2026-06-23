import os
import re

from lrclib import LrcLibAPI

api = LrcLibAPI(user_agent='lyric-to-album/0.0.1')


CACHE = os.path.join(os.path.dirname(__file__), "cache")

def get_lyrics(album, artist) -> str:

    print(album)

    ALBUM_CACHE_FOLDER = f'{album.title} - {album.artist}'
    ALBUM_CACHE_FOLDER_LOC = os.path.join(CACHE, ALBUM_CACHE_FOLDER)
    os.makedirs(ALBUM_CACHE_FOLDER_LOC, exist_ok=True)

    lyrics = []

    for song in album.get_tracks():
        secure_title = re.sub(r'[<>:"/\\|?*\x00-\x1F]', '', song.title)
        CACHE_FILE = f'{secure_title} - {album.title} - {album.artist}.txt'
        CACHE_FILE_LOC = os.path.join(ALBUM_CACHE_FOLDER_LOC, CACHE_FILE)

        if CACHE_FILE in os.listdir(ALBUM_CACHE_FOLDER_LOC):
            with open(CACHE_FILE_LOC, 'r') as f:
                lyrics.append(f.read())
        else:
            print(song)
            try:
                song = api.search_lyrics(
                    track_name= song.title,
                    artist_name= artist
                )
            except Exception as e:
                print(e)

            if song:
                song_lyrics = song[0].plain_lyrics or ''
                lyrics.append(song_lyrics)
                print(lyrics)

                with open(CACHE_FILE_LOC, 'w+') as f:
                    f.write(song_lyrics)

    return ''.join(''.join(lyrics).split())