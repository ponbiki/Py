#!/usr/bin/python

import json
import xmltodict

with open('PublicIPs_20151109.xml') as fd: # http://www.microsoft.com/en-us/download/confirmation.aspx?id=41653
   obj = xmltodict.parse(fd.read())

holder = []
x = 0
for range in obj['AzurePublicIpAddresses']['Region']:
   name = range['@Name']
   holder.append({name: []})
   x += 1
   for ip in range['IpRange']:
      subnet = ip['@Subnet']
      holder[x-1][name].append(subnet)

with open('azure_region.json') as az: # referenced https://azure.microsoft.com/en-us/regions/
   template = json.loads(az.read())

ip_list = []
for region in holder:
   ip_region = region.keys()
   for reg in ip_region:
      for ip in region[reg]:
         ip_list.append({ip: ip_region[0]})

shunt_list = []
for sub in ip_list:
   snkey = sub.keys()[0]
   data = sub.values()[0]
   shunt = template[data]
   shuntjs = {snkey: shunt}
   print("  " + (json.dumps(shuntjs))[1:-1] + ",")
