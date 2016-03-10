#!/usr/bin/env python

import re
import sys
import json
from pymongo import MongoClient
from pprint import pprint

database = 'test'
collection = 'geo_shunts'
with open('states.json') as fd:
    states = json.loads(fd.read())
with open('countries.json') as fd:
    countries = json.loads(fd.read())

pprint(states)
pprint(countries)


class MongoShunt:

    def __init__(self):
        client = MongoClient()
        db = client[database]
        self.gs = db[collection]
        self.results = []
        self.__ver = ''

    def find_ip4(self, ip_addr):
        rgx = r'.*' + re.escape(ip_addr) + '.*'
        reg = re.compile(rgx)
        for shunt in list(self.gs.find({'prefixes': reg})):
            self.results.append(shunt)

    @property
    def ver(self):
        return self.__ver

    @ver.setter
    def ver(self, ver_in):
        if ver_in == "4":
            self.__ver = "ipv4"
        elif ver_in == "6":
            self.__ver = "ipv6"
        else:
            return "Invalid Protocol"
            exit()



def main():
    x = MongoShunt()
    x.ver = sys.argv[1]
    x.find_ip4(sys.argv[2])
    pprint(x.results)


if __name__ == '__main__':
    sys.exit(main())
