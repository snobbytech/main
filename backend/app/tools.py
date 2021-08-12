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

def get_bounding_latlons(lat, lon, dist_away_miles):
    lat_offset = abs(dist_away_miles / 69.0)
    lon_offset = abs(dist_away_miles / (69.0 * cos(radians(lat))))


    lat_max = lat + lat_offset
    lat_min = lat - lat_offset

    lon_max = lon + lon_offset
    lon_min = lon - lon_offset

    # Bound them accordingly.  Latitudes cannot roll over, whereas longitudes can.
    lat_max = min(lat_max, 90)
    lat_min = max(lat_min, -90)

    # Note that, because of how longitude is defined, that
    # this is not going to be right if we are near the 180th meridien.
    # But because this only goes through parts of the russian land bridge, antarctica,
    # and fiji, I think we can punt this until we get big enough there.

    return {'lat_max': lat_max, 'lat_min': lat_min, 'lon_max': lon_max, 'lon_min': lon_min}





##################################################################################3
# Stripe-related stuff.

import stripe
"""

Some basic stuff for Stripe on the backend. This should be replaced with the foodsnob
stripe account.
"""

LIVEKEY = ''
TESTKEY = 'sk_test_51HtkfVI5P0GyTyGvnYuTVQudtwJGXOmyPc4E7zamtEZGyirSqN7eYN76LSofjPHECce1prlzHp0IOqyJP
F6Dsvsa00hXf2atuI'

LIVEDOMAIN = ''
TESTDOMAIN = 'http://localhost:3000'

# This is accounts I used for booktime, and I'll have to update it when we switch over
# to running live with foodsnob. Anyway, it's just a placeholder, otay?
#
live_acct_id = ''
test_acct_id = 'acct_1HzOAXRA9kMKFb8T'

stripe.api_key = test_acct_id

# Note that we aren't modifying anything, we are just converting things over to
# stripe land and returning an intent and stuff.
def get_stripe_secret(amount_in_dollars):
    # TODO: figure out if this is the form

    amount_in_cents = int(amount_in_dollars * 100)
    payment_intent = stripe.PaymentIntent.create(
        payment_method_types=['card'],
        amount=amount_in_cents,
        currency='usd',
        transfer_data={
            'destination': test_acct_id
            }
        )
    # This gives the client_secret that we'd need for this transaction.
    return payment_intent.client_secret

# TODO: figure out stripe ACH payouts.
# For now: we could just do some things by hand. PUNTING FOR NOW.
