import requests
import json
username = "%0d11>8$8 e917308362964@cqupt"

login_json = {"method": "do", "login": {"password": "ubc8e6wuLTefbwK"}}
response = requests.post('http://192.168.1.1', json=login_json).text
response = json.loads(response)
print(response['stok'])
dail_url = 'http://192.168.1.1/stok=%s/ds' % response['stok']
dail_json = {"protocol": {"wan": {"wan_type": "pppoe"}, "pppoe": {
"username": username, "password": "230279"}}, "method": "set"}
response = requests.post(dail_url, json=dail_json).text
print(response)