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
    pass


@flask_app.route("/get_dish_info", methods=['GET'])
def get_dish_info():
    pass

@flask_app.route("/get_restaurant_info", methods=['GET'])
def get_restaurant_info():
    pass

@flask_app.route("/get_restaurant_dishes", methods=['GET'])
def get_restaurant_dishes():
    pass


@flask_app.route("/
