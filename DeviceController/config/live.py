from mongoengine import connect
from pymongo import read_preferences

connect(
    'alarms',
    host='db',
    port=27017,
    read_preference=read_preferences.ReadPreference.PRIMARY
)
