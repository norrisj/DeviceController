import os
import unittest
import tempfile
import DeviceController

class MovementTests(unittest.TestCase):
    def setUp(self):
        self.db_fb, flaskr.app.config['DATABASE'] = tempfile.mkstemp()
        flaskr.app.config['TESTING'] = True
        self.app = flaskr.app.test_client()
        flaskr.init_db()

    def tearDown(self):
        os.close( self.db_fb )
        os.unlink(flaskr.app.config['DATABASE'])
    
    def test_hello_world (self):
        rv = self.app.get('/')
        assert 'Hello world' in rv.data

if __name__ == '__name__':
    unittest.main()
