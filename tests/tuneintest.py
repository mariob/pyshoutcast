import unittest
import shoutcast

valid_pls = """
[playlist]
numberofentries=1
File1=http://domain:port/stream
Title1=Radio Channel
Length1=-1
Version=2
"""

class TuneInTest(unittest.TestCase):

    def url_downloader(self, url):
        self.requested_url = url
        return valid_pls

    def setUp(self):
        self.shoutcast = shoutcast.ShoutCast(self.url_downloader)

    def tearDown(self):
        self.shoutcast = None

    def test_tune_in_urls(self):
        """ Verify that tune_in() formats URLs correctly """
        expected_url = 'http://yp.shoutcast.com/sbin/tunein-station.pls?id=1234'
        actual = self.shoutcast.tune_in('1234')
        self.assertEquals(expected_url, self.requested_url)

    def test_tune_in(self):
        """ Verify that tune_in() returns a play list """
        actual = self.shoutcast.tune_in('1234')
        self.assertEquals(valid_pls, actual)

if __name__ == "__main__":
    unittest.main()
