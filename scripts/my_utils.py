from spotipy import Spotify
import spotipy.util as util
from collections import defaultdict

# TODO: move spaghetti into method //no-commit
user = 'gsuehr'
token = util.prompt_for_user_token(user, 'playlist-read-private')
sp = Spotify(auth=token)

def all_playlists(user):
    playlists = defaultdict()

    offset = 0    
    while True:
        response = sp.user_playlists(user, offset=offset)
        for item in response['items']:
            if (item['owner']['id'] == user):
                playlists[ item['uri'] ] = item['name']

        if len(response['items']) < response['limit']: break
        offset += response['limit']
 
    return playlists

def all_playlist_tracks(user, playlists=None):
    if playlists is None:
        playlists = all_playlists(user)
        
    assert type(playlists) == defaultdict
    tracks = defaultdict()

    for playlist_id in playlists.keys():
        offset = 0

        while True:
            response = sp.playlist_tracks(playlist_id, offset=offset)
            for track in [_['track'] for _ in response['items']]:
                tracks[track['uri']] = track['name']

            if len(response['items']) < response['limit']: break
            offset += response['limit']

    return tracks

def chunk_track_ids(track_ids, n=100):
    for i in range(0,len(track_ids),n):
        yield track_ids[i:i+n]
