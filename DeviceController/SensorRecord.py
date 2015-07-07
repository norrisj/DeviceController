from mongoengine import *
import os, json

class LocationRecord(DynamicDocument):
    pass

class SensorRecord(Document):
    sensorid=UUIDField(required=True, unique=True)
    username=StringField(max_length=200)
    location=GenericEmbeddedDocumentField(LocationRecord)
    type=StringField(max_length=200)
    
    
