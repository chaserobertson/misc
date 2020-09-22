# BEFORE RUNNING THIS SCRIPT: duplicate the vars_template into a new vars.py specific to you

import json, util, vars

filepath_in = util.getFilepath(vars.bulk_update_file)

# open input json and load data as dict
with open(filepath_in, 'r') as input:
    update_data = json.load(input)
print('Requested ticket creation data:\n' + json.dumps(update_data))

# send request to bulk create tickets
util.bulkUpdate(update_data)

print('Finished')
