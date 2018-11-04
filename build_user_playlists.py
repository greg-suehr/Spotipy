from spotipy import Spotify
import spotipy.util as utilfrom spotipy import Spotify
import spotipy.util as util

def get_playlist_tracks( user, pid ):
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
            

def build_user_playlists( user, limit=50):
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

    return pids
    for i in range(len(pids)):        
        print pids[i], nams[i]


from collections import defaultdict, Counter
from time import sleep 

def count_tracks(user):
    score = Counter()

    user_pids = build_user_playlists(user)
    for pid in user_pids:
        print "processing %s... " % pid
        sleep(1)
        for i in get_playlist_tracks(user, pid):
            score[ i ] += 1

    for k, v in score.iteritems():
        print "%30s: %d" % (k,v)
    return scorey


if __name__ == "__main__":
    user = 'gsuehr'
    token = util.prompt_for_user_token(user, 'playlist-read-private')
    sp = Spotify(auth=token)

    count_tracks(user)
