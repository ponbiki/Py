#!/usr/bin/env python

import json
import pycurl
import sys
import time
from StringIO import StringIO

'''
simple zone/record backups called with api key following, and outputs json
usage:
python zone_clone.py <key> original_zone backup_zone
'''

AUTH = 'X-NSONE-Key: ' + sys.argv[1]
URL = 'https://api.nsone.net/v1/zones'
OLD_ZONE = sys.argv[2]
NEW_ZONE = sys.argv[3]
if len(sys.argv) > 4:
    AUTH2 = "X-NSONE-Key: " + sys.argv[4]


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

new_zone_msg = json.loads(curl_api(URL + sys.argv[3], "PUT", AUTH, json.dumps({"zone": sys.argv[3]})))
if new_zone_msg == {"message":"zone already exists"}:
    exit
    print "Zone %s already exists; exiting..." % sys.argv[3]
    exit()

zone_arg = URL + "/" + OLD_ZONE
jsons = json.loads(curl_api(zone_arg, 'GET', AUTH))
domain_list = []
new_domain_list = []

for x in jsons['records']:
    if x['type'] != "NS":
        domain_list.append([x['domain'], x['type']])
        x['domain'] = x['domain'].replace(OLD_ZONE, NEW_ZONE)
        new_domain_list.append([x['domain'], x['type']])

stripped_records = []

for y in domain_list:
    time.sleep(.75)
    record_arg = URL + "/" + OLD_ZONE + "/" + y[0] + "/" + y[1]
    temp_record = (json.loads(curl_api(record_arg, "GET", AUTH)))
    temp_record['domain'] = temp_record['domain'].replace(OLD_ZONE, NEW_ZONE)
    temp_record['zone'] = temp_record['zone'].replace(OLD_ZONE, NEW_ZONE)
    clone_arg = URL + "/" + NEW_ZONE + "/" + temp_record['domain'] + "/" + temp_record['type']
    jzonz = json.dumps(temp_record)
    if len(sys.argv) > 4:
        key = AUTH2
    else:
        key = AUTH
    message = json.dumps(curl_api(clone_arg, "PUT", key, jzonz))
    print(message)
    if "Rate limit" in message:
        time.sleep(3)
        message = json.dumps(curl_api(clone_arg, "PUT", key, jzonz))
        print(message)
    if "unknown feed id" in message:
        stripped_records.append(temp_record['domain'])
        answer_count = 0
        for z in temp_record['answers']:
            temp_record['answers'][answer_count]['feeds'] = []
            temp_record['answers'][answer_count]['meta'] = {}
            answer_count += 1
        jaysons = json.dumps(temp_record)
        message = json.dumps(curl_api(clone_arg, "PUT", key, jaysons))
        print(message)

    temp_record.clear()

print(stripped_records)