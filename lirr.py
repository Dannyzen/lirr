#!/usr/bin/env python
"""
Get Long Island Railroad departure, arrival and duration times.

Usage: python lirr.py (--source | -s) <source> (--dest | -d) <destination> [(--additional_hour | -a) <hours>]

Arguments: 
    -source             The train station you are starting your journey from.
    -dest               The train station you are ending your journey
    -additional_hour    The additional hours in the future you want train times for
    
Notes:
    Autocompletion for -source and -dest requires 3 or more characters.

Output:
The 4 most recent:
  - Departure times (if -a is not passed it uses current time. if -a is passed it will add to current hour)
  - Corresponding arrival times
  - Corresponding duration times

Written by: dannyzen & jcrivera & venatius
"""

from __future__ import print_function
import argparse
import ast
import datetime
import docopt
import json
import os.path
import sys
import urllib2
from suffixarray import SuffixArray
from tabulate import tabulate

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
    """
    load stations in as a dict from stations.txt
    Ex: {"Penn Station":"NYK"}

    Uses a suffix array implementation for fuzzy string matching
    """
    suffix_array = SuffixArray()
    stations = {}
    stations = ast.literal_eval(open('stations.txt').read())
    # lowercase all station names in stations
    stations = dict((k.lower(), v) for k, v in stations.iteritems())
    # try to match the station to the dict's keys
    # TODO: Need to do better catching for scenarios where:
    #   1. Station matches multiple station names
    #   2. Station is straight up wrong
    try:
        value = next(v for (k,v) in stations.iteritems() if station in k)
        return(value)
    except:
        print("Tried to find the station. Couldn't. Blaming you.")

def stationStringSizeCheck(source, destination):
    if len(source) < 3:
        print("Please provide a source station name with > 3 characters")
    if len(destination) < 3:
        print("Please provide a destination name with > 3 characters")
    else:
        return True

def getFeed(source, destination, additional_hour):
    if not source:
        print("source was fucked up")
    if not destination:
        print("destionat was fucked up")
    # this is a very ugly function, It is a tragedy to humans. I don't care. It works.
    global feed
    feed = json.load(urllib2.urlopen("http://wx3.lirr.org/lirr/portal/api/TrainTime?startsta="
                                     + getStationId(source)
                                     + "&endsta="
                                     + getStationId(destination)
                                     + "&year="
                                     + str(datetime.date.today().year)
                                     + "&month="
                                     + str(datetime.date.today().month)
                                     + "&day="
                                     + str(datetime.date.today().day)
                                     + "&hour="
                                     + getHour(additional_hour)
                                     + "&minute="
                                     + str(datetime.datetime.time(datetime.datetime.now()).minute)
                                     + "&datoggle=d"))
    return feed
# def check

def getHour(additional_hour):
    current_hour = (datetime.datetime.time(datetime.datetime.now()).hour)
    if additional_hour:
        current_hour += int(additional_hour)
    return str(current_hour)

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
    new_times = []
    for time in times:
        d = datetime.datetime.strptime(time, "%H%M")
        time = d.strftime("%I:%M %p")
        new_times.append(time)
    return new_times


def getTrainTimes(source, destination, additional_hour):
    headers = ["Source departure times", "Destination arrival times", "Trip duration in minutes"]
    feed = getFeed(source, destination, additional_hour)
    departures = convertTimes(getDepartureTimes(feed))
    arrivals = convertTimes(getArrivalTimes(feed))
    durations = getDuration(feed)
    table = zip(departures, arrivals, durations)
    print(tabulate(table, headers))

# lirr/portal/api/TrainTime?startsta=NYK&endsta=HVL&year=2014&month=5&day=31&hour=18&minute=05&datoggle=d

# TODO:
# 1. Figure out a way to support (or prevent) scenarios like: -s Hewlett -d Hicksville

if __name__ == "__main__":
    opts = docopt.docopt(__doc__, sys.argv)
    if os.path.isfile('stations.txt'):
        if stationStringSizeCheck(opts['<source>'], opts['<destination>']) == True:
            getTrainTimes(opts['<source>'], opts['<destination>'], opts['<hours>'])
    else:
        try:
            writeStationList()
        except IOError:
            print("Stations.txt does not exist, we tried to write it to this folder. We couldn't. Make sure this folder is writeable.")
            raise
        getTrainTimes(opts['<source>'], opts['<destination>'], opts['<hours>'])
