import sqlite3
from collections import defaultdict

def stringify_list(l):
    """Turn a string of any object to a list of strings

    Useful for nonsense like "','".join(identifiers).join(["'","'",])
    """
    if type(l[0]) == str and type(l[-1]) == str: return l
    m = [None] * len(l)
    for i, _ in enumerate(l):
        m[i] = str(_)
    return m

def unpack_list_of_tuples(l):
    """Take a list of 1-tuples, e.g. [(1,),(2,),...], and return a list of strings"""
    m = [None] * len(l)
    for i, _ in enumerate(l):
        m[i] = str(_[0])
    return m

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
    c = conn.cursor() # TODO: figure out when I should be passing Connections vs Cursors
    results = c.execute("PRAGMA TABLE_INFO(%s)" % table)
    pk_field = field_to_indice(results, 'pk')
    name_field = field_to_indice(results, 'name')

    for _ in results:
        if _[pk_field] == 1:
            return _[name_field]

    raise ValueError('%s doesnt have a primary key?!')

def select_dicts_of_fields(conn, query):
    # split string between SELECT ... FROM
    #  if matches '*', error: "Explicit field mapping required."

    fields = [ _.strip() for _ in query.split("SELECT")[1].split("FROM")[0].split(",")] # :)

    # leave the rest (tables exist, contain fields, ...) up to sqlite3.OperationalErrors

    c       = conn.cursor()
    results = c.execute(query) # TODO: make select_dict_of_fields injection-proof
    rows    = results.fetchall()

    return_list = [None] * len(rows)
    dictionary_format = defaultdict()                  # TODO: should select_dicts_of_fields
    for field in fields: dictionary_format[field] = '' # fill with EMPTIES or NULLS?
    dictionary_format = dict(dictionary_format)

    for r, row in enumerate(rows):
        dictionary = dictionary_format.copy() # deep copy
        for f, field in enumerate(fields):
            dictionary[field] = row[f]
        return_list[r] = dictionary

    return return_list
