import urllib2
import json

def loadStations():
    return json.load(urllib2.urlopen("http://wx3.lirr.org/lirr/portal/api/Stations-All"))

def stationStringCheck(station):
    if len(station) < 3:
        return "Please provide a station name with > 3 characters, you lazy bastard"
    else:
        station_id =  getStationId(station)
        if station_id is not None:
            return station_id
        else:
            return "Fuck"

def getStationId(station):
    """Gets a station ID given the Station Name"""
    data = loadStations()
    for key, value in data.iteritems():
            for values in value.iteritems():
                for items in values:
                    if isinstance(items,dict):
                        stations = {}
                        stations.update({items["NAME"]:items["ABBR"]})
                        for station_name, short_station_name in stations.iteritems():
                            if station in station_name.lower():
                                return short_station_name

# Need to get departure time and arrival time

# lirr/portal/api/TrainTime?startsta=NYK&endsta=HVL&year=2014&month=5&day=31&hour=18&minute=05&datoggle=d

foo = stationStringCheck("ronk")
print foo