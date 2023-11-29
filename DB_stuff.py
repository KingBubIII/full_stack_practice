import pymysql
from datetime import date
import classes

login_details = open('sql_login.txt','r').readlines()
_db_conn = pymysql.connect(user=login_details[0].strip(), password=login_details[1].strip(), host=login_details[2].strip(), db=login_details[3].strip())
_cursor = _db_conn.cursor()

def login(identifier):
    user_data = list()
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

    return successful, result

def signUp(form):
    any_blank = False in [bool(x) for x in form]
    result = 0
    # checks for matching passwords
    if any_blank is False and form['password1'] == form['password2']:
        result = _cursor.execute("""INSERT INTO user_info (firstName, email, password, join_date) VALUES (%s, %s, %s, %s)""", ( form['firstName'], form['email'], form['password1'], date.today() ) )
        if result:
            _db_conn.commit()
    
    return result

def loadUser(id:str):
    return classes.USER(id)