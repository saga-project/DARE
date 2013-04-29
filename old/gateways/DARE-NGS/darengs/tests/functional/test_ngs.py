from darengs.tests import *

class TestNgsController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='ngs', action='index'))
        # Test response...
