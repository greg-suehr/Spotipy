import unittest
from datastore import field_to_indice, select_primary_key
     # TODO: eventually, these methods will be moved to sqlite3_util

import sqlite3 
class field_to_indice_tester(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        self.conn = sqlite3.connect('test.db')
        self.c = self.conn.cursor()

        # Create a stub table
        try:
            self.c.execute("CREATE TABLE test (id INTEGER PRIMARY key, a TEXT, b TEXT)")
        except sqlite3.OperationalError: pass  # this is "table test already exists"
        
        super(field_to_indice_tester, self).__init__(*args, **kwargs)

    def test_primary_key(self):
        results = self.c.execute("SELECT * FROM test")
        self.assertEqual(field_to_indice(results, 'id'), 0)

    def test_another_key(self):
        results = self.c.execute("SELECT * FROM test")
        self.assertEqual(field_to_indice(results, 'b'), 2)


class select_primary_key_tester(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        self.conn = sqlite3.connect('test.db')
        self.c = self.conn.cursor()

        # Create a stub table
        try:
            self.c.execute("CREATE TABLE test (id INTEGER PRIMARY key, a TEXT, b TEXT)")
        except sqlite3.OperationalError: pass  # this is "table test already exists"
        
        super(select_primary_key_tester, self).__init__(*args, **kwargs)

    def test_primary_key(self):
        self.assertEqual(select_primary_key(self.conn, 'test'), 'id')


if __name__ == '__main__':
    unittest.main()
