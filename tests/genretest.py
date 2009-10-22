import unittest
import shoutcast

valid_genre = """
<genrelist>
<genre name="Rock"/>
<genre name="Pop"/>
<genre name="Punk"/>
</genrelist>
"""

class GenreTest(unittest.TestCase):

    def url_downloader(self, url):
        self.requestedUrl = url
        return valid_genre

    def setUp(self):
        self.shoutcast = shoutcast.ShoutCast(url_downloader=self.url_downloader)

    def tearDown(self):
        self.shoutcast = None

    def testGenre(self):
        expectedUrl = 'http://yp.shoutcast.com/sbin/newxml.phtml'
        expected = ('Rock', 'Pop', 'Punk')
        actual = self.shoutcast.genres()
        self.assertEquals(expectedUrl, self.requestedUrl)
        self.assertEquals(expected, actual)

if __name__ == "__main__":
    unittest.main()
