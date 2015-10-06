#!/usr/bin/python

import json
import pycurl
import re
from subprocess import check_output
from StringIO import StringIO
from operator import itemgetter
from pprint import pprint

API_URI = "https://api.nsone.net/v1/"
NSONE_NS = "dns1.p01.nsone.net"
RANDOM_HOSTNAME = "a41be866d9e771d2363d1bb6aa46c5e3"
AUTH_HEAD = "X-NSONE-Key: "

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

def ns_get(fqdn):
    out = check_output(['dig', '+short', fqdn, 'NS'])
    legacy_ns = out.split()
    return legacy_ns[0]

def record_list(zone_json):
    zone = json.loads(zone_json)
    rec_list = []
    for records in zone['records']:
        if records['type'] != 'NS':
            recs = {
                'domain': records['domain'],
                'type': records['type']
            }
            rec_list.append(recs)
    return rec_list

def lookup(record, type, ns):
    out = check_output(['dig', '+nocmd', '+noall', '+answer', '+ttlid', type, '@' + ns, record])
    answers = out.split("\n")
    results = []
    for answer in answers:
        if len(answer) != 0:
            component = answer.split("\t")
            result = [
                component[4], #answer
                component[1], #ttl
                component[0]  #record
            ]
            results.append(result)
            sorted(results, key=itemgetter(0))
    return results

def diff_rec(list_o_records):
    old_list = []
    new_list = []
    diff_list = []
    for record in list_o_records:
        if re.match(r"^\*", record['domain']):
            re.sub(r"\*", RANDOM_HOSTNAME, record['domain'], max=1)
        old_list.append(lookup(record['domain'], record['type'], legacy_ns))
        new_list.append(lookup(record['domain'], record['type'], NSONE_NS))
    crap_list = [old_list, new_list]
    return crap_list

print('Please enter API key:')
api_key = raw_input() #sanitize
print('Please enter fully qualified domain name:') #sanitize
fqdn = raw_input() #sanitize
legacy_ns = ns_get(fqdn)
pprint(diff_rec(record_list(curl_api(API_URI + "zones/" + fqdn, "GET", AUTH_HEAD + api_key))))
