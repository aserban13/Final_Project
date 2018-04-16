 # You must create at least 3 test cases and use
 # at least 15 assertions or calls to ‘fail( )’
from PRAW_final import *
import unittest
DB_NAME = 'reddit_db.sqlite'

class TestTitleTable(unittest.TestCase):
    def inserting_unique_titles(self):
        conn = sqlite.connect(DB_NAME)
        cur = conn.cursor()

        drop_table = '''
        DROP TABLE IF EXISTS  Title
        DROP TABLE IF EXISTS Details
        '''

        cur.execute(drop_table)
        conn.commit()

        DB.create_table()
        DB.insert_values('hello')
        DB.insert_values('hello')
        check_title = '''
            SELECT Title, COUNT(Title)
            FROM Title
        '''
        cur.execute(check_title)
        conn.commit()
        print(cur.fetchall())

        self.assertEqual(cur.fetchall()[0], 'hello')
        self.assertEqual(cur.fetchall()[1], 0)

        conn.close()


         # return 0



if __name__ == '__main__':
    unittest.main()
