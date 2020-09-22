# BEFORE RUNNING THIS SCRIPT: duplicate the vars_template into a new vars.py specific to you

import json, util, vars

filepath_csv_in = util.getFilepath(vars.bulk_create_file)

# open input csv and format data as json ticket request dict
tickets_list = util.getTickets(filepath_csv_in)
print('Requested ticket creation data:\n' + str(tickets_list))

# get a comprehensive list of Zendesk users as a list of dicts
users_list = util.getUsersFromServer()
print('User list:\n' + json.dumps(users_list))

# restructure the users list into a dict, with email address as key
users = {}
for user in users_list:
    users[user['email']] = user
print('User list restructured to user dict:\n' + str(users))

# add Zendesk user and agent IDs to each ticket dict based on their email address
# also delete the string email fields, bc those are not an arg for ZD API
for ticket in tickets_list:
    ticket['requester_id'] = users[ticket['requester_email']]['id']
    ticket['assignee_id'] = users[ticket['assignee_email']]['id']
    del ticket['requester_email']
    del ticket['assignee_email']
print('Request data with user IDs:\n' + str(tickets_list))

# send request to bulk create tickets
util.bulkCreate({'tickets': tickets_list})

print('Finished')
