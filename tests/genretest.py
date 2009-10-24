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
        self.requested_url = url
        return self.genre_data

    def setUp(self):
        self.genre_data = valid_genre
        self.shoutcast = shoutcast.ShoutCast(url_downloader=self.url_downloader)

    def tearDown(self):
        self.shoutcast = None
        self.genre_data = None

    def test_genre_url(self):
        """ Verify that genres() formats URLs correctly """
        expected_url = 'http://yp.shoutcast.com/sbin/newxml.phtml'
        actual = self.shoutcast.genres()
        self.assertEquals(expected_url, self.requested_url)

    def test_genre(self):
        """ Verify that genres() returns the expected genre list """
        expected = ('Rock', 'Pop', 'Punk')
        actual = self.shoutcast.genres()
        self.assertEquals(expected, actual)

    def test_empty_genre_list(self):
        """ Verify that genres() handles empty genre lists """
        self.genre_data = '<genrelist></genrelist>'
        expected = ()
        actual = self.shoutcast.genres()
        self.assertEquals(expected, actual)

    def test_non_named_genre_entry(self):
        """ Verify that genres() handles non-named genre entries"""
        self.genre_data = '<genrelist><genre name="Rock"/><genre /></genrelist>'
        expected = ('Rock',)
        actual = self.shoutcast.genres()
        self.assertEquals(expected, actual)

if __name__ == "__main__":
    unittest.main()
