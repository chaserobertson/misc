# BEFORE RUNNING SCRIPTS: duplicate this file as vars.py and fill in your auth info

# the email address of the person sending the api request, plus the token indicator
user = 'your_username_here@lucidchart.com' + '/token'

# the temporarily-granted api token for the above user - request this from a Zendesk admin
api_token = 'your_api_token_here'

# the filename to use when sending a ticket creation requests
bulk_create_file = 'ticket_details.csv'

bulk_update_file = 'update.json'

# the email addresses of Zendesk agents that tickets should be assigned to
zendesk_agents = [
    'xxxxxxx@lucidchart.com',
    'xxxxxxx@lucidchart.com',
    'xxxxxxx@lucidchart.com',
]

# tickets to update
ticket_ids = ["", ""]

# the HTTP request headers required by Zendesk api
headers = {
    'accept': "application/json",
    'content-type': "application/json"
}

# the server address to send the api request to
server = 'https://lucidsoftware.zendesk.com'

# ----------API ENDPOINTS------------ #
users_endpoint = "/api/v2/users.json"
tickets_endpoint = "/api/v2/tickets.json"
ticket_fields_endpoint = "/api/v2/ticket_fields.json"
bulk_create_endpoint = "/api/v2/tickets/create_many.json"
bulk_update_endpoint = "/api/v2/tickets/update_many.json"