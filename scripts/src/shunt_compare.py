#!/usr/bin/python

# Compares new list of json shunts
# to existing and builds a list of any duplication

from pprint import pprint

new_shunt_file = 'azure.json' # new list
production_shunt_file = 'geo_shunts.json'  # production list

new_list = []
with open(new_shunt_file, 'r') as f:
   for line in f:
      new_list.append(line.split(None, 1)[0])

comp_list = []
with open(production_shunt_file, 'r') as g:
   for lines in g:
      if len(lines) > 1:
         comp_list.append(lines.split(None, 1)[0])

exist_list = []
for ip in new_list:
   for inpr in comp_list:
      if ip == inpr:
         exist_list.append(ip)

pprint(exist_list)
