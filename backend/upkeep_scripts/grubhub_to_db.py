#! /usr/bin/env python

"""
Given a grubhub url (what the restaurant is), we'll go in and
grab the restaurant's properties and menu.


Step 1: I'm going to output its menu to a JSON file.

Example usage:
./grubhub_to_db.py --mode JSON --url https://www.grubhub.com/restaurant/love-burn-130-northwood-dr-south-san-francisco/2428407?=undefined&utm_source=google&utm_medium=cpc&utm_campaign=&utm_term=f%3Aplacesheet%3Afeature_id_fprint%3D17868528579844763466&utm_content=acct_id-3075806372%3Acamp_id-10331808441%3Aadgroup_id-122350726255%3Akwd-1063567739721%3Acreative_id-533614949007%3Aext_id-147051630757%3Amatchtype_id-%3Anetwork-g%3Adevice-c%3Aloc_interest-1014221%3Aloc_physical-9067609&gclid=CjwKCAjw95yJBhAgEiwAmRrutMKX43bB6KKy8zaVl3hkPexFbTDohGB5jLcwUpMNRZjw5KXzSr3zQhoC5AcQAvD_BwE

Step 2: I'm going to straight up

Example usage:

Step 3: bypass the JSON output and just modify the database, end to end.


"""
import os
import sys
import requests
import json
import argparse

sys.path.insert(0, os.path.abspath('..'))

os.environ['APP_CONFIG_FILE'] = '../config/dev.py'

from app import flask_app
from app.models import modelTools as mt
from app.models.modelDefs import to_public_dict


##############################################################################
# Stuff for accessing grubhub.
cur_access_token = ''

# In the future, we can probably save these access- and refresh- tokens.
# Looks like some of these units are returned in minutes. It looks like the refresh
# tokens will last like, a week. Not that it's necessarily useful like this.

def get_access_token():
    global cur_access_token
    ac_headers = {
        'authority': 'api-gtm.grubhub.com',
        'authorization': 'Bearer aaa',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36',
        'content-type': 'application/json;charset=UTF-8',
        'accept': '*/*',
        'origin': 'https://www.grubhub.com',
        'sec-fetch-site': 'same-site',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://www.grubhub.com/',
        'accept-language': 'en-US,en;q=0.9',
    }

    ac_data = '{"brand":"GRUBHUB","client_id":"beta_UmWlpstzQSFmocLy3h1UieYcVST","device_id":-563554861,"refresh_token":"0e8002a8-5b90-4002-9993-c0d2624c4463"}'

    ac_response = requests.post('https://api-gtm.grubhub.com/auth', headers=ac_headers, data=ac_data)
    if ac_response.status_code != 200:
        print("We failed trying to get an access token - check the request? ")
        sys.exit()
    # Otherwise, read the json.

    ac_json = json.loads(ac_response.text)

    ac_key = ac_json['session_handle']['access_token']
    # Can print out the other stuff too...
    cur_access_token = ac_key


    pass




rest_headers = {
    'authority': 'api-gtm.grubhub.com',
    'cache-control': 'max-age=0',
    'accept': 'application/json',
    'authorization': 'Bearer {}',
    'if-modified-since': '0',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36',
    'origin': 'https://www.grubhub.com',
    'sec-fetch-site': 'same-site',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://www.grubhub.com/',
    'accept-language': 'en-US,en;q=0.9',
}

rest_params = (
    ('hideChoiceCategories', 'true'),
    ('version', '4'),
    ('variationId', 'rtpFreeItems'),
    ('orderType', 'standard'),
    ('hideUnavailableMenuItems', 'true'),
    ('hideMenuItems', 'false'),
)
rest_tgt = 'https://api-gtm.grubhub.com/restaurants/{}'




# Note, in this case, the auntie guan's kitchen url is
# https://www.grubhub.com/restaurant/auntie-guans-kitchen-108-108-w-14th-st-new-york/322383
# So, they're just using the restaurant's uid.
# Interesting, so I'm guessing we could probably scrape the entire grubhub thing over time, if we scaled it out. Hah.

#response = requests.get('https://api-gtm.grubhub.com/restaurants/322383', headers=headers, params=params)

