#!/usr/bin/env python
# Author    : Manjesh Munegowda
# Date      : Jun-20 2023
# Assignment: Write a program that does the following:  
#               - Read Json file (with specific test data provided in test.json) and print the tenants whoes status is ACTIVE
#
import json

try:
   with open('test.json') as fp:
     jobject = json.loads(fp.read())
except IOError as err:
   print("{}".format(err))
   #print("{} : {}".format(err.errno, err))
   exit()

print("** Requirement is, If the Tenant State is ACTIVE, then print the Tenant Name")

for key,value in jobject.items():
  print("\n** This is the list of dictionary after parsing {} : {} ".format(key, value))
  print("\n** Below is the list of tenants who's state is ACTIVE...")

  for item in value:
    if item.get("tenantState") == "ACTIVE":
       print("Tenant {} status is ACTIVE".format(item.get("tenantName")))
