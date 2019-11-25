import unittest
import sqlite3 

from sqlite3_util import stringify_list, field_to_indice, select_primary_key, select_dicts_of_fields

class field_to_indice_tester(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        self.conn = sqlite3.connect('test.db')
        self.c = self.conn.cursor()

        # Create a stub table
        try:
            self.c.execute("CREATE TABLE test (id INTEGER PRIMARY key, a TEXT, b TEXT);")
            self.conn.commit()
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
            self.c.execute("CREATE TABLE test (id INTEGER PRIMARY key, a TEXT, b TEXT);")
            self.conn.commit()
        except sqlite3.OperationalError: pass  # this is "table test already exists"
        
        super(select_primary_key_tester, self).__init__(*args, **kwargs)

    def test_primary_key(self):
        self.assertEqual(select_primary_key(self.conn, 'test'), 'id')

class select_dicts_of_fields_tester(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        self.conn = sqlite3.connect('test.db')
        self.c = self.conn.cursor()

        # Create a stub table
        try:
            self.c.execute("DROP TABLE test;")
            self.c.execute("CREATE TABLE test (id INTEGER PRIMARY key, a TEXT, b TEXT);")
            self.c.execute("INSERT INTO test VALUES (1, 'A', 'B');")
            self.c.execute("INSERT INTO test VALUES (2, 'x', 'y');")
            self.conn.commit()
        except sqlite3.OperationalError: pass  # this is "table test already exists"

        super(select_dicts_of_fields_tester, self).__init__(*args, **kwargs)

    def test_find_all(self):
        self.assertEqual(select_dicts_of_fields(self.conn, "SELECT a, b FROM test"),
                         [{'a': 'A', 'b': 'B'}, {'a': 'x', 'b': 'y'}])

    def test_find_some(self):
        self.assertEqual(select_dicts_of_fields(self.conn, "SELECT a, b FROM test WHERE id IN (1,2,2999)"),
                         [{'a': 'A', 'b': 'B'}, {'a': 'x', 'b': 'y'}])

    def test_find_none(self):
        self.assertEqual(select_dicts_of_fields(self.conn, "SELECT a, b FROM test WHERE id IN (2999)"),
                         [])

class stringify_list_tester(unittest.TestCase):
    pass

class unpack_list_of_tuples_tester(unittest.TestCase):
    pass


if __name__ == '__main__':
    unittest.main()
