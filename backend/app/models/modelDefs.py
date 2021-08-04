
from .modelBase import ModelBase

from collections import defaultdict
from datetime import datetime

import re
from sqlalchemy import Column, Integer, String, Date, ForeignKey, Float, Boolean, DateTime
from sqlalchemy.orm import relationship, backref
from sqlalchemy.dialects.postgresql import UUID
from time improt time
from werkzeug.security import generate_password_hash, check_password_hash

# Maybe timetools
import uuid

"""
Simple method to help convert model instances to dicts.
Note that this should only be used to display public-facing stuff for our site.
So we dont include private fields.

By the way, for member fields, I'm using underscore_naming because I think table values
get easier to read with that.
So maybe for class variables we use underscores, and then for local variables we use
camelCase? Ugh.


"""

def to_public_dict(modelbaseInstance):
    today = datetime.now()
    dictRep = {}
    publicFields = modelbaseInstance.public_fields()
    for key in modelbaseInstance.__dict__:
        if key in publicFields:
            if key == 'id':
                dictRep[key] = str(modelbaseInstace.__dict__[key])
            else:
                dictRep[key] = modelbaseInstance.__dict__[key]

    return dictRep


# TODO: sanitize datetimes.

# Single parent structure that encompasses users (normal) and influencers(tastemakers)
class User(ModelBase):
    __tablename__ = 'users'
    id    = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # This we need. I guess it doesn't need to be set at the start though, we can just
    # set it for them.
    firebaseId  = Column(String, unique=True)

    # We should have the actual email for all of these folks.
    email       = Column(String, unique=True)

    # This is more like their handle and url.
    displayName = Column(String)
    firstName   = Column(String)
    lastName    = Column(String)

    # Can't have multiple phones...
    phone     = Column(String, unique=True)

    # My old code used to roll its own security, for now let's just use firebase.
    # This is just to
    lastLat  = Column(Float)
    lastLon  = Column(Float)
    lastZip  = Column(String)

    # TODO: there should be some memory of delivery addresses and other things associated
    # to this person.

    # Path to their profile photo.
    avatarPath   = Column(String)

    # This is
    isInfluencer = Column(Boolean, default=False)

    # Influencer-specific fields.
    numPosts     = Column(Integer, default=0)
    numFollowers = Column(Integer, default=0)

    # Is this different than #posts in a significant way? I don't know yet but let's
    # leave it in for now. We can remove later.
    numReviews   = Column(Integer, default=0)

    # This is used for payouts and stuff.
    stripe_id    = Column(String)
    # Potentially useless column, putting it here just in case.
    preferred_payout = Column(String)
    pass

# This is different from a post. This is more of a list of dishes that a normal user has
# hearted or something.
class UserFaveDishes(ModelBase):
    __tablename__ = 'userfavedishes'
    id = Column(Integer, primary_key=True)
    userId = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    # I can probably include a backref here, but I don't really want to look it up right now?

    dishId = Column(Integer, ForeignKey('dishes.id'))

    # Is there more stuff we need? I don't think so?
    pass

# Maps from influencers<> their favorite restaurants
class UserFaveRestaurants(ModelBase):
    __tablename__ = 'userfaverestaurants'

    id = Column(Integer, primary_key=True)
    userId = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    restaurantId = Column(Integer, ForeignKey('restaurants.id'))


# Different dishes at different restaurants.
class Dish(ModelBase):

    __tablename__ = 'dishes'
    # I don't think this needs any dumb hash anyway.
    id = Column(Integer, primary_key=True)

    # Readable name.
    name = Column(String)
    restaurantId = Column(Integer, ForeignKey('restaurants.id'))

    # Maybe better in integers?
    price = Column(Float)
    description = Column(String)

    # This might end up needing to be a collection, versus a string.
    category = Column(String)

    numViews = Column(Integer)
    # Needs to match with a hearts table, but easier to keep it stored locally.
    numHearts = Column(Integer, default=0)
    # Path to the main photo.
    # This cannot be empty.
    mainPhoto = Column(String)

    # Dishes will need some amount of scoring associated with them..



