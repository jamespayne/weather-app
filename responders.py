#!/usr/bin/python
import stage2 as s
from stage2 import Station

# this is suitable for a GET - it has no parameters
def initialPage():

	# Set up the arrays/dictionaries to be output into the form dropdowns

	stations = s.getStations()
	timeperiods = s.getTimePeriods()
	from_specifiers = s.getFromSpecifiers()
	days = s.getDays()
	hours = s.getHours()
	minutes = s.getMinutes()

	data = "<!DOCTYPE html>"
	data += '<html>\n<head>\n'
	data += '<title>Train Weather Forecast Checker</title>\n\t'
	data += '<link rel="stylesheet" type="text/css" href="bootstrap.min.css">\n'
	data += '<link rel="stylesheet" type="text/css" href="bootstrap-theme.min.css">\n'
	data += '<link rel="stylesheet" type="text/css" href="main.css">\n'
	data += '</head>\n<body>\n'
	data += '<div class="container">\n' #Start Container
	data += '<form action="http://127.0.0.1:34567/" method="POST">\n'
	data += '<div class="form-group">\n'
	data += '<label for="station">Station</label>\n'
	data += '<select name="station" class="form-control">\n'
	for stops in stations:
		data += '\t<option value="'+stops+'">'+stops+'</option>\n'
	data += '</select>\n'
	data += '</div>\n'
	data += '<div class="row vertical-align">\n' #Start first row
	data += '<div class="col-sm-6">\n' #Start col-sm-6
	data += '<div class="form-group">\n'
	data += '<label for="days">Number of Days, Weeks, or Months</label>\n'
	data += '<input type="text" id="days" name="days" class="form-control">\n'
	data += '</div>\n'
	data += '</div>\n' #End col-sm-6
	data += '<div class="col-sm-6">\n' #Start col-sm-6
	data += '<div class="form-group">\n'
	data += '<label for="day">Time Period</label>\n'
	data += '<select name="time_period" class="form-control" selected="None">\n'
	data += '<option value="0">None</option>\n'
	for item in timeperiods:
		data += '\t<option value="'+item+'">'+item+'</option>\n'
	data += '</select>\n'
	data += '</div>\n'
	data += '</div>\n' #End col-sm-6
	data += '</div>\n' #End row
	data += '<div class="form-group">\n'
	data += '<label for="from_specifier">From</label>\n'
	data += '<select name="from_specifier" class="form-control" selected="None">\n'
	data += '<option value="0">None</option>\n'
	for item in from_specifiers:
		data += '\t<option value="'+item+'">'+item+'</option>\n'
	data += '</select>\n'
	data += '</div>\n'
	data += '<div class="form-group">\n'
	data += '<label for="dayofweek">Day</label>\n'
	data += '<select name="dayofweek" class="form-control" selected="None">\n'
	data += '<option value="0">None</option>\n'
	for value in sorted(days):
		data += '\t<option value="'+value+'">'+days[value]+'</option>\n'
	data += '</select>\n'
	data += '</div>\n'
	data += '<div class="form-group">\n'
	data +=	'<div class="checkbox">'
  	data +=	'<label><input id="showtime" type="checkbox" onclick="showTime()">Add a specific time</label>'
	data +=	'</div>'
	data += '</div>\n'
	data += '<div class="row" id="time">\n' #Start Time Row
	data += '<div class="col-sm-4">\n' #Start 1st time col
	data += '<div class="form-group">\n'
	data += '<label for="hour">Hour</label>\n'
	data += '<select name="hour" class="form-control">\n'
	for hour in hours:
		data += '\t<option value="'+hour+'">'+hour+'</option>\n'
	data += '</select>\n'
	data += '</div>\n'
	data += '</div>\n' #End 1st time col
	data += '<div class="col-sm-4">\n' #Start 2nd time col
	data += '<div class="form-group">\n'
	data += '<label for="minute">Minute</label>\n'
	data += '<select name="minute" class="form-control">\n'
	for minute in minutes:
		data += '\t<option value="'+minute+'">'+minute+'</option>\n'
	data += '</select>\n'
	data += '</div>\n'
	data += '</div>\n' #End 2nd time col
	data += '<div class="col-sm-4">\n' #Start 3rd time col
	data += '<div class="form-group">\n'
	data += '<label for="meridian">am/pm</label>\n'
	data += '<select name="meridian" class="form-control">\n'
	data += '<option value="am">am</option>\n'
	data += '<option value="pm">pm</option>\n'
	data += '</select>\n'
	data += '</div>\n'
	data += '</div>\n' #End 3rd time col
	data += '</div>\n' # End Time Row
	data += '<button class="btn btn-primary pull-right" type="submit">Get Forecast</button>\n'
	data += '</form>\n'
	data += '</div>\n' # End Container
	data += '<script src="main.js"></script>'
	data += '</body>\n</html>'
	return data

