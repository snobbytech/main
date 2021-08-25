#! /usr/bin/env python

"""
Yo. This script tries to parse Sheng's ig data and output useful things.

Taking a break from normal life to try this out.

The major tasks for this script:

- Given an ig post:
  - ID if there's a promotion/brand partnership
  - ID if there are dishes mentioned and see what the location is.

Anyway, first order of action is to just read and parse this big ole csv.

Headers are:
postUrl,description,commentCount,likeCount,location,locationId,pubDate,likedByViewer,isSidecar,type,caption,profileUrl,username,fullName,taggedFullName1,taggedUsername1,taggedFullName2,taggedUsername2,taggedFullName3,taggedUsername3,taggedFullName4,taggedUsername4,taggedFullName5,taggedUsername5,taggedFullName6,taggedUsername6,taggedFullName7,taggedUsername7,taggedFullName8,taggedUsername8,taggedFullName9,taggedUsername9,taggedFullName10,taggedUsername10,taggedFullName11,taggedUsername11,taggedFullName12,taggedUsername12,taggedFullName13,taggedUsername13,imgUrl,postId,timestamp,query,taggedFullName14,taggedUsername14,taggedFullName15,taggedUsername15,taggedFullName16,taggedUsername16,taggedFullName17,taggedUsername17,taggedFullName18,taggedUsername18,sidePostUrl,videoUrl,viewCount,taggedFullName19,taggedUsername19,taggedFullName20,taggedUsername20

Things we want to keep:

postUrl,description,location,locationId,pubDate,isSidecar,type,caption,profileUrl,username,fullName,imgUrl,postId,timestamp,query

# This will probably change in the future, but still.

"""


import argparse
import sys
import os
import csv


# Finds lines that we think are dishes, and gives the urls to those.
def id_dishes(filepath):
    pass


# All sequences of words that probably mean they're doing a partnership deal.
promotion_keywords = [
    'thank you to',
    'partnering with',
    'from ',
    'sending me',
    'sent me',
    'working with',
    'promo code',
    '% off',
    ' code ',
    'giveaway',
]

def id_promotions(list_of_dicts):
    # OK, let's... do it.

    #

    pass

# List of urls that we processed already.
# This is used for deduping.
processed_links = set()

wanted_cols = ['postUrl', 'description', 'location', 'isSidecar', 'profileUrl', 'username', 'fullName', 'imgUrl', 'taggedFullName1', 'taggedUsername1', 'taggedFullName2', 'taggedUsername2', 'taggedFullName3', 'taggedUsername3']
#wanted_cols = ['location']

def main():
    parser = argparse.ArgumentParser()
    # The file containing all our gathered ig lines.

    # first
    parser.add_argument('--infile', default='first_lines.csv')
    # TODO: add options so they can select which function to call.
    args = parser.parse_args()

    # Actually, let's read in the file here and dedup lines.

    kept_dicts = []
    with open(args.infile, 'r' ) as igFile:
        reader = csv.DictReader(igFile)
        # Let's only keep the ones that are type photo.
        for line in reader:
            reduced_line = {}
            if line['type'] != 'Photo':
                continue
            if line['postUrl'] in processed_links:
                continue
            processed_links.add(line['postUrl'])
            for col in wanted_cols:
                reduced_line[col] = line[col]
            #print(reduced_line)
            kept_dicts.append(reduced_line)


    # Now that we've gone and kept our links, let's pass these over to the promotion spotter...
    id_promotions(kept_dicts)
    print("Done")




if __name__ == '__main__':
    main()
