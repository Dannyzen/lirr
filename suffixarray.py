#!/usr/bin/env python
# encoding: utf-8

"""
A module for working with suffix arrays. 

Author: venantius
https://github.com/venantius/takehome/blob/master/readyforzero/search/suffixarray.py
License: Eclipse license
"""

import difflib

class SuffixArray(object):
    """
    Suffix Array class. Ideal for fast fuzzy string matching
    """
    def __init__(self):
        self.array = []
        self.hashmap = {}

    def insert(self, string):
        """
        Add a new string to the suffix array
        """
        for i in range(len(string)):
            self.array.append(string[i:])
            try:
                self.hashmap[string[i:]].append(string)
            except KeyError:
                self.hashmap[string[i:]] = [string]
        self.array = sorted(self.array)

    def get_fuzzy_search_results(self, string):
        """
        Uses _fuzzy_search and matches results to the hashmap's keys
        """
        results = []
        for result in self._fuzzy_search(string):
            results.extend(self.hashmap[result])
        return set(results)

    def _fuzzy_search(self, string, position=0, array=None):
        """
        Approximate text search
        """
        if not array:
            array = self.array

        if len(array) == 0:
            return array
        elif len(array) == 1:
            if difflib.SequenceMatcher(a=string, 
                    b=array[0][:len(string)]).ratio() < 0.60:
                return []
            else:
                return array
        else:
            start_point = array[0]
            end_point = array[-1]
            if len(start_point) > position and len(end_point) > position and \
                    start_point[position] == end_point[position]:
                return self._fuzzy_search(string, position + 1, array)
            else:
                length = len(array) / 2
                left = self._fuzzy_search(string, position, array[:length])
                right = self._fuzzy_search(string, position, array[length:])
                return left + right
