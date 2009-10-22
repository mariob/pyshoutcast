""" Fake station data """

expected_stations = (
     ("Radio station 1", '1234', '128', 'Artist1 - Title1',  '15'),
     ("Radio station 2", '1235', '64', 'Artist2 - Title2',  '150'),
     ("Radio station 3", '1236', '256', 'Artist3 - Title3',  '24'))

def create_stations_xml(stations):
    entry = '<station name="{0}" mt="audio/mpeg" id="{1}" br="{2}" genre="Rock" ct="{3}" lc="{4}"/>'
    entries = ['<stationlist>']
    entries.extend([entry.format(*s) for s in stations])
    entries.append('</stationlist>')
    return '\n'.join(entries)

