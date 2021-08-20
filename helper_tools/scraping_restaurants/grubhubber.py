#! /usr/bin/env python

"""
Given a grubhub url (what the restaurant is), we'll go in and
grab the restaurant's properties and menu. All that good stuff.
And output it all in our own nice little JSON file.

"""

import sys
import requests
import json

headers = {
    'authority': 'api-gtm.grubhub.com',
    'cache-control': 'max-age=0',
    'accept': 'application/json',
    'authorization': 'Bearer 6babddd0-157e-4596-89de-49fbfda21e08',
    'if-modified-since': '0',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36',
    'origin': 'https://www.grubhub.com',
    'sec-fetch-site': 'same-site',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://www.grubhub.com/',
    'accept-language': 'en-US,en;q=0.9',
}

grubhub_params = (
    ('hideChoiceCategories', 'true'),
    ('version', '4'),
    ('variationId', 'rtpFreeItems'),
    ('orderType', 'standard'),
    ('hideUnavailableMenuItems', 'true'),
    ('hideMenuItems', 'false'),
)

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
    'authorization': 'Bearer c3ce4abe-e398-4e83-a985-5dba3f3f7d11',
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


api_pt = 'https://api-gtm.grubhub.com/restaurants/{}'
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

    calling_url = api_pt.format(id_num)


    # OK, now we can make the requests call.
    gh_response = requests.get(calling_url, headers=headers, params=gh_params)

    if gh_response.status_code != 200:
        # Something broke, alert and be quiet.
        print("Something broke when grabbing {}, exiting".format(github_url))
        sys.exit()

    # Otherwise, we can... do it... and we can read the results.
    json_response = json.loads(gh_response.text)

    try:
        rest = json_response['restaurant']
        avail = json_response['restaurant_availability']

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

                perdish_url = perdish_tgt.format(id_num, dish_kept['id'])
                # I think the extra things here are about the same.
                perdish_response = requests.get(perdish_url, headers=header, params=gh_params)

                if perdish_response.status_code != 200:
                    # Something broke, alert and be quiet.
                    print("Something broke when grabbing {}, exiting".format(perdish_url))
                    sys.exit()

                # Bunch of options...
                perdish_options = []

                # I don't really want to save this until later, but it is
                # stuff we'll have to deal with at some point.

                # Otherwise, we can... do it... and we can read the results.
                perdish_json = json.loads(perdish_response.text)

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
                    for one_option in one_category['choice_option_list']:
                        option_values.append({'name': one_option['description'], 'price': one_option['price']['amount']})
                    one_option['options'] = option_values
                    # And, add this to the perdish options...

                    # At some point, this has got to be stored in some thing somewhere.
                    perdish_options.append(one_option)



        # OK, hm. It looks like there are follow-up calls that tell you what the options are:




    menu_data = {}



    pass
