#!/usr/bin/env python

from flask import Flask, render_template, request
from station import *

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route('/')
def index():
    stations = jsonify(getStations())
    hours = getHours()
    minutes = getMinutes()
    return render_template('index.html', stations=stations)

@app.route('/report', methods=['POST'])
def report():
    station = request.form.get('station')
    return render_template('report.html', station=station)
