#!/usr/bin/python

import json
import pycurl
from StringIO import StringIO
from copy import deepcopy

def buster(url, verb, authhead, *args):
    buffer = StringIO()
    c = pycurl.Curl()
    c.setopt(c.URL, url)
    c.setopt(c.CUSTOMREQUEST, verb)
    c.setopt(c.HTTPHEADER, [authhead])
    for arg in args:
        c.setopt(c.POSTFIELDS, arg)
    c.setopt(c.WRITEDATA, buffer)
    c.perform()
    c.close()
    return buffer.getvalue()

print('**********************************************')
print('* Simple A <=> CNAME <=> Alias swapping tool *')
print('**********************************************')
print('Enter your API key')
key = raw_input() #sanitize

authhead = "X-NSONE-Key: " + key
base_url = 'https://api.nsone.net/v1/'
validate_url = base_url + "zones"
validate_verb = "GET"

body = buster(validate_url, validate_verb, authhead)

if json.loads(body) == {'message': 'Unauthorized'}:
    print("Sorry, that key is not valid! Exiting")
    exit()

print('Please enter the record name that you want to change')

record = raw_input().lower() #sanitize blah blah some kind of validation
record_list = record.split('.')
subd = len(record_list)
zone = record_list[subd - 2] + '.' + record_list[subd - 1]

print('Please enter current record type ( A / ALIAS / CNAME )')

temp_type = raw_input().upper()

if temp_type == "A":
    old_type = "A"
elif temp_type == "ALIAS":
    old_type = "ALIAS"
elif temp_type == "CNAME":
    old_type = "CNAME"
else:
    print('Sorry, ' + temp_type + ' was not a valid record type')
    exit()

print('Please enter new record type ( A / ALIAS / CNAME )')

temp_new_type = raw_input().upper()

if temp_new_type == old_type:
    print('Well ' + record + ' is already set then....nothing to do here...exiting!')
    exit()
elif temp_new_type == "A":
    new_type = "A"
elif temp_new_type == "ALIAS":
    new_type = "ALIAS"
elif temp_new_type == "CNAME":
    new_type = "CNAME"
else:
    print('Sorry, ' + new_temp_type + ' was not a valid record type')
    exit()

print('This will change ' + record + ' from record type ' + old_type + ' to record type ' + new_type)
print('Do you wish to continue? ( Y/n ) ')

do_you = raw_input().lower()

if do_you != "y":
    print('Exiting now!')
    exit()
    
old_rec_url = base_url + "zones/" + zone + "/" + record + "/" + old_type
old_rec_verb = "GET"

old_json = buster(old_rec_url, old_rec_verb, authhead)
old_json_dict = json.loads(old_json)
new_json_dict = deepcopy(old_json_dict)
new_json_dict['type'] = new_type

for answer in new_json_dict['answers']:
    print("Please enter the replacement answer for " + answer['answer'][0])
    answer['answer'][0] = raw_input().lower() #sanitize and validate

if new_type == "CNAME" or new_type == "ALIAS":
    n_one = {'filter': 'select_first_n', 'config': {'N': 1}}
    if not any (filter['filter'] == 'select_first_n' for filter in new_json_dict['filters']):
        new_json_dict['filters'].append(n_one)
        print("Added SELECT_FIRST_N filter for CNAME RFC compliance.\n")
        
new_json = json.dumps(new_json_dict)

new_rec_url = base_url + "zones/" + zone + "/" + record + "/" + new_type
new_rec_verb = "PUT"

new_body = buster(new_rec_url, new_rec_verb, authhead, new_json)

print("New " + new_type + " record " + record + " has now been created\n")

print("Would you like to delete the " + record + " " + old_type + " record now (Y/n)")

well_do_you = raw_input().lower()

if well_do_you != "y":
    print(record + " " + old_type + " record was not deleted...exiting now!")
    exit()

del_rec_url = base_url + "zones/" + zone + "/" + record + "/" + old_type
del_rec_verb = "DELETE"

del_body = buster(del_rec_url, del_rec_verb, authhead)

print("The " + record + " " + old_type + " record has been deleted. \n In case you really did not want to do this, here's a JSON dump of it...\n")

print(old_json)

exit()