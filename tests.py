import pyramid_subscribers_beaker_https_session

# core testing facility
import unittest

# pyramid testing requirements
from pyramid import testing

class TestPyramid(unittest.TestCase):

    def setUp(self):
        self.config = testing.setUp()
        self.context = testing.DummyResource()
        self.request = testing.DummyRequest()


    def tearDown(self):
        testing.tearDown()

    def test_setup(self):
        pass
