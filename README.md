# Decoding zip compressed, base64 encoded message ::
## ./json_base64_decode.py
Decoding zip compressed, base64 encoded message...Done
--- Raw Data after decoding zip compressed base64 data ---
### b'[["Timestamp", "Requestor IP", "Message"], ["2023-01-05 05:32:00", "123.156.123.156", "FOO_EVENT lorem ipsum."], ["2023-01-06 05:32:00", "22.33.44.55", "FOO_EVENT"], ["2023-01-07 05:32:00", "22.33.44.55", "Nulla interdum risus."], ["2023-01-08 05:32:00", "44.55.66.77", "Curabitur FOO_EVENT orci."], ["2023-01-09 05:32:00", "99.88.77.66", "Pellentesque est at maximus."], ["2023-01-10 05:32:00", "55.66.77.88", "Nunc sit amet erat eget."], ["2023-01-11 05:32:00", "123.156.123.156", "Aliquam id felis vulputate sapien."], ["2023-01-12 05:32:00", "99.88.77.66", "Integer neque auctor."], ["2023-01-13 05:32:00", "55.66.77.88", "Vivamus quis velit."], ["2023-01-14 05:32:00", "44.55.66.77", "FOO_EVENT Fusce eget nunc."], ["2023-01-15 05:32:00", "99.88.77.66", "FOO_EVENT Fusce eget nunc."], ["2023-01-16 05:32:00", "123.156.123.156", "Praesent quis ornare nisl FOO_EVENT."], ["2023-01-16 06:32:00", "99.88.77.66", "Aenean vel quis enim."], ["2023-01-16 07:32:00", "55.66.77.88", "Nunc vel dui a risus lobortis luctus."], ["2023-01-16 08:32:00", "22.33.44.55", "Phasellus ut diam. NOT_FOO_EVENT"], ["2023-01-16 09:32:00", "55.66.77.88", "Pellentesque ac dapibus."], ["2023-01-16 10:32:00", "99.88.77.66", "Sed et FOO_EVENT erat."], ["2023-01-16 11:32:00", "55.66.77.88", "Nulla sit tempus mauris."], ["2023-01-16 12:32:00", "123.156.123.156", "Sed at amet mauris."], ["2023-01-16 13:32:00", "99.88.77.66", "FOO_EVENT Fusce sed auctor nunc."], ["2023-01-16 13:33:00", "99.88.77.66", "Sed  FOO_EVENT rhoncus. Likely to be IGNORED by time."], ["2023-01-16 15:32:00", "22.33.44.55", "FOO_EVENT Fusce eget auctor nunc."], ["2023-01-16 16:32:00", "99.88.77.66", "Praesent quis ornare nisl."], ["2023-01-16 17:32:00", "55.66.77.88", "Aenean vel non quis enim."], ["2023-01-16 18:32:00", "123.156.123.156", "Nunc vel dui FOO_EVENT."]]'

### ================================S O L U T I O N================================
### Parsing list of lists in Json data: for following condition
### ●   Return a count of "foo events" per requestor IP. 
### ●   A "foo event" is denoted by a  FOO_EVENT  in the log message.
### ================================================================================
#### ['2023-01-05 05:32:00', '123.156.123.156', 'FOO_EVENT lorem ipsum.']
#### ['2023-01-06 05:32:00', '22.33.44.55', 'FOO_EVENT']
#### ['2023-01-08 05:32:00', '44.55.66.77', 'Curabitur FOO_EVENT orci.']
#### ['2023-01-14 05:32:00', '44.55.66.77', 'FOO_EVENT Fusce eget nunc.']
#### ['2023-01-15 05:32:00', '99.88.77.66', 'FOO_EVENT Fusce eget nunc.']
#### ['2023-01-16 05:32:00', '123.156.123.156', 'Praesent quis ornare nisl FOO_EVENT.']
#### ['2023-01-16 10:32:00', '99.88.77.66', 'Sed et FOO_EVENT erat.']
#### ['2023-01-16 13:32:00', '99.88.77.66', 'FOO_EVENT Fusce sed auctor nunc.']
#### ['2023-01-16 13:33:00', '99.88.77.66', 'Sed  FOO_EVENT rhoncus. Likely to be IGNORED by time.']
#### ['2023-01-16 15:32:00', '22.33.44.55', 'FOO_EVENT Fusce eget auctor nunc.']
#### ['2023-01-16 18:32:00', '123.156.123.156', 'Nunc vel dui FOO_EVENT.']
#### Parsing list of lists in Json data...Done
#### ================================================================================
#### Total FOO_EVENT count is : 11
#### [{'IP': '99.88.77.66', 'count': 4}, {'IP': '22.33.44.55', 'count': 2}, {'IP': '123.156.123.156', 'count': 3}, {'IP': '44.55.66.77', 'count': 2}]
#### ================================================================================

# ===================================
# Decoding gzip compressed, base64 encoded CSV data ::
## myPython % ./csv_base64_decode.py
--- Raw Data after decoding zip compressed base64 data ---
b'"name","position","start date","salary"\n"Paul Smith","Lead Analys","Mon, 02 Jan 2006","173,000"\n"Lisa Wilkinson","Director, Information Technology","Mon, 02 Jan 2006","385,000"\n"Ryan Elliot","Custodian","Mon, 02 Jan 2006","89,000"\n"Kendra Chin","QA Engineer","Mon, 02 Jan 2006","156,000"\n'

#### ================================S O L U T I O N================================
#### Parsing CSV data: for following condition
#### ●   Find the Highest earner and print the details of the highest earner. 
#### ●   Find the Average salary from the salary datae.
#### ================================================================================
#### Salary list is : [89000, 156000, 173000, 385000]
#### Highest salary is : 385000
#### Highest salary of $385000 is earned by : Lisa Wilkinson,Director, Information Technology,Mon, 02 Jan 2006,385,000
#### The Average salary eared is $200750.0

#### ==================================The END===================================
