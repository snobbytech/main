#! /usr/bin/env python

"""
Given a doordash url, go in and grab that restaurant's properties and menu. Output
in our nice little json file.


Sample usage:

"""
import os, sys, requests, json, argparse
sys.path.insert(0, os.path.abspath('../../backend'))

os.environ['APP_CONFIG_FILE'] = '../config/dev.py'

from app import flask_app
from app.models import modelTools as mt
from app.models.modelDefs import to_public_dict


# Something to
import requests

# This part is switched between differen places.
dd_menu_headers = {
    'authority': 'www.doordash.com',
    'x-channel-id': 'marketplace',
    'apollographql-client-name': '@doordash/app-consumer-production-ssr',
    'accept-language': 'en-US',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36',
    'content-type': 'application/json',
    'accept': '*/*',
    'x-experience-id': 'doordash',
    'apollographql-client-version': '1.0',
    'x-csrftoken': '',
    'origin': 'https://www.doordash.com',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    # This gets switched between different restaurants.
#    'referer': 'https://www.doordash.com/store/woodhouse-fish-co-san-francisco-981727',
    'cookie': 'x-device-id=268bd3a5-c19d-414d-b508-a4023b8c9a6d; __cf_bm=065c7c1d646a0d83302a8b4e547f13aae55217c6-1630417621-1800-AQPaHZ8LV7OyIYKhqpwCh8ZnrLg7GdIIDN2p/euxMDFG+kTIo2Iqau+eeCaUvhz/nFwKFPkzqGWxmaAIXAVKflOEJu/6CYMZnkuG8zAy5XMy; __cfruid=4653f5bddafbfca7c1badec5aaf2828cbf664ee2-1630417621; ajs_anonymous_id=%227d659388-c671-4e1d-a8fa-81d64f8e77d5%22',
}

