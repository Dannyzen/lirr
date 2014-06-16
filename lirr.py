from __future__ import print_function
import urllib2
import json
import ast
import datetime

def loadStations():
    return json.load(urllib2.urlopen("http://wx3.lirr.org/lirr/portal/api/Stations-All"))

# Writing
def writeToFile(content,file_name="stations.txt"):
    print(content,file=open(file_name,'w'))

def writeStationList():
    """Pull stations down and writes them to stations.txt"""
    data = loadStations()
    stations = {}
    for key, value in data.iteritems():
            for values in value.iteritems():
                for items in values:
                    if isinstance(items,dict):
                        stations.update({items["NAME"]:items["ABBR"]})
                        writeToFile(stations)

def getStationId(station):
    # load stations in as a dict from stations.txt
    stations = {}
    stations = ast.literal_eval(open('stations.txt').read())
    # lowercase all keys in stations
    stations = dict((k.lower(), v) for k, v in stations.iteritems())
    # now try to match the station to the dict's keys
    try:
        value = next(v for (k,v) in stations.iteritems() if station in k)
        return(value)
    except:
        print("Tried to find the station. Couldn't. Blaming you.")



def stationStringCheck(src_station,dest_station):
    if len(src_station) < 3:
        return "Please provide a station name with > 3 characters, you lazy bastard"
    if len(dest_station) < 3:
        return "Please provide a station name with > 3 characters, you lazy bastard"
    else:
        return getDepartureTime(src_station,dest_station)


def getDepartureTime(src_station,dest_station):
    # this is a very ugly function, It is a tragedy to humans. I don't care. It works.
    return json.load(urllib2.urlopen("http://wx3.lirr.org/lirr/portal/api/TrainTime?startsta="
                                     + getStationId("penn station")
                                     + "&endsta="
                                     + getStationId("hewlett")
                                     + "&year="
                                     + str(datetime.date.today().year)
                                     + "&month="
                                     + str(datetime.date.today().month)
                                     + "&day="
                                     + str(datetime.date.today().day)
                                     + "&hour="
                                     + str(datetime.datetime.time(datetime.datetime.now()).hour)
                                     + "&minute="
                                     + str(datetime.datetime.time(datetime.datetime.now()).minute)
                                     + "&datoggle=d"))

# Todo:

# lirr/portal/api/TrainTime?startsta=NYK&endsta=HVL&year=2014&month=5&day=31&hour=18&minute=05&datoggle=d

# station_id = getStationId('hewlett')

print(stationStringCheck('penn', 'hicksville'))