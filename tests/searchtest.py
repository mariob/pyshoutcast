import unittest
import shoutcast
import stationdata

class SearchTest(unittest.TestCase):

    def mock_generate_stations(self, url):
        self.generate_stations_called = True
        self.requested_url = url

    def setUp(self):
        self.generate_stations_called = False
        self.shoutcast = shoutcast.ShoutCast(None)
        self.shoutcast._generate_stations = self.mock_generate_stations

    def tearDown(self):
        self.shoutcast = None

    def test_search_url(self):
        """ Verify that search() formats URLs correctly """
        expected_url = 'http://yp.shoutcast.com/sbin/newxml.phtml?search=Radio station'
        self.shoutcast.search('Radio station')
        self.assertEquals(expected_url, self.requested_url)

        expected_url = 'http://yp.shoutcast.com/sbin/newxml.phtml?search=Keywords&limit=10'
        self.shoutcast.search('Keywords', 10)
        self.assertEquals(expected_url, self.requested_url)

    def test_search(self):
        """ Verify that search() delegates to _generate_stations() """
        self.shoutcast.search('')
        self.assertTrue(self.generate_stations_called)

if __name__ == "__main__":
    unittest.main()
