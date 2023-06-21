#!/usr/bin/python3

#to test my console conntion to mysql

import MySQLdb
import unittest


class TableRecordCountTestCase(unittest.TestCase):
    def setUp(self):
        self.con = MySQLdb.connect(host="MySql", port=3306, user="MySql", passwd="MySql", db="MySql", charset="utf8")
        self.cursor = self.con.cursor()

        self.cursor.execute('''CREATE TABLE state (
            id INTEGER PRIMARY KEY,
            name VARCHAR(256) NOT NULL
        )''')

        self.cursor.execute("INSERT INTO state (name) VALUES ('California')")
        self.cursor.execute("INSERT INTO state (name) VALUES ('Abuja')")
        self.cursor.execute("INSERT INTO state (name) VALUES ('Lagos')")

        def test_record_count(self):
        # Execute a query to get the record count
            self.cursor.execute("SELECT COUNT(*) FROM state")
            count = self.cursor.fetchall()

        # Assert the count matches the expected value
            self.assertEqual(count, 3)

        def tearDown(self):
        # Clean up resources
            self.cursor.close()
            self.con.close()

if __name__ == '__main__':
    unittest.main()


