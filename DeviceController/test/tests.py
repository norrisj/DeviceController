import os
import unittest
import DeviceController
import json
import uuid
import dateutil.parser

class VideoTests(unittest.TestCase):
    @staticmethod
    def getTestPath(fname):
        script_dir = os.path.dirname(__file__)
        return os.path.join(script_dir, "res", fname)
        

    def setUp(self):
        self.app = DeviceController.app.test_client()
        db = DeviceController.connect_db()
        DeviceController.drop_db(db)

    def tearDown(self):
        pass

    def test_get_videos(self):
        rv = self.app.get('/videos')
        parsed = json.loads ( rv.data )
        assert len( parsed ) == 0

    def post_video(self, fname):
        f = VideoTests.getTestPath( fname )
        jsondata = json.load(open(f))
        return self.app.post('/videos', data=json.dumps(jsondata) )
        
        # is something a UUID: a = uuid.UUID( rv.data, version=4 )

    def test_post_minimal_video(self):
        rv = self.post_video( "test_videorecord_minimal.json" )
        assert ( rv.status_code == 200 )
        a = int(rv.data, 16)

    def test_post_invalid_data(self):
        rv = self.post_video( "test_videorecord_invalid.json" )
        assert ( rv.status_code == 400 )

    def test_post_complete_video(self):
        rv = self.post_video( "test_videorecord_complete.json" )
        assert ( rv.status_code == 200 )
        a = int(rv.data, 16)        

    def test_get_complete_record(self):
        f = VideoTests.getTestPath( "test_videorecord_complete.json" )
        jsondata = json.load(open(f))
        rv = self.app.post('/videos', data=json.dumps(jsondata) )

        key = int(rv.data, 16)
        
        rv = self.app.get('/videos/' + rv.data )
        assert (rv.status_code == 200 )
        
        # Check presence of all fields
        jsonresp = json.loads(rv.data)

        outtime = str(dateutil.parser.parse(jsonresp['start']).ctime())
        intime = str(dateutil.parser.parse(jsondata['start']).ctime())
        assert ( intime == outtime )

        outtime = str(dateutil.parser.parse(jsonresp['end']).ctime())
        intime = str(dateutil.parser.parse(jsondata['end']).ctime())
        assert ( intime == outtime )

        sensorid = uuid.UUID( jsonresp['sensorid'], version=4 )
        assert ( 'id' in jsonresp )
        assert ( 'videoref' in jsonresp )

    def test_get_minimal_record(self):
        pass

if __name__ == '__main__':
    unittest.main()

