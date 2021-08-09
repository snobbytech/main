from app import flask_app

from flask import Flask, jsonify, request, Response
import sys
import traceback
import json
import tools

from models.modelDefs import to_public_dict
from models import modelTools as mt

"""
Basic endpoints from the backend. We'll eventually take some of this biz logic
outside, because we'll want backend scripts running too.


Right now: I'm going to make endpoints for each of these.

- Set session memory (zip <> ip address)
- Set zip code
- Zip code <> latlon
- address_to_latlon

- Get influencer's basic data
- Get influencer's dishes
- Get influencers' dishes within an area
- Get dish info
- Get restaurant info
- Get restaurant dishes
- Get local restaurants

# For order flow
- Get expected payment information for order
- Finalize payment for order
- Send email request after order

I'm going to do a bunch of the business logic in here, but at some point I'll move them
into its own thing.

Also, to start: making all these GETS, but eventually will move things to POST.

"""


@flask_app.route('/')
def index():
    return "Hello, World!"

# Probably don't need a full address solution yet.
@flask_app.route("/zip_to_latlon", methods=['GET'])
def zip_to_latlon():

    # Usually, request.form['zip']
    zip = '10011'

    latlon = tools.decode_zip(zip)
    return jsonify(zip)

@flask_app.route("/get_influencer_public", methods=['GET'])
def get_influencer_public():

    #
    # usually, request.form['influencer_name']
    influencer_name = 'fionaeats365'
    influencer_obj = mt.get_user(display_name=influencer_name)
    if influencer_obj:
        influencer_dict = to_public_dict(influencer_obj)
        return jsonify(influencer_dict)

    # Failure mode.
    return {}

# Has option of restricting by location too.
@flask_app.route("/get_influencer_dishes", methods=['GET'])
def get_influencer_dishes():

    influencer_name = 'fionaeats365'
    # Again, usually populated from request form.
    dishes = mt.get_dishes_for_user(influencerName=influencer_name)

    all_dishes = []
    for one_dish in dishes:
        all_dishes.append(to_public_dict(one_dish))
    return jsonify(all_dishes)


@flask_app.route("/get_influencer_dishes_area", methods=['GET'])
def get_influencer_dishes_area():
    influencer_name = 'fionaeats365'
    # in miles.
    radius = '5'
    zipCode = '10011'

    latlons = tools.decode_zip(zipCode)
    influencer = mt.get_user(display_name=influencer_name)
    local_dishes = mt.get_influencer_local_dishes(userId=influencer.id,
                                                  lat=latlons['lat'],
                                                  lon=latlons['lon'],
                                                  milesRadius=5)

    # We should probably get the restaurants too? Maybe in teh future at least.
    all_dishes = []
    for one_dish in local_dishes:
        all_dishes.append(to_public_dict(one_dish))

    return jsonify(all_dishes)


@flask_app.route("/get_dish_info", methods=['GET'])
def get_dish_info():

    # Pretty simple thing, eh?
    dish_name = 'Fried Chicken and Waffles'
    one_dish = mt.get_dish_with_name(dish_name)

    # Uhh, I guess then I... do it?
    if one_dish:
        return jsonify(to_public_dict(one_dish))
    return None

@flask_app.route("/get_restaurant_info", methods=['GET'])
def get_restaurant_info():

    restaurant_name = 'Cafeteria'
    # Really, should be getting this from a restaurant_id or a name-and-internal thing
    # or something.
    the_restaurant = mt.get_restaurant_from_name(restaurant_name)

    return jsonify(to_public_dict(the_restaurant))


@flask_app.route("/get_restaurant_dishes", methods=['GET'])
def get_restaurant_dishes():

    pass

# Initial go with the
@flask_app.route("/get_dish_payment", methods=['GET'])
def get_dish_payment():
    pass

# This grabs stuff like
@flask_app.route("/finalize_dish_order", methods=['GET'])
def finalize_dish_order():
    pass

# After the
@flask_app.route("/get_order_status", methods=['GET'])
def get_order_status():
    pass


# I'm guessing this is from some webhook or something, but basically after we
# fulfill an order this needs to mark the order as DONE.
@flask_app.route("/finalize_order", methods=['GET'])
def finalize_order():
    pass
