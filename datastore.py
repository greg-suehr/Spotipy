import sqlite3
# import framework # TODO: define a framework module for messaging, etc
from collections import defaultdict

# Datastore is a per-application instance of the Datastore framework
# A Store is a database table mapping (identifier, data)
# The Cache is a key store of data from various Stores used in analysis
#
# A top level request is a per-application defined method that extends an API method,
#  for example `spotipy.get_all_user_playlists`. A top level request may simply pass
#  it's arguments to an API and return the results. 
#    - get_all requests typically implement a `while, offset` loop around API requests
#    - get_by_ids may do the same, unless size(ids) is less than the API's limit


DATASTORE = 'spotipy.db'  # TODO: load per-application configurations from .conf
LIMIT = 50  # universal limit for all requests

conn = sqlite3.connect(DATASTORE)


# These are actually sqlite3 utility functions - should be broken out
def field_to_indice(cursor, field_name, table=None):
    """Use a sqlite3 cursor.description to translate field names into the indice we'll
       find that data in the returned tuples.

       Specify `table` to provide a better error message.
    """
    mapping = defaultdict()
    for indice, _ in enumerate(cursor.description):
        if _[0] == field_name: # _ = ('request_format',None,None,None,None,None,None)
            return indice 

    # TODO: Report ERROR, WARNING, MESSAGE up to a framework module
    if table is not None:
        raise ValueError('%s is not a field in %s.' % (field_name, table))
    else:
        raise ValueError('%s is not a known field.' % field_name)

def select_primary_key(conn, table):
    c = conn.cursor()
    results = c.execute("PRAGMA TABLE_INFO(%s)" % table)
    pk_field = field_to_indice(results, 'pk')
    name_field = field_to_indice(results, 'name')
    
    for _ in results:
        if _[pk_field] == 1:
            return _[name_field]

    raise ValueError('%s doesnt have a primary key?!')


# Thus begins the DataStore
def interpret_request(conn, request_format):
    """Translate a top-level request to an (identifier, data) mapping and search
       Datastore for a known Store.
    """
    c = conn.cursor()
    results = c.execute("SELECT * FROM request_mappings WHERE request_format = '%s'"
                      % request_format)  # TODO: is this safe, or open to injection?
    store = results.fetchall()

    if len(store) > 1: 
        raise ValueError('Multiple store mappings defined for %s' % top_level_request)
    if len(store) == 0: 
        raise ValueError('No store mapping defined for %s' % top_level_request)

    store_table_name = field_to_indice(results, 'store_table_name', 'request_mappings')
    return store[0][store_table_name]


def load_from_datastore(conn, store_table_name, identifiers):
    """Load seen data from a local Store into the Cache.
    """
    pass

def load_from_service(conn, store_table_name, identifiers):
    """Load unseen data from a local Store into the Cache.
    """
    pass

def clean_datastore():
    """Delete records from datastore based on a scheduled expiration_date defineded
       per Store.
    """
    pass
    
if __name__ == '__main__':
    print(interpret_request(conn, 'get_all_user_playlists'))
