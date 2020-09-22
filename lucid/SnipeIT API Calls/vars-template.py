from datetime import datetime

timestamp = datetime.now().strftime("%y-%m-%d_%H-%M-%S")

server = "https://snipeit.lucidutil.com"

api_key = ""

headers = {
    'authorization': "Bearer " + api_key,
    'accept': "application/json",
    'content-type': "application/json"
    }
