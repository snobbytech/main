#! /usr/bin/env python

"""

This will need to get updated, but:

- It should take in a bunch of test data, create the database (if needed), and then
  populate the database with stuff.

More on this later.

"""

import os
import argparse
import sys

# This is only going to work in dev mode right now.

# This is the kind of bs I have to do to do relative imports.  Why? Because
# guido sucks.  See this: https://mail.python.org/pipermail/python-3000/2007-April/006793.html
# Anyway, this means I can then add like, ..models I guess
sys.path.insert(0, os.path.abspath('..'))


os.environ['APP_CONFIG_FILE'] = '../config/dev.py'

from app import flask_app
from app.models import modelTools as mt
from app.models.modelDefs import to_public_dict

# Each is a list of prop dicts.
# FYI, this is janky af and assumes that we dont have name collisions and stuff.
# I think we can live with that for now.
def populate_db_action(users, restaurants, dishes, userFaves):

    # Add the influencers.
    new_users = []
    for user in users:
        new_user = mt.add_user(user)
        new_users.append(new_user)

    # OK, now we can do restaurants?
    new_restaurants = []
    for restaurant in restaurants:
        new_rest = mt.add_restaurant(restaurant)
        new_restaurants.append(new_rest)

    # OK, now we can do dishes?
    new_dishes = []
    for dish in dishes:
        # Have to figure out which restaurant it is too.
        the_restaurant = None
        for one_rest in new_restaurants:
            if dish['restaurant'] == one_rest.name:
                the_restaurant = one_rest

        # Have to store the restaurant name now.
        dish['restaurant_id'] = the_restaurant.id

        if the_restaurant is None:
            print("We made a mistake in naming a restaurant for {}".format(dish))
            # Halt the assembly line, because there's something the matter!
            sys.exit()

        new_dish = mt.add_dish(dish)
        new_dishes.append(new_dish)

    for userFave in userFaves:
        the_user = None
        the_dish = None
        # Have to find both of them.
        # Let's make it so that we're dealing with the user by screenname.

        for one_user in new_users:
            if one_user.display_name == userFave['user_display_name']:
                the_user = one_user
        for one_dish in new_dishes:
            if one_dish.name == userFave['dish_name']:
                the_dish = one_dish

        # Add a userfave with the corresponding ids.
        if the_user is None or the_dish is None:
            print("We made a mistake in speccing out userfaves, for some reason. Please check your data")
            print("new_users: ", new_users)
            print("dishes: ", new_dishes)
            print("userFaves: ", userFaves)
            sys.exit()

        # If it works, we set the favoriting.
        mt.set_fave_dish(the_user.id, the_dish.id, isFave=True)


    # OK, now we can hook up the favs?
    # Annoying, but the UserFaves are going to be

    print("Done!")


    # Add the

    pass


