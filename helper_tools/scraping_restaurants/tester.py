#! /usr/bin/env python

# So stupid.
import subprocess

# OK, I REALLY don't get why the shell isn't letting me run this thing from within python, so...
# Let's just try doing some foolery.

# All this shit works. Great.

import json
# Do the first thing.
"""
cmd_1 = "cat dd_rest_cmd.sh | sed 's#OUR_DOORDASH_URL#https://www.doordash.com/store/woodhouse-fish-co-san-francisco-981727/#' | bash"

result = subprocess.getoutput(cmd_1)
# OK, I think... this might be OK? I just need to remove all this stupid output.


if '{' in result:
    first_idx = result.find('{')
    sub_result = result[first_idx:]
    #print(sub_result)
    # Check if I can turn this into a json?
    x = json.loads(sub_result)
    print(x)
"""


"""
# Do the second thing: getting dish info.
cmd_2 = "cat dd_dish_cmd.sh | sed 's#OUR_DOORDASH_URL#https://www.doordash.com/store/woodhouse-fish-co-san-francisco-981727/#' | sed 's#DD_ITEMID#155124970#'| sed 's#DD_STORE_ID#981727#'| bash"

result = subprocess.getoutput(cmd_2)
y = json.loads(result)
print(y)

"""
