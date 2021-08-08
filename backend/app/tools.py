#! /usr/bin/env python

"""
Just a bunch of useful tools for us.  This can include cool things like...


- Geography tools
- Mail tools
- Stripe tools.

"""

from math import radians, sin, cos, acos

import pgeocode
geo = pgeocode.Nominatim('us')

def decode_zip(zipCode):
    x = geo.query_postal_code(zipCode)
    #print(dir(x))

    print(x.latitude)
    print(x.longitude)

    return {'lat': x.latitude, 'lon': x.longitude}


# References:
# Haversine formula:
# https://en.wikipedia.org/wiki/Haversine_formula
#
# Actual code example: https://www.plumislandmedia.net/mysql/haversine-mysql-nearest-loc/

# From this, we get that the distance between two points in space is
# arccos( cos(lat1_radians)*cos(lat2_radians)*cos(long1_radians-long2_radians) + sin(lat1_radians)*sin
# That gives you an angular measure, and then you need to turn it back into units of length
# again.  I trust you know how to do that, good sir.

def get_bounding_latlons(lat, lon, dist_away_mils):
