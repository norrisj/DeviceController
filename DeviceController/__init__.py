from flask import Flask, request, abort
from bson import json_util
from mongoengine import connect
from pymongo import read_preferences

app = Flask(__name__)

connect(
    'alarms',
    host='db',
    port=27017,
    read_preference=read_preferences.ReadPreference.PRIMARY
)

import DeviceController.views

    
