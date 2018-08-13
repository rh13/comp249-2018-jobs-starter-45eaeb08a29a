"""
Created on Mar 26, 2012

@author: steve
"""

# this variable MUST be used as the name for the cookie used by this application
COOKIE_NAME = 'sessionid'
from database import password_hash
import uuid
from bottle import response, request


def check_login(db, usernick, password):
    """returns True if password matches stored"""
    password = password_hash(password) 
    sql = '''SELECT  * FROM users WHERE nick='%s' AND password='%s';''' %(usernick, password)
    cursor = db.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    if rows:
        return True
    else:
        return False


def generate_session(db, usernick):
    """create a new session and add a cookie to the response object (bottle.response)
    user must be a valid user in the database, if not, return None
    There should only be one session per user at any time, if there
    is already a session active, use the existing sessionid in the cookie
    """


    key = str(uuid.uuid4())
    cursor= db.cursor()


    cursor.execute("SELECT nick FROM users WHERE nick=?", (usernick,))
    row = cursor.fetchone()

    if not row:
        return None


    cursor.execute('''SELECT sessionid FROM sessions WHERE usernick=?''', (row[0],))

    row = cursor.fetchone()
    

    if row:
        return row[0]

    cursor.execute(f"INSERT INTO sessions VALUES ('{key}', '{usernick}')")
    db.commit()

    response.set_cookie(COOKIE_NAME, key)

    return key




def delete_session(db, usernick):
    """remove all session table entries for this user"""
    cursor = db.cursor()
    cursor.execute(f"DELETE FROM sessions WHERE usernick='{usernick}'")
    db.commit()



def session_user(db):
    """try to
    retrieve the user from the sessions table
    return usernick or None if no valid session is present"""
    key = request.get_cookie(COOKIE_NAME)

    cursor = db.cursor()
    cursor.execute('''SELECT usernick FROM sessions WHERE sessionid=?''' ,(key,))

    row = cursor.fetchone()

    if row:
        return row[0]
    else:
        None




