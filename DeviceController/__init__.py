from flask import Flask, request, abort, g
from bson import json_util
from mongoengine import connect
from pymongo import read_preferences

app = Flask(__name__)

app.config.from_envvar('DC_CONFIG_FILE')

@app.before_request
def before_request():
    g.db = connect(
        app.config['DATABASE_TABLE'],
        host=app.config['DATABASE_URI'],
        port=app.config['DATABASE_PORT'],
        read_preference=read_preferences.ReadPreference.PRIMARY
    )

@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'db'):
        g.db.disconnect()

def drop_db():
    """Drops all data in the database, for testing really"""
    if hasattr(g, 'db'):
        g.db.drop_database( app.config['DATABASE_TABLE'] )
        
import DeviceController.views