#NB. Original query string below. It seems impossible to parse and
#reproduce query strings 100% accurately so the one below is given
#in case the reproduced version is not "correct".
# response = requests.get('https://api-gtm.grubhub.com/restaurants/322383?hideChoiceCategories=true&version=4&variationId=rtpFreeItems&orderType=standard&hideUnavailableMenuItems=true&hideMenuItems=false', headers=headers)



# For calling about per-dish options:
perdish_headers = {
    'authority': 'api-gtm.grubhub.com',
    'cache-control': 'no-cache',
    'accept': 'application/json',
    'authorization': 'Bearer {}',
    'perimeter-x': 'eyJ1IjoiZDAzMWM5OTAtMDFjZC0xMWVjLTg3YTktMzE2ZTYzN2JiMGYxIiwidiI6ImQwMzQyMmVhLTAxY2QtMTFlYy05ODZkLTUzNWE0MzRjNTc1OSIsInQiOjE2Mjk0ODIxMTQyOTYsImgiOiI3MTg3OGNhZGU3YjNhYWI5YWUzNjVjMGFlMmNkYTFlYjU1NGJhODVkMmE0MTg5MTU2NGU0ZjdiMzZiMWIyZTcwIn0=',
    'if-modified-since': '0',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36',
    'origin': 'https://www.grubhub.com',
    'sec-fetch-site': 'same-site',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://www.grubhub.com/',
    'accept-language': 'en-US,en;q=0.9',
}

perdish_params = (
    ('time', '1630036032687'),
    ('hideUnavailableMenuItems', 'true'),
    ('orderType', 'standard'),
    ('version', '4'),
)

perdish_tgt = 'https://api-gtm.grubhub.com/restaurants/{restaurant_id}/menu_items/{item_id}'


pd_headers = {
    'authority': 'api-gtm.grubhub.com',
    'cache-control': 'no-cache',
    'accept': 'application/json',
    'authorization': 'Bearer 05b79a24-d8ce-445f-9185-c3ab4f8d67b6',
    'perimeter-x': 'eyJ1IjoiYTUzYjc4OTAtMDZiOC0xMWVjLThiMzMtZWQyNWIzN2NmN2RhIiwidiI6ImFkZTIyM2ZlLTAxMzMtMTFlYy1iNjViLTQ0NDc0ZDYzNDM3MiIsInQiOjE2MzAwMzY1MzA0ODMsImgiOiJlOTZhYzQxZTNhMThmOTg3MzhlYjllODM1MDJhMmE3ZWRlMjM3YzI1NjFiMjRmMjZmNTgzMTI3Mjg1MzAxN2U2In0=',
    'if-modified-since': '0',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36',
    'origin': 'https://www.grubhub.com',
    'sec-fetch-site': 'same-site',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://www.grubhub.com/',
    'accept-language': 'en-US,en;q=0.9',
}

pd_params = (
    ('time', '1630036032687'),
    ('hideUnavailableMenuItems', 'true'),
    ('orderType', 'standard'),
    ('version', '4'),
)

pd_tgt = 'https://api-gtm.grubhub.com/restaurants/{restaurant_id}/menu_items/{item_id}'
#pd_response = requests.get(, headers=headers, params=params)

#NB. Original query string below. It seems impossible to parse and
#reproduce query strings 100% accurately so the one below is given
#in case the reproduced version is not "correct".
# response = requests.get('https://api-gtm.grubhub.com/restaurants/2428407/menu_items/3474491997?time=1630036032687&hideUnavailableMenuItems=true&orderType=standard&version=4', headers=headers)



#NB. Original query string below. It seems impossible to parse and
#reproduce query strings 100% accurately so the one below is given
#in case the reproduced version is not "correct".
# response = requests.get('https://api-gtm.grubhub.com/restaurants/322383/menu_items/17844438?time=1629481712797&hideUnavailableMenuItems=true&orderType=standard&version=4', headers=headers)