# this is suitable for a POST - it has a single parameter which is
# a dictionary of values from the web page form.

def respondToSubmit(formData):
	fieldNames = formData.keys()
	station = Station(formData.get('station'),
	          formData.get('hour'),
	          formData.get('minute'),
			  formData.get('meridian'),
	          from_specifier=formData.get('from_specifier'),
			  time_period=formData.get('time_period'),
			  n=formData.get('days')
			  )
	station.getWeather()

	data = "<!DOCTYPE html>\n"
	data += '<html>\n<head>\n'
	data += '<title>Train Weather Forecast Checker</title>\n'
	data += '<link rel="stylesheet" type="text/css" href="bootstrap.min.css">\n'
	data += '<link rel="stylesheet" type="text/css" href="bootstrap-theme.min.css">\n'
	data += '<link rel="stylesheet" type="text/css" href="weather-icons.min.css">\n'
	data += '<link rel="stylesheet" type="text/css" href="main.css">\n'
	data += '<script src="http://maps.googleapis.com/maps/api/js"></script>'

	data += '</head>\n<body>\n'
	data += '<div class="container">\n'
	if(station.data_available):
		data += '<div id="lat">'+station.lat+'</div>'
		data += '<div id="lon">'+station.lon+'</div>'
		data += '<h1>Forecast for ' + station.getName()+' @ '+station.api_datetime+ '</h1>\n'
		data += '<div class="row">\n' # Start Row
		data += '<div class="col-sm-2">\n'
		data += '<i class="wi wi-fw wi-forecast-io-'+station.icon.lower()+'"></i>\n'
		data += '</div>\n' # End col-sm-4
		data += '<div class="col-sm-3">\n'
		data += '<p>Summary: ' + station.icon + '</p>\n'
		data += '<p>Temperature: ' + station.temp + '&deg;</p>\n'
		data += '<p>Chance of Rain: ' + station.precipp + '%</p>\n'
		data += '<p>Rain Intensity: ' + station.precipi + 'in./hr.</p>\n'
		data += '<p>Wind Speed: ' + station.windSpeed + '</p>\n'
		data += '<p>Wind Direction: ' + station.windBearing + '&deg;</p>\n'
		data += '</div>\n' # End col-sm-8
		data += '<div class="col-sm-7">\n'
		data += '<div id="map"></div>'
		data += '</div>\n' # End col-sm-8
		data += '</div>\n' # End Row
		data += '<a class="btn btn-primary" href="/">Get Another Forecast</a>\n'

	else:

		data += '<p>Data not available at this time</p>'
	# Debug section
	# data += station.day_specifier
	# for field in fieldNames:
	# 	data += "field is " + field + ", value is " + formData[field] + '<br>'
	data += '<p>Powerered by DarkSky forecast API'
	data += '</div>\n' # End container
	data += '<script src="main.js"></script>'
	data += '</body>\n</html>'
	return data
