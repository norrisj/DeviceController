from mongoengine import *
import os
import json

class VideoRecord(Document):
    start=DateTimeField()
    end=DateTimeField()
    videoref=StringField(max_length=200)
    sensorid=UUIDField()

    @staticmethod
    def get_json_schema():
        script_dir = os.path.dirname(__file__)
        rel_path = "VideoRecord.json"
        abs_file_path = os.path.join(script_dir, rel_path)
        
        with open( abs_file_path ) as data_file:    
            return json.load(data_file)
