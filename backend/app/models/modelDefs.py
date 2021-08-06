
from .modelBase import ModelBase

from collections import defaultdict
from datetime import datetime

import re
from sqlalchemy import Column, Integer, String, Date, ForeignKey, Float, Boolean, DateTime
from sqlalchemy.orm import relationship, backref
from sqlalchemy.dialects.postgresql import UUID
from time import time
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
    firebase_id  = Column(String, unique=True)

    # We should have the actual email for all of these folks.
    email       = Column(String, unique=True)

    # This is more like their handle and url.
    display_name = Column(String)
    first_name   = Column(String)
    last_name    = Column(String)

    # Can't have multiple phones...
    phone     = Column(String, unique=True)

    # My old code used to roll its own security, for now let's just use firebase.
    # This is just to
    last_lat  = Column(Float)
    last_lon  = Column(Float)
    last_zip  = Column(String)

    # TODO: there should be some memory of delivery addresses and other things associated
    # to this person.

    # TODO: photo management will soon be its own thing, we'll have to deal with it.
    # Path to their profile photo.
    avatar_path   = Column(String)

    # This is
    is_influencer = Column(Boolean, default=False)

    # Influencer-specific fields.
    num_posts     = Column(Integer, default=0)
    num_followers = Column(Integer, default=0)

    # Is this different than #posts in a significant way? I don't know yet but let's
    # leave it in for now. We can remove later.
    num_reviews   = Column(Integer, default=0)

    # This is used for payouts and stuff.
    stripe_id    = Column(String)
    # Potentially useless column, putting it here just in case.
    preferred_payout = Column(String)

    # Only update the things in the dict.
    # props is a dict.
    def populate_from_dict(self, props):
        # Man, can this be templatized too? Probably could be, but let's do that at a
        # later date. TODO.

        # TODO: wrap this in a try/catch.

        if 'firebase_id' in props:
            self.firebase_id = props['firebase_id']
        if 'email' in props:
            self.email = props['email']
        if 'display_name' in props:
            self.display_name = props['display_name']
        if 'first_name' in props:
            self.first_name = props['first_name']
        if 'last_name' in props:
            self.last_name = props['last_name']
        if 'phone' in props:
            self.phone = props['phone']

        if 'last_lat' in props:
            self.last_lat = float(props['last_lat'])
        if 'last_lon' in props:
            self.last_lon = float(props['last_lon'])

        if 'avatar_path' in props:
            self.avatar_path = props['avatar_path']

        if 'is_influencer' in props:
            self.is_influencer = bool(props['is_influencer'])

        # The numposts, followers, reviews should probably be updated elsewhere.
        # But oh well, single source of entry.
        if 'num_posts' in props:
            self.num_posts = props['num_posts']
        if 'num_followers' in props:
            self.num_followers = props['num_followers']
        if 'num_reviews' in props:
            self.num_reviews = props['num_reviews']

        if 'stripe_id' in props:
            self.stripe_id = props['stripe_id']
        if 'preferred_payout' in props:
            self.preferred_payout = props['preferred_payout']

        # Fin.

    # returns a 2-tuple (bool, str)
    def validate(self):
        if not self.email:
            return (False, "Every user needs an email")
        # TODO: check that email is valid.

        if not self.display_name:
            return (False, "Every user needs a handle")

        # At some point, can just have a last name.
        if (not self.first_name) or (not self.last_name):
            return (False, "Person needs a name.")

        if not self.phone:
            return (False, "User needs a phone number so we can do validation")

        # Yay, this is the best.
        return (True, "")