def parse_dish(dish_txt):
    perdish_options = []

    # I don't really want to save this until later, but it is
    # stuff we'll have to deal with at some point.

    # Otherwise, we can... do it... and we can read the results.
    perdish_json = json.loads(dish_txt)

    # Now we get the specific things for the dish, yay.
    perdish_categories = perdish_json['choice_category_list']
    # This can be a list.
    for one_category in perdish_categories:
        one_option = {}
        one_option['name'] = one_category['name']
        one_option['max_options'] = one_category['max_choice_options']
        one_option['min_options'] = one_category['min_choice_options']
        # There's also a list, poopity scoop.
        option_values = []
        for tmp_option in one_category['choice_option_list']:
            option_values.append({'name': tmp_option['description'], 'price': tmp_option['price']['amount']})
            #one_option['options'] = option_values
            # And, add this to the perdish options...

            # At some point, this has got to be stored in some thing somewhere.
        one_option['options'] = option_values
        perdish_options.append(one_option)
    return perdish_options

def parse_rest(rest_id, rest_txt):
    rest_dict = json.loads(rest_txt)

    rest = rest_dict['restaurant']
    avail = rest_dict['restaurant_availability']

    avail_kept = {}
    rest_kept  = {}
    menu_kept  = []

    # Things to maybe keep in the future:
    # cash_accepted
    # Cool, now let's figure out what's in here.
    avail_kept['available_for_delivery'] = avail['available_for_delivery']
    avail_kept['available_for_pickup'] = avail['available_for_pickup']
    avail_kept['hours'] = avail['available_hours']
    avail_kept['hours_pickup'] = avail['available_hours_pickup']
    avail_kept['delivery_fee_taxable'] = avail['delivery_fee_taxable']
    avail_kept['order_minimum'] = avail['order_minimum']
    avail_kept['pickup_cutoff'] = avail['pickup_cutoff']
    avail_kept['pickup_estimate_range'] = avail['pickup_estimate_range_v2']
    avail_kept['restaurant_id_gh'] = avail['restaurant_id']
    avail_kept['sales_tax'] = avail['sales_tax']
    # They also have a service toll fee? Check this later.

    # Now: go through rest_kept.
    rest_kept['address'] = rest['address']
    # This makes it easy.
    rest_kept['latitude'] = rest['latitude']
    rest_kept['longitude'] = rest['longitude']
    rest_kept['name'] = rest['name']
    rest_kept['phone_ordering_available'] = rest['phone_ordering_available']
    rest_kept['phone'] = rest['phone_number_for_delivery']

    menu = rest['menu_category_list']
    # We also should store the menu items here.

    # Each item is a category.
    perdish_access_headers = perdish_headers.copy()
    perdish_access_headers['authorization'] = perdish_access_headers['authorization'].format(cur_access_token)


    for one_item in menu:

        cat_dict = {}
        cat_dict['available'] = one_item['available']
        cat_dict['name'] = one_item['name']

        # Now get the list of dish3es.
        dish_list = one_item['menu_item_list']
        dishes = []
        for one_dish in dish_list:
            #print("DISH looks like ")
            #print(one_dish)
            dish_kept = {}
            dish_kept['avalable'] = one_dish['available']
            dish_kept['name'] = one_dish['name']
            # There's also a currency, but for now we're only
            # dealing with USD anyway.
            dish_kept['price'] = one_dish['price']['amount']
            dish_kept['id'] = one_dish['id']

            # This also lets us pull in extra options about the dish...
            # But it's inefficient. It means we have to make a lot of network calls every time we want to scrape a restaurant.
            # Oh well. In the long term, we can probably do a best-guess re: whether a dish "should" have extra options.

            perdish_url = perdish_tgt.format(restaurant_id=rest_id, item_id=dish_kept['id'])
            # I think the extra things here are about the same.
            perdish_response = requests.get(perdish_url, headers=perdish_access_headers, params=perdish_params)

            if perdish_response.status_code != 200:
                # Something broke, alert and be quiet.
                print(perdish_response)
                print("Something broke when grabbing {}, exiting".format(perdish_url))
                sys.exit()
            #print("Got perdish info for {}".format(one_dish['name']))
            # Otherwise, parse the perdish stuff.
            dish_options = parse_dish(perdish_response.text)
            dish_kept['options'] = dish_options
            dishes.append(dish_kept)
        cat_dict['dishes'] = dishes
        menu_kept.append(cat_dict)

            # Bunch of options...
    return {'avail': avail_kept,
            'rest': rest_kept,
            'menu': menu_kept}