# Pretty simple, right.
class Restaurant(ModelBase):
    __tablename__ = 'restaurants'
    id = Column(Integer, primary_key=True)

    name = Column(String)
    # For contact.
    phone = Column(String)
    # Need this to send orders for now.
    email = Column(String)

    # eg. UberEats, DoorDash.
    # For now, let's keep this as the stringification of a list? shrug emoji.
    deliveryOptions = Column(String)

    # eg. Toast
    posOptions = Column(String)

    # Full address string.
    streetAddress = Column(String)

    # More in-depth address lines.
    # Grabbed from https://developers.google.com/maps/documentation/javascript/examples/places-autocomplete-address
    streetNumber = Column(String)
    route         = Column(String)
    # eg. apartment no.
    extra_address_id = Column(String)

    city      = Column(String)

    # State
    state = Column(String)
    country       = Column(String)
    # Zip.
    zip_code   = Column(String)

    # These are used more for
    lat = Column(Float)
    lon = Column(Float)

    # Just something to expedite.
    numHearts = Column(Integer, default=0)
    # Needs to be changed eventually.
    category  = Column(String)

    # Will need scoring parameters too.

    # TODO: probably need some fees in here.

    pass

# A single order.
class Order(ModelBase):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)

    # If this order was generated from an influencer, we need to
    # attribute them.
    source_influencer = Column(Integer, ForeignKey('users.id'))
    restaurant_id     = Column(Integer, ForeignKey('restaurants.id'))

    # Right now, we're not creating users for order-ers, so we're storing these for
    # reconciliation later.
    orderer_email = Column(String)
    orderer_phone = Column(String)

    # This is a string because it's a list of dish ids.
    dish_ids       = Column(String)

    # This is more resilient (eg. if dishes change, then we don't want those to be reflected here)
    dishes_stringified = Column(String)

    subtotal      = Column(Float)
    taxes         = Column(Float)
    delivery_fee  = Column(Float)
    tip           = Column(Float)
    total_cost    = Column(Float)

    our_cut       = Column(Float)
    influencers_cut = Column(Float)
    restaurant_payout = Column(Float)

    # Bunch of address fields.
    street_number = Column(String)
    route = Column(String)
    extra_address_id = Column(String)
    city = Column(String)
    state = Column(String)
    zip_code = Column(String)

    delivery_notes = Column(String)

    # One of a few states, we'll have to figure this out.
    delivery_state = Column(String)


# TODO: do this.
# A DishReview can be done by an influencer
#class DishReview(ModelBase):
#    pass

# Do this later?
#class ResturantReview(ModelBase):
#    pass


# Quick saves.
#class DishHeart(ModelBase):
#    pass

#class RestaurantHeart(ModelBase):
#    pass


# Types of tags.
# TODO: do this.
#class Tag(ModelBase):
#    pass

# These are usually payouts.
class UserTransaction(ModelBase):
    __tablename__ = 'usertransactions'
    id = Column(Integer, primary_key=True)

    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'))

    # Also, all times are done in UTC.
    initiated_time = Column(DateTime, default=datetime.utcnow)

    last_updated   = Column(DateTime, default=datetime.utcnow)

    amount = Column(Float)

    # We can either give them money or take away money?
    give_them_money = Column(Boolean)

    # Not sure if this has real meaning yet, just in case.
    status = Column(String)

    # More useful name for them.
    transactionType = Column(String)
    #
    notes  = Column(String)



class RestaurantTransactions(ModelBase):
    __tablename__ = 'restauranttransactions'
    id = Column(Integer, primary_key=True)
    restaurant_id = Column(Integer, ForeignKey('restaurants.id'))

    initiated_time = Column(DateTime, default=datetime.utcnow)
    last_updated = Column(DateTime, default=datetime.utcnow)

    amount = Column(Float)
    give_them_money = Column(Boolean)

    status = Column(String)
    transaction_type = Column(String)
    notes = Column(String)
