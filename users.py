import  uuid
import bottle
from bottle import response, request

# this variable MUST be used as the name for the cookie used by this application
COOKIE_NAME = 'sessionid'

def check_login(db, usernick, password):
    """returns True if password matches stored"""
    cur = db.cursor()
    cur2=db.cursor()
    enPass = db.crypt(password)
    sqlUserCheck = "SELECT * FROM users WHERE nick=?"
    cur2.execute(sqlUserCheck, (usernick,))

    var1 = cur2.fetchall()
    if (len(var1) == 0):
        return False

    sql = "SELECT password FROM users WHERE nick=?"
    cur.execute(sql, (usernick,))

    var2=cur.fetchall()[0][0]
    if(enPass==var2):
        return True
    else:
        return False




def generate_session(db, usernick):
    """create a new session and add a cookie to the response object (bottle.response)
    user must be a valid user in the database, if not, return None
    There should only be one session per user at any time, if there
    is already a session active, use the existing sessionid in the cookie
    """
    cur = db.cursor()
    sql = "SELECT * FROM users WHERE nick=?"
    cur.execute(sql, (usernick,))
    var1 = cur.fetchall()
    if (len(var1) == 0):
        return None


    cur.execute("SELECT sessionid FROM sessions WHERE usernick=?", (usernick,))
    key = cur.fetchone()
    if not key:
        key = str(uuid.uuid4())
        cur2 = db.cursor()
        sql2="INSERT INTO sessions (sessionid, usernick) VALUES (?, ?)"
        cur2.execute(sql2, (key, usernick,))
        db.commit()
        response.set_cookie(COOKIE_NAME, key)
    if len(key)==1:
        bottle.response.set_cookie(COOKIE_NAME, key[0])
        return key[0]

    return key

def delete_session(db, usernick):
    """remove all session table entries for this user"""
    cur = db.cursor()
    sql = "DELETE FROM sessions WHERE usernick=?"
    cur.execute(sql, (usernick,))
    db.commit()

def session_user(db):
    """try to
    retrieve the user from the sessions table
    return usernick or None if no valid session is present"""
    sid = request.get_cookie(COOKIE_NAME)

    cur = db.cursor()
    cur.execute("SELECT usernick FROM sessions WHERE sessionid=?", (sid,))
    val = cur.fetchone()
    if (val!=None):
        return val[0]
    else:
        return None


