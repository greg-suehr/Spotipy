import spotipy.util as util
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOauthError
from collections import defaultdict


def chunk(l,n):
    for i in range(0, len(l), n):  
        yield l[i:i + n]


class Classifier(Spotify):
    def __init__(self, user, auth='playlist-read-private'):
        super().__init__()
        self.user   = user
        self.auth   = auth
        self.token  = self.authenticate()
        self.sp     = Spotify(auth=self.token)
        self.artist_cache = defaultdict()
        self.playlist_track = defaultdict()

        
    def authenticate(self):
        token   = util.prompt_for_user_token(self.user,self.auth)
        self.sp = Spotify(auth=token)
        
        return token            
                
    def _populate_artist_cache(self):
        if len(self.playlist_track) == 0:
            self._populate_playlist_tracks_cache()

        for pid,tracklist in self.playlist_track.items():
            for track in tracklist:
                for artist in track['artists']:
                    self.artist_cache[artist['uri']] = None


        artists = []
        for aids in chunk(list(self.artist_cache.keys()), 50):
            artists += self.sp.artists(aids)['artists']

        for artist in artists:
            self.artist_cache[artist['uri']] = artist

            
    def _populate_playlist_tracks_cache(self):
        self.playlist_track = self.all_playlist_tracks(self.all_playlists())
        

    
    def all_playlists(self):
        p = self.items_from_method('items',
                                   self.sp.user_playlists,
                                   self.user)
        
        p = self.filter_items(p, ['owner','id'], self.user)

        return p

        
    def add_genres_to_playlist_tracks(self, pid, group='track'):
        """
        Inputs
        user - string - Spotify username matching token
        pid - string - playist id or uri
        group - enum - 'track','artist'
        
        Returns
          tracks{'uri' : {'name' : str, 'genres' : list}}
          tracks{'uri' : {'artists' : {'uri' : int, name : str, genres : list
        """
        if len(self.artist_cache) == 0:
            self._populate_artist_cache()
            
        playlist_track = self.items_from_method('items',
                                   self.sp.playlist_tracks,
                                   pid)

        tracks = defaultdict()
        for track in playlist_track:
            track  = track['track']
            genres = []

            aids    = [_['uri'] for _ in track['artists']]
            
            artists = [self.artist_cache[aid] for aid in aids]

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

        playlist_tracks = defaultdict()
        for playlist in playlists:
            pid          = playlist['uri']
            items = self.items_from_method('items',self.sp.playlist_tracks,pid)
            playlist_tracks[pid] = [_['track'] for _ in items]
                                                  
        return playlist_tracks


    def playlist_genres_by_artist(self, playlists):
        """
        Inputs
        playlists - list of playlist ids or uris
        
        Returns
        genres - dict mapping artist id:name to list of genres
        """
        
        genres = defaultdict(list)
        playlist_tracks = self.all_playlist_tracks(playlists)
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
        """
        Iterates through a list of nested objects, stepping down the object
        hierarchy 
        """
        remain = []

        # if this into a list comprehension, I wouldn't comprehend it
        for item in items:
            child = item
            for key in keys:
                child = child[key]
            if child == match:
                remain.append(item)
                
        return remain
