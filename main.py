__author__ = 'Steve Cassidy'

from bottle import Bottle, template, static_file, debug
import interface
from database import SocialMediaDb
import bottle
import users

COOKIE_NAME = 'sessionid'

application = Bottle()
# turn on debugging for bottle during testing
debug()

@application.route('/')
def index():
    """Generate the main page of the app 
    with a list of the most recent posts"""
    db = SocialMediaDb()

    if (users.session_user(db)==None):
        loginS = False
    else:
        loginS = True
    #print(users.session_user(db))
    #print(bottle.request.get_cookie(COOKIE_NAME))
    loggedUser = users.session_user(db)
    info = {
        'title': "¡Welcome to SimpleSocial!",
        'posts': interface.post_list(db),
        'name': "User Login"

    }

    return template('index', info, loginStatus=loginS, lus = loggedUser)


@application.route('/login', method='POST')
def do_login():
    db = SocialMediaDb()
    username = bottle.request.forms.get('nick')
    password = bottle.request.forms.get('password')
    if users.check_login(db,username,password):
        x=users.generate_session(db, username)
        #print(x)

        y=users.session_user(db)
        #print(bottle.request.get_cookie(COOKIE_NAME))
        return bottle.redirect('/')
    else:

        info = {
            'title': "¡Welcome to SimpleSocial!",
            'posts': interface.post_list(db),
            'name': "Login Failed, please try again"
        }

        return template('failed', info, loginStatus=False, lus = None)


@application.route('/logout', method='POST')
def do_logout():
    db = SocialMediaDb()
    loggedUser = users.session_user(db)
    users.delete_session(db,loggedUser)

    return bottle.redirect('/')

@application.route('/post', method='POST')
def do_post():
    db = SocialMediaDb()
    loggedUser = users.session_user(db)
    msg = bottle.request.forms.get('post')
    interface.post_add(db,loggedUser,msg)

    return bottle.redirect('/')


@application.route('/mentions/<who>')
def mentions(who):
    """Generate a page that lists the mentions of a
    given user"""
    db = SocialMediaDb()

    info = dict()
    info['title'] = "Mentions of " + who

    info['posts'] = interface.post_list_mentions(db, usernick=who)
    info['name'] = "User Login"

    if (users.session_user(db)==None):
        loginS = False
    else:
        loginS = True

    loggedUser = users.session_user(db)
    # re-use the index template since this is just a list of posts
    #return template('index', info)
    return template("index", info, loginStatus=loginS, lus = loggedUser)


@application.route('/users/<who>')
def userpage(who):
    """Generate a page with just the posts for a given user"""

    db = SocialMediaDb()

    info = {
        'title': "User page for " + who,
        'posts': interface.post_list(db, usernick=who),
        'name': "User Login"
    }
    if (users.session_user(db)==None):
        loginS = False
    else:
        loginS = True

    loggedUser = users.session_user(db)
    # re-use the index template since this is just a list of posts
    return template("index", info, loginStatus=loginS, lus = loggedUser)


@application.route('/about')
def about():
    """Generate the about page"""
    db = SocialMediaDb()
    info = {
        'title': "¡Welcome to SimpleSocial!",
        'posts': interface.post_list(db),
        'name': "User Login"
    }
    if (users.session_user(db)==None):
        loginS = False
    else:
        loginS = True

    loggedUser = users.session_user(db)

    return template('about', info, title="About", loginStatus=loginS, lus = loggedUser)


@application.route('/static/<filename:path>')
def static(filename):
    """Serve static files from the static folder"""

    return static_file(filename=filename, root='static')


if __name__ == '__main__':
    application.run(debug=True, port=8010)
