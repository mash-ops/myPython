#! ~/venv/bin/python
# Author     : Manjesh.munegowda@stanfordchildrens.org
# Purpose    : List all Nodes in SolarWinds using solarwind api, display output in tabular format
# How to use : python programName <Solarwinds UserName>

import getpass, requests, json, sys, importlib.util
#from orionsdk import SwisClient
from urllib3.exceptions import InsecureRequestWarning

if len(sys.argv) == 1:
  print("\nUsage:\n\t {} <SolarWinds username>\n".format(str(sys.argv[0])))
  sys.exit()

module_name = "orionsdk"
spec = importlib.util.find_spec(module_name)

if spec is not None:
    print(f"The module '{module_name}' is installed.")
    from orionsdk import SwisClient
else:
    print(f"The module '{module_name}' is not installed, Try pip install orionsdk")
    sys.exit()

# Suppress the warnings from urllib3
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
#user = getpass.getuser()    #Get the current logged in user
user = "lpch\\" + str(sys.argv[1])
#secret = str(sys.argv[2])
#print(user)
#print(secret)

try:
    print("User : {}".format(user))
    secret = getpass.getpass(prompt='Password :')
except Exception as error:
    print('ERROR', error)
#else:
    
hostName = 'psrpsolrapp02'
swqlQuery = """SELECT IPAddress, DNS, SysName, Vendor, MachineType FROM Orion.Nodes Order by MachineType"""
swis = SwisClient(hostName, user, secret, verify=False)

try:
  # let's run the query and store the results in a variable
  response = swis.query(swqlQuery)
except Exception as error:
  print('ERROR', error)
else:    
  #print the Header
  print('*' * 120)
  print("{:^50} {:^30} {:^18} {:^20}" .format('Host Name', 'Machine Type', 'IP Address','Vendor'))
  print('*' * 120)

  win_counter = lin_counter = vmW_counter = unk_counter = other_counter = 0
  for val in response['results']:
     print("{0: <50} {1: >30} {2: >18} {3: >20}" .format(val['DNS'], val['MachineType'], val['IPAddress'], val['Vendor']))
     if val['Vendor'] == "Windows":
        win_counter += 1
     elif val['Vendor'] == "Linux":
        lin_counter += 1
     elif val['Vendor'] == "VMware Inc.":
        vmW_counter += 1
     elif val['Vendor'] == "Unknown":
        unk_counter += 1
     else:
        other_counter += 1

print('*' * 140)
print(f'Number of Nodes found : {len(response['results'])}')
print(f'Total Windows: {win_counter}\n\tLinux: {lin_counter}\n\tVmWare: {vmW_counter}\n\tUnknown: {unk_counter}\n\tOther: {other_counter}')
