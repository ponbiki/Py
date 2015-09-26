#!/usr/bin/python

import json
import pycurl
from StringIO import StringIO
from pprint import pprint
from copy import deepcopy

print('**********************************************')
print('Simple A record <=> CNAME record swapping tool')
print('**********************************************')
print('Enter your API key')
key = raw_input()

authhead = "X-NSONE-Key:" + key
base_url = 'https://api.nsone.net/v1/'
validate_url = base_url + "zones"
validate_verb = "GET"

def buster(url, verb, authhead):
    buffer = StringIO()
    c = pycurl.Curl()
    c.setopt(c.URL, url)
    c.setopt(c.CUSTOMREQUEST, verb)
    c.setopt(c.HTTPHEADER, [authhead])
    c.setopt(c.WRITEDATA, buffer)
    c.perform()
    c.close()
    return buffer.getvalue()

body = buster(validate_url, validate_verb, authhead)

if json.loads(body) == {'message': 'Unauthorized'}:
    print("Sorry, that key is not valid! Exiting")
    exit()

print('Please enter the record name that you want to change')

record = raw_input() #sanitize blah blah some kind of validation

print('Please enter record type ( A or CNAME )')

temp_type = raw_input()

if temp_type == "A":
    old_type = "A"
    new_type = "CNAME"
elif temp_type == "CNAME":
    old_type = "CNAME"
    new_type = "A"
else:
    print('Sorry, that was not a valid record type')
    exit()

print('This will change ' + record + ' from record type ' + old_type + ' to record type ' + new_type)
print('''!!!!!!THIS IS IRREVERSIBLE!!!!!!''')
print('Do you wish to continue? ( Y/n ) ')

do_you = raw_input().lower()

if do_you != "y":
    print('Exiting now!')
    exit()
    
old_rec_url = base_url + "zones/" + record + "/" + record + "/" + old_type
old_rec_verb = "GET"

old_json = buster(old_rec_url, old_rec_verb, authhead)

pprint(json.loads(old_json)[0])
print ("\n\r\n\r")
print(old_json)
new_json = copy.deepcopy(old_json)
new_json['type'] = new_type
print ("\n\r\n\r")
pprint(new_json)
print ("\n\r\n\r")
print(new_json)