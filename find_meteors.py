# -*- coding: utf-8 -*-
"""
Created on Mon May 14 14:01:23 2018

@author: JESUDDI1
"""

#------ This part of the code to set the proxies for accessing website from intranet
import os, os.path

os.environ['HTTP_PROXY']="http://nibr-proxy.global.nibr.novartis.net:2011"
os.environ['HTTPS_PROXY']="http://nibr-proxy.global.nibr.novartis.net:2011"
#----

import math

def calc_dist(lat1, lon1, lat2, lon2):
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)

    h = math.sin( (lat2 - lat1) / 2 ) ** 2 + \
        math.cos(lat1) * math.cos(lat2) * math.sin( (lon2 - lon1) / 2) ** 2

    return 6372.8 * 2 * math.asin(math.sqrt(h))
#------------------------------------------------------------------------------

import requests

#From NASA website that provides meteorite landing data get the data to python var
#It is a list of dictionaries, each dictionary represents a single meteorite landing location

meteor_resp=requests.get('https://data.nasa.gov/resource/y77d-th95.json')

#store the data in JSON format
meteor_data = meteor_resp.json()

'''
From https://www.findlatitudeandlongitude.com/find-latitude-and-longitude-from-address
find the lattitude and longitude of a source location from where we want
to find the distance of all meteor landings
'''
my_loc = (42.360083, -71.05888)   #tuple to store the location values of Boston, MA
for meteor in meteor_data:
    if 'reclat' not in meteor or 'reclong' not in meteor:
        continue
    else:
        #add the 'distance' key to the meteor data
        meteor['distance'] = calc_dist( float(meteor['reclat']), float(meteor['reclong']), my_loc[0], my_loc[1])
'''
Now that the distance is computed for all meteor landings from my location
let us sort them on it. As the meteor data is  LIST of DICTIONARIES it is not
possible to access the distance field directly. We can use the function as a parameter
in python that gets the distance and supply it to the built in sort()
'''
def get_dist(x):
    return x.get('distance', math.inf)

meteor_data.sort(key=get_dist)

#print( meteor_data[0] )  #The first element is the landing site closest to Boston

'''
Since many landings did not have the distance field(as there are no location data)
we can list how many don't have that. We use list comprehension
'''
no_dist = [x for x in meteor_data if 'distance' not in x]
print(len(no_dist), 'meteors landed in unknown locations')
print(no_dist)