# This is different from a post. This is more of a list of dishes that a normal user has
# hearted or something.
class UserFaveDishes(ModelBase):
    __tablename__ = 'userfavedishes'
    id = Column(Integer, primary_key=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    # I can probably include a backref here, but I don't really want to look it up right now?

    dish_id = Column(Integer, ForeignKey('dishes.id'))

    # Is there more stuff we need? I don't think so?
    pass

# Maps from influencers<> their favorite restaurants
class UserFaveRestaurants(ModelBase):
    __tablename__ = 'userfaverestaurants'

    id = Column(Integer, primary_key=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    restaurant_id = Column(Integer, ForeignKey('restaurants.id'))

# Different dishes at different restaurants.

# TODO (important): allow for dish modifications. Stuff like,
# add an egg, what sauce, etc. Basically need a way for this to be easily
# done for the restaurant
class Dish(ModelBase):

    __tablename__ = 'dishes'
    # I don't think this needs any dumb hash anyway.
    id = Column(Integer, primary_key=True)

    # Readable name.
    name = Column(String)
    restaurant_id = Column(Integer, ForeignKey('restaurants.id'))

    # Maybe better in integers?
    price = Column(Float)
    description = Column(String)

    # This might end up needing to be a collection, versus a string.
    category = Column(String)

    num_views = Column(Integer)
    # Needs to match with a hearts table, but easier to keep it stored locally.
    num_hearts = Column(Integer, default=0)
    # Path to the main photo.
    # This cannot be empty.
    main_photo = Column(String)

    # Dishes will need some amount of scoring associated with them..

    def populate_from_dict(self, props):
        if 'name' in props:
            self.name = props['name']
        if 'restaurant_id' in props:
            self.restaurant_id = props['restaurant_id']
        if 'price' in props:
            self.price = float(props['price'])
        if 'description' in props:
            self.description = props['description']
        if 'category' in props:
            self.category = props['category']
        if 'num_views' in props:
            self.num_views = props['num_views']
        if 'main_photo' in props:
            self.main_photo = props['main_photo']

    def validate(self):
        if (not self.name):
            return (False, "Every dish needs a name")

        if (not self.restaurant_id):
            return (False, "Every dish needs to be at a restaurant")

        if self.price <= 0:
            return (False, "Dish {} price {} must be positive".format(self.id, self.price))

        return (True, "")

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
    delivery_options = Column(String)

    # Introducing a

    # eg. Toast
    pos_options = Column(String)

    # Full address string.
    street_address = Column(String)

    # More in-depth address lines.
    # Grabbed from https://developers.google.com/maps/documentation/javascript/examples/places-autocomplete-address
    street_number = Column(String)
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
    num_hearts = Column(Integer, default=0)
    # Needs to be changed eventually.
    category  = Column(String)

    # Will need scoring parameters too.

    # TODO: probably need some fees in here.

    def populate_from_dict(self, props):
        if 'name' in props:
            self.name = props['name']
        if 'phone' in props:
            self.phone = props['phone']
        if 'email' in props:
            self.email = props['email']
        if 'delivery_options' in props:
            self.delivery_options = props['delivery_options']
        if 'pos_options' in props:
            self.pos_options = props['pos_options']

        if 'street_address' in props:
            self.street_address = props['street_address']

        if 'street_number' in props:
            self.street_number = props['street_number']
        if 'route' in props:
            self.route = props['route']
        if 'extra_address_id' in props:
            self.extra_address_id = props['extra_address_id']
        if 'city' in props:
            self.city = props['city']
        if 'state' in props:
            self.state = props['state']
        if 'country' in props:
            self.country = props['country']
        if 'zip_code' in props:
            self.zip_code = props['zip_code']

        if 'lat' in props:
            self.lat = props['lat']
        if 'lon' in props:
            self.lon = props['lon']

        if 'num_hearts' in props:
            self.num_hearts = props['num_hearts']

        if 'category' in props:
            self.category = props['category']

    # Returns a 2-tuple (bool, message)
    def validate(self):
        if (not self.name) or (not self.phone) or not (self.email):
            return (False, "Crucial info is missing: name {} email {} phone {} must all be filled".format(self.name, self.email, self.phone))

        if (not self.delivery_options) or (not self.pos_options):
            return (False, "pos options delivery {} pos_options {} must be filled".format(self.delivery_options, self.pos_options))

        return (True, "")

# A single order.
class Order(ModelBase):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)

    # If this order was generated from an influencer, we need to
    # attribute them.
    source_influencer = Column(UUID(as_uuid=True), ForeignKey('users.id'))
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

    # Bunch of address fields for delivering.
    street_number = Column(String)
    route = Column(String)
    extra_address_id = Column(String)
    city = Column(String)
    state = Column(String)
    zip_code = Column(String)

    delivery_notes = Column(String)

    # One of a few states, we'll have to figure this out.
    delivery_state = Column(String)

    def populate_from_dict(self, props):
        if 'source_influencer' in props:
            self.source_influencer = props['source_influencer']
        if 'restaurant_id' in props:
            self.restaurant_id = props['restaurant_id']
        if 'orderer_email' in props:
            self.orderer_email = props['orderer_email']
        if 'orderer_phone' in props:
            self.orderer_phone = props['orderer_phone']
        if 'dish_ids' in props:
            self.dish_ids = props['dish_ids']
        if 'dishes_stringified' in props:
            self.dishes_stringified = props['dishes_stringified']
        if 'subtotal' in props:
            self.subtotal = float(props['subtotal'])
        if 'taxes' in props:
            self.taxes = float(props['taxes'])
        if 'delivery_fee' in props:
            self.delivery_fee = float(props['delivery_fee'])
        if 'tip' in props:
            self.tip = float(props['tip'])
        if 'total_cost' in props:
            self.total_cost = float(props['total_cost'])
        if 'our_cut' in props:
            self.our_cut = float(props['our_cut'])
        if 'influencers_cut' in props:
            self.influencers_cut = float(props['influencers_cut'])
        if 'restaurant_payout' in props:
            self.restaurants_cut = float(props['restaurant_payout'])

        if 'street_number' in props:
            self.street_number = props['street_number']
        if 'route' in props:
            self.route = props['route']
        if 'extra_address_id' in props:
            self.extra_address_id = props['extra_address_id']
        if 'city' in props:
            self.city = props['city']
        if 'state' in props:
            self.state = props['state']
        if 'zip_code' in props:
            self.zip_code = props['zip_code']

        if 'delivery_notes' in props:
            self.delivery_notes = props['delivery_notes']
        if 'delivery_state' in props:
            self.delivery_state = props['delivery_state']

    def validate(self):
        # This doesn't need to be a big deal... so let's keep it simple for now.
        return (True, "")


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

# Deal with this later.
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
    transaction_type = Column(String)
    #
    notes  = Column(String)


# Deal with this later.
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
