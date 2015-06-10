import os
import unittest
import DeviceController

class MovementTests(unittest.TestCase):
    def setUp(self):
        self.app = DeviceController.app.test_client()
        
    def tearDown(self):
        pass

    def test_hello_world (self):
        rv = self.app.get('/')
        assert 'Hello world' in rv.data

if __name__ == '__main__':
    unittest.main()

