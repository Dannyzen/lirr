#!/usr/bin/python
# Script fully supports use cases where source and destination are on the same train line
# Get Long Island Railroad departure, arrival and duration time.
# Usage: python lirr.py -s SOURCE -d DESTINATION
# Ex: python lirr.py -s penn -d babylon
# Output:
# 4 most recent:
#  departure times
#  corresponding arrival times
#  corresponding duration times
# Written by: @dannyzen & jcrivera

from __future__ import print_function
import urllib2
import json
import ast
import datetime
import argparse
import os.path

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
    # Ex: {"Penn Station":"NYK"}
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
    # else:
    #     return getFeed(source,destination)


def getFeed(source,destination):
    if not source:
        print("source was fucked up")
    if not destination:
        print("destionat was fucked up")
    # this is a very ugly function, It is a tragedy to humans. I don't care. It works.
    return json.load(urllib2.urlopen("http://wx3.lirr.org/lirr/portal/api/TrainTime?startsta="
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
                                     + str(datetime.datetime.time(datetime.datetime.now()).hour)
                                     + "&minute="
                                     + str(datetime.datetime.time(datetime.datetime.now()).minute)
                                     + "&datoggle=d"))

# def check

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


def getTrainTimes(source,destination):
    print("Source departure times")
    print(convertTimes(getDepartureTimes(getFeed(source, destination))))
    print("Destination arrival times")
    print(convertTimes(getArrivalTimes(getFeed(source, destination))))
    print("Trip duration in minutes")
    print(getDuration(getFeed(source, destination)))


def main():
    parser = argparse.ArgumentParser(
        description="Get Long Island Railroad departure, arrival and duration time."
    )
    parser.add_argument('-source', metavar='-s', type=str, help='The train station you are starting your journey from (Autocomplete requires 3 characters ore more)' )
    parser.add_argument('-destination', metavar='-d', type=str, help='The train station you are ending your journey (Autocomplete requires 3 characters ore more)')
    options = parser.parse_args()
    if os.path.isfile('stations.txt'):
        if stationStringSizeCheck(options.source,options.destination) == True:
            getTrainTimes(options.source,options.destination)
    else:
        try:
            writeStationList()
        except IOError:
            print("Stations.txt does not exist, we tried to write it to this folder. We couldn't.")
            raise
        getTrainTimes(options.source,options.destination)



# lirr/portal/api/TrainTime?startsta=NYK&endsta=HVL&year=2014&month=5&day=31&hour=18&minute=05&datoggle=d

# TODO:
# 1. Figure out a way to support (or prevent) scenarios like: -s Hewlett -d Hicksville

if __name__ == "__main__":
    main()