from spotipy import Spotify
import spotipy.util as util
from collections import defaultdict

# TODO: move spaghetti into method
user = 'gsuehr'
token = util.prompt_for_user_token(user, 'playlist-read-private')
sp = Spotify(auth=token)

def build_P(user):
    P = defaultdict()

    # DANGER: if offset not set, could go for forever...
    offset = 0
    while True:
        response = sp.user_playlists(user, offset=offset)
        for item in response['items']:
            if (item['owner']['id'] == user):
                P[ item['name'] ] = item['uri']

        if len(response['items']) < response['limit']: break
        offset += response['limit']
 
    return P

def build_S(user):
    pass

def build_G(user):
    pass

def build_W(user):
    pass
