# -*- coding: utf-8 -*-
"""
Created on Fri Jan  7 20:57:11 2022

@author: Admin
"""

import requests
from flask import Flask, jsonify, request
import re
import sys
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import json
import datetime

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
@app.route('/')
def earthquake():
    try:
        outbreakList=[]
        city = request.args.get("city")
        startdate = request.args.get("startdate")
        enddate = request.args.get("enddate")
        minmagnitude = request.args.get("minmagnitude")
        url = "https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson"
        geolocator = Nominatim(user_agent="myGeocoder")
        location = geolocator.geocode(city)
        latitude = location.latitude
        longitude = location.longitude
        starttime = startdate
        endtime = enddate
        url = url+"&latitude="+str(latitude)+"&longitude="+str(longitude)+"&maxradiuskm=1000&minmagnitude="+str(minmagnitude)+"&starttime="+starttime+"&endtime="+endtime
        webpage = requests.get(url)
        data = json.loads(webpage.text)
        Total_occurances = data["metadata"]["count"]
        features = data["features"]
        allf = []
        jsonresponse={}
        for indivi in features:
            earthquakes = {}
            magnitude = indivi["properties"]["mag"]
            timeDetails = indivi["properties"]["time"]
            earthquake_time = datetime.datetime.fromtimestamp((timeDetails/ 1e3)).strftime("%c")
            epicenter = (indivi["geometry"]["coordinates"][0],indivi["geometry"]["coordinates"][1])
            depth = indivi["geometry"]["coordinates"][2]
            earthquakes["magnitude"]=magnitude
            earthquakes["time"]=earthquake_time
            earthquakes["epicenter"]=epicenter
            earthquakes["depth"]=depth
            allf.append(earthquakes)
        jsonresponse["count"]=Total_occurances
        jsonresponse["location"]=city
        jsonresponse["startdate"]=startdate
        jsonresponse["enddate"]=enddate
        jsonresponse["minmagnitude"]=minmagnitude
        jsonresponse["details"]=allf
        return jsonresponse
    except:
        return sys.exc_info()[0]

if __name__ == '__main__':
    app.run(debug = False)
