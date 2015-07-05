from flask import Flask, request, abort, g
from bson import json_util
from mongoengine import connect
from pymongo import read_preferences
from functools import wraps
import json
import requests

app = Flask(__name__)

app.config.from_envvar('DC_CONFIG_FILE')

def connect_db():
    return connect(
        app.config['DATABASE_TABLE'],
        host=app.config['DATABASE_URI'],
        port=app.config['DATABASE_PORT'],
        read_preference=read_preferences.ReadPreference.PRIMARY
    )

def close_db(db):
    db.disconnect()

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_appcontext
def teardown(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'db'):
        close_db( g.db )

def drop_db(db):
    """Drops all data in the database, for testing really"""
    db.drop_database( app.config['DATABASE_TABLE'] )

def verify_user(f):
    @wraps(f)
    def wrapper(*args, **kwds):
        authkey = request.headers.get('Authorization')

        # Validate the user on authrocket
        headers = {'X-Authrocket-Account': app.config['AUTHROCKET_ACCOUNT'], 'X-Authrocket-Api-Key': app.config['AUTHROCKET_API_KEY'], 'X-Authrocket-Realm': app.config['AUTHROCKET_REALM'], 'Accept': 'application/json', 'Content-type': 'application/json' }
        urlparams = {'expand': 'memberships' }
        payload = {'api_key': authkey, 'request': {'ip': '127.0.0.1'}}
        authres = requests.post ( app.config['AUTHROCKET_API'] + 'users/authenticate_key', headers=headers, data=json.dumps(payload), params=urlparams)

        if ( authres.status_code == 401 ):
            abort (401)
        elif ( authres.status_code != 200 ):
            abort (500)

        # print ( authres.text )
        g.userdetails = json.loads ( authres.text )
        return f(*args, **kwds)
    return wrapper

def verify_user_isadmin(f):
    @wraps(f)
    @verify_user
    def wrapper(*args, **kwds):
        memberships = g.userdetails['memberships']
        for membership in memberships:
            if ( app.config['PERM_ADMIN'] in membership['permissions'] ):
                return f(*args, **kwds)
        
        abort(401)
    return wrapper

import DeviceController.views
