#!/usr/bin/env python

import json
import pycurl
import sys
from StringIO import StringIO

'''
simple zone/record backups called with api key following, and outputs json
does not grab monitors, feeds, etc
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

jsons = json.loads(curl_api(URL, 'GET', AUTH))

zone_list = []

for jss in jsons:
   zone_list.append(jss['zone'])

big_dic = {}

for zone in zone_list:
   record = curl_api(URL + '/' + zone, 'GET', AUTH)
   thing = {zone: [json.loads(record)]}
   big_dic.update(thing)

print json.dumps(big_dic)