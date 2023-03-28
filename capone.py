# This is written for PYTHON 3
# Don't forget to install requests package

import requests
import json

customerId = '1245'
apiKey = '824033b25cb6a2e95fd6bef97119187f'

url = 'http://api.reimaginebanking.com/customers/{}/accounts?key={}'.format(customerId,apiKey)
payload = {
  "type": "Savings",
  "nickname": "test",
  "rewards": 10000,
  "balance": 10000,	
}
# Create a Savings Account
response = requests.post( 
	url, 
	data=json.dumps(payload),
	headers={'content-type':'application/json'},
	)

print(response.json())
if response.status_code == 200:
	print('account created')