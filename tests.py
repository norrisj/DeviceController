import os
import unittest
import DeviceController

class MovementTests(unittest.TestCase):
    def setUp(self):
        self.app = DeviceController.app.test_client()
        DeviceController.drop_db()

    def tearDown(self):
        pass

    def test_get_videos(self):
        rv = self.app.get('/videos')
        assert '[]' in rv.data

if __name__ == '__main__':
    unittest.main()

