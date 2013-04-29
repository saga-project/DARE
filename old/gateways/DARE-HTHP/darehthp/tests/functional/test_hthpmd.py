from darehthp.tests import *

class TestHthpmdController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='hthpmd', action='index'))
        # Test response...
