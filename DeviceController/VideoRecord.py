from mongoengine import *
import os
import json

class VideoRecord(Document):
    start=DateTimeField()
    end=DateTimeField()
    videoref=StringField(max_length=200)
    sensorid=UUIDField(required=True)

    @staticmethod
    def get_json_schema():
        script_dir = os.path.dirname(__file__)
        rel_path = "VideoRecord.json"
        abs_file_path = os.path.join(script_dir, rel_path)
        
        with open( abs_file_path ) as data_file:    
            return json.load(data_file)

    def to_json(self):
        d = {
            "id": str(self.id),
            "sensorid": str(self.sensorid),
        }
        if self.start is not None:
            d['start'] = self.start.isoformat()
        if self.end is not None:
            d['end'] = self.end.isoformat()
        if self.videoref is not None:
            d['videoref'] = self.videoref
        return json.dumps(d)

