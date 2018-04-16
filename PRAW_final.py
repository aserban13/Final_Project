import praw
import secrets
import json
import ast
import sqlite3 as sqlite

client_id = secrets.CLIENT_ID
client_secrets = secrets.CLIENT_SECRET
username = secrets.USERNAME
password = secrets.PASSWORD
my_user_agent = "ChangeMeClient/0.1] by YourUsername"
# UAuthentication, these are the credentials that it will need
reddit = praw.Reddit(client_id=client_id,
                     client_secret=client_secrets,
                     user_agent=my_user_agent,
                     username=username,
                     password=password)
CACHE_FNAME = 'cache_file_name.json'


#Access Reddits account and find the needed information from it
#Parameters: a quert, search word
#returns the top 10 searche titles, the score, and the url for that query
def search_subreddit(query):
    subreddit = reddit.subreddit("all").search(query, sort='hot')
    results = []
    for submission in subreddit:
        title = submission.title  # Output: the submission's title
        score = submission.score  # Output: the submission's score
        id = submission.id   # Output: the submission's ID
        url = submission.url    # Output: the submission's url
        # print(title, '\n', url, '\n')
        tup = (score, title, url)
        # print(type(score))
        results.append(tup)
    # print(results)
    results.sort(reverse=True)
    # print(results[:10])
    return results[:10]

def caching_data(query):
    CACHE_DICTION = {}
    unique_url= 'https://www.reddit.com/search?q=' + query + '&sort=top'
    opening = CACHE_FNAME.strip()
    fw = open(opening)
    parse = fw.read()
    dicti = ast.literal_eval(parse)
    if unique_url in dicti:
        fw = open(opening)
        print("Fetching cached data...")
        parse = fw.read()
        # will convert the string to a dictionary
        dicti = ast.literal_eval(parse)
        CACHE_DICTION[unique_url] = dicti[unique_url]
        fw.close()
        # print(CACHE_DICTION[unique_url])
        return CACHE_DICTION[unique_url]
        # return CACHE_DICTION[unique_url]
    else:
        print("Making a request for new data...")
        result = search_subreddit(query)
        CACHE_DICTION[unique_url] = str(result)
        fw = open(CACHE_FNAME, "w")
        fw.write(str(CACHE_DICTION))
        # print(CACHE_DICTION[unique_url])
        fw.close()
        return CACHE_DICTION[unique_url]


DB_NAME = 'reddit_db.sqlite'
# This class has all the functions
class DB:
    def create_table():
        conn = sqlite.connect(DB_NAME)
        cur = conn.cursor()
        try:
            statement = '''
                CREATE TABLE 'Title' (
                    'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
                    'Title' TEXT
                );'''
            cur.execute(statement)
            conn.commit()
        except:
            pass
        try:
            statement = '''
                CREATE TABLE 'Details' (
                    'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
                    'TitleId' INTEGER,
                    'Title_Top10' TEXT,
                    'Urls' TEXT
                )
                '''
            cur.execute(statement)
            conn.commit()
        except:
            pass


    def insert_values(query):
        conn = sqlite.connect(DB_NAME)
        cur = conn.cursor()

        # create_table()
    # ______________________Add values onto the Title and the Details table_____________________

        # Makes sure that the title is unique in the table
        # so that there isn't more than mone title in each
        # table
        unique_title = '''
            SELECT Title
            FROM Title
        '''
        cur.execute(unique_title)
        d = cur.fetchall()
        similar = 0
        for c in d:
            if c[0] == query:
                similar += 1
            else:
                pass
        if similar == 0:
            add_statement = '''
                INSERT INTO 'Title'
                VALUES(NULL, ?)
             '''
            cur.execute(add_statement, [query])
            conn.commit()

            # Make a dictionary of the unique TitleId in a dictionary
            # In the dictionary, there is a title and the unique primary id
            extract_id = {}

            extract = 'SELECT Title, Id FROM Title'
            cur.execute(extract)
            conn.commit()
            for c in cur:
                extract_id[c[0]] = c[1]

        # Adding values on the Details Table
            parse = caching_data(query)
            dicti = ast.literal_eval(parse)

            titles = []
            urls = []

            for num in range(0,10):
                tupl = (extract_id[query], dicti[num][1], dicti[num][2] )
                add_details = '''
                    INSERT INTO 'Details'
                    VALUES(NULL, ?, ?, ?)
                '''
                cur.execute(add_details, tupl)
                conn.commit()
        else:
            pass

# DB.insert_values('watr')
# caching_data('winter')
# caching_data('summer')
# caching_data('c')
# caching_data('cd')
# caching_data('cd')
# caching_data('cdf')
# caching_data('cde')
# search_subreddit('cool')
