import requests, os, sys
from vars import timestamp, server, headers

url = server+"/api/v1/categories"

payload = {
    "use_default_eula": False,
    "require_acceptance": False,
    "checkin_email": False
}

response = requests.request("GET", url, headers=headers, json=payload)

filepath = os.path.join(sys.path[0], timestamp + '.json')
with open(filepath, "w") as f:
    f.write(response.text)

print(timestamp)
