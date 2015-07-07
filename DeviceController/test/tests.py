import unittest
from VideoTests import VideoTests
from SensorTests import SensorTests

videotests = unittest.TestLoader().loadTestsFromTestCase(VideoTests)
sensortests = unittest.TestLoader().loadTestsFromTestCase(SensorTests)

alltests = unittest.TestSuite([videotests, sensortests])
unittest.TextTestRunner(verbosity=2).run(alltests)
