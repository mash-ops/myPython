#! ~/venv/bin/python
# Author     : Manjesh.munegowda@stanfordchildrens.org
# Purpose    : To call solarwind api to query orion node and display alert/s in tabular format
# How to use : execute this python script from command line with username as parameter, who has access to Solarwinds server
#Prerequisite: pip install orionsdk, preferably in venv. Tested with orionsdk version 0.4.0
#

import getpass, requests, json, sys
from orionsdk import SwisClient
from urllib3.exceptions import InsecureRequestWarning

# Suppress the warnings from urllib3
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
user = "yourAD\\" + str(sys.argv[1])
#user = getpass.getuser()    #Get the current logged in user

try:
    print("User : {}".format(user))
    secret = getpass.getpass(prompt='Password :')
except Exception as error:
    print('ERROR', error)
else:
    hostName = 'YourSolarWindsServerName'
    '''         WHEN 0 THEN 'Informational'
        WHEN 1 THEN 'Warning'
                WHEN 2 THEN 'Critical'
        WHEN 3 THEN 'Serious'
        WHEN 4 THEN 'Notice' '''
    swqlQuery = """SELECT
        o.AlertConfigurations.Name AS [ALERT NAME]
        ,'/Orion/NetPerfMon/ActiveAlertDetails.aspx?NetObject=AAT:' + ToString(o.AlertObjectID) AS [_LinkFor_ALERT NAME]
        ,o.EntityCaption AS [ALERT OBJECT]
        ,o.EntityDetailsURL AS [_LinkFor_ALERT OBJECT]
        ,o.RelatedNodeCaption AS [RELATED NODE]
        ,o.RelatedNodeDetailsURL AS [_LinkFor_RELATED NODE]
        ,ToLocal(o.AlertActive.TriggeredDateTime) AS [ALERT TRIGGER TIME]
        ,o.AlertActive.TriggeredMessage AS [ALERT MESSAGE]
        ,CASE o.AlertConfigurations.Severity
                WHEN 2 THEN 'Critical'
        ELSE CONCAT('Unknown Severity: ', o.AlertConfigurations.Severity)
        END AS [Severity]
--      ,N.CustomProperties.NodeRegion
FROM Orion.AlertObjects AS o
LEFT JOIN Orion.Nodes AS N ON N.Caption = o.RelatedNodeCaption
WHERE o.AlertActive.TriggeredMessage <> ''
ORDER by o.AlertActive.TriggeredDateTime DESC"""
    swis = SwisClient(hostName, user, secret, verify=False)
    
    # let's run the query and store the results in a variable
    response = swis.query(swqlQuery)
    #print(response['results'])
    # print the Header
    print('*' * 140)
    print("{:^50} {:^30} {:^18} {:^20} {:^20}" .format('Alert Name', 'Node Name', 'Alert Time','Alert Message','Severity'))
    print('*' * 140)

    counter = 0
    for val in response['results']:
        if counter >= 25:
            exit()
        else:
            print("{} {} {} {} {}" .format(val['ALERT NAME'], val['ALERT OBJECT'], val['ALERT TRIGGER TIME'], val['ALERT MESSAGE'], val['Severity']))
            #print("{:<50} {:<30} {:<18} {:<20} {:<20}" .format(val['ALERT NAME'], val['ALERT OBJECT'], val['ALERT TRIGGER TIME'], val['ALERT MESSAGE'], val['Severity']))
            #print("{0: <50} {1: >30} {2: >18} {3: >20} {4: >20}" .format(val['ALERT NAME'], val['ALERT OBJECT'], val['ALERT TRIGGER TIME'], val['ALERT MESSAGE'], val['Severity']))
            counter += 1
