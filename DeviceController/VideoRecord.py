from mongoengine import *

class VideoRecord(Document):
    testing=StringField(max_length=50)
