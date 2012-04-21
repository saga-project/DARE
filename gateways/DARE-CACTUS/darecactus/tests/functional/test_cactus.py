from darecactus.tests import *

class TestCactusController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='cactus', action='index'))
        # Test response...
