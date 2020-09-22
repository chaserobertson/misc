import requests, os, sys, json, csv
from vars import timestamp, server, headers

url = server+"/api/v1/hardware"

querystring = {
    "sort": "created_at",
    "order": "asc",
    "status_id": 1, #Ready to Deploy
    "category_id": 10, #Computers
    "limit": 500
}

columns = ["asset_tag", "serial"]

special_columns = {
    "model": "name",
    "purchase_date": "date",
    "created_at": "datetime",
    "category": "name",
    "status_label": "name",
}

super_special_columns = {
    "assigned_to": ["username", "name"]
}

all_columns = []
for col in columns:
    all_columns.append(col)
for key in special_columns.keys():
    all_columns.append(key)
for key in super_special_columns.keys():
    for sub_key in super_special_columns.get(key):
        all_columns.append(sub_key)

response = requests.request("GET", url, headers=headers, params=querystring)

json_filepath = os.path.join(sys.path[0], timestamp + '.json')
with open(json_filepath, "w", newline='') as f:
    f.write(response.text)
    data = json.loads(response.text)

asset_data = data["rows"]

csv_filepath = os.path.join(sys.path[0], timestamp + '.csv')
with open(csv_filepath, "w", newline='') as f:
    csv_writer = csv.writer(f)
    csv_writer.writerow(all_columns)
    for asset in asset_data:
        asset_values = []
        for col in columns:
            asset_values.append(asset.get(col))
        for key in special_columns.keys():
            sub_key = special_columns.get(key)
            sub_dict = asset.get(key)
            if sub_dict:
                asset_values.append(sub_dict.get(sub_key))
            else:
                asset_values.append("")
        for key in super_special_columns.keys():
            key_list = super_special_columns.get(key)
            sub_dict = asset.get(key)
            for list_item in key_list:
                if sub_dict:
                    asset_values.append(sub_dict.get(list_item))
                else:
                    asset_values.append("")
        csv_writer.writerow(asset_values)

print(timestamp)
