# 2017.12.10 22:35:53 EST
# Embedded file name: tools.py
from spotipy import Spotify
import spotipy.util as util
from time import sleep
from collections import defaultdict

user = 'gsuehr'
token = util.prompt_for_user_token(user, 'playlist-read-private')
sp = Spotify(auth=token)

P = None
S = None
A = None
G = None
W = None
P2S = None
S2G = None

def build_P(user, verbose = False):
    global P
    p = defaultdict()
    offset = 0
    while True:
        sleep(1)
        response = sp.user_playlists(user, offset=offset)
        for item in response['items']:
            if item['owner']['id'] == user:
                p[item['name']] = item['uri']

        if verbose:
            print 'Processed %d items...' % len(p.keys())
        if len(response['items']) < response['limit']:
            break
        offset += response['limit']

    P = p
    return p


def build_S(user, verbose = False):
    global A
    global S
    global P2S
    if not P:
        build_P(user)
    s = defaultdict()
    a = defaultdict()
    p2s = defaultdict()
    for pid in P.values():
        p2s[pid] = []
        offset = 0
        while True:
            sleep(1)
            response = sp.user_playlist_tracks(user, playlist_id=pid, offset=offset)
            for track in [ item['track'] for item in response['items'] ]:
                s[track['name'], track['artists'][0]['name']] = track['uri']
                p2s[pid].append((track['name'], track['artists'][0]['name']))
                for artist in track['artists']:
                    a[artist['name']] = artist['uri']

            if verbose:
                print 'Processed %d items...' % len(s.keys())
            if len(response['items']) < response['limit']:
                break
            offset += response['limit']

    A = a
    S = s
    P2S = p2s
    return s


def build_G(user, verbose = False):
    global S2G
    global G
    if not A:
        build_S(user)
    g = defaultdict(set)
    s2g = defaultdict()
    artist_batches = [ A.values()[i:i + 50] for i in range(0, len(A.values()), 50) ]
    verb_lim = 0
    for batch in artist_batches:
        sleep(0.01)
        response = sp.artists(batch)
        for artist in response['artists']:
            for genre in artist['genres']:
                for cogenre in artist['genres']:
                    if genre != cogenre:
                        g[genre].add(cogenre)

            if verbose and len(g.keys()) > verb_lim:
                print 'Processed %d items...' % len(g.keys())
                verb_lim += 100

    G = g
    S2G = s2g
    return g


