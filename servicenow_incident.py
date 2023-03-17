#!/usr/bin/python
import requests
 
#url = 'https://myinstance.service-now.com/api/now/table/incident?sysparm_limit=10'
url = 'https://YourCompany.service-now.com/nav_to.do?uri=%2Fincident.do%3Fsys_id%3D6a6c8484db6f87409053778ebf961983'
user = 'manjesh'
pwd = 'SuperSecret'
headers = {"Accept":"application/json"}
response = requests.get(url, auth=(user, pwd), headers=headers )
if response.status_code != 200:
   print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:',response.json())
   exit()
 
print('Status:',response.status_code,'Headers:',response.headers,'Response:',response.json())
print('Cookies', response.cookies)
