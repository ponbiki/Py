#!/usr/bin/env python

import json
import pycurl
import sys
import time
from StringIO import StringIO

'''
simple zone/record backups called with api key following, and outputs json
'''

AUTH = 'X-NSONE-Key: ' + sys.argv[1]
URL = 'https://api.nsone.net/v1/zones'


def curl_api(url, verb, authhead, *args):
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

zone_arg = URL + "/" + sys.argv[2]
jsons = json.loads(curl_api(zone_arg, 'GET', AUTH))
domain_list = []
new_domain_list = []

for x in jsons['records']:
    if x['type'] != "NS":
        domain_list.append([x['domain'], x['type']])
        x['domain'] = x['domain'].replace(sys.argv[2], sys.argv[3])
        new_domain_list.append([x['domain'], x['type']])

for y in domain_list:
    time.sleep(.75)
    record_arg = URL + "/" + sys.argv[2] + "/" + y[0] + "/" + y[1]
    temp_record = (json.loads(curl_api(record_arg, "GET", AUTH)))
    temp_record['domain'] = temp_record['domain'].replace(sys.argv[2], sys.argv[3])
    temp_record['zone'] = temp_record['zone'].replace(sys.argv[2], sys.argv[3])
    clone_arg = URL + "/" + sys.argv[3] + "/" + temp_record['domain'] + "/" + temp_record['type']
    jzonz = json.dumps(temp_record)
    message = json.dumps(curl_api(clone_arg, "PUT", AUTH, jzonz))
    print(message)
    if "Rate limit" in message:
        time.sleep(3)
        message = json.dumps(curl_api(clone_arg, "PUT", AUTH, jzonz))
        print(message)
    temp_record.clear()