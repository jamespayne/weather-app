#!/usr/bin/env python

import csv

stops = csv.reader(open('google_transit/stops.txt'))

stations = []

for row in stops:
    line = row[1].split()
    try:
        if(len(line) == 4):
            stations.append(line[0])
        elif(len(line) == 5 and line[1] != 'Railway'):
            stations.append(line[0]+" "+line[1])
    except IndexError:
        pass
    finally:
        stations.sort()
print stations
