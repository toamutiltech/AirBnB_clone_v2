#!/usr/bin/python3

#to test my console conntion to mysql

import MySQLdb
import unittest


class TableRecordCountTestCase(unittest.TestCase):
    def setUp(self):
        self.con = MySQLdb.connect(host="localhost", port=3306, user="root", passwd="root", db="mysql", charset="utf8")
        self.cur = self.con.cursor()

        self.cur.execute('''CREATE TABLE state (
            id INTEGER PRIMARY KEY,
            name VARCHAR(256) NOT NULL
        )''')

        self.cur.execute("INSERT INTO state (name) VALUES ('California')")
        self.cur.execute("INSERT INTO state (name) VALUES ('Abuja')")
        self.cur.execute("INSERT INTO state (name) VALUES ('Lagos')")

        def test_record_count(self):
        # Execute a query to get the record count
            self.cur.execute("SELECT COUNT(*) FROM state")
            count = self.cur.fetchone()[0]

        # Assert the count matches the expected value
            self.assertEqual(count, 3)

        def tearDown(self):
        # Clean up resources
            self.cur.close()
            self.con.close()

if __name__ == '__main__':
    unittest.main()


