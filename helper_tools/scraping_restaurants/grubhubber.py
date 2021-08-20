#! /usr/bin/env python

"""
Given a grubhub url (what the restaurant is), we'll go in and
grab the restaurant's properties and menu. All that good stuff.
And output it all in our own nice little JSON file.

I made two text files: thai_restaurant.txt and thai_dish.txt that have the raw data
for thai villa in NYC, to make sure our ish works.

"""

import sys
import requests
import json

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
    'authorization': '',
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
    ('time', '1629481712797'),
    ('hideUnavailableMenuItems', 'true'),
    ('orderType', 'standard'),
    ('version', '4'),
)

perdish_tgt = 'https://api-gtm.grubhub.com/restaurants/{restaurant}/menu_items/{item_id}'


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

def parse_rest(rest_txt):
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
        # Now get the list of dishes.
        dish_list = one_item['menu_item_list']
        dishes = []
        for one_dish in dish_list:
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

            if False:
                perdish_url = perdish_tgt.format(id_num, dish_kept['id'])
                # I think the extra things here are about the same.
                perdish_response = requests.get(perdish_url, headers=header, params=perdish_params)

                if perdish_response.status_code != 200:
                    # Something broke, alert and be quiet.
                    print("Something broke when grabbing {}, exiting".format(perdish_url))
                    sys.exit()
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


def scrape_restaurant(github_url):
    # First order: take the url and grab the actual id:
    id_num = ''
    split_url = github_url.split('/')
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
        print("Something broke when grabbing {}, exiting".format(github_url))
        print(gh_response)
        print(gh_response.status_code)
        sys.exit()

    x = parse_rest(gh_response.text)
    return(x)


get_access_token()
grubhub_url = 'https://www.grubhub.com/restaurant/thai-villa-5-e-19th-st-new-york/340205'
grub_dicts = scrape_restaurant(grubhub_url)
print(grub_dicts)
