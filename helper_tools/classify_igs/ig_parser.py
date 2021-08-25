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

TODO:
- There's a real problem in detecting the partner. When there's a giveaway, sometimes they change the description to mention the winner first.
- I'll have to deal with those. Ugh.

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
    'partnering with',
    'partnering ',
    'sending me',
    'sent me',
    'working with',
    'promo code',
    '% off',
    ' code ',
    ' discount ',
    'giveaway',
]

def id_promotions(list_of_dicts, outfile):
    # OK, let's... do it.

    kept_posts = []
    for one_dict in list_of_dicts:
        # Let's actually filter out the ones that don't make it, first.
        lowercase_post = one_dict['description'].lower()
        should_keep = False
        for one_keyword in promotion_keywords:
            if one_keyword in lowercase_post:
                should_keep = True
        # This means we probably identified a brand.
        # OK, let's add it, but also print if it's not kept.

        # OK, right here, I should ID two things.
        # the tagged_usernames are not consistent. But what seems to be true is that the
        # first tagged thing is probably the brand or group in question.

        first_tagged = ''
        removed_newlines = ' '.join(lowercase_post.split('\n'))


        # Find the first tagged thing.
        at_loc = removed_newlines.find('@')
        if at_loc >= 0:
            short_newlines = removed_newlines[at_loc:]
            short_newlines = short_newlines.replace(',', ' ')
            potential_tag = short_newlines.split(' ')[0]
            first_tagged = potential_tag

        one_dict['inline_desc'] = removed_newlines
        one_dict['potential_tag'] = first_tagged

        if should_keep:
            # Find the first tagged section.
            kept_posts.append(one_dict.copy())
        else:
            pass

    with open(outfile, 'w', newline='') as csvfile:
        fieldnames = ['postUrl', 'location', 'username', 'tag', 'desc']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for one_post in kept_posts:
            writer.writerow({'postUrl': one_post['postUrl'], 'location': one_post['location'], 'username': one_post['username'], 'tag': one_post['potential_tag'], 'desc': one_post['inline_desc']})
    print("Done?")

    return
    for one_post in kept_posts:
        print("*"*80)

        print('{url}, {location}, {username}, {tag}, {desc}'.format(url=one_post['postUrl'], location=one_post['location'], username=one_post['username'], tag=one_post['potential_tag'], desc=one_post['inline_desc'] ))

# List of urls that we processed already.
# This is used for deduping.
processed_links = set()

wanted_cols = ['postUrl', 'description', 'location', 'isSidecar', 'profileUrl', 'username', 'fullName', 'imgUrl', 'taggedFullName1', 'taggedUsername1', 'taggedFullName2', 'taggedUsername2', 'taggedFullName3', 'taggedUsername3', 'taggedUsername4', 'taggedUsername5', 'taggedUsername6']
#wanted_cols = ['location']

def main():
    parser = argparse.ArgumentParser()
    # The file containing all our gathered ig lines.

    # first
    parser.add_argument('--infile', default='first_lines.csv')
    parser.add_argument('--outfile', default='outfile.csv')
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
    id_promotions(kept_dicts, args.outfile)
    print("Done")




if __name__ == '__main__':
    main()