def populate_dev():
    # Making my sample data...
    print("About to start recreating data")

    # Let's have two users at least.
    users = [
        {
            'email': 'fake@email.com',
            'display_name': 'fionaeats365',
            'first_name': 'Fiona',
            'last_name': 'Lee',
            'phone': '5555555555',
            # TODO: make these real
            'last_lat': '40.7',
            'last_lon': '-74',
            'avatar_path': 'https://cdn.igblade.com/platform-cache/accounts/282268/profile-picture.jpg',
            'cover_path': 'https://i.redd.it/l69k8t3php751.jpg',
            'is_influencer': True,
            'num_posts': 5,
            'num_followers': 100,
            'stripe_id': '',
            'preferred_payout': 'SOMETHING'
        },
        {
            'email': 'fake1@email.com',
            'display_name': 'food_ilysm',
            'first_name': 'Devon',
            'last_name': 'Rushton',
            'phone': '5555555556',
            # TODO: make these real
            'last_lat': '40.6',
            'last_lon': '-74',
            # I grabbed thsi... urgh.
            'avatar_path': 'https://media-exp1.licdn.com/dms/image/C4E03AQGXiMoCqqZIJg/profile-displayphoto-shrink_400_400/0/1613672787216?e=1634169600&v=beta&t=ZgfY1HpaUdXY6AdyoPQp-kac6SiwmckGa8GHBp1N_k0',
            'cover_path': 'https://i.redd.it/7wyyv8kdh7s31.jpg',
            'is_influencer': True,
            'num_posts': 3,
            'num_followers': 10,
            'stripe_id': '',
            'preferred_payout': 'SOMETHING'
        },

    ]

    # Let's... hm.
    restaurants = [
        {
            'name':'Cafeteria',
            'phone': '5555552222',
            'email': 'fakeemail@fakeemail.com',
            'delivery_options': 'DOORDASH',
            'pos_options': 'SQUARE',
            'street_address': '119 7th ave, New York, NY 10011',
            'street_number': '119',
            'route': '7th Ave',
            'extra_address_id': '',
            'city': 'New York',
            'state': 'NY',
            'country': 'USA',
            'zip_code': '10011',
            'lat': '40.8',
            'lon': '-74',
            'num_hearts': 0,
            'category': ''
        },

        {
            'name':'The Commons Chelsea',
            'phone': '1112223333',
            'email': 'fakecommons@fake.com',
            'delivery_options': 'TOAST',
            'pos_options': 'TOAST',
            'street_address': '128 7th Ave, New York, NY 10011',
            'street_number': '128',
            'route': '7th Ave',
            'extra_address_id': '',
            'city': 'New York',
            'state': 'NY',
            'country': 'USA',
            'zip_code': '10011',
            'lat': '40.7',
            'lon': '-74',
            'num_hearts': 0,
            'category': ''
        },

    ]

    dishes = [

        {
            'name': 'Silver Dollar Pancakes',
            'restaurant': 'Cafeteria',
            'price': '11',
            'main_photo': 'https://s3-media0.fl.yelpcdn.com/bphoto/-7i6wHY23i3wwAnVXwH5Qg/o.jpg',
        },
        {
            'name': 'Truffled Eggs',
            'restaurant': 'Cafeteria',
            'price': '13',
            'main_photo': 'https://s3-media0.fl.yelpcdn.com/bphoto/hlHb4zOT8GBoXTcQ_GHGtw/o.jpg',
        },
        {
            'name': 'Fried Chicken and Waffles',
            'restaurant': 'Cafeteria',
            'price': '20',
            'main_photo': 'https://s3-media0.fl.yelpcdn.com/bphoto/BtWyrapyUIN2WaizmIRGbQ/o.jpg',
        },
        {
            'name': 'Mac Attack Tasting of All Three',
            'restaurant': 'Cafeteria',
            'price': '14',
            'main_photo': 'https://s3-media0.fl.yelpcdn.com/bphoto/BOJrbEf9D0mGCgHJr-CkJw/o.jpg',
        },

        ####################################################
        {
            'name': 'Avocado Toast',
            'restaurant': 'The Commons Chelsea',
            'price': '12',
            'main_photo': 'https://s3-media0.fl.yelpcdn.com/bphoto/jb5E6lkoaXmfQX2wWbMyAg/o.jpg',
        },
        {
            'name': 'Mushroom Toast',
            'restaurant': 'The Commons Chelsea',
            'price': '11',
            'main_photo': 'https://s3-media0.fl.yelpcdn.com/bphoto/IcxvCw6nnlDxCLOdfoJIBQ/o.jpg',
        },
        {
            'name': 'Yogurt, Fruit, and Granola',
            'restaurant': 'The Commons Chelsea',
            'price': '8',
            'main_photo': 'https://s3-media0.fl.yelpcdn.com/bphoto/zQO-SvvJruP73z1RSjfaUQ/o.jpg',
        },


    ]

    userfaves = [

        {
            'user_display_name':'fionaeats365',
            'dish_name': 'Silver Dollar Pancakes',
        },
        {
            'user_display_name':'fionaeats365',
            'dish_name': 'Truffled Eggs',
        },
        {
            'user_display_name':'fionaeats365',
            'dish_name': 'Fried Chicken and Waffles',
        },
        {
            'user_display_name':'fionaeats365',
            'dish_name': 'Avocado Toast',
        },
        {
            'user_display_name':'fionaeats365',
            'dish_name': 'Mushroom Toast',
        },
        {
            'user_display_name':'fionaeats365',
            'dish_name': 'Yogurt, Fruit, and Granola',
        },

################################################

        {
            'user_display_name':'food_ilysm',
            'dish_name': 'Truffled Eggs',
        },
        {
            'user_display_name':'food_ilysm',
            'dish_name': 'Fried Chicken and Waffles',
        },
        {
            'user_display_name':'food_ilysm',
            'dish_name': 'Mushroom Toast',
        },
        {
            'user_display_name':'food_ilysm',
            'dish_name': 'Yogurt, Fruit, and Granola',
        },
    ]

    populate_db_action(users, restaurants, dishes, userfaves)
    pass


# Always recreate the tables.
mt.recreate_tables()

# The fateful call...
populate_dev()
