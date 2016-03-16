#!/usr/bin/env python

import time
import json
import pycurl
import sys
from StringIO import StringIO

'''
call program followed by api key to find all domains idle for the last 30d
'''

AUTH = 'X-NSONE-Key: ' + sys.argv[1]
URL = 'https://api.nsone.net/v1/'

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

jsons = json.loads(curl_api(URL + 'zones', 'GET', AUTH))

zone_list = []

for jss in jsons:
    zone_list.append(jss['zone'])

big_dic = {}

print 'No queries in the last month for:'

for zone in zone_list:
    record = curl_api(URL + 'zones/' + zone, 'GET', AUTH)
    thing = {zone: []}
    z = json.loads(record)
    for r in z['records']:
        time.sleep(1)
        stats = json.loads(curl_api(URL + 'stats/usage/' + zone + '/' + r['domain'] + '/' + r['type'] + '?period=30d', 'GET', AUTH))
        if stats[0]['queries'] == 0:
            print 'Zone: %30s ||| Record: %30s ||| Type: %7s\n' % (zone, r['domain'], r['type'])
        else:
            pass
