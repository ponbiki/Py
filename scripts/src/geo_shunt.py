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


class MongoShunt(object):

    def __init__(self):
        client = MongoClient()
        db = client[database]
        self.__gs = db[collection]
        self.__results = []
        self.ver = ''
        self.__search_param = {}
        self.shunt = {}

    def find_ip4(self, ip_addr):
        rgx = r'.*' + re.escape(ip_addr) + '.*'
        reg = re.compile(rgx)
        for shunt in list(self.__gs.find({'prefixes': reg})):
            self.__results.append(shunt)

    @property
    def shunt(self):
        self.__shunt

    @shunt.setter
    def shunt(self, selected_shunt):
        self.shunt = selected_shunt

    @property
    def search_param(self):
        pass

    @search_param.setter
    def search_param(self, param):
        self.__search_param = param

    @property
    def ver(self):
        return self.__ver

    @ver.setter
    def ver(self, ver_in):
        if ver_in == "4":
            self.ver = "ipv4"
        elif ver_in == "6":
            self.ver = "ipv6"
        else:
            print("Invalid Protocol")
            exit()

    def matches_list(self):
        if len(self.__results) > 1:
            self.select_shunt()
        else:
            self.shunt = self.__results[0]

    def select_shunt(self):
        pass


def main():
    x = MongoShunt()
    x.ver = sys.argv[1]
    x.find_ip4(sys.argv[2])
    pprint(x.results)


if __name__ == '__main__':
    sys.exit(main())
