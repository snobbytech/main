#! /usr/bin/env python

import requests
import json



"""

Some sample scripts to calculate engagement.

Sample run:

python calc_engagement.py --ig FILE_WITH_IG_HANDLES_ONE_PER_LINE.txt

"""

import requests
import argparse

inbeat_headers = {
    'authority': 'graphql.inbeat.co',
    'pragma': 'no-cache',
    'cache-control': 'no-cache',
    'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
    'sec-ch-ua-mobile': '?0',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36',
    'content-type': 'application/json',
    'accept': '*/*',
    'origin': 'https://www.inbeat.co',
    'sec-fetch-site': 'same-site',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://www.inbeat.co/',
    'accept-language': 'en-US,en;q=0.9',
}



def inbeat_parse(ig_name):
    inbeat_data = '{"platform":"instagram","username":"' + ig_name + '"}'
    inbeat_response = requests.post('https://graphql.inbeat.co/engagement-calculator', headers=inbeat_headers, data=inbeat_data)

    if inbeat_response.status_code != 200:
        print("ERROR!!!! {}".format(ig_name))


    # Otherwise, we can parse through the jsons.
    json_response = json.loads(inbeat_response.text)

    running_likes = 0
    running_comments = 0
    running_engagement = 0
    counter = 0
    # OK, so the posts are keyed by posts.
    the_posts = json_response['posts']

    for one_post in the_posts:
        running_likes += one_post['likes']
        running_comments += one_post['comments']
        running_engagement += one_post['engagement']
        counter += 1

    if counter == 0:
        avg_likes = 0
        avg_comments = 0
        avg_engagement = 0
    else:
        avg_likes = running_likes / counter
        avg_comments = running_comments / counter
        avg_engagement = running_engagement / counter

    return {'handle': ig_name, 'likes': avg_likes, 'comments': avg_comments, 'engagement': avg_engagement}

    pass


# Let's just productionize it to take in a file with ig handles.


#inbeat_parse("lvciaeats")
def main():

    parser = argparse.ArgumentParser()
    # String or a file of ig handles
    parser.add_argument('--ig', required=True)
    parser.add_argument('--out_file', default='results.csv')

    args = parser.parse_args()
    # OK, cool.
    wanted_igs = []

    # Check if it's a file.
    try:
        with open(args.ig, 'r') as f:
            for one_line in f.readlines():
                wanted_igs.append(one_line.replace("\n", ""))
    except Exception as e:
        # Then it's probably not the file you wanted.
        wanted_igs = [args.ig]

    #print("We would've run on ")
    #print(wanted_igs)

    output_stuff = []
    for one_ig in wanted_igs:
        try:
            ig_results = inbeat_parse(one_ig)
            output_stuff.append(ig_results)
        except Exception as e:
            continue
    # Now, go and print them all out.
    #print(output_stuff)

    # OK, now let's just go line by line and print it out.
    output_lines = 'handle,likes,comments,engagement\n'
    for one_output in output_stuff:
        output_lines += '{h},{l},{c},{e}\n'.format(h=one_output['handle'], l=one_output['likes'], c=one_output['comments'], e=one_output['engagement'])

    # OK, now we can print it or we can write it, or los dos.
    print(output_lines)
    with open(args.out_file, 'w') as f:
        f.write(output_lines)

if __name__ == '__main__':
    main()
