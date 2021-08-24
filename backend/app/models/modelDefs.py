
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
                dictRep[key] = str(modelbaseInstance.__dict__[key])
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

    # This is like the facebook cover photo.
    cover_path    = Column(String)

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
        if 'cover_path' in props:
            self.cover_path = props['cover_path']

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

    # Stuff that the average person should be able to see.
    def public_fields(self):
        return ['id', 'display_name', 'first_name', 'last_name', 'phone', 'last_lat', 'last_lon', 'last_zip', 'avatar_path', 'cover_path', 'is_influencer', 'num_posts', 'num_followers']


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


# Note: in general, a dish can be a member of multiple categories.
class DishCategory(ModelBase):
    __tablename__ = 'dishcategories'
    id = Column(Integer, primary_key=True)


    name = Column(String)
    # How to sort categories when displaying a menu
    rank = Column(Integer)
    restaurant_id = Column(Integer, ForeignKey('restaurants.id'))

# Note: when implementing population, I should make sure there arent
#       double entries here...
#       Also: I think there are better ways of doing this with
#       sqlalchemy, but too lazy to look it up right now.
class DishCategoryMap(ModelBase):
    __tablename__ = 'dishcategorymap'

    id = Column(Integer, primary_key=True)
    dish_id = Column(Integer, ForeignKey('dishes.id'))
    category_id = Column(Integer, ForeignKey('dishcategories.id'))


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

    # Just in case, going to keep this in here.
    grubhub_id = Column(String)
    # There will probably be lines here for ubereats and dd.

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
        if 'grubhub_id' in props:
            self.grubhub_id = props['grubhub_id']

    def validate(self):
        if (not self.name):
            return (False, "Every dish needs a name")

        if (not self.restaurant_id):
            return (False, "Every dish needs to be at a restaurant")

        if self.price <= 0:
            return (False, "Dish {} price {} must be positive".format(self.id, self.price))

        return (True, "")

    def public_fields(self):
        return ['id', 'name', 'restaurant_id', 'price', 'description', 'category', 'num_views', 'num_hearts', 'main_photo']

class DishAddons(ModelBase):
    __tablename__ = 'dishaddons'

    name = Column(String)
    # For the ordering.
    rank = Column(Integer)
    min_options = Column(Integer, default=0)
    max_options = Column(Integer)

    # Going to just stringify and unstringify these.
    # Going to be a list of dicts, "name", "price".
    options = Column(String)

    def public_fields(self):
        return ['id', 'name', 'rank', 'min_options', 'max_options', 'options']

