import unittest
import shoutcast
import stationdata

class RandomTest(unittest.TestCase):

    def mockStations(self, genre):
        self.requestedGenre = genre
        pass

    def setUp(self):
        self.shoutcast = shoutcast.ShoutCast(None)
        self.shoutcast.stations = self.mockStations

    def tearDown(self):
        self.shoutcast = None

    def testRandom(self):
        actual = self.shoutcast.random()
        self.assertEquals('random', self.requestedGenre)


class Top500Test(unittest.TestCase):

    def mockStations(self, genre):
        self.requestedGenre = genre
        pass

    def setUp(self):
        self.shoutcast = shoutcast.ShoutCast(None)
        self.shoutcast.stations = self.mockStations

    def tearDown(self):
        self.shoutcast = None

    def testTop500(self):
        actual = self.shoutcast.top_500()
        self.assertEquals('Top500', self.requestedGenre)


class StationTest(unittest.TestCase):

    def url_downloader(self, url):
        self.requestedUrl = url
        return stationdata.create_stations_xml(stationdata.expected_stations)
    
    def setUp(self):
        self.shoutcast = shoutcast.ShoutCast(self.url_downloader)

    def tearDown(self):
        self.shoutcast = None

    def testStations(self):
        expectedUrl = 'http://yp.shoutcast.com/sbin/newxml.phtml?genre=Rock'
        actual_stations = self.shoutcast.stations('Rock')
        self.assertEquals(expectedUrl, self.requestedUrl)
        self.assertEquals(stationdata.expected_stations, actual_stations)

if __name__ == "__main__":
    unittest.main()
