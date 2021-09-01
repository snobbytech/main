#! /usr/bin/env python

"""
Given a doordash url, go in and grab that restaurant's properties and menu. Output
in our nice little json file.


Sample usage:

./dd_to_db.py --mode JSON --url https://www.doordash.com/store/woodhouse-fish-co-san-francisco-981727/


"""
import os, sys, requests, json, argparse, subprocess
sys.path.insert(0, os.path.abspath('../../backend'))

os.environ['APP_CONFIG_FILE'] = '../config/dev.py'

from app import flask_app
from app.models import modelTools as mt
from app.models.modelDefs import to_public_dict


# Something to
import requests

# TODO: read this json, process and add each perdish thing.
def parse_dish_addon(dish_dict):
    # Given a json with a dish's addons, parse it...

    # This is a list of layers of options.
    toret = []
    dish_dict = dish_dict['data']['itemPage']
    # dish price.
    cur_rank = 0
    for one_option_layer in dish_dict['optionLists']:
        cur_options = {}
        cur_options['name'] = one_option_layer['name']
        cur_options['rank'] = cur_rank
        cur_options['min_options'] = one_option_layer['minNumOptions']
        cur_options['max_options'] = one_option_layer['maxNumOptions']
        all_options = []
        for one_option in one_option_layer['options']:
            cur_option_dict = {}
            cur_option_dict['name']  = one_option['name']
            cur_option_dict['price'] = one_option['unitAmount'] * 0.01
            all_options.append(cur_option_dict)
        cur_options['options'] = json.dumps(all_options)
        cur_rank += 1
        toret.append(cur_options)
    # Now, return all of these things...
    return toret

# This part processes the doordash json obj.
def parse_dd_rest_json(rest_dict, rest_url):
    rest_dict = rest_dict['data']['storepageFeed']

    # I guess, now we can start playing around? Let's start populating the stuff...
    # Then, we need to get the menu items:

    final_rest_dict = {}
    # Start parsing the stuff..
    store_header = rest_dict['storeHeader']
    # used for getting dish info.
    store_id = store_header['id']

    final_rest_dict['name'] = store_header['name']
    # I guess no phone info.
    # TODO: validate this.
    final_rest_dict['delivery_options'] = 'DOORDASH'
    final_rest_dict['available_pickup'] = store_header['offersPickup']
    final_rest_dict['street_address']   = store_header['address']['street']
    final_rest_dict['street_number']    = store_header['address']['street'].split()[0]
    final_rest_dict['route']            = store_header['address']['street'].split()[1:]
    # Not given
    final_rest_dict['extra_address_id'] = ''
    final_rest_dict['city']             = store_header['address']['city']
    # Probably find the last two-digit thing
    final_rest_dict['state'] = ''
    # Not really necessary, I guess.
    final_rest_dict['country'] = 'USA'
    final_rest_dict['lat'] = store_header['address']['lat']
    final_rest_dict['lon'] = store_header['address']['lng']

    # This can be formatted differently.
    final_rest_dict['hours'] = rest_dict['menuBook']['displayOpenHours']
    final_rest_dict['hours_pickup'] = rest_dict['menuBook']['displayOpenHours']
    # Not sure if this is necessary..
    final_rest_dict['pickup_cutoff'] = ''


    final_rest_dict['pickup_estimate_min'] = store_header['status']['pickup']['minutes'].split('-')[0].strip()
    final_rest_dict['pickup_estimate_max'] = store_header['status']['pickup']['minutes'].split('-')[1].strip()
    # I guess this is just relative to the state...
    final_rest_dict['sales_tax_rate'] = ''
    final_rest_dict['delivery_fee_taxable'] = ''
    # IDK, but maybe we can just set this at $30?
    final_rest_dict['order_minimum'] = 30
    # We gotta know this.
    final_rest_dict['dd_url'] = rest_url

    # A list of itemlist, I guess.
    menu = []
    # Now, let's go through the itemList.
    for one_itemlist in rest_dict['itemLists']:
        itemlist_dict = {}
        itemlist_dict['id'] = one_itemlist['id']
        itemlist_dict['name'] = one_itemlist['name']
        # Now we go through the dishes.
        dishes = []
        for one_dish in one_itemlist['items']:
            dish_dict = {}
            dish_dict['id'] = one_dish['id']
            dish_dict['name'] = one_dish['name']
            dish_dict['price'] = float(one_dish['displayPrice'].replace('$', ''))

            dish_options_dict = grab_dish_json(rest_url, store_id, one_dish['id'])
            # parse it more.
            smaller_dict_options = parse_dish_addon(dish_options_dict)
            dish_dict['options'] = smaller_dict_options
            # Add tqhis to the itemlist...

            dishes.append(dish_dict)
        itemlist_dict['dishes'] = dishes
        menu.append(itemlist_dict)
            # We should get the addon too.
            # TODO: add this dish to the thinger.

    # I think this should capture it.
    toret = {
        'rest': final_rest_dict,
        'menu': menu
        }
    return toret

def grab_dish_json(rest_url, rest_id, dish_id):
    dish_cmd = "cat dd_dish_cmd.sh | sed 's#OUR_DOORDASH_URL#{}#' | sed 's#DD_ITEMID#{}#'| sed 's#DD_STORE_ID#{}#'| bash".format(rest_url, dish_id, rest_id)
    dish_out = subprocess.getoutput(dish_cmd)
    dish_dict = json.loads(dish_out)
    # And... I can return this, yeh.
    return dish_dict

# This part scrapes and extracts the json from a doordash menu.
def grab_rest_json(restaurant_url):

    # Process the url in case there are other args.
    rest_url = restaurant_url.split('?')[0]
    rest_cmd = "cat dd_rest_cmd.sh | sed 's#OUR_DOORDASH_URL#{}#' | bash".format(rest_url)
    rest_out = subprocess.getoutput(rest_cmd)
    rest_dict = json.loads(rest_out)
    return rest_dict


def scrape_restaurant(rest_url):
    # First, grab the dd stuff.
    rest_json = grab_rest_json(rest_url)
    # Now process it.

    processed_rest = parse_dd_rest_json(rest_json, rest_url)
    return processed_rest

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', required=True)
    # JSON or DB or ALL
    parser.add_argument('--mode', required=True)
    parser.add_argument('--iofile', default='dd.json')
    args = parser.parse_args()
    # This should update the url too.

    if args.mode == 'JSON':
        # Grab the stuff
        dd_dicts = scrape_restaurant(args.url)
        with open(args.iofile, 'w') as f:
            json.dump(dd_dicts, f)
    elif args.mode == 'DB':
        with open(args.iofile, 'r') as f:
            dd_dicts = json.load(f)
        db_populate_rest(dd_dicts)
    elif args.mode == 'ALL':
        dd_dicts = scrape_restaurant(args.url)
        db_populate_rest(dd_dicts)
    # DONE.


    pass

if __name__ == '__main__':
    main()
