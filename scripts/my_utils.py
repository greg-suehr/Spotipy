import spotipy.util as util
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOauthError
from collections import defaultdict


class Classifier(Spotify):
    def __init__(self, user, auth='playlist-read-private'):
        super().__init__()
        self.user   = user
        self.auth   = auth
        self.token  = self.authenticate()
        self.sp     = Spotify(auth=token)
        self.acache = defaultdict()

        
    def authenticate(self):
        token   = util.prompt_for_user_token(self.user,self.auth)
        self.sp = Spotify(auth=token)
        
        return token


    def all_playlists(self):
        p = self.items_from_method('items',
                                   self.sp.user_playlists,
                                   self.user)
        
        p = self.filter_items(p, ['owner','id'], self.user)

        return p

    
    def playlist_genres(self, pid, group='track'):
        """
        Inputs
        user - string - Spotify username matching token
        pid - string - playist id or uri
        group - enum - 'track','artist'
        
        Returns
          tracks{'uri' : {'name' : str, 'genres' : list}}
          tracks{'uri' : {'artists' : {'uri' : int, name : str, genres : list
        """
        ptrack = self.items_from_method('items',
                                   self.sp.playlist_tracks,
                                   pid)

        def chunk(l,n):
            for i in range(0, len(l), n):  
                yield l[i:i + n]

        # add to the artists cache
        for track in ptrack:
            for artist in track['track']['artists']:
                self.acache[artist['uri']] = None

        artists = []
        for aids in chunk(list(self.acache.keys()), 50):
            artists += self.sp.artists(aids)['artists']

        for artist in artists:
            self.acache[artist['uri']] = artist
            
        tracks = defaultdict()
        for track in ptrack:
            track  = track['track']
            genres = []

            aids    = [_['uri'] for _ in track['artists']]
            
            artists = [self.acache[aid] for aid in aids]

            for artist in artists:
                genres += [_ for _ in artist['genres']]
                aids   += [artist['uri']]
                
            uri  = track['uri']
            tracks[uri] = { uri :
                            { 'name'    : track['name'],
                              'genres'  : genres,
                              'artists' : aids
                             }
                           }
        return tracks


    def all_playlist_tracks(self, playlists=None):
        if playlists is None:
            playlists = self.all_playlists()

        ptracks = defaultdict()
        for playlist in playlists:
            pid          = playlist['uri']
            ptracks[pid] = self.items_from_method('items',
                                                  self.sp.playlist_tracks,
                                                  pid)
        return ptracks



    def playlist_genres_by_artist(self, playlists):
        """
        Inputs
        playlists - list of playlist ids or uris
        
        Returns
        genres - dict mapping artist id:name to list of genres
        """
        
        genres = defaultdict(list)
        ptracks = self.all_playlist_tracks(playlists)
        return genres

    
    def items_from_method(self,key,method,*args,**kwargs):
        items = []
        offset = 0
        while True:
            r = method(*args,**kwargs,offset=offset)
            items += [item for item in r[key]]
            offset += r['limit']
            if len(r[key]) < r['limit']:
                break

        return items

    
    def filter_items(self,items,keys,match):
        remain = []

        for item in items:
            child = item
            for key in keys:
                child = child[key]
            if child == match:
                remain.append(item)
                
        return remain
