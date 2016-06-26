#!/usr/bin/env python

import sys, re, json, urllib2, time, csv
import datetime as dt
from dateutil.relativedelta import relativedelta

class Station:

	def __init__(self, station, hour, minute, meridian, dayofweek=0,
				n=0, from_specifier='', day='', time_period = ''):

		# Set up some basic class attributes

		self.station = station
		self.meridian = meridian
		self.timetoadd = 0
		self.from_specifier = from_specifier
		self.time_period = time_period.lower()
		self.hour = int(hour)
		self.minute = int(minute)
		self.data_available = True
		self.lat = ''
		self.lon = ''

		# Catch any errors where n is not entered

		try:
			self.n = int(n)
		except ValueError:
			self.n = 0


		# Convert the input time to a useable datetime object

		self.input_time = hour+':'+minute+meridian
		new_time = dt.datetime.strptime(self.input_time, '%I:%M%p' ).time()
		self.current_date = dt.date.today()
		self.out_dt = dt.datetime.combine(self.current_date, new_time)

		# Get required lat, lon and key for api

		self.getLatLon()
		self.getKey()

		# Process the input

		self.calcTimeDifference()
		self.buildDateTime()

	def getName(self):
		return self.station

	def getWeather(self):
		url = 'https://api.forecast.io/forecast/'
		url += self.key+'/'+self.lat+','+self.lon+','+self.api_datetime
		url += '?units=auto'
		print url
		forecast = json.load(urllib2.urlopen(url))
		try:
			self.summary = forecast['currently']['icon']
			self.temp = str(forecast['currently']['temperature'])
			self.precipp = str(forecast['currently']['precipProbability']*100)
			self.precipi = str(forecast['currently']['precipIntensity'])
			self.windSpeed = str(forecast['currently']['windSpeed'])
			self.windBearing = str(forecast['currently']['windBearing'])
			self.icon = str(forecast['currently']['icon'])
		except KeyError:

			# Handle situations where there is no data available
			# or there is an error in the API call.

			self.data_available = False
			return

	def buildDateTime(self):

		#  Function to format the datetime for api

		self.api_datetime = self.out_dt.strftime('%Y-%m-%dT%H:%M:%S')

	def calcTimeDifference(self):

		# Function to add any time if specified.

		from_specifiers = {'Tomorrow':1, 'Next Week':7, 'Today':0, 'Now':0}

		if self.time_period == 'days':
			self.timetoadd = self.n
			print self.timetoadd
			self.out_dt += relativedelta(days=self.n)
		if self.time_period == 'weeks':
			self.timetoadd = self.n
			self.out_dt += relativedelta(weeks=self.n)
		if self.time_period == 'months':
			self.timetoadd = self.n
			self.out_dt += relativedelta(months=self.n)

	def getLatLon(self):
		stops = csv.reader(open('google_transit/stops.txt'))
		for line in stops:
			if re.search(self.station, line[1]):
				self.lat = str(line[2])
				self.lon = str(line[3])

	def getKey(self):
		with open('forecastKey') as key:
			for line in key:
				line = line.replace('\n','')
				self.key = str(line)
		key.close()

def main():
	pass

if __name__ == '__main__':
	main()

# Form Helper Functions. Keep back-end seperated from front-end.

def getStations():

	stations = []

	stops = csv.reader(open('google_transit/stops.txt'))

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
	return stations


def getFromSpecifiers():
	days = ['Tomorrow','Now','Today', 'Next Week']
	return days

def getTimePeriods():
	timeperiods = ['Days','Weeks','Months']
	return timeperiods

def getDays():
	days = {'1':'Monday', '2':'Tuesday', '3':'Wednesday',
			'4':'Thursday','5':'Friday', '6':'Saturday', '7':'Sunday'}
	return days

def getHours():
	hours = []
	for hour in range(1,13,1):
		hours.append(str(hour))
	return hours

def getMinutes():
	minutes = []
	for minute in range(0, 60, 1):
		if minute < 10:
			minute = '0' + str(minute)
			minutes.append(minute)
		else:
			minutes.append(str(minute))
	return minutes

def validateForm():
	pass
