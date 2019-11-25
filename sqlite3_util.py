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
    c = conn.cursor()
    results = c.execute("PRAGMA TABLE_INFO(%s)" % table)
    pk_field = field_to_indice(results, 'pk')
    name_field = field_to_indice(results, 'name')

    for _ in results:
        if _[pk_field] == 1:
            return _[name_field]

    raise ValueError('%s doesnt have a primary key?!')
