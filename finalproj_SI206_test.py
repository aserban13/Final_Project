 # You must create at least 3 test cases and use
 # at least 15 assertions or calls to ‘fail( )’
from finalproj_SI206 import *
import unittest
DB_NAME = 'reddit_db.sqlite'

# Inserting values into the table
# There are 4 assert statements in here
class TestTitleTable(unittest.TestCase):
# checks the caching
# 7
    def test_caching(self):
        # caching_data returns the score, titlename, and the url
        find = "Anxiety is like when video game combat music is playing but you can't "
        find += 'find any enemies.'
        r = caching_data('find')
        q = ast.literal_eval(r)
        self.assertEqual(len(q), 10)
        self.assertEqual(len(q[0]), 3)
        self.assertTrue(q[0][0] >= q[1][0])
        self.assertEqual(q[0][1], find)


        hello = "I'm no longer banned from playing in magic tournaments. I have risen from the ashe"
        hello += "s to defend my honor against the scrubs of Earth. Prepare yourselves."
        a = caching_data('hello')
        q = ast.literal_eval(a)
        self.assertEqual(len(q), 10)
        self.assertEqual(len(q[0]), 3)
        self.assertTrue(q[0][0] >= q[1][0])
        self.assertEqual(q[0][1], hello)

        b = caching_data('hello')
        r = ast.literal_eval(b)
        self.assertEqual(r, q)










# Checks the outcome of the title and the details table
# 7
    def test_inserting_unique_titles(self):
        conn = sqlite.connect(DB_NAME)
        cur = conn.cursor()
        #
        drop_table = '''
        DROP TABLE IF EXISTS  Title;
        '''
        cur.execute(drop_table)
        conn.commit()
        stat = '''
        DROP TABLE IF EXISTS Details;
        '''
        cur.execute(stat)
        conn.commit()

        DB.create_table()

        DB.insert_value('hello')
        check_title = '''
            SELECT Title, COUNT(Title)
            FROM Title
        '''
        cur.execute(check_title)
        conn.commit()
        # print(cur.fetchall())
        # checks the title table
        k  = cur.fetchall()[0]
        self.assertEqual(k[0], 'hello')
        self.assertTrue(k[1], 1)


        # checks the details table
        titles = '''
            SELECT Title_Top10, Urls
            FROM Details
        '''
        cur.execute(titles)
        conn.commit()
        # print(cur.fetchall())
        k  = cur.fetchall()
        # Check the outputs for the
        check4 = 'Friendly penguin hops up to say hello.'
        check4url = 'https://i.imgur.com/xWPixwD.gifv'
        check10 = 'This guy broke the fourth wall to say hello'
        check10url = 'https://gfycat.com/ReasonableScrawnyGeese'

        self.assertEqual(len(k), 10)
        self.assertEqual(k[3][0], check4)
        self.assertEqual(k[3][1], check4url)
        self.assertEqual(k[9][0], check10)
        self.assertEqual(k[9][1], check10url)

        conn.close()













# 2 more results
# checks the total length of title table and details table
# 3
    def test_length_result(self):
        conn = sqlite.connect(DB_NAME)
        cur = conn.cursor()

        drop_table = '''
        DROP TABLE IF EXISTS  Title;
        '''
        cur.execute(drop_table)
        conn.commit()
        stat = '''
        DROP TABLE IF EXISTS Details;
        '''
        cur.execute(stat)
        conn.commit()

        DB.create_table()
        # length of 0
        stat = '''
        SELECT TitleId
        FROM Details
        '''
        cur.execute(stat)
        conn.commit()
        r = cur.fetchall()
        self.assertEqual(len(r), 0)

        # length more than 0
        DB.insert_value('first')
        DB.insert_value('second')
        result = DB.access_query('first')
        self.assertTrue(len(result)<= 10)

        DB.insert_value('third')
        statement = '''
        SELECT COUNT(*)
        FROM Details
        '''
        cur.execute(statement)
        conn.commit()

        r = cur.fetchone()[0]
        self.assertTrue(r <= 30)
        conn.close()














# Join the tables and get the query search and
# that there is a primary key
# 1
    def test_join_table(self):
        conn = sqlite.connect(DB_NAME)
        cur = conn.cursor()

        drop_table = '''
        DROP TABLE IF EXISTS  Title;
        '''
        cur.execute(drop_table)
        conn.commit()
        stat = '''
        DROP TABLE IF EXISTS Details;
        '''
        cur.execute(stat)
        conn.commit()

        DB.create_table()

        DB.insert_value('hello')
        DB.insert_value('hey')

        statement = '''
        SELECT Title.Id
        FROM Title
        JOIN Details as D ON Title.Id == D.TitleId
        WHERE D.Title_Top10 == 'Oh hey John Mayer'
        '''
        cur.execute(statement)
        conn.commit()

        result = cur.fetchone()
        self.assertEqual(result[0], 2)
        conn.close()


if __name__ == '__main__':
    unittest.main()
