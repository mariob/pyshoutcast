import xml.etree.ElementTree as etree
import urllib2

class ShoutCast(object):
    """ Manages shoutcast requests. """

    def __init__(self):
        """ Creates a Shoutcast API instance """

        self.genre_url = 'http://yp.shoutcast.com/sbin/newxml.phtml'
        self.station_url = 'http://yp.shoutcast.com/sbin/newxml.phtml?genre={0}'
        self.tune_in_url = 'http://yp.shoutcast.com/sbin/tunein-station.pls?id={0}'
        self.search_url = 'http://yp.shoutcast.com/sbin/newxml.phtml?search={0}'

    def genres(self):
        """ Return a tuple with genres. """
        genrelist = self._parse_xml(self.genre_url)
        return tuple(genre.get('name')
                     for genre in genrelist.findall('genre') if genre.get('name'))

    def stations(self, genre):
        """ Return a tuple with stations for the specified genre. """
        url = self.station_url.format(genre)
        return self._generate_stations(url)

    def search(self, criteria, limit=-1):
        """ 
        Searches station name, current playing track and genre.
        To limit the result specify 'limit' to the number of items to return.
        """
        if limit > 0:
            criteria = '{0}&limit={1}'.format(criteria, limit)

        url = self.search_url.format(criteria)
        return self._generate_stations(url)

    def random(self):
        """ Return a tuple with 20 random stations. """
        return self.stations('random')

    def top_500(self):
        """ Return a tuple with the top 500 stations. """
        return self.stations('Top500')

    def tune_in(self, station_id):
        """ Return the station's play list (shoutcast pls) as a file-like object. """
        url = self.tune_in_url.format(station_id)
        return urllib2.urlopen(url)

    def _parse_xml(self, url):
        """
        Returns an etree Element by downloading and parsing the XML from the
        specified URL.
        """
        file = urllib2.urlopen(url)
        return etree.parse(file)

    def _generate_stations(self, url):
        """ Return a tuple with stations traversing the stationlist element tree. """
        stationlist = self._parse_xml(url)
        result = []

        for station in stationlist.findall('station'):
            entry = (station.get('name'),
                     station.get('id'),
                     station.get('br'),
                     station.get('ct'),
                     station.get('lc'))
            result.append(entry)

        return tuple(result)
