import os, sys, requests, vars
from datetime import datetime

# for purposes of creating a unique, identifiable output file for each run
timestamp = datetime.now().strftime('%y-%m-%d_%H-%M-%S')

def getFilepath(filename):
    return os.path.join(sys.path[0], filename)

def getTickets(filepath):
    tickets_list = []
    with open(filepath, 'r') as input:
        input_rows = input.readlines()
        request_keys = input_rows[0].split("\n")[0].split(",")
        for row in input_rows[1:]:
            row_data = row.split("\n")[0].split(",")
            ticket_dict = dict(zip(request_keys, row_data))
            ticket_dict['comment'] = {'body': ticket_dict['comment']}
            ticket_dict['tags'] = [ticket_dict['tags'], 'sojo']
            tickets_list.append(ticket_dict)
    return tickets_list

def getUsersFromServer():
    users = []
    url = vars.server + vars.users_endpoint
    while url:
        print('Requesting ' + url)
        response = requests.get(url, auth=(vars.user, vars.api_token), headers=vars.headers)
        response_json = response.json()
        users += response_json['users']
        url = response_json['next_page']
        print(response)
    return users

def bulkCreate(request_data):
    url = vars.server + vars.bulk_create_endpoint
    print('Sending bulk create request to ' + url)
    response = requests.post(url, auth=(vars.user, vars.api_token), headers=vars.headers, json=request_data)
    response_json = response.json()
    try:
        status = response_json['job_status']['status']
        print('Bulk create job status: ' + status)
    except:
        print('Bulk create response:\n' + str(response_json))

def getTicketFields():
    ticket_fields = []
    url = vars.server + vars.ticket_fields_endpoint
    print('Requesting ' + url)
    response = requests.get(url, auth=(vars.user, vars.api_token), headers=vars.headers)
    response_json = response.json()
    ticket_fields += response_json['ticket_fields']
    print(response)
    return ticket_fields

def bulkUpdate(request_data):
    url = vars.server + vars.bulk_update_endpoint + "?ids=" + ','.join(vars.ticket_ids)
    print('Requesting ' + url)
    response = requests.put(url, auth=(vars.user, vars.api_token), headers=vars.headers, json=request_data)
    response_json = response.json()
    try:
        status = response_json['job_status']['status']
        print('Bulk update job status: ' + status)
    except:
        print('Bulk update response:\n' + str(response_json))