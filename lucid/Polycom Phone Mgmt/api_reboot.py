import requests

cookies = {
    'Authorization': 'Basic xxxxxxxxxxxxxxxxxxx=',
}

headers = {
    'Sec-Fetch-Mode': 'cors',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9',
    'Authorization': 'Basic xxxxxxxxxxxxxxxxxxx=',
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
    'Content-type': 'application/JSON',
    'Accept': '*/*',
    'Cache-Control': 'no-cache',
    'Sec-Fetch-Site': 'same-origin',
}

data = {
}

# newline separated list of IP's
f = open('test_IP.txt', 'r').read().split('\n')

for ip in f:
	response = requests.post('https://%s/api/v1/mgmt/safeReboot' % ip, headers=headers, cookies=cookies, data=data, verify=False)
	print('reboot sent to %s: %s' % (ip, response))