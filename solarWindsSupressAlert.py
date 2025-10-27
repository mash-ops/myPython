#! ~/venv/bin/python
# Author     : Manjesh.munegowda@stanfordchildrens.org
# Purpose    : To Suppress alerts for Nodes for a scheduled time period
# How to use : execute this python script from command line
#            : Input file nodesToSuppressAlert.csv, one node per line with following columns
#            : #Node, SuppressionFrom, SuppressUntil
#            : testnode01.your.domain,9/28/23 11:00:00,9/28/23 12:00:00
# NOTE       : If same node with two different time is provided the last one is used, from below input the 10:46 will be used to Suppress the alert
#              testnode01.your.domain,10/2/23 10:40:00,10/2/23 10:45:00
#              testnode01.your.domain,10/2/23 10:46:00,10/2/23 10:48:00
# Update     : Oct2-2023, added exception handling for 400 Client Error: Until date '10/02/2023 10:45:00' cannot be smaller than from date '10/02/2023 10:58:00'
#            : 2) Added validation for DateTime less then current DateTime, 3) validating access, 4) print status of skipped / notfound
#Prerequisite: pip install orionsdk, tested with 0.4.0 ; Solarwinds user who has permissions to supress alerts
#
import getpass, requests, json, csv, sys
from orionsdk import SwisClient
from urllib3.exceptions import InsecureRequestWarning
from datetime import datetime

# Suppress the warnings from urllib3
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
user = 'your.domain\\' + getpass.getuser()    #Get the current logged in user

try:
    print("User : {}".format(user))
    secret = getpass.getpass(prompt='Password :')
    try:
        hostName = 'psrpsolrapp02'
        filename = 'nodesToSuppressAlert.csv'
        swis = SwisClient(hostName, user, secret, verify=False)
        # swis.query("SELECT Uri FROM Orion.Nodes WHERE DNS=@DNS", DNS=hostName)
    except requests.exceptions.HTTPError as AuthError:
        sys.exit('{}'.format(AuthError))
except Exception as error:
    print('ERROR', error)
else:
    try:
        with open(filename, newline='\n') as iFH:
            reader = csv.reader(iFH)
            # swis = SwisClient(hostName, user, secret, verify=False)
            comment = '#'
            date_format = '%m/%d/%y %H:%M:%S'
            current_datetime = datetime.now()
            Suppress_status = []
            for row in reader:
                print(row)
                if comment not in row[0]:
                #    print(row[0])
                   try:
                       uri = swis.query("SELECT Uri FROM Orion.Nodes WHERE DNS=@DNS", DNS=row[0])['results'][0]['Uri']
                       SuppressionFrom = datetime.strptime(row[1], date_format)
                       SuppressUntil = datetime.strptime(row[2], date_format)
                       # uri = swis.query("SELECT Uri FROM Orion.Nodes WHERE SysName=@SysName", SysName=row[0])['results'][0]['Uri']
                       print('{}\t{}\t {}\t{}' .format(row[0], uri,SuppressionFrom,SuppressUntil))                  
                       try:
                           if (current_datetime < SuppressionFrom) and (current_datetime < SuppressUntil):
                              swis.invoke('Orion.AlertSuppression', 'SuppressAlerts', [uri], SuppressionFrom, SuppressUntil)
                              alert_suppress = str(row[::]) + ' ' + '==> Success - Alert Suppressed'
                              Suppress_status.append(alert_suppress)
                           else:
                               print ('Skipping :: {} : SuppressFrom {} Or SuppressUntil {} cannot be less than current DateTime [{}]'.format(row[0], SuppressionFrom, SuppressUntil, current_datetime))
                               date_skipped = str(row[::]) + ' ' + '==> Skipped - Check input date/s'
                               Suppress_status.append(date_skipped)
                               continue
                       except requests.exceptions.HTTPError as ClientError:
                           print('{} :: Skipping...'.format(ClientError))
                   except IndexError:
                       print('{} Not Found...' .format(row[0]))
                       Node_notFound = str(row[::]) + ' ' + '==> Not Found - Check if the Hostname is correct'
                       Suppress_status.append(Node_notFound)
            print('*' * 120) 
            for final_stats in Suppress_status:
                print('{}'.format(final_stats))
            print('*' * 120)
    except csv.Error as Ferror:
        sys.exit('file {}, line {}: {}'.format(filename, reader.line_num, Ferror))
