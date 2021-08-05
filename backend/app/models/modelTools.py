"""
Some accessible functions for dealing with our db. This separation of ideas is easier for me to deal with.


"""

from .modelDefs import to_public_dict, User, Dish, Restaurant, Order, UserTransaction, RestaurantTransaction
from .modelSetup import session_scope, con, dropAllTables
from . import modelBase


from collections import defaultdict
import datetime
import json
import os
import random
from sqlalchemy import func, inspect, or_, and_
from sqlalchemy.orm import joinload
from sqlalchemy.dialects.postgresql import UUID



def recreate_tables():
    dropAllTables()
    modelBase.ModelBase.metadata.create_all(con)


# Actual logic.

############################################################
# Users

# TODO: put in training wheels.
def add_user(userDict):
    newUser = User()
    newUser.populate_from_dict(userDict)
    valid, msg = newUser.validate():
    if valid:
        # Add it to the db.
        with session_scope() as ss:
            ss.add(newNuser)
            ss.flush()
        return newUser

    # If it didn't work, then complain?
    print("We could not add user {} because: {}".format(userDict, msg))
    return None

# Users cannot have
def mod_user(userDict):
    user = None
    if 'id' in userDict and userDict['id']:
        user = get_user(userId=userDict['id'])
    else:
        user = get_user(email=userDict['email'])

    # OK, now populate form our existing thing.
    user.populate_from_dict(userDict)
    # Also modify their updated time? datetime.datetime.utcnow()
    valid, msg = user.validate()
    if valid:
        with session_scope() as ss:
            ss.add(user)
        return user
    print("We could not modify a user because: {}".format(msg))

    return None


# TODO: make this.
def delete_user(userId):
    pass

def get_user(userId=None, email=''):
    with session_scope() as ss:
        if userId:
            return ss.query(User).get(userId)
        elif email:
            return ss.query(User).filter(User.email==email).first()
        # Failure mode.
        return None

###########################################################
# Dishes

# I think, same thing as before.
def add_dish(dishDict):
    newDish = Dish()
    newDIsh.populate_from_dict(dishDict)
    valid, msg = newDict.validate()
    if valid:
        with session_scope() as ss:
            ss.add(newDish)
            ss.flush()
        return newDish
    # Otherwise, error.
    print("We could not add dish {} because of {}".format(dishDict, msg))

def mod_dish(dishDict):
    dish = get_dish(dishDict['id'])
    dish.populate_from_dict(dishDict)

    valid, msg = dish.validate()
    if valid:
        with session_scope() as ss:
            ss.add(dish)
        return dish
    # Error state.
    print("Could not modify dish {} because {}".format(dishDict, msg))
    return None

def delete_dish(dishId):
    pass

# Pretty simple, right?
def get_dish(dishId):
    with session_scope() as ss:
        return ss.query(Dish).get(dishId)
    return None

###########################################################
# Restaurants
def add_restaurant(restaurantDict):
    newRestaurant = Restaurant()
    newRestaurant.populate_from_dict(restaurantDict)
    valid, msg = newRestaurant.validate()
    if valid:
        with session_scope() as ss:
            ss.add(newRestaurant)
            ss.flush()
        return newRestaurant
    print("Could not add restaurant {} because {}".format(restaurantDict, msg))
    return None

# Is it dumb that I did all this rewriting of the same ish? I should have just
# written a generic. Stupid guy.
def mod_restaurant(restaurantDict):
    restaurant = get_restaurant(restaurantDict['id'])
    restaurant.populate_from_dict(restaurantDict)
    valid, msg = restaurant.validate()
    if valid:
        with session_scope() as ss:
            ss.add(restaurant)
            ss.flush()
        return restaurant
    print("Could not modify restaurant {} because {}".format(restaurantDict, msg))
    return None

def delete_restaurant(restaurantId):
    # TODO: do this.
    pass

def get_restaurant(restaurantId):
    with session_scope() as ss:
        return ss.query(Restaurant).get(restaurantId)
    return None


###########################################################
# Connectors.

# Cool, now we're doing per-user dishes.
def get_dishes_for_user(userId):
    pass

# false means taking it out.
def fave_dish(userId, dishId, isFave=True):
    pass

def get_dishes_for_restaurant(restaurantId):
    pass


def get_local_influencers(lat, lon, milesRadius=5):
    pass

# Only get their dishes that are close to you.
def get_influencer_local_dishes(userId, lat, lon, milesRadius=5):
    pass

def get_local_dishes(lat, lon, milesRadius=5):
    pass

###########################################################
# Initiate order

def make_order(orderDict):
    pass

# What does this mean?
def update_order(orderDict):
    pass

def finalize_order(orderDict):
    pass


# Get all my orders.
def get_users_orders(userId):
    pass

# Gets all the money actions we've done for them.
def get_users_transactions(userId):
    # TODO: do this.
    pass


def get_restaurant_orders(restaurantId):
    # TODO: do this.
    pass

def get_restaurant_transactions(restaurantId):
    # TODO: do this.
    pass
