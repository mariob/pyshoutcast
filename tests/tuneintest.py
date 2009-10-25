import unittest
import shoutcast
import urllib2
import StringIO

valid_pls = """
[playlist]
numberofentries=1
File1=http://domain:port/stream
Title1=Radio Channel
Length1=-1
Version=2
"""

class TuneInTest(unittest.TestCase):

    def mock_urlopen(self, url):
        self.requested_url = url
        return StringIO.StringIO(valid_pls)

    def setUp(self):
        self.old_urlopen = urllib2.urlopen
        urllib2.urlopen = self.mock_urlopen
        self.shoutcast = shoutcast.ShoutCast()

    def tearDown(self):
        urllib2.urlopen = self.old_urlopen
        self.shoutcast = None

    def test_tune_in_urls(self):
        """ Verify that tune_in() formats URLs correctly """
        expected_url = 'http://yp.shoutcast.com/sbin/tunein-station.pls?id=1234'
        actual = self.shoutcast.tune_in('1234')
        self.assertEquals(expected_url, self.requested_url)

    def test_tune_in(self):
        """ Verify that tune_in() returns a play list """
        actual = self.shoutcast.tune_in('1234')
        self.assertEquals(valid_pls, actual.read())

if __name__ == "__main__":
    unittest.main()
