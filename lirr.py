#!/usr/bin/env python
"""
Get Long Island Railroad departure, arrival and duration times.

Usage: python lirr.py  (-f <favorite> | -s <source> -d <destination>) [(--additional_hour | -a) <hours>]

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

def getFavoriteByNumber(fave_number):
    data = loadFavorites()
    favorites = {}
    favorites['source'] = data[int(fave_number)][str(fave_number)]["source"]
    favorites['destination'] = data[int(fave_number)][str(fave_number)]["destination"]
    return favorites

def loadFavorites():
    favorite_data = json.load(open('favorites.json'))
    return favorite_data

#TODO: Figure out writing favorites.
# Writing
# def writeFavorites(source, destination):
#     data = loadFavorites()
#     position = len(data)
#     new_favorite = {i:{"source":source,"destination":destination}}
#     data.append(new_favorite)
#     with open('favorites.json', mode='w', encoding='utf-8') as favorites_json:
#         json.dump(data.append(new_favorite),favorties_json)

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

"""
def checkFavoriteFile(favorite_number):
    This should return true if a key already exists with the passed number

TODO: Figure out writing favorites.
Writing
def updateFavorites(source, destination):
    data = loadFavorites()
    position = len(data)
    new_favorite = {i:{"source":source,"destination":destination}}
    data.append(new_favorite)
    with open('favorites.json', mode='w', encoding='utf-8') as favorites_json:
        json.dump(data.append(new_favorite),favorties_json)

def writeFavoriteFile(favorite_number):
    initial writing of favorties.json
    check if file exists
    if not write it
        handle issues writing
"""

def populateSuffixArray(keys):
    """
    Takes a list of keys and initializes and populates a 
    suffixarray.SuffixArray object
    """
    suffix_array = SuffixArray()
    for key in keys:
        suffix_array.insert(key)
    return suffix_array

def getStationId(station):
    """
    Load stations in as a dict from stations.txt
    Ex: {"Penn Station":"NYK"}

    Uses a suffix array implementation for fuzzy string matching
    """
    stations = {}
    stations = ast.literal_eval(open('stations.txt').read())
    # lowercase all station names in stations
    stations = dict((k.lower(), v) for k, v in stations.iteritems())
    suffix_array = populateSuffixArray(stations.keys())
    results = [v for (k, v) in stations.iteritems() if station in k]
    if len(results) == 1:
        return results[0]
    else:
        results = suffix_array.get_fuzzy_search_results(station)
        if len(results) == 0:
            print("Tried to find the station. Couldn't. Blaming you.")
            sys.exit()
        elif len(results) == 1:
            print("Assuming you meant to type '%s' when you wrote '%s'" % \
                    (list(results)[0], station), file=sys.stderr)
            return stations[list(results)[0]]
        else:
            print("Couldn't autocomplete '%s' - did you mean one of the following?" % \
                    station, file=sys.stderr)
            for potential_match in list(results):
                print(potential_match, file=sys.stderr)
            sys.exit()

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
        print("destination was fucked up")
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
    #TODO I reckon this is broken when you add more hours than there are left in the day...
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
    headers = [source + " departure times", destination + " arrival times", "Trip duration in minutes"]
    feed = getFeed(source, destination, additional_hour)
    departures = convertTimes(getDepartureTimes(feed))
    arrivals = convertTimes(getArrivalTimes(feed))
    durations = getDuration(feed)
    table = zip(departures, arrivals, durations)
    print(tabulate(table, headers))

# TODO:
# Figure out a way to support (or prevent) scenarios like: -s Hewlett -d Hicksville

if __name__ == "__main__":
    opts = docopt.docopt(__doc__, sys.argv)
    if os.path.isfile('stations.txt'):
        # If stations.txt exists
        if opts['<favorite>']:
            #If a favorite option is passed
            if os.path.isfile('favorites.json'):
                #If the favorites file exists
                    favorites = getFavoriteByNumber(opts['<favorite>'])
                    getTrainTimes(favorites["source"],favorites["destination"],opts["<hours>"])
            else:
                    #Favorite file does not exist, we need to make it
                    #TODO Make favorite file
                    print("No favorites file loaded")
        else:
            #If favorite param is not passed
            if stationStringSizeCheck(opts['<source>'], opts['<destination>']) == True:
                getTrainTimes(opts['<source>'], opts['<destination>'], opts['<hours>'])
    else:
        #If stations.txt does not exist
        try:
            writeStationList()
        except IOError:
            print("Stations.txt does not exist, we tried to write it to this folder. We couldn't. Make sure this folder is writeable.")
            raise
        getTrainTimes(opts['<source>'], opts['<destination>'], opts['<hours>'])
