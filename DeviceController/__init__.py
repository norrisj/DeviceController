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

def verify_admin(f):
    @wraps(f)
    def wrapper(*args, **kwds):
        authkey = request.headers.get('Authorization')

        # Validate the user on authrocket
        headers = {'X-Authrocket-Account': app.config['AUTHROCKET_ACCOUNT'], 'X-Authrocket-Api-Key': app.config['AUTHROCKET_API_KEY'], 'X-Authrocket-Realm': app.config['AUTHROCKET_REALM'], 'Accept': 'application/json', 'Content-type': 'application/json' }
        payload = {'api_key': authkey, 'request': {'ip': '127.0.0.1'}}
        authres = requests.post ( app.config['AUTHROCKET_API'] + 'users/authenticate_key', headers=headers, data=json.dumps(payload))

        if ( authres.status_code == 401 ):
            abort (401)
        elif ( authres.status_code != 200 ):
            abort (500)

        # We're all good, check this is an admin user, make a user object and store it on the global cache
        g.userdetails = json.loads ( authres.text )
        print ( g.userdetails['username'] ) 

        return f(*args, **kwds)
    return wrapper
    
import DeviceController.views
