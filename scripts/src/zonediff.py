#!/usr/bin/python

import json
import pycurl
import re
from subprocess import check_output
from StringIO import StringIO

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
                records['type'] == 'A'
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
            ans_prts = answer.split("\t")
            ans_prts[0] = ans_prts[0].lower()
            answers_list.append(' '.join(ans_prts))
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
        if len(diff_list) > 0:
            results.append([diff_list, record['domain'], record['type'], old_answers, new_answers])
    for item in results:
        if len(item) != 0:
            warn.append(item)
    return warn

def key_check(key):
    if re.match(r"^[a-zA-Z\d]+$", key):
        api_kck_uri = API_URI + "zones/"
        if json.loads(curl_api(api_kck_uri, "GET", AUTH_HEAD + key)) == {'message': 'Unauthorized'}:
            print("Sorry, that key is not valid! Exiting")
            exit()
    else:
        print("Sorry, your key is not in the correct format! Exiting")
        exit()

def zone_check(api_key, domain):
    if len(domain) > 255:
        print("Domain name is too long! Exiting")
        exit()
    if re.match(r"^(?=.{4,255}$)([a-zA-Z\d-][a-zA-Z\d-]{,61}[a-zA-Z\d]\.)+[a-zA-Z\d]{2,5}$", domain):
        api_dck_uri = API_URI + "zones/" + domain
        if json.loads(curl_api(api_dck_uri, "GET", AUTH_HEAD + api_key)) == {'message': "zone not found"}:
            print("Sorry, " + domain + " is not associated with this API key! Exiting")
            exit()
    else:
        print("Sorry, " + domain + " is not a valid domain name! Exiting")
        exit()

def presenter(warn_list):
    item = ''
    i = 0
    for oops in warn_list:
        i += 1
        item += str(i)
        item += " There may be a difference in domain " + oops[1] + " record type " + oops[2] + "\n"
        item += "!!Please double check the Answer(s), TTL, and record type!!\n"
        item += "\n>>>>Current NS answers:\n"
        for answer in oops[3]:
            item += answer + "\n"
        item += "\n>>>>NSONE NS answers:\n"
        for answer in oops[4]:
            item += answer + "\n"
        item += "\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n\n"
    return item

def banner():
    print('*****************************************************************')
    print('*!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!*')
    print('*!!!!!!!!!!!!!!!!!!Zone_Consistancy_Checker_v1!!!!!!!!!!!!!!!!!!*')
    print('*!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!*')
    print('*****************************************************************')    

banner()
print('Please enter API key:')
api_key = raw_input()
key_check(api_key)
print('Please enter fully qualified domain name:')
fqdn = raw_input()
zone_check(api_key, fqdn)
legacy_ns = ns_get(fqdn)
print(presenter(diff_rec(record_list(curl_api(API_URI + "zones/" + fqdn, "GET", AUTH_HEAD + api_key)))))

# todo 
# re-attach * to for random string test answers
# allow data re-entry
# allow txt file option "zone_cmp_" + fqdn + int(time.time()) + ".txt"     (needs import time)