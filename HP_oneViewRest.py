#! ~/venv/bin/python
# Author     : Manjeshtm@gmail.com
# Purpose    : Get list of OneView server profile and write output to screen and file (/tmp/oneview.output)
# How to use : execute this python script from command line (python and program_Name)
# Hint       : pip install hpeOneView (10.2.0) in venv, as of Sep 2025, tested on Python 3.12.1
# Refer API  : https://support.hpe.com/docs/display/public/dp00003271en_us/index.html#rest/server-profiles

import getpass, requests, sys, importlib.util, os
from urllib3.exceptions import InsecureRequestWarning

program_name = os.path.basename(sys.argv[0])
module_name = "hpeOneView.oneview_client"
spec = importlib.util.find_spec(module_name)
server_list = ['Server01', 'Server02.Your.domain', 'Server03.Your.domain', 'Server04.Your.domain', 'Server05.Your.domain']
output_file = "/tmp/oneview.output"

def usage():
  return print(f"Usage: \n{program_name} <OneView user name>\n" )

if spec is not None:
  print(f"Prerequisite '{module_name}' is installed.\n Welcome to HP OneView \n Login to get list of Server Profile\n")
  from hpeOneView.oneview_client import OneViewClient
else:
  print(f"The module '{module_name}' is not installed, Try pip install orionsdk")
  sys.exit()

try:
   first_arg = sys.argv[1] 
except IndexError:
    usage()
    sys.exit()

# Suppress the warnings from urllib3
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
user = "YourAD\\" + str(sys.argv[1])

try:
  print("User : {}".format(user))
  secret = getpass.getpass(prompt='Password :')
except Exception as error:
  print('Username/Password ERROR', error) 

for server in server_list:
  print(f"processing server: '{server}")
  try:
    config = {
      "ip": server,
      "credentials": { "userName": user, "password": secret },
      #"api_version": 2000,
      "ssl_certificate_verification": False
      }
  except Exception as error:
      print('ERROR', error)

  try:
    oneview_client = OneViewClient(config)
    print(f"HPE OneView Session ID: {oneview_client}")
    server_hardware = oneview_client.server_hardware.get_all()
    print("Found {} server profile/s.".format(len(server_hardware)))
    server_profiles = oneview_client.server_profiles.get_all()
    if server_profiles:
        print("Server Profiles found:")
        with open(output_file, '+a') as f_handle:
          f_handle.write(f"{'*' * 55} \nHP OneView Server Profile/s : on {server} \n{'*' * 55}\n")
          f_handle.write("Found {} server profile/s.\n".format(len(server_hardware)))   
        for profile in server_profiles:
            print(f"  Name: {profile['name']}, URI: {profile['uri']}")
            with open(output_file, '+a') as f_handle:
              f_handle.write(f"{server}, {profile['name']}, {profile['uri']} \n")
    else:
       print("No Server Profiles found.")
  except Exception as error:
     print('OneView Client ERROR : ', error)
