#! ~/venv/bin/python
# Author     : Manjesh.munegowda@stanfordchildrens.org
# Purpose    : To call solarwind api to query orion node and display output in tabular format
# How to use : execute this python script from command line
#Prerequisite: pip install orionsdk, tested with version 0.4.0
#

import getpass, requests, json, string
from orionsdk import SwisClient
from urllib3.exceptions import InsecureRequestWarning
from datetime import datetime

# from solarwind.swqlQuery import swqlQuery

# Suppress the warnings from urllib3
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
user = 'YourAD\\' + getpass.getuser()    #Get the current logged in user

# class SafeDict(dict):
#     def __init__(self, missing='#', empty='', *args, **kwargs):
#         super(SafeDict, self).__init__(*args, **kwargs)
#         self.missing = missing
#         self.empty = empty
#     def __getitem__(self, item):
#         return super(SafeDict, self).__getitem__(item) or self.empty
#     def __missing__(self, key):
#         return self.missing
    
class Default(dict):
    def __missing__(self, key):
        return '{'+key+'}'
    
try:
    print("User : {}".format(user))
    secret = getpass.getpass(prompt='Password :')
except Exception as error:
    print('ERROR', error)
else:
    hostName = 'YourSolarWindsServer'
    swqlQuery = """SELECT DISTINCT
        CASE
          WHEN [EntityUri] LIKE 'swis://%/Orion/Orion.Nodes/NodeID=%' AND [EntityUri] NOT LIKE 'swis://%/Orion/Orion.Nodes/NodeID=%/%'
             THEN [N].[Caption]
          WHEN [EntityUri] LIKE 'swis://%/Orion/Orion.Nodes/NodeID=%/Interfaces/InterfaceID=%'
            THEN [I].[FullName]
          WHEN [EntityUri] LIKE 'swis://%/Orion/Orion.Nodes/NodeID=%/Applications/ApplicationID=%'
            THEN [AA].[FullyQualifiedName]
          ELSE 'SomethingElse'
       END AS [Element],
       CASE
          WHEN [EntityUri] LIKE 'swis://%/Orion/Orion.Nodes/NodeID=%' AND [EntityUri] NOT LIKE 'swis://%/Orion/Orion.Nodes/NodeID=%/%'
             THEN [N].[Status]
          WHEN [EntityUri] LIKE 'swis://%/Orion/Orion.Nodes/NodeID=%/Interfaces/InterfaceID=%'
             THEN [I].[Status]
          WHEN [EntityUri] LIKE 'swis://%/Orion/Orion.Nodes/NodeID=%/Applications/ApplicationID=%'
             THEN [AA].[Status]
          ELSE 30
       END AS [Status],
       [AE].AccountID AS [AccountID],
       ToLocal([SuppressFrom]) AS [LocalSuppressFrom],
       ToLocal([SuppressUntil]) AS [LocalSuppressUntil] 
FROM Orion.AlertSuppression AS [AlertSup] 
LEFT OUTER JOIN Orion.Nodes AS [N]
   ON [AlertSup].[EntityUri] = [N].[Uri]
LEFT OUTER JOIN Orion.NPM.Interfaces AS [I]
   ON [AlertSup].[EntityUri] = [I].[Uri]
LEFT OUTER JOIN Orion.APM.Application AS [AA]
   ON [AlertSup].[EntityUri] = [AA].[Uri]
LEFT OUTER JOIN Orion.AuditingEvents AS [AE]
   ON [AE].AuditEventMessage LIKE CONCAT('%', CASE
          WHEN [EntityUri] LIKE 'swis://%/Orion/Orion.Nodes/NodeID=%' AND [EntityUri] NOT LIKE 'swis://%/Orion/Orion.Nodes/NodeID=%/%'
             THEN [N].[NodeName]
          WHEN [EntityUri] LIKE 'swis://%/Orion/Orion.Nodes/NodeID=%/Interfaces/InterfaceID=%'
             THEN [I].[InterfaceCaption]
          WHEN [EntityUri] LIKE 'swis://%/Orion/Orion.Nodes/NodeID=%/Applications/ApplicationID=%'
             THEN [AA].[Name]
          ELSE 'Wrong'
       END, '%') AND [EntityUri] LIKE CONCAT('%=', [AE].NetObjectID)
INNER JOIN Orion.AuditingActionTypes AS [AT]
   ON [AE].ActionTypeID = [AT].ActionTypeID
WHERE [AT].ActionTypeDisplayName LIKE '%mute%' """
    # ORDER BY [AlertSup].[LocalSuppressFrom]

    swis = SwisClient(hostName, user, secret, verify=False)
    
    # let's run the query and store the results in a variable
    response = swis.query(swqlQuery)
   #  print(response['results'])
    # print the Header
    print('*' * 140)
    print("{:^30} {:^30} {:^30} \t {:^20} {:^20}" .format('Node Name', 'Supress From', 'Supressed Until','Supressed By','Status'))
    print('*' * 140)

    counter = 0
    date_format = '%Y-%m-%d %H:%M:%S%z'
    for val in response['results']:
      #   if counter >= 25:
      #       exit()
      #   else:
            values = Default(val)
            # print(type(val['LocalSuppressFrom']))
            # print("{0: <30} {1: >30} {2: >18} {3: >20} {4: >20}" .format_map(values))
            print("{Element:<25} \t {LocalSuppressFrom} \t {LocalSuppressUntil} \t {AccountID:>20} \t {Status}" .format_map(values))
            # print("{Element:<25} {datetime.datetime.strptime(datetime(LocalSuppressFrom), date_format)} \t {LocalSuppressUntil} \t {AccountID:>20} {Status:>20}" .format_map(values))
            # ['Element'], values['LocalSuppressFrom'], values['LocalSuppressUntil'], values['AccountID'], values['Status']))
            # string.Formatter().vformat(values['Element'], values['LocalSuppressFrom'], values['LocalSuppressUntil'], values['AccountID'], values['Status'])
            # print("{0: <30} {1: >30} {2: >18} {3: >20} {4: >20}" .format_map(val['Element'], val['LocalSuppressFrom'], val['LocalSuppressUntil'], val['AccountID'], val['Status']))
            # counter += 1
print('*' * 140)
print('Number of Muted Nodes : {}' .format(len(response['results'])))
