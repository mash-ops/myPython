#! ~/venv/bin/python
# Author     : Manjesh.munegowda@stanfordchildrens.org
# Purpose    : To Resume alerts for Node/s, after a scheduled Alert supression for a node/s has ended.
# How to use : execute this python script from command line
#            : Input file nodesToResumeAlert.csv, one node per line using dns nodename
#            : #NodeName 
#            : testNode.your.domain
#Prerequisite: pip install orionsdk, tested with version 0.4.0; user with permission to unmute alerts; input file as above
#

import getpass, requests, json, csv, sys
from orionsdk import SwisClient
from urllib3.exceptions import InsecureRequestWarning

# Suppress the warnings from urllib3
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
user = 'yourAD\\' + getpass.getuser()    #Get the current logged in user

try:
    print("User : {}".format(user))
    secret = getpass.getpass(prompt='Password :')
except Exception as error:
    print('ERROR', error)
else:
    hostName = 'YourSolarwindsServer'
    filename = 'nodesToResumeAlert.csv'
    try:
        with open(filename, newline='\n') as iFH:
            reader = csv.reader(iFH)
            swis = SwisClient(hostName, user, secret, verify=False)
            comment = '#'
            date_format = '%m/%d/%y %H:%M:%S'
            for row in reader:
                if comment not in row[0]:
                   try:
                       uri = swis.query("SELECT Uri FROM Orion.Nodes WHERE DNS=@DNS", DNS=row[0])['results'][0]['Uri']
                       print('{}\t{}' .format(row[0], uri))
                       swis.invoke('Orion.AlertSuppression', 'ResumeAlerts', [uri])
                   except IndexError:
                       print('{} Not Found...' .format(row[0]))
    except csv.Error as Ferror:
        sys.exit('file {}, line {}: {}'.format(filename, reader.line_num, Ferror))
    except FileNotFoundError as FnotFound:
        sys.exit('{}'.format(FnotFound))
