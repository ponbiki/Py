#!/usr/bin/python

import json
import pycurl
import re
from subprocess import check_output
from StringIO import StringIO
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
            if records['type'] == 'ALIAS':
                records['type'] == 'CNAME'
            recs = {
                'domain': records['domain'],
                'type': records['type']
            }
            rec_list.append(recs)
    return rec_list

def lookup(record, type, ns):
    out = check_output(['dig', '+nocmd', '+noall', '+answer', '+ttlid', type, '@' + ns, record])
    answers = out.split("\n")
    answers_list = []
    for answer in answers:
        if len(answer) != 0:
            answer = answer.upper()
            answers_list.append(' '.join(answer.split("\t")))
            answers_list.sort()
    return answers_list

def diff_rec(record_list):
    results = []
    warn = []
    for record in record_list:
        if re.match(r"^\*", record['domain']):
            re.sub(r"\*", RANDOM_HOSTNAME, record['domain'], max=1)
        old_answers = lookup(record['domain'], record['type'], legacy_ns)
        new_answers = lookup(record['domain'], record['type'], NSONE_NS)
        diff_list = filter(lambda x:x not in new_answers, old_answers)
        results.append(diff_list)
    for item in results:
        if len(item) != 0:
            warn.append(item)
    return warn

def key_check(key):
    api_kck_uri = API_URI + "zones/"
    if json.loads(curl_api(api_kck_uri, "GET", AUTH_HEAD + api_key)) == {'message': 'Unauthorized'}:
        print("Sorry, that key is not valid! Exiting")
        exit()

def zone_check(api_key, domain):
    api_dck_uri = API_URI + "zones/" + domain
    if json.loads(curl_api(api_dck_uri, "GET", AUTH_HEAD + api_key)) == {'message': "zone not found"}:
        print("Sorry, " + domain + " is not associated with this API key! Exiting")
        exit()

print('Please enter API key:')
api_key = raw_input() #sanitize
key_check(api_key)
print('Please enter fully qualified domain name:') #sanitize
fqdn = raw_input() #sanitize
zone_check(api_key, fqdn)
legacy_ns = ns_get(fqdn)
pprint(diff_rec(record_list(curl_api(API_URI + "zones/" + fqdn, "GET", AUTH_HEAD + api_key))))
