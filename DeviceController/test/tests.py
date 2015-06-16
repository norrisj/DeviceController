import os
import unittest
import DeviceController
import json
import uuid

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

    def test_get_record(self):
        pass

if __name__ == '__main__':
    unittest.main()

