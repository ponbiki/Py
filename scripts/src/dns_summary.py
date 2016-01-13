#!/usr/bin/python

import json
import pycurl
import sys
from StringIO import StringIO

'''Outputs an account summary as a formatted print or a JSON with usage as:
user@computer ~ $ python dns_summary.py <key> <option>
JSON option: j
CSV option: c  ## will change to proper CSV lib handling
print option: p
May be extended to output BIND files'''

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
   thing = {zone: []}
   z = json.loads(record)
   for r in z['records']:
      domain = r['domain']
      rec_type = r['type']
      ttl = r['ttl']
      answers = r['short_answers']
      thing[zone].append({'domain': domain, 'type': rec_type, 'ttl': ttl, 'answers': answers})
   big_dic.update(thing)

if sys.argv[2] == 'j':
   print(json.dumps(big_dic))
elif sys.argv[2] == 'p':
   for y in zone_list:
      print('\nZone:   ' + y + '\n')
      for x in big_dic[y]:
         print('    Record:   ' + x['domain'])
         print('      Type:   ' + x['type'])
         print('       TTL:   ' + str(x['ttl']))
         for w in x['answers']:
            print('    Answer:   ' + w)
         print('\n')
elif sys.argv[2] == 'c':
    print "zone, record, type, ttl, answer\n"
    for y in zone_list:
        for x in big_dic[y]:
            for w in x['answers']:
                print "%s, %s, %s, %s, %s" % (y, x['domain'], x['type'], str(x['ttl']), w)
else:
   print('Unrecognized option: ' + sys.argv[2])

