from spotipy import Spotify
import spotipy.util as util

def get_all_playlist_tracks( user, pid ):
    """builds list of (track, artist) of playlist uri"""

    response = sp.user_playlist_tracks(user, playlist_id = pid)
    
    tracks = [ ( r['track']['name'], r['track']['artists'][0]['name'] ) 
               for r in response['items'] ]

    if len(tracks) == response['total']:
        return tracks
    else:
        while len(tracks) < response['total']:
            response = sp.user_playlist_tracks(user, playlist_id = pid, offset=len(tracks))
            tracks += [ ( r['track']['name'], r['track']['artists'][0]['name'] ) 
                        for r in response['items'] ]

    return tracks
            

def get_all_user_playlists( user, limit=50):
    """returns a list of user-made playlist pids"""
    
    nams = []
    pids = []
    offset = 0
    response = {'items': range(limit)}
    while len( response['items'] ) >= limit:
        response = sp.user_playlists(user, offset=offset, limit=limit)

        pids += [ item['uri'] for item in response['items'] if item['owner']['id'] == user ]
        nams += [ item['name'] for item in response['items'] if item['owner']['id'] == user ]
        offset += limit

    return pids, nams
    for i in range(len(pids)):        
        print(pids[i], nams[i])


from collections import defaultdict, Counter
from time import sleep 

def count_all_playlist_tracks(user):
    score = Counter()

    user_pids, playlist_names = get_all_user_playlists(user)
    for i, pid in enumerate(user_pids):
        print("processing %s... " % playlist_names[i])
        sleep(1)
        for _ in get_all_playlist_tracks(user, pid):
            score[ _ ] += 1

    
    g = open('scores.dat', 'w')
    for k, v in score.items():
        g.write("%30s# %d\n" % (k,v))
#        print("%30s: %d" % (k,v))
    g.close()
    return score


def get_all_playlist_tracks( user, pid ):
    """builds list of (track, artist) of playlist uri"""

    response = sp.user_playlist_tracks(user, playlist_id = pid)

    tracks = [ ( r['track']['name'], r['track']['artists'][0]['name'] )
               for r in response['items'] ]

    if len(tracks) == response['total']:
        return tracks
    else:
        while len(tracks) < response['total']:
            response = sp.user_playlist_tracks(user, playlist_id = pid, offset=len(tracks))
            tracks += [ ( r['track']['name'], r['track']['artists'][0]['name'] )
                        for r in response['items'] ]

    return tracks


def get_all_user_playlists( user, limit=50):
    """returns a list of user-made playlist pids"""

    nams = []
    pids = []
    offset = 0
    response = {'items': range(limit)}
    while len( response['items'] ) >= limit:
        response = sp.user_playlists(user, offset=offset, limit=limit)

        pids += [ item['uri'] for item in response['items'] if item['owner']['id'] == user ]
        nams += [ item['name'] for item in response['items'] if item['owner']['id'] == user ]
        offset += limit

    return pids, nams
    for i in range(len(pids)):
        print(pids[i], nams[i])

if __name__ == "__main__":
    user = 'gsuehr'
    token = util.prompt_for_user_token(user, 'playlist-read-private')
    sp = Spotify(auth=token)

    count_all_playlist_tracks(user)
