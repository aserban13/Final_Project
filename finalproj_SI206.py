import praw
import secrets
import json
import ast
import webbrowser
import sqlite3 as sqlite

client_id = secrets.CLIENT_ID
client_secrets = secrets.CLIENT_SECRET
username = secrets.USERNAME
password = secrets.PASSWORD
# YourUsername
# u/hellenhello123
# ChangeMeClient/0.1]
my_user_agent = "ChangeMeClient/0.1] by u/hellenhello123"
# UAuthentication, these are the credentials that it will need
reddit = praw.Reddit(client_id=client_id,
                     client_secret=client_secrets,
                     user_agent=my_user_agent,
                     username=username,
                     password=password)

CACHE_FNAME = 'cache_file_name.json'

# print(reddit.user.me())


#Access Reddits account and find the needed information from it
#Parameters: a quert, search word
#returns the top 10 searche titles, the score, and the url for that query
def search_subreddit(query):
    subreddit = reddit.subreddit("all").search(query, sort='hot')
    results = []
    for submission in subreddit:
        title = submission.title  # Output: the submission's title
        score = submission.score  # Output: the submission's score
        url = submission.url    # Output: the submission's url
        tup = (score, title, url)
        results.append(tup)
    results.sort(reverse=True)
    return results[:10]

# This is the official caching functions used later on to make these searches
# Parameter: the search term, query
# Returns: the cached data whether or not it was cached or not.
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
    # Returns: will create two tables if they do not already exit
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

    # Parameter: A search term for it to gather data and add onto the two tables
    # Returns: Will insert data into two tables: Title and Details
    def insert_value(query):
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
            # print(dicti[num][1])

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
    def access_query(query):
        conn = sqlite.connect(DB_NAME)
        cur = conn.cursor()
        # Join the two tables and then find the results corresponding
        # with it
        # extract the titles and the urls

        access_statement = "SELECT Title_Top10, Urls FROM [Details] as D"
        access_statement += " JOIN Title ON Title.Id = D.TitleId "
        access_statement += " WHERE Title.Title = '" + query +"' "
        # print(access_statement)
        cur.execute(access_statement)
        conn.commit()
        # print(cur.fetchall())
        return cur.fetchall()

    def access_url(title_name):
        conn = sqlite.connect(DB_NAME)
        cur = conn.cursor()
        statement = "SELECT Urls FROM Details WHERE Title_Top10 "
        if "'" and '"' in title_name:
            r = title_name[:20]
            if "'" and '"' in r:
                r = title_name[:10]
                if '"' in r:
                    statement += " LIKE '" + r + "%'"
                elif "'" in r:
                    statement += ' LIKE "' + r + '%"'
                else:
                    statement += " LIKE '" + r + "%'"
            elif '"' in r:
                statement += " LIKE '" + r + "%'"
            elif "'" in r:
                print("I am here ")
                statement += ' LIKE "' + r + '%"'
            else:
                statement += " LIKE '" + r + "%'"
        elif '"' in title_name:
            statement += "== '" + title_name + "'"
        elif "'" in title_name:
            statement += '== "' + title_name + '"'
        else:
            statement += "== '" + title_name + "'"
        cur.execute(statement)
        conn.commit()
        return cur.fetchone()[0]


# interactive function
def interactive():
    print("\n\n\t\tHello, Welcome to Andreea's Program:\n")
    statement = "   This program searches for the top ten subreddits from Reddit."
    statement += "\n   All of these outputs are from Reddit currently."
    print(statement)
    print("\n   If you would like to quit the program, please type in 'exit'.\n")
    say = input('Please type a search term: ')
    DB.create_table()
    list_of_searches = []
    num = 0
    while(say != 'exit'):
        num += 1
        DB.insert_value(str(say))
        if say == 'more':
            break
        else:
            pass
        tup = (num, str(say))
        list_of_searches.append(tup)

        print("\n\ttype 'more' for more deatils\n")
        say = input('Please type a search term: ')

        if say == 'exit':
            break
        else:
            pass

# What to do when user types 'more'
    if say == 'more':
        if len(list_of_searches) == 0:
            print("\n\tIt seems that you haven't searched any other terms.")
            print("\tIf you would like to continue with this option, ")
            print("\trun the program again and enter more search keys\n")
        else:
            print('\n\tBelow are your previous searches:')
            for s in list_of_searches:
                print('\t',s[0], s[1])
            inside = input("Please select a NUMBER that you would like to explore more about: ")
            search = 'word'
            inside = int(inside)
            for s in list_of_searches:
                if inside == s[0]:
                    search = s[1]
                else:
                    pass
            if search == 'word':
                # not a valid option
                print("This is not a valid number.")
            else:
                r = DB.access_query(search)
                n = 0
                output = []
                print("\nThese are the top 10 subreddits on Reddit from the search: ", search,"\n")
                for c in r:
                    n += 1
                    t = (n,c[0])
                    output.append(t)
                    print(n, c[0])
                print("\nIf you would like to go back to enter in more search terms, type 'back'.")
                print("If you would like to open up the page of an output, type the number of the title.")
                command = input("Please enter a command: ")
                while command != 'exit':
                    print("If you would like to go back to enter in more search terms, type 'back'.")
                    print("If you would like to open up the page of an output, type the \nnumber of the title.\n\n")

                    if command == 'back':
                        interactive()
                    else:
                        title = 'url'
                        for n in output:
                            if n[0] == int(command):
                                title = n[1]
                            else:
                                pass
                        if title == 'url':
                            pass
                        else:
                            url = DB.access_url(title)
                            webbrowser.open_new_tab(url)
                    pass
                    command = input("Please enter a command: ")
                    if command == 'exit':
                        break
    else:
        pass

    print('\n\nYou are quiting from this Program!')
    print('I hoped you enjoyed it!\n')

# interactive()
