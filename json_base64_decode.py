#!/usr/bin/env python3
# Author    : Manjesh Munegowda
# Date      : May-15 2023
# Assignment: Write a program that does the following:  
#                  ●   Return a count of "foo events" per requestor IP.  
#                  ●   A "foo event" is denoted by a  FOO_EVENT  in the log message.  
#                  ●   Built-in libraries for base64, gzip, and JSON parsing should be used. 
#             There will be events such as  NOT_FOO_EVENT  that should not be counted as a foo event
#             -  The JSON contains a list of log events with Timestamp, Requestor IP, and a log Message.  
#             -  The JSON was compressed using gzip; the gzip result was encoded with base64
#
import base64, gzip, zlib, json, re

base64_message = '''H4sIAKU6UWQC/42UW2/aQBCF/8qI58TyBRvIW9SSCKkFlKK8oCha7ClZxbuGvUTtv+8s  pAIb74Ynay3P55kz5+x6PVhxgdowsRvcwOAJ95ZOjYLZ0p1/otZsi4OXG1gP0jjNbuPk  Ns4hzu+y9C6O3TdJmkVJXkSfT/fqYbF4nT5P5yuoG4UC+E5bEXUoRYuSplGWRcNhlOct  QqdoFCqa27pmwKVBVVkBimuru38dtwCH0qgootHIHb9ZxTbcWAWnCRpV8i5k0oJMJtF4  TATiuOMS6xqpB01SAokJzIBgf7i4aCaJW5z/nRDtOI0sQXOqF2gAFWFwi6bLSL5axn3N  95bREir4jTXX8GHrnTXMIGi24yi7xDQ03Ywm26IC6ZwCzJZkli4gC431zD8YSQF761qh  hi4mGoZWdFrMg9UlHiQBSVJ1KXloiqspxVfqLhVDTes+ztMoyRSC5Lo+WaiHWXg7u0eJ  TDphjkSUXPQARmHbuPLKcmDHEFAMN40yhKtpYZc+JODYm6rlG9NkaaJYAxVnIoL5YvXq  SahjTbzNtbLBSqjIgJu+fpLYq9AvrIC2dVqhi0YPIQlI5O4JFy2DYkeDCWZJpx5GGty9  64R95tOLyK42oXa4Q6A8VnSszC/KmSTqrZEl6Qo/+DvWf8E0sEGYPc4XT9PvsKEXdOv3  /OCKC/k8MeFu/Sb3hqaH4nf6WVRkI0NxScbBPbYicx7bl3+77YqDIAcAAA=='''

print("Decoding zip compressed, base64 encoded message",end='')
base64_bytes = base64_message.encode('utf-8')
message_bytes = base64.b64decode(base64_bytes)
#print(gzip.decompress(message_bytes))
uncompressed_data = gzip.decompress(message_bytes)
print("...Done")
print("--- Raw Data after decoding zip compressed base64 data ---")
print(uncompressed_data)

#Below method, running into error: Error -3 while decompressing data: incorrect header check
#print(zlib.decompress(base64.b64decode(base64_bytes))) 

print("\n" + '=' * 32 + "S O L U T I O N" + "=" * 32)
print("Parsing list of lists in Json data: for following condition")
print("●   Return a count of \"foo events\" per requestor IP. \n●   A \"foo event\" is denoted by a  FOO_EVENT  in the log message.")
print('=' * 80)

j_object = json.loads(uncompressed_data)

#Check if FOO_EVENT in the message and filter NOT_FOOT_EVENT in the message
event_counter = 0
count_items = []
for lst in j_object:
    #search = lambda word: filter(lambda x: word in x, lst[2])
    #search('FOO_EVENT')
    #if lst[2].startswith("FOO_EVENT"):
    #if lst[2].startswith("Fusce"):
    #if lst[2] == "^FOO_EVENT":
    if re.search(r'\bFOO_EVENT\b',lst[2]):
       print(lst)
       event_counter += 1
       count_items.append(lst[1])

print("Parsing list of lists in Json data...Done")
count_list=[{"IP":d,"count": count_items.count(d)} for d in set(count_items)]
print('=' * 80)
print(f'Total FOO_EVENT count is : {event_counter}')
print(count_list)
print('=' * 80)
