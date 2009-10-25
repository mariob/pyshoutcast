import unittest
import shoutcast
import stationdata
import StringIO
import urllib2

class RandomTest(unittest.TestCase):

    def mock_stations(self, genre):
        self.requested_genre = genre

    def test_random(self):
        """ Verify that random() delegates to stations() """
        self.shoutcast = shoutcast.ShoutCast()
        self.shoutcast.stations = self.mock_stations

        actual = self.shoutcast.random()
        self.assertEquals('random', self.requested_genre)


class Top500Test(unittest.TestCase):

    def mock_stations(self, genre):
        self.requested_genre = genre
        pass

    def test_top500(self):
        """ Verify that top500() delegates to stations() """
        self.shoutcast = shoutcast.ShoutCast()
        self.shoutcast.stations = self.mock_stations

        actual = self.shoutcast.top_500()
        self.assertEquals('Top500', self.requested_genre)


class StationTest(unittest.TestCase):

    def mock_generate_stations(self, url):
        self.generate_stations_called = True
        self.requested_url = url

    def setUp(self):
        self.generate_stations_called = False
        self.shoutcast = shoutcast.ShoutCast()
        self.shoutcast._generate_stations = self.mock_generate_stations
    
    def tearDown(self):
        self.shoutcast = None

    def test_stations_url(self):
        """ Verify that stations() formats URLs correctly """
        expected_url = 'http://yp.shoutcast.com/sbin/newxml.phtml?genre=Rock'
        self.shoutcast.stations('Rock')
        self.assertEquals(expected_url, self.requested_url)

        expected_url = 'http://yp.shoutcast.com/sbin/newxml.phtml?genre=Pop'
        self.shoutcast.stations('Pop')
        self.assertEquals(expected_url, self.requested_url)

    def test_stations(self):
        """ Verify that stations() delegates to _generate_stations() """
        self.shoutcast.stations('Rock')
        self.assertTrue(self.generate_stations_called)

class GenerateStationsTest(unittest.TestCase):

    def mock_urlopen(self, url):
        return StringIO.StringIO(self.stations_data)

    def setUp(self):
        self.stations_data = stationdata.create_stations_xml(stationdata.expected_stations)
        self.old_urlopen = urllib2.urlopen
        urllib2.urlopen = self.mock_urlopen
        self.shoutcast = shoutcast.ShoutCast()

    def tearDown(self):
        urllib2.urlopen = self.old_urlopen
        self.shoutcast = None

    def test_empty_stations(self):
        self.stations_data = '<stationlist></stationlist>'
        expected = ()
        actual = self.shoutcast.stations('Rock')
        self.assertEquals(expected, actual)

if __name__ == "__main__":
    unittest.main()
