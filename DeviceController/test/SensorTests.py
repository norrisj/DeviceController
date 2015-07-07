import os
import unittest
import DeviceController
import json
import uuid
import dateutil.parser

class SensorTests(unittest.TestCase):
    adminkey = 'VGDCOUA7eZgsrgFSzeq31LBcJLQla0vzeXLtY3sGDr2'
    devicekey = '4Os2BF8nwqXi2VOJ27oRTpSMaNDMNxhA7XbVDuqYOgr'

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

    def test_get_sensors(self):
        header = {'Authorization': self.adminkey}
        rv = self.app.get('/sensors', headers=header)
        assert ( rv.status_code == 200 )
        parsed = json.loads( rv.data )
        assert len( parsed ) == 0
