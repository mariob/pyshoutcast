import xml.etree.ElementTree as etree

class ShoutCast(object):
    """ Manages shoutcast requests. """

    def __init__(self, url_downloader):
        """
        Specify which url_downloader to be used for this instance.

        A 'url_downloader' is simply a function that takes a URL (string) as argument
        and returns the content for that URL.

        Example:
        def urllib2_downloader(url):
            return urllib2.urlopen(url).read()
        """

        self.url_downloader = url_downloader
        
        self.genre_url = 'http://yp.shoutcast.com/sbin/newxml.phtml'
        self.station_url = 'http://yp.shoutcast.com/sbin/newxml.phtml?genre={0}'
        self.tune_in_url = 'http://yp.shoutcast.com/sbin/tunein-station.pls?id={0}'
        self.search_url = 'http://yp.shoutcast.com/sbin/newxml.phtml?search={0}'

    def genres(self):
        """ Return a tuple with genres. """
        content = self.url_downloader(self.genre_url)
        genrelist = etree.XML(content)
        return tuple(genre.get('name') for genre in genrelist.findall('genre'))

    def stations(self, genre):
        """ Return a tuple with stations for the specified genre. """
        url = self.station_url.format(genre)
        content = self.url_downloader(url)
        return self._parse_stations(content)

    def search(self, criteria, limit=-1):
        """ 
        Searches station name, current playing track and genre.
        To limit the result specify 'limit' to the number of items to return.
        """
        if limit > 0:
            criteria = '{0}&limit={1}'.format(criteria, limit)

        url = self.search_url.format(criteria)
        content = self.url_downloader(url)
        return self._parse_stations(content)

    def random(self):
        """ Return a tuple with 20 random stations. """
        return self.stations('random')
    
    def top_500(self):
        """ Return a tuple with the top 500 stations. """
        return self.stations('Top500')

    def tune_in(self, station_id):
        """ Return the station's play list (shoutcast pls) as a string. """
        url = self.tune_in_url.format(station_id)
        return self.url_downloader(url)

    def _parse_stations(self, content):
        """ Return a tuple with stations for the specified genre. """
        stationlist = etree.XML(content)

        result = []
        
        for station in stationlist.findall('station'):
            entry = (station.get('name'),
                     station.get('id'),
                     station.get('br'),
                     station.get('ct'),
                     station.get('lc'))
            result.append(entry)

        return tuple(result)
