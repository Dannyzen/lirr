#!/usr/bin/python
from __future__ import print_function
import urllib2
import json
import ast
import datetime
from optparse import OptionParser
import pprint


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



def stationStringCheck(src_station, dest_station):
    if len(src_station) < 3:
        return "Please provide a station name with > 3 characters, you lazy bastard"
    if len(dest_station) < 3:
        return "Please provide a station name with > 3 characters, you lazy bastard"
    else:
        return getFeed(src_station,dest_station)


def getFeed(src_station,dest_station):
    # this is a very ugly function, It is a tragedy to humans. I don't care. It works.
    return json.load(urllib2.urlopen("http://wx3.lirr.org/lirr/portal/api/TrainTime?startsta="
                                     + getStationId(src_station)
                                     + "&endsta="
                                     + getStationId(dest_station)
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

def getDuration(feed):
    durations = []
    for i in range (len(feed)):
        durations.append(feed['TRIPS'][i]['DURATION'])
    return durations

def getDepartureTimes(feed):
    departure_times = []
    for i in range (len(feed)):
        departure_times.append(feed['TRIPS'][i]['LEGS'][0]['DEPART_TIME'])
    return departure_times

def getArrivalTimes(feed):
    departure_times = []
    for i in range (len(feed)):
        departure_times.append(feed['TRIPS'][i]['LEGS'][0]['ARRIVE_TIME'])
    return departure_times

def convertTimes(times):
    times = []
    for time in times:
        print(time)
        d = datetime.datetime.strptime(time, "%H:%M")
        print(d)
        d.strftime("%I:%M %p")
        times.append()
    return times




# lirr/portal/api/TrainTime?startsta=NYK&endsta=HVL&year=2014&month=5&day=31&hour=18&minute=05&datoggle=d

parser = OptionParser()
parser.add_option("-s", "--source", dest="source", help="source station", default="")
parser.add_option("-d", "--dest", dest="dest", help="destination station", default="")

(options, args) = parser.parse_args()

# pp.pprint(stationStringCheck(options.source, options.dest))
data = stationStringCheck(options.source, options.dest)
# print(data['TRIPS'][1])

#V1
print(getDepartureTimes(stationStringCheck(options.source, options.dest))))
print(getArrivalTimes(stationStringCheck(options.source, options.dest)))
print(getDuration(stationStringCheck(options.source, options.dest)))

