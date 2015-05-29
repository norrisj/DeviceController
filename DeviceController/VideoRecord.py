from mongoengine import *

class VideoRecord(Document):
    id=ObjectIdField(primary_key=True)
    testing=StringField(max_length=50)
