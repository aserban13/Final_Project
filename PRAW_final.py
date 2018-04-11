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

reddit = praw.Reddit(client_id=client_id,
                     client_secret=client_secrets,
                     user_agent=my_user_agent,
                     username=username,
                     password=password)
CACHE_FNAME = 'cache_file_name.json'



# try:
#     cache_file = open(CACHE_FNAME, 'r')
#     cache_contents = cache_file.read()
#     # CACHE_DICTION = json.loads(cache_contents)
#     cache_file.close()
# # if there was no file, no worries. There will be soon!
# except:
#     CACHE_DICTION = {}

#
#
#
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

#
#
#
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

DB_NAME = 'reddit_db.sqlite'

def db_function(query):
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

    cd = caching_data(query)
    data = ast.literal_eval(cd)
    for d in data:
        # d[0].strip()
        q = (d[0].strip())
        add_statement = '''
            INSERT INTO 'Title'
            VALUES(NULL, ?)
         '''
        cur.execute(add_statement, q)
        conn.commit()



    # statement = '''
    #     CREATE TABLE 'Urls' (
    #         'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
    #         'TitleId' INTEGER,
    #         'Urls' TEXT
    #     )
    #     '''
    # cur.execute(statement)
    # conn.commit()

caching_data('winter')
caching_data('summer')
caching_data('c')
caching_data('cd')
caching_data('cd')
# caching_data('cdf')
# caching_data('cde')
# search_subreddit('cool')
