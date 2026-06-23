import itertools
import os, dotenv
from datetime import datetime
import pylast
from get_artwork import get_artwork
from get_lyrics import get_lyrics
dotenv.load_dotenv()


# You have to have your own unique two values for API_KEY and API_SECRET
# Obtain yours from https://www.last.fm/api/account/create for Last.fm
API_KEY = os.getenv('PYLAST_API_KEY') # this is a sample key
API_SECRET = os.getenv('PYLAST_API_KEY')

network = pylast.LastFMNetwork(
    api_key=API_KEY,
    api_secret=API_SECRET
)

SAVES = os.path.join(os.path.dirname(__file__), "saves")
os.makedirs(SAVES, exist_ok=True)

CACHE = os.path.join(os.path.dirname(__file__), "cache")
os.makedirs(CACHE, exist_ok=True)

def get_data(album='Currents', artist='Tame Impala', size=3000) -> tuple:
    album = get_album(album, artist)
    artwork = get_artwork(album, artist, size)
    lyrics = get_lyrics(album, artist)

    return artwork, lyrics

def get_album(album='Currents', artist='Tame Impala'):
    albums = network.search_for_album(album).get_next_page()
    try:
        album = next(a for a in albums if a.artist.name.lower() == artist.lower())
    except StopIteration:
        print(f'No album called {album} made by {artist}!')
        exit()

    return album

def image_to_text(data):

    image = data[0]
    lyrics = data[1]

    iterator = itertools.cycle(''.join(lyrics.split()))


    content = []

    height = int(image.height)
    width = int(image.width)

    # height = width = 30

    for y in range(height):
        for x in range(width):
            r,g,b = image.getpixel((x,y))

            content.append(f"<span style='color:rgb({r},{g},{b})'>{next(iterator)}</span>")

            print(f'Line: {y}/{height}, Column: {x}/{width}')

        content.append('<br>')

    content = ''.join(content)

    template = f'''<html>
    <head>
    <style>
    body {{
    margin: 40px;
    display: flex;
    justify-content: center;
    align-items: center;
    
    }}
    
    content {{
    display: none;
    font-family: monospace;
    font-weight: bold;
    line-height: 1;
    letter-spacing: 0px;
    background: #111;
    text-align: center;
    overflow: hidden;
    }}

    </style>
    </head>
    <body>
    <content>
    {content}
    </content>
    <script>
    document.addEventListener('DOMContentLoaded', () => {{
    document.querySelector('content').style.fontSize = `${{(window.innerHeight * 0.8) / {height}}}px`
    document.querySelector('content').style.display = `block`
    }})
    </script>
    </body>
    </html>'''

    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    with open(os.path.join(SAVES, f'{timestamp}.html'), 'w+') as f:
        f.write(template)

    print(''.join(lyrics.split()))
artist_ = input('Enter artist: ')
album_ = input('Enter album: ')
size_ = input('Enter size (or leave blank): ')

if not size_:
    size_ = 200
else:
    size_ = int(size_)

image_to_text(get_data(album=album_, artist=artist_, size=size_))