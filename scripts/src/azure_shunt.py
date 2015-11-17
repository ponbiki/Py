#!/usr/bin/python

import xmltodict
from pprint import pprint

with open('PublicIPs_20151109.xml') as fd:
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
pprint(holder)
