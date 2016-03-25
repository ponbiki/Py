#!/usr/bin/env python

import re
import sys
import json
import ipaddress
from pymongo import MongoClient
from pprint import pprint

database = 'test'
collection = 'geo_shunts'
with open('states.json') as fd:
    states = json.loads(fd.read())
with open('countries.json') as fd:
    countries = json.loads(fd.read())
with open('provinces.json') as fd:
    provinces = json.loads(fd.read())


class MongoShunt(object):

    def __init__(self):
        client = MongoClient()
        db = client[database]
        self.__gs = db[collection]
        self.__results = []
        self.ver = ''
        self.__search_param = {}
        self.shunt = {}
        self.country = {}
        self.ipv4_valid = None

    def find_ip4(self, ip_addr):
        rgx = r'.*' + re.escape(ip_addr) + '.*'
        reg = re.compile(rgx)
        for match in list(self.__gs.find({'prefixes': reg})):
            self.__results.append(match)

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
            return "Invalid Protocol"

    @property
    def country(self):
        return self.__country

    @country.setter
    def country(self, cc_in):
        cc_clean = self.cc_validate(cc_in)
        if cc_clean is False:
            return "Invalid Country Code"
        else:
            self.country = {cc_clean: countries[cc_clean]}

    @staticmethod
    def cc_validate(cc_unchecked):
        cc_prepped = cc_unchecked.strip().upper()
        if cc_prepped in countries:
            return cc_prepped
        else:
            return False

    def matches_list(self):
        if len(self.__results) > 1:
            self.select_shunt()
        else:
            self.shunt = self.__results[0]

    def select_shunt(self):
        pass  # will implement

    @staticmethod
    def ipv4_validate(ipv4_in):
        rgx = r'^([01]?[0-9]?[0-9]|2[0-4][0-9]|25[0-5])\.([01]?[0-9]?[0-9]|2[0-4][0-9]|25[0-5])' \
              '\.([01]?[0-9]?[0-9]|2[0-4][0-9]|25[0-5])\.([01]?[0-9]?[0-9]|2[0-4][0-9]|25[0-5])/([0-3]?[0-9])$'
        reg = re.compile(rgx)
        if re.match(reg, ipv4_in) is True:
            try:
                return str(ipaddress.IPv4Interface(unicode(ipv4_in)).network.with_prefixlen)
            except ValueError:
                return "Invalid IPv4 Subnet"
        else:
            return "Invalid IPv4 Subnet"


def main():
    x = MongoShunt()
    x.ver = sys.argv[1]
    x.find_ip4(sys.argv[2])
    pprint(x.results)


if __name__ == '__main__':
    sys.exit(main())

'''
import re
import sys
from pymongo import MongoClient
from pprint import pprint

database = 'test'
collection = 'geo_shunts'


class MongoShunt:

    def __init__(self):
        client = MongoClient()
        db = client[database]
        self.gs = db[collection]
        self.results = []
        self.ver = ''

    def find_ip4(self, ip_addr):
        rgx = r'.*' + re.escape(ip_addr) + '.*'
        reg = re.compile(rgx)
        for shunt in list(self.gs.find({'prefixes': reg})):
            self.results.append(shunt)

    def ver_set(self, ver):
        if ver == "4":
            self.ver = "ipv4"
        elif ver == "6":
            self.ver = "ipv6"
        else:
            print("Invalid Protocol")
            exit()


def main():
    x = MongoShunt()
    x.ver_set(sys.argv[1])
    x.find_ip4(sys.argv[2])
    pprint(x.results)


if __name__ == '__main__':
    sys.exit(main())
'''