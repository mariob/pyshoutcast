# This code is licensed under the new-BSD license
# (http://www.opensource.org/licenses/bsd-license.php)
# Copyright (C) 2009 Mario Boikov <mario@beblue.org>.

import xml.etree.ElementTree as etree
import urllib
import urllib2

class ShoutCast(object):
    """
    Python front-end to the shoutcast web-radio service.
    
    This class uses urllib2.urlopen() when accessing the shoutcast service.
    Any errors that might occur while accessing the service will be propagated
    to the caller without any modifications.
    
    The shoutcast service uses XML as protocol and to parse the result from
    the service the ElementTree XML API is used. Any errors that might occur
    while parsing the XML will be propagated to the caller without any
    modifications. 
    """

    def __init__(self):
        """ Creates a Shoutcast API instance """

        self.genre_url = 'http://yp.shoutcast.com/sbin/newxml.phtml'
        self.station_url = 'http://yp.shoutcast.com/sbin/newxml.phtml?genre={0}'
        self.tune_in_url = 'http://yp.shoutcast.com/sbin/tunein-station.pls?id={0}'
        self.search_url = 'http://yp.shoutcast.com/sbin/newxml.phtml?{0}'

    def genres(self):
        """
        Return a tuple with genres.
        Each entry in the tuple is a string with the name of the genre.
        
        Example:
        ('Rock', 'Pop', '...')
        """
        genrelist = self._parse_xml(self.genre_url)
        return tuple(genre.get('name')
                     for genre in genrelist.findall('genre') if genre.get('name'))

    def stations(self, genre):
        """
        Return a tuple with stations for the specified genre.
        Each entry in the tuple is a tulpe with the following content:
        station name, station id, bitrate, currently playing track and
        listener count

        Example:
        (('Hit Radio Station #1', 1234, 128, 'An artist - A Hit song', 123),
         ('Hit Radio Station #2', 5678, 256, 'A track name', 43)) 
        """
        url = self.station_url.format(genre)
        return self._generate_stations(url)

    def search(self, criteria, limit=-1):
        """ 
        Searches station name, current playing track and genre.
        To limit the result specify 'limit' to the number of items to return.
        
        Returns the same kind of tuple as stations()
        """
        params = {'search' : criteria}
        if limit > 0:
            params['limit'] = limit

        url = self.search_url.format(urllib.urlencode(params))
        return self._generate_stations(url)

    def random(self):
        """ Return a tuple (same as stations()) with 20 random stations. """

        return self.stations('random')

    def top_500(self):
        """ Return a tuple (same as stations()) with the top 500 stations. """
        return self.stations('Top500')

    def tune_in(self, station_id):
        """ Return the station's play list (shoutcast pls) as a file-like object. """
        url = self.tune_in_url.format(station_id)
        return urllib2.urlopen(url)

    def _parse_xml(self, url):
        """
        Returns an ElementTree element by downloading and parsing the XML from the
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
