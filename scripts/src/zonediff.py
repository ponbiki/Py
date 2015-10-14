#!/usr/bin/python
# requires python-software-properties, pycurl, and of course *NIX dig

import json
import pycurl
import re
import time
from getpass import getpass
from subprocess import check_output
from StringIO import StringIO

API_URI = "https://api.nsone.net/v1/"
NSONE_NS = "dns1.p01.nsone.net"
RAND_HOST = "a41be866d9e771d2363d1bb6aa46c5e3"
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
            answers_list.append("\t".join(ans_prts))
            answers_list.sort()
    return answers_list

def diff_rec(record_list):
    results = []
    warn = []
    for record in record_list:
        if re.match(r"^\*", record['domain']):
            re.sub(r"\*", RAND_HOST, record['domain'], max=1)
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
            print("\nSorry, that key is not valid!")
            return 1
    else:
        print("\nSorry, your key is not in the correct format!")
        return 1

def zone_check(api_key, domain):
    if len(domain) > 255:
        print("\nDomain name is too long! Exiting")
        exit()
    if re.match(r"^(?=.{4,255}$)([a-zA-Z\d-][a-zA-Z\d-]{,61}[a-zA-Z\d]\.)+[a-zA-Z\d]{2,5}$", domain):
        api_dck_uri = API_URI + "zones/" + domain
        if json.loads(curl_api(api_dck_uri, "GET", AUTH_HEAD + api_key)) == {'message': "zone not found"}:
            print("\nSorry, " + domain + " is not associated with this API key!")
            return 1
    else:
        print("\nSorry, " + domain + " is not a valid domain name!")
        return 1

def presenter(warn_list):
    item = ''
    i = 0
    for oops in warn_list:
        i += 1
        item += "\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n\n"
        item += str(i)
        ouch = oops[1].split(".")
        if ouch[0] == RAND_HOST:
            ouch[0] = "*"
        oops[1] = '.'.join(ouch)
        item += ") There may be a difference in domain " + oops[1] + " record type " + oops[2] + "\n"
        item += "!!Please double check the Answer(s), TTL, and record type!!\n"
        item += "\n>>>> " + legacy_ns + " answers:\n"
        for answer in oops[3]:
            item += answer + "\n"
        item += "\n>>>> " + NSONE_NS + " answers:\n"
        for answer in oops[4]:
            item += answer + "\n"
    return item

def save_file(domain, text):
    thyme = str(time.time()).split('.', 1)[0]
    f_name = "zone_test_" + domain + "_" + thyme + ".txt"
    try:
        file = open(f_name, 'w')
        file.write(text)
        file.close()
        good = "\n-----> " + f_name + " was written successfully!"
        return good
    except:
        bad = "\nThere was a problem writing to " + check_output(['pwd']).rstrip()
        return bad

def try_another(maybe):
    if maybe.lower()[:1] == 'n':
        return 1

def banner():
    print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
    print('+---------------------------------------------------------------+')
    print('+------------------Zone_Consistancy_Checker_v1------------------+')
    print('+---------------------------------------------------------------+')
    print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')

banner()
print("\nPlease enter API key:")
api_key = getpass(prompt="")
while key_check(api_key) == 1:
    print("\nPlease try your API key again:")
    api_key = getpass(prompt="")
maybe = 'y'
while try_another(maybe) != 1:
    print("\nPlease enter fully qualified domain name:")
    fqdn = raw_input()
    while zone_check(api_key, fqdn) == 1:
        print("\nPlease try entering your domain again:")
        fqdn = raw_input()
    legacy_ns = ns_get(fqdn)
    results = (presenter(diff_rec(record_list(curl_api(API_URI + "zones/" + fqdn, "GET", AUTH_HEAD + api_key)))))
    print(results)
    if len(results) > 0:
        print("\nWould you like a text copy in " + check_output(['pwd']).rstrip() + "? ( Y/n )")
        txt_me = raw_input()
        if txt_me.lower()[:1] == 'y':
            print(save_file(fqdn, results))
    else:
        print("\nThe records in the " + fqdn + " zone match on the current and NS1 nameservers.")
    print("\nDo you want to test another domain? ( Y/n ):")
    maybe = raw_input()

#issues
#not comparing empty (legacy?) results
#not handling *
#add SOA comparison