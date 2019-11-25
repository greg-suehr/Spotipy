# Datastore is a per-application instance of the Datastore framework
# A Store is a database table mapping (identifier, data)
# The Cache is a key store of data from various Stores used in analysis
#
# A top level request is a per-application defined method that extends an API method,
#  for example `spotipy.get_all_user_playlists`. A top level request may simply pass
#  it's arguments to an API and return the results. 
#    - get_all requests typically implement a `while, offset` loop around API requests
#    - get_by_ids may do the same, unless size(ids) is less than the API's limit

import sqlite3
# import framework # TODO: define a framework module for messaging, etc
from collections import defaultdict
from sqlite3_util import stringify_list, field_to_indice, select_primary_key

DATASTORE = 'spotipy.db'  # TODO: load per-application configurations from .conf
LIMIT = 50  # universal limit for all requests

conn = sqlite3.connect(DATASTORE)

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

def load_from_datastore(c, store_table_name, identifier_fields, identifiers):
    """Load seen data from a local Store into the Cache.
    
    Args:
        c (sqlite3.Cursor): cursor to the Datastore
        store_table_name (string): request_mapping.store_table_name
        identifier_fields (list): list of field_mapping.fields in $store_table_name
        identifiers (list): list of tuples, must match the size of identifier_fields
         NOTE: multi-field lookups are not yet supported.

    Returns:
        results (dict): a one level dict containing two lists:
            found: a flexible list of data from the Datastore
            missed: a trimmed list of identifiers to pass along
    """
    identifiers = stringify_list(identifiers)
    # TODO: verify store_table_name exists in the schema?
    #       or interpret the sqliteOperationalError later?
    # TODO: verify that len(identifier_fields) == len(identifiers[0]) ? or save time?
    results = c.execute("""SELECT * FROM %s WHERE %s IN (%s)""" % (store_table_name,  
                        identifier_fields[0], "','".join(identifiers).join(["'","'",])))
    # TODO: reformat load_from_datastore to support multi-field lookups
    found = results.fetchall()

    results = c.execute("""SELECT %s FROM %s WHERE %s IN (%s)""" % (identifier_fields[0],  
                                                                    store_table_name,
                        identifier_fields[0], "','".join(identifiers).join(["'","'",])))
    found_ids = results.fetchall()
    
    missing_ids = []
    for identifier_tuple in identifier_fields:
        if identifier_tuple not in identifier_fields:
            missing.append(identifier_tuple)

    return { 'found': found, 'missing': missing_ids }

def load_from_service(cursor, store_table_name, identifiers):
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
