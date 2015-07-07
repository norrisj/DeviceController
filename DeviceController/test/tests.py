import unittest
from VideoTests import VideoTests

suite = unittest.TestLoader().loadTestsFromTestCase(VideoTests)
unittest.TextTestRunner(verbosity=2).run(suite)