def scrape_restaurant(grubhub_url):
    # First order: take the url and grab the actual id:
    id_num = ''
    split_url = grubhub_url.split('/')
    for one_part in split_url:
        if len(one_part):
            id_num = one_part

    # Get the last thing in a slash.
    # Also, remove url params.
    id_num = id_num.split('?')[0]

    calling_url = rest_tgt.format(id_num)

    rest_access_headers = rest_headers.copy()
    rest_access_headers['authorization'] = rest_access_headers['authorization'].format(cur_access_token)

    # OK, now we can make the requests call.
    gh_response = requests.get(calling_url, headers=rest_access_headers, params=rest_params)


    if gh_response.status_code != 200:
        # Something broke, alert and be quiet.
        print("Something broke when grabbing {}, exiting".format(grubhub_url))
        print(gh_response)
        print(gh_response.status_code)
        sys.exit()

    x = parse_rest(id_num, gh_response.text)
    # give it the url too...
    x['gh_url'] = grubhub_url
    return(x)

def db_populate_rest(rest_dicts):

    # First step: populate the restaurant data.
    rest_dict = {}
    print(rest_dicts.keys())
    rest_dict['name']            = rest_dicts['rest']['name']
    # TODO: let modelTools make sure this doesn't overlap with anything.
    rest_dict['url_name']         = '-'.join(rest_dicts['rest']['name'].lower().split(' '))
    rest_dict['phone']            = rest_dicts['rest']['phone']
    rest_dict['email']            = ''
    # Not sure what to put here.
    rest_dict['delivery_options'] = ''
    # Not sure what to put here. So putting nothing.
    rest_dict['pos_options']      = ''

    rest_dict['available_pickup'] = rest_dicts['avail']['available_for_pickup']
    rest_dict['street_address']   = rest_dicts['rest']['address']['street_address']
    rest_dict['street_number']    = rest_dicts['rest']['address']['street_address'].split()[0]
    rest_dict['route']            = ' '.join(rest_dicts['rest']['address']['street_address'].split()[1:])
    # This could be messed up later on. Not sure.
    rest_dict['extra_address_id'] = ''
    rest_dict['city']             = rest_dicts['rest']['address']['locality']
    rest_dict['state']            = rest_dicts['rest']['address']['region']
    rest_dict['country']          = rest_dicts['rest']['address']['country']
    rest_dict['zip_code']         = rest_dicts['rest']['address']['zip']
    rest_dict['lat']              = rest_dicts['rest']['latitude']
    rest_dict['lon']              = rest_dicts['rest']['longitude']

    rest_dict['num_hearts']    = 0
    rest_dict['category']      = ''
    # Stringifying a json.
    rest_dict['hours']         = json.dumps(rest_dicts['avail']['hours'])
    rest_dict['hours_pickup']  = json.dumps(rest_dicts['avail']['hours_pickup'])
    rest_dict['pickup_cutoff'] = rest_dicts['avail']['pickup_cutoff']

    # Note that this is in absolute numbers, so we'll have to divide by 100 later on.
    # This is easy to display though.
    rest_dict['sales_tax_rate']       = rest_dicts['avail']['sales_tax']
    rest_dict['delivery_fee_taxable'] = rest_dicts['avail']['delivery_fee_taxable']
    rest_dict['order_minimum']        = rest_dicts['avail']['order_minimum']['amount']
    rest_dict['grubhub_url']          = rest_dicts['gh_url']


    # I'll have to update modelTools to do this properly too. O well.

    # Second step: populate the menu categories data


    # Third step: populate the dish data


    # Fourth step: populate the dish to category data.


    # TODO: make this error resilient.
    pass


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', required=False)
    # Values: JSON, DB, ALL
    parser.add_argument('--mode', required=True)
    parser.add_argument('--iofile', default='grubhubs.json')
    args = parser.parse_args()

    if args.mode == 'JSON':
        get_access_token()
        grub_dicts = scrape_restaurant(args.url)
        # Write grub_dicts.
        with open(args.iofile, 'w') as iof:
            json.dump(grub_dicts, iof)
        print("Done")
    elif args.mode == 'DB':
        # If this is the case, great!
        with open(args.iofile, 'r') as iof:
            grub_dicts = json.load(iof)
        #print("I got the json, it looks like ")
        #print(grub_dicts)
        db_populate_rest(grub_dicts)
        # Pass this along to the thing that's updating our restaurant/menu...


if __name__ == '__main__':
    main()
