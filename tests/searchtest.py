import unittest
import shoutcast
import stationdata

class SearchTest(unittest.TestCase):

    def url_downloader(self, url):
        self.requestedUrl = url
        return stationdata.create_stations_xml(stationdata.expected_stations)
    
    def setUp(self):
        self.shoutcast = shoutcast.ShoutCast(self.url_downloader)

    def tearDown(self):
        self.shoutcast = None

    def testStations(self):
        expectedUrl = 'http://yp.shoutcast.com/sbin/newxml.phtml?search=Radio station'
        actual_stations = self.shoutcast.search('Radio station')
        self.assertEquals(expectedUrl, self.requestedUrl)
        self.assertEquals(stationdata.expected_stations, actual_stations)

if __name__ == "__main__":
    unittest.main()
