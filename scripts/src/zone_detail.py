#!/usr/bin/env python

import json
import pycurl
import sys
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

for x in jsons['records']:
    domain_list.append([x['domain'], x['type']])

record_list = []

for y in domain_list:
    record_arg = URL + "/" + sys.argv[2] + "/" + y[0] + "/" + y[1]
    record_list.append(json.loads(curl_api(record_arg, "GET", AUTH)))

print(json.dumps(record_list))
