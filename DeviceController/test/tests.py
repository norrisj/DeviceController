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
        
    @staticmethod
    def loadJson(fname):
        f = VideoTests.getTestPath( fname )
        return json.load(open(f))

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

    def post_video(self, jsondata):
        return self.app.post('/videos', data=json.dumps(jsondata) )
        
        # is something a UUID: a = uuid.UUID( rv.data, version=4 )

    def test_post_minimal_video(self):
        jsondata = VideoTests.loadJson ( "test_videorecord_minimal.json" )
        rv = self.post_video( jsondata )
        assert ( rv.status_code == 200 )
        a = int(rv.data, 16)

    def test_post_invalid_data(self):
        jsondata = VideoTests.loadJson ( "test_videorecord_invalid.json" )
        rv = self.post_video( jsondata )
        assert ( rv.status_code == 400 )

    def test_post_complete_video(self):
        jsondata = VideoTests.loadJson ( "test_videorecord_complete.json" )
        rv = self.post_video( jsondata )
        assert ( rv.status_code == 200 )
        a = int(rv.data, 16)        

    def test_get_complete_record(self):
        jsondata = VideoTests.loadJson ( "test_videorecord_complete.json" ) 
        rv = self.post_video ( jsondata )

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
        jsondata = VideoTests.loadJson ( "test_videorecord_minimal.json" ) 
        rv = self.post_video ( jsondata )
        key = int(rv.data, 16)
        
        rv = self.app.get('/videos/' + rv.data )
        assert (rv.status_code == 200 )
        
        # Check presence of all fields
        jsonresp = json.loads(rv.data)

        assert ( 'start' not in jsonresp )
        assert ( 'end' not in jsonresp )
        assert ( 'videoref' not in jsonresp )
        assert ( 'id' in jsonresp )
        sensorid = uuid.UUID( jsonresp['sensorid'], version=4 )

    def test_delete_record(self):
        jsondata = VideoTests.loadJson ( "test_videorecord_minimal.json" ) 
        rv = self.post_video ( jsondata )
        key = int(rv.data, 16) #bungs an exception if bad data
        key = rv.data 

        rv = self.app.delete ( '/videos/' + key )
        assert ( rv.status_code == 200 )

        # Make sure the object was returned
        records = json.loads ( rv.data )
        assert ( records['id'] == key )

        # now verify the record is no longer there
        rv = self.app.get('/videos')
        records = json.loads ( rv.data )

        assert ( key not in records )

        # delete again and check 404
        rv = self.app.delete ( '/videos/' + key )
        assert ( rv.status_code == 404 )

    def test_delete_non_exist_record(self):
        madeupkey = "000000000000000000000000" 
        rv = self.app.delete ( '/videos/' + madeupkey )
        assert ( rv.status_code == 404 )

if __name__ == '__main__':
    unittest.main()