# This part is fixed.
dd_menu_data = '${"operationName":"storepageFeed","variables":{"storeId":"981727","menuId":"","isMerchantPreview":false,"fulfillmentType":"Pickup","includeNestedOptions":true,"includeQuickAddContext":false},"query":"query storepageFeed($storeId: ID\\u0021, $menuId: ID, $isMerchantPreview: Boolean, $fulfillmentType: FulfillmentType, $includeNestedOptions: Boolean\\u0021, $includeQuickAddContext: Boolean\\u0021) {\\\\n storepageFeed(storeId: $storeId, menuId: $menuId, isMerchantPreview: $isMerchantPreview, fulfillmentType: $fulfillmentType) {\\\\n storeHeader {\\\\n id\\\\n name\\\\n description\\\\n priceRange\\\\n priceRangeDisplayString\\\\n offersDelivery\\\\n offersPickup\\\\n offersGroupOrder\\\\n isConvenience\\\\n isDashpassPartner\\\\n isShippingOnly\\\\n address {\\\\n lat\\\\n lng\\\\n city\\\\n street\\\\n displayAddress\\\\n cityLink\\\\n __typename\\\\n }\\\\n business {\\\\n id\\\\n name\\\\n link\\\\n differentialPricingEnabled\\\\n __typename\\\\n }\\\\n businessTags {\\\\n name\\\\n link\\\\n __typename\\\\n }\\\\n deliveryFeeLayout {\\\\n title\\\\n subtitle\\\\n isSurging\\\\n displayDeliveryFee\\\\n __typename\\\\n }\\\\n deliveryFeeTooltip {\\\\n title\\\\n description\\\\n __typename\\\\n }\\\\n coverImgUrl\\\\n coverSquareImgUrl\\\\n businessHeaderImgUrl\\\\n ratings {\\\\n numRatings\\\\n numRatingsDisplayString\\\\n averageRating\\\\n isNewlyAdded\\\\n __typename\\\\n }\\\\n savelists {\\\\n id\\\\n __typename\\\\n }\\\\n distanceFromConsumer {\\\\n value\\\\n label\\\\n __typename\\\\n }\\\\n enableSwitchToPickup\\\\n asapStatus {\\\\n unavailableStatus\\\\n displayUnavailableStatus\\\\n unavailableReason\\\\n displayUnavailableReason {\\\\n title\\\\n subtitle\\\\n __typename\\\\n }\\\\n isAvailable\\\\n unavailableReasonKeysList\\\\n __typename\\\\n }\\\\n asapPickupStatus {\\\\n unavailableStatus\\\\n displayUnavailableStatus\\\\n unavailableReason\\\\n displayUnavailableReason {\\\\n title\\\\n subtitle\\\\n __typename\\\\n }\\\\n isAvailable\\\\n unavailableReasonKeysList\\\\n __typename\\\\n }\\\\n status {\\\\n delivery {\\\\n isAvailable\\\\n minutes\\\\n operatingStatusEta {\\\\n value\\\\n unit\\\\n __typename\\\\n }\\\\n displayUnavailableStatus\\\\n unavailableReason\\\\n isTooFarFromConsumer\\\\n isStoreInactive\\\\n __typename\\\\n }\\\\n pickup {\\\\n isAvailable\\\\n minutes\\\\n displayUnavailableStatus\\\\n unavailableReason\\\\n isStoreInactive\\\\n __typename\\\\n }\\\\n __typename\\\\n }\\\\n isMenuV2\\\\n currency\\\\n travelTime {\\\\n value\\\\n type\\\\n __typename\\\\n }\\\\n __typename\\\\n }\\\\n banners {\\\\n pickup {\\\\n id\\\\n title\\\\n text\\\\n __typename\\\\n }\\\\n catering {\\\\n id\\\\n text\\\\n __typename\\\\n }\\\\n demandGen {\\\\n id\\\\n title\\\\n text\\\\n modals {\\\\n type\\\\n modalKey\\\\n modalInfo {\\\\n title\\\\n description\\\\n buttonsList {\\\\n text\\\\n action\\\\n __typename\\\\n }\\\\n __typename\\\\n }\\\\n __typename\\\\n }\\\\n __typename\\\\n }\\\\n demandTest {\\\\n id\\\\n title\\\\n text\\\\n modals {\\\\n type\\\\n modalKey\\\\n modalInfo {\\\\n title\\\\n description\\\\n buttonsList {\\\\n text\\\\n action\\\\n __typename\\\\n }\\\\n __typename\\\\n }\\\\n __typename\\\\n }\\\\n __typename\\\\n }\\\\n shipAnywhere {\\\\n id\\\\n title\\\\n text\\\\n modals {\\\\n type\\\\n modalKey\\\\n modalInfo {\\\\n title\\\\n description\\\\n buttonsList {\\\\n text\\\\n action\\\\n __typename\\\\n }\\\\n __typename\\\\n }\\\\n __typename\\\\n }\\\\n popup {\\\\n title\\\\n dismissButtonText\\\\n bulletCopyList\\\\n __typename\\\\n }\\\\n __typename\\\\n }\\\\n __typename\\\\n }\\\\n carousels {\\\\n id\\\\n type\\\\n name\\\\n description\\\\n items {\\\\n id\\\\n name\\\\n description\\\\n displayPrice\\\\n imgUrl\\\\n dynamicLabelDisplayString\\\\n calloutDisplayString\\\\n nextCursor\\\\n orderItemId\\\\n reorderCartId\\\\n reorderUuid\\\\n unitAmount\\\\n currency\\\\n ... @include(if: $includeNestedOptions) {\\\\n nestedOptions\\\\n __typename\\\\n }\\\\n specialInstructions\\\\n quickAddContext {\\\\n isEligible\\\\n price {\\\\n currency\\\\n decimalPlaces\\\\n displayString\\\\n sign\\\\n symbol\\\\n unitAmount\\\\n __typename\\\\n }\\\\n nestedOptions\\\\n specialInstructions\\\\n __typename\\\\n }\\\\n __typename\\\\n }\\\\n __typename\\\\n }\\\\n menuBook {\\\\n id\\\\n name\\\\n displayOpenHours\\\\n menuCategories {\\\\n id\\\\n name\\\\n numItems\\\\n next {\\\\n anchor\\\\n cursor\\\\n __typename\\\\n }\\\\n __typename\\\\n }\\\\n menuList {\\\\n id\\\\n name\\\\n displayOpenHours\\\\n __typename\\\\n }\\\\n __typename\\\\n }\\\\n itemLists {\\\\n id\\\\n name\\\\n description\\\\n items {\\\\n id\\\\n name\\\\n description\\\\n displayPrice\\\\n imageUrl\\\\n dynamicLabelDisplayString\\\\n calloutDisplayString\\\\n secondaryCallout {\\\\n logo\\\\n text\\\\n __typename\\\\n }\\\\n ... @include(if: $includeQuickAddContext) {\\\\n quickAddContext {\\\\n isEligible\\\\n price {\\\\n currency\\\\n decimalPlaces\\\\n displayString\\\\n sign\\\\n symbol\\\\n unitAmount\\\\n __typename\\\\n }\\\\n nestedOptions\\\\n specialInstructions\\\\n __typename\\\\n }\\\\n __typename\\\\n }\\\\n __typename\\\\n }\\\\n __typename\\\\n }\\\\n disclaimersList {\\\\n id\\\\n text\\\\n __typename\\\\n }\\\\n reviewPreview {\\\\n maxNumStars\\\\n consumerReviewData {\\\\n avgRating\\\\n numRatings\\\\n numRatingsDisplayString\\\\n insufficientRatings\\\\n numReviews\\\\n numReviewsDisplayString\\\\n consumerReviews {\\\\n consumerReviewUuid\\\\n reviewerDisplayName\\\\n starRating\\\\n reviewedAt\\\\n reviewText\\\\n isVerified\\\\n experience\\\\n __typename\\\\n }\\\\n __typename\\\\n }\\\\n __typename\\\\n }\\\\n popupContent {\\\\n id\\\\n type\\\\n title\\\\n message\\\\n dismissButtonText\\\\n metadataList {\\\\n key\\\\n value\\\\n __typename\\\\n }\\\\n bulletCopyList\\\\n showOnce\\\\n __typename\\\\n }\\\\n __typename\\\\n }\\\\n}\\\\n"}'



def grab_doordash_main(restaurant_url):
    restaurant_header = dd_menu_headers.copy()

    # Process the url in case there are other args.
    restaurant_url = restaurant_url.split('?')[0]

    # OK, now give the referrer stuff.
    restaurant_header['referer'] = restaurant_url

    # OK, now make the request
    dd_response = requests.post('https://www.doordash.com/graphql', headers=restaurant_header, data=dd_menu_data)
    if dd_response.status_code != 200:
        print("Something broke when trying to grab {}, exiting".format(restaurant_url))
        print(dd_response.status_code)
        sys.exit()
    # Otherwise, parse the json

    js_obj = json.loads(dd_response.text)
    # Now, let's just print it?
    print(js_obj)

    pass

def main():
    the_url = 'https://www.doordash.com/store/woodhouse-fish-co-san-francisco-981727/'
    grab_doordash_main(the_url)

    pass

if __name__ == '__main__':
    main()
