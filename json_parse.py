#!/usr/bin/env python
# Author    : Manjesh Munegowda
# Date      : Jun-19 2023
# Assignment: Write a program that does the following:  
#               - Parse the sample Json data and print the tenants whoes status is ACTIVE
#
import json

jdata='{ "Items" : [ { "tenantID" : 1, "tenantName" : "TEST1", "tenantState" : "ACTIVE" }, { "tenantID" : 2, "tenantName" : "TEST2", "tenantState" : "ACTIVE" }, { "tenantID" : 3, "tenantName" : "TEST3", "tenantState" : "DELETED" } ] }'

#jobject = json.loads(jdata.decode('utf-8'))
jobject = json.loads(jdata.decode('ascii','ignore'))
print("** The data type we got from Json is {}".format(type(jobject)))

for key,value in jobject.items():
  print("** After parsing the dictionary ended up with {} of dictionary".format(type(value)))
  print("** This is the list of dictionary after parsing : {} ".format(value))
  print("** Requirement is, If the Tenant State is ACTIVE, then print the Tenant Name")
  print("** Below is the list of tenants who's state is ACTIVE...")

  for item in value:
    #print(item)
    if item.get("tenantState") == "ACTIVE":
       print(item.get("tenantName"))
