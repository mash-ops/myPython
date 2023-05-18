#!/usr/bin/env python3
# Author    : Manjesh Munegowda
# Date      : May-17 2023
# Assignment: Write a program that does the following:  
#                  ●   Parse the URL and decode the base64 encoded and gzip compressed, CSV file with Data
#                  ●   Find the Highest earner and print the details of the highest earner
#                  ●   Find the Average salary from the salary data
#             -  The CSV was compressed using gzip; the gzip result was encoded with base64
#

import urllib.request, base64, gzip, csv, sys, time

url = "https://gist.githubusercontent.com/rootshellz/b6390de20cd00e36370649da0b8400cd/raw/9ab65ecab313979e23515001cd67b832ff65d9e0/csv.gz.b64"
webUrl  = urllib.request.urlopen(url)

base64_data = webUrl.read()
message_bytes = base64.b64decode(base64_data)
uncompressed_data = gzip.decompress(message_bytes)
print("...Done")
print("--- Raw Data after decoding zip compressed base64 data ---")
print(uncompressed_data)

#Decoding byte string
#decode_string = uncompressed_data.decode('utf-8')

# Convert the byte string to a string using the str() constructor
decode_string = str(uncompressed_data, encoding='utf-8')

print("\n" + '=' * 32 + "S O L U T I O N" + "=" * 32)
print("Parsing CSV data: for following condition")
print("●   Find the Highest earner and print the details of the highest earner. \n●   Find the Average salary from the salary datae.")
print('=' * 80)

my_list = []
for row in decode_string.split('\n'):
  my_list.append(row)

salary_list = []
for col in my_list[1:]:         # Skipping the first row, since it contains header info for the fields
  col = col.replace('"','')     # Replacing double quotes with blank surrounding each comma separated field
  #print(col[-7:])
  if col != "":
     #print(int(col[-7:].replace(',','')))              
     salary_list.append(int(col[-7:].replace(',','')))  #The salary field has comma in the number replacing with blank

salary_list.sort()                                      #For somereason max() method did not work, trying sort method
print("Salary list is : {}".format(salary_list))
print("Highest salary is : {}".format(salary_list[-1]))
high_salary = salary_list[-1]

for fnd in my_list:                                     #Iterating the list to get the details of highest paid individual 
  if str(high_salary) in fnd.replace(',',''):
     earned_by = fnd.replace('"','')
     #print(fnd)

print("Highest salary of ${} is earned by : {}".format(high_salary,earned_by))
print("The Average salary eared is ${}".format((sum(salary_list) / len(salary_list))))
print("\n" + '=' * 34 + "The END" + "=" * 35)
