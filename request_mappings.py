from datastore import load_from_datastore, load_from_service
from sqlite3_util import select_dict_of_fields

import sqlite3
import spotipy as sp


# naming convention is request_format + store_table_name
def user_playlist_tracks_user_tracks(*args, **kwargs):
    # this is a good example to start with, because we'll never check store for


    ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ##
    # This block should be abstracted out before implemented another request_mapping
    #
    # CALL API
    # usually, you'll start with a call to the `request_format`
    response = sp.user_playlist_tracks(*args, **kwargs)
    #
    # UNPACK
    tracks = [ r['track'] for r in response['items'] ]
    #
    # RETURN OR COLLATE
    if len(tracks) == response['total']: 
        continue
    else:
        offset = response['total']
        while len(tracks) < response['total']:
            resposnse = sp.user_playlist_tracks(*args, *kwargs, offset=offset)
            tracks += [ r['track'] for r in response['items'] ]
            offset += response['total']
    #
    ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ##            
    conn = sqlite3.connect('spotipy.db')
    c    = conn.cusor()

    
    request_mapping_id = select_dict_of_fields(c, "SELECT request_mapping_id")[0]['request_mapping_id']
    results = select_dict_of_fields(c,      # TODO: make select_dict_of_fields injection proof
                          """SELECT store_table_name, store_field_name 
                             FROM field_mappings         
                             JOIN request_field_mappings USING (field_mapping_id)
                             WHERE request_mapping_id = %s """ % request_mapping_id)


    return 
    
    

def current_user_top_tracks_user_tracks(*args, **kwargs):
    pass

def current_user_saved_tracks_user_tracks(*args, **kwargs)
    pass

# as good practice, write a method for each request_mapping and "super" method per store_table_name
def user_tracks(*args, **kwargs):
    user_playlist_tracks_user_tracks(*args, **kwargs)
    current_user_top_tracks_user_tracks(*args, **kwargs)
    current_user_saved_tracks_user_tracks(*args, **kwargs)