# Pretty simple, right.
class Restaurant(ModelBase):
    __tablename__ = 'restaurants'
    id = Column(Integer, primary_key=True)

    name = Column(String)

    # We should be using this for url endpoints.
    url_name = Column(String)

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

    available_pickup = Column(Boolean)

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

    # This is a stringified version of an hours_open thing.
    # Note that this is given in like, UTC Time or something.
    # TODO: figure this ish out.
    hours     = Column(String)
    hours_pickup = Column(String)
    # I'm guessing it's like,
    pickup_cutoff = Column(Number)

    # Time range that these pickups tend to be.
    pickup_estimate_min = Column(Number)
    pickup_estimate_max = Column(Number)


    # This is in the number multipled. So, 1% is 0.01
    sales_tax_rate = Column(Float)
    delivery_fee_taxable = Column(Boolean)

    # This is in dollars.
    order_minimum = Column(Float)

    # For data syncing.
    grubhub_url  = Column(String)
    ubereats_url = Column(String)
    dd_url       = Column(String)
    yelp_url     = Column(String)

    # Will need scoring parameters too.

    # TODO: probably need some fees in here.

    def populate_from_dict(self, props):
        if 'name' in props:
            self.name = props['name']
        if 'url_name' in props:
            self.url_name = props['url_name']
        if 'phone' in props:
            self.phone = props['phone']
        if 'email' in props:
            self.email = props['email']
        if 'delivery_options' in props:
            self.delivery_options = props['delivery_options']
        if 'available_pickup' in props:
            self.available_pickup = props['available_pickup']

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
        if 'hours' in props:
            self.hours = props['hours']
        if 'hours_pickup' in props:
            self.hours_pickup = props['hours_pickup']
        if 'pickup_cutoff' in props:
            self.pickup_cutoff = props['pickup_cutoff']
        if 'pickup_estimate_min' in props:
            self.pickup_estimate_min = props['pickup_estimate_min']
        if 'pickup_estimate_max' in props:
            self.pickup_estimate_max = props['pickup_estimate_max']
        if 'sales_tax_rate' in props:
            self.sales_tax_rate = props['sales_tax_rate']
        if 'delivery_fee_taxable' in props:
            self.delivery_fee_taxable = props['delivery_fee_taxable']
        if 'order_minimum' in props:
            self.order_minimum = props['order_minimum']

        if 'grubhub_url' in props:
            self.grubhub_url = props['grubhub_url']
        if 'ubereats_url' in props:
            self.ubereats_url = props['ubereats_url']
        if 'dd_url' in props:
            self.dd_url = props['dd_url']
        if 'yelp_url' in props:
            self.yelp_url = props['yelp_url']

    # Returns a 2-tuple (bool, message)
    def validate(self):
        if (not self.name) or (not self.phone) or not (self.email):
            return (False, "Crucial info is missing: name {} email {} phone {} must all be filled".format(self.name, self.email, self.phone))

        if (not self.delivery_options) or (not self.pos_options):
            return (False, "pos options delivery {} pos_options {} must be filled".format(self.delivery_options, self.pos_options))

        if not (self.url_name):
            return (False, "Creating a restaurant: empty url_names are not allowed")
        return (True, "")

    def public_fields(self):
        return ['name', 'url_name', 'phone', 'delivery_options', 'pos_options', 'available_pickup', 'street_address', 'zip_code', 'lat', 'lon', 'num_hearts', 'category', 'hours', 'hours_pickup', 'pickup_cutoff', 'pickup_estimate_min', 'pickup_estimate_max', 'sales_tax_rate', 'delivery_fee_taxable', 'order_minimum']

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

    order_notes    = Column(String)

    subtotal       = Column(Float)

    # These adjustments are made on the order-level (vs. on the orderline-level).
    # The adjustments are independent of the ones on the orderline.
    adjustments    = Column(Float)
    adjustment_note = Column(String)
    promo_code     = Column(String)

    taxes          = Column(Float)
    delivery_fee   = Column(Float)
    tip            = Column(Float)
    dasher_tip     = Column(Float)
    total_cost     = Column(Float)
    our_fees       = Column(Float)
    influencers_cut = Column(Float)
    restaurant_payout = Column(Float)

    # Bunch of address fields for delivering.
    street_number    = Column(String)
    route            = Column(String)
    extra_address_id = Column(String)
    city             = Column(String)
    state            = Column(String)
    zip_code         = Column(String)
    delivery_notes   = Column(String)

    # One of a few states, we'll have to figure this out.
    #ORDER_CREATED, RESTAURANT_PREP, OUT_FOR_DELIVERY, DELIVERED, REFUNDED
    delivery_state = Column(String)

    # Stuff like DOORDASH, OLO, etc.
    delivery_method = Column(String)

    # like the stripe payment id or something.
    payment_id     = Column(String)

    # eg. STRIPE, etc.
    payment_method = Column(String)

    pay_state      = Column(String)

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
        if 'order_notes' in props:
            self.order_notes = props['order_notes']
        if 'subtotal' in props:
            self.subtotal = float(props['subtotal'])
        if 'adjustments' in props:
            self.adjustments = float(props['adjustments'])
        if 'adjustment_note' in props:
            self.adjustment_note = props['adjustment_note']
        if 'promo_code' in props:
            self.promo_code = props['promo_code']
        if 'local_taxes' in props:
            self.taxes = float(props['local_taxes'])
        if 'delivery_fee' in props:
            self.delivery_fee = float(props['delivery_fee'])
        if 'tip' in props:
            self.tip = float(props['tip'])
        if 'dasher_tip' in props:
            self.dasher_tip = float(props['tip'])
        if 'total_cost' in props:
            self.total_cost = float(props['total_cost'])
        if 'our_fees' in props:
            self.our_cut = float(props['our_fees'])
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
        if 'delivery_method' in props:
            self.delivery_method = props['delivery_method']

        if 'payment_id' in props:
            self.payment_id = props['payment_id']
        if 'payment_method' in props:
            self.payment_method = props['payment_method']
        if 'pay_state' in props:
            self.pay_state = props['pay_state']

    def validate(self):
        # This doesn't need to be a big deal... so let's keep it simple for now.
        return (True, "")

    # This needs to be done, m8.
    def public_fields(self):
        return ['source_influencer', 'restaurant_id', 'orderer_email', 'orderer_phone', 'dish_ids', 'dishes_stringified', 'order_notes', 'subtotal', 'adjustments', 'adjustment_note', 'promo_code', 'local_taxes', 'delivery_fee', 'tip', 'dasher_tip', 'total_cost', 'our_fees', 'influencers_cut', 'restaurant_payout', 'street_number', 'route', 'extra_addrses_id', 'city', 'state', 'zip_code', 'delivery_notes', 'delivery_state', 'delivery_method', 'payment_method', 'pay_state']
        pass

class OrderLineItem(ModelBase):
    # An order can have multiple line items, fyi.
    __tablename__ = 'orderlineitems'

    id       = Column(Integer, primary_key=True)

    order_id = Column(Integer, ForeignKey('orders.id'))

    name      = Column(String)
    dish_id   = Column(Integer, ForeignKey('dishes.id'))
    dish_name = Column(String)

    # Note that we don't have a notion of "quantity". We want every instance of a dish to
    # have its own line - so it's easier to order a Chicken Pad Thai and a Beef Pad Thai too.

    # Price after all adjustments.
    end_price = Column(Float)

    # Positive or negative. Usually negative, because we could have a promotion or something.
    adjustments = Column(Float)
    adjustment_note = Column(String)

    # Basically, a stringified dict of the addons for the dish. The dict looks like:
    # {"option": "Beef", "Price": "3"}
    addons = Column(String)

    # If there are any customizations needed.
    notes  = Column(String)

    def populate_from_dict(self, props):
        if 'order_id' in props:
            self.order_id = props['order_id']
        if 'name' in props:
            self.name = props['name']
        if 'dish_id' in props:
            self.dish_id = props['dish_id']
        if 'end_price' in props:
            self.end_price = props['end_price']
        if 'adjustments' in props:
            self.adjustments = props['adjustments']
        if 'adjustment_note' in props:
            self.adjustment_note = props['adjustment_note']
        if 'addons' in props:
            self.addons = props['addons']
        if 'notes' in props:
            self.notes = props['notes']

    def public_fields(self):
        return ['id', 'order_id', 'name', 'dish_id', 'end_price', 'adjustments', 'adjustment_note', 'notes']


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
