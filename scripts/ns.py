#!/usr/bin/env python

import json
import pycurl
import sys
import time
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
    record = curl_api(URL + '/' + zone + '/' + zone + '/NS', 'GET', AUTH)
    rec_dic = json.loads(record)
    done = False
    for answer in rec_dic['answers']:
        if 'dns1.p09.nsone.net' in answer['answer'][0]:
            done = True
        else:
            continue
    if done is False:
        for i in range(4):
            rec_dic['answers'].append({'answer': ['dns' + str(i + 1) + '.p09.nsone.net']})
        new_record =  json.dumps(rec_dic)
        print 'updating %s' % zone
        resp = curl_api(URL + '/' + zone + '/' + zone + '/NS', 'POST', AUTH, new_record)
        print resp
        time.sleep(1)
    else:
        continue