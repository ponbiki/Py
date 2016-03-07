#!/usr/bin/env python

import re
import sys
from pymongo import MongoClient
from pprint import pprint

database = 'test'
collection = 'xxxx'


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

    def search(self, ver):
        if ver == "4":
            self.ver = "ipv4"
        elif ver == "6":
            self.ver = "ipv6"
        else:
            print("Invalid Protocol")
            exit()


def main():
    x = MongoShunt()
    x.find_ip4(sys.argv[1])
    pprint(x.results)


if __name__ == '__main__':
    sys.exit(main())

