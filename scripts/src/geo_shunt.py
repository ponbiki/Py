#!/usr/bin/env python

import re
import sys
from pymongo import MongoClient

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
        for shunt in list(self.gs.find(ip_addr)):
            self.results.append(shunt)

    def search(self, ver):
        if ver == "4":
            self.ver = "ipv4"
        elif ver == "6":
            self.ver = "ipv6"


def main():
    x = MongoShunt()
    srch = sys.argv[1]
    rgx = r'.*' + re.escape(srch) + '.*'
    reg = re.compile(rgx)
    x.find_ip4({'prefixes':reg})


if __name__ == '__main__':
    sys.exit(main())

