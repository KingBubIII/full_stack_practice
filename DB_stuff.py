import pymysql
from datetime import date
import classes

login_details = open('sql_login.txt','r').readlines()
_db_conn = pymysql.connect(user=login_details[0].strip(), password=login_details[1].strip(), host=login_details[2].strip(), db=login_details[3].strip())
_cursor = _db_conn.cursor()

def login(identifier):
    # queries for an account with matching credentials from the form
    if type(identifier) is tuple:
        query = _cursor.execute("""SELECT * FROM user_info WHERE email=%s AND password=%s""",(identifier[0], identifier[1]))
    elif type(identifier) is str:
        query = _cursor.execute("""SELECT * FROM user_info WHERE personID=%s""",(identifier))

    # checks validity of return
    if query == 1:
        successful = True
        result = _cursor.fetchone()
    elif query > 1:
        print('Error: Too many account matches')
        successful = False
    else:
        successful = False
        result = None

    return successful, result

def signUp(form):
    any_blank = False in [bool(x) for x in form]
    result = 0
    # checks for matching passwords
    if any_blank is False and form['password1'] == form['password2']:
        result = _cursor.execute( """INSERT INTO user_info (firstName, email, password, join_date) VALUES (%s, %s, %s, %s)""", ( form['firstName'], form['email'], form['password1'], date.today() ) )
        if result:
            _db_conn.commit()
    
    return result

def loadUser(id:str):
    return classes.USER(id)

def storySavedStatus(user_id, story_id):
    _cursor.execute( """SELECT count(*) FROM saved_stories WHERE person_record_id = %s AND hacker_news_id = %s;""", (user_id, story_id) )
    copy_exists = _cursor.fetchone()[0]
    return copy_exists

def saveStory(user_id, story_id):
    if bool(storySavedStatus(user_id, story_id)):
        return -1
    
    result = _cursor.execute( """INSERT INTO saved_stories (person_record_id, hacker_news_id, date_saved) VALUES (%s, %s, %s);""", (user_id, story_id, date.today()) )
    if result:
        _db_conn.commit()
        return 1
    else:
        return 0
    
def getAllSavedStoriesInfo(user_id, count, offset_count):
    _cursor.execute("""SELECT hacker_news_id, date_saved FROM saved_stories WHERE person_record_id = %s ORDER BY date_saved DESC, hacker_news_id DESC LIMIT %s OFFSET %s;""", (user_id, count, offset_count*count) )
    
    story_info = _cursor.fetchall()
    return story_info

def removeStory(user_id, story_id):
    # check that story exists 
    if not bool(storySavedStatus(user_id, story_id)):
        return -1
    
    result = _cursor.execute( """DELETE FROM saved_stories WHERE person_record_id = %s AND hacker_news_id = %s;""", (user_id, story_id) )
    # commit changes only if 1 row was changed 
    if result == 1:
        _db_conn.commit()
        return result
    # if no changes are detected do not commit changes
    else:
        _db_conn.rollback()
        return 0