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

    restaurant_name = 'Cafeteria'
    the_restaurant = mt.get_restaurant_from_name(restaurant_name)

    # Now get dishes
    the_dishes = mt.get_dishes_for_restaurant(the_restaurant.id)
    all_dishes = []
    for one_dish in the_dishes:
        all_dishes.append(to_public_dict(one_dish))

    return jsonify(all_dishes)

# Returns a dict...
@flask_app.route("/get_dish_payment", methods=['GET'])
def get_dish_payment():

    dish_name = 'Fried Chicken and Waffles'
    the_dish = mt.get_dish_with_name(dish_name)


    ret_dict = {}
    ret_dict['subtotal'] = the_dish.price

    # TODO SOON: get an actual tax calculator for the actual thing.
    # Goign to take the worst case scenario for californian restaurants.
    ret_dict['local_tax'] = the_dish.price *0.1025


    # Let's assume this?
    ret_dict['delivery'] = 7.00

    # I guess we can make our own fees too.
    ret_dict['our_fees'] = the_dish.price * 0.15

    # TODO: let the user tip the restaurant
    ret_dict['tip'] = 0.


    # TODO: let the user tip the dasher.
    ret_dict['dasher_tip'] = 0.


    ret_dict['total_cost'] = ret_dict['subtotal'] + ret_dict['local_tax'] + ret_dict['delivery'] + ret_dict['our_fees'] + ret_dict['tip'] + ret_dict['dasher_tip']


    # OK, is it fair? I dont know.
    return jsonify(ret_dict)


    # Basically we do a calculation of fees.

# This happens after the user pays. We grab the order and finalize it in our db.
@flask_app.route("/finalize_create_order", methods=['GET'])
def finalize_dish_order():

    # This kind of stuff should be grabbed from the POST variables.
    order_dict = {
        'source_influencer': '',
        'restaurant_id': '',
        'orderer_email': 'itsdchen@gmail.com',
        'orderer_phone': '8057763767',
        'dish_ids': '["2000"]',
        'dishes_stringified': 'BLOOP BLOP',
        'subtotal': 50,
        'taxes': 5.13,
        'delivery_fee': 7,
        'tip': 10.,
        'dasher_tip': 0,
        'total_cost': 90,
        'our_cut': 10.,
        'influencers_cut': 3,
        'restaurant_payout': 70,
        'street_number': '50',
        'route': 'Broadway',
        'extra_address_id': '# 8C',
        'city': 'New York',
        'State': 'NY',
        'zip_code': '10011',
        'delivery_notes': 'Please just leave it there and I can come down and pick it up',
        'delivery_state': 'ORDER_CREATED',
        'payment_id': '988',
        'payment_method': 'STRIPE'
    }

    # We made the order, so we'll just make it. Yeah.

    the_order = mt.make_order(order_dict)

    if the_order:
        return jsonify({'success': True, 'order_id': the_order.id})
    # Otherwise, we have bitter defeat.
    return None

    pass

# We have to grab the order and return its values, no biggie.
@flask_app.route("/get_order_status", methods=['GET'])
def get_order_status():


    order_id = 30
    the_order = mt.get_order(order_id)

    # I guess I can just... take the dict.
    return jsonify(to_public_dict(the_order))


# I'm guessing this is from some webhook or something, but basically after we
# fulfill an order this needs to mark the order as DONE.
@flask_app.route("/finalize_order", methods=['GET'])
def finalize_order():

    order_id = 30
    the_order = mt.get_order(order_id)

    update_dict = {}
    update_dict['delivery_state'] = 'RESTAURANT_PREP'

    mt.update_order(order_id, update_dict)
    return jsonify({'success': True})
