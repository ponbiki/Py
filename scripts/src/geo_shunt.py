#!/usr/bin/env python

import re
import sys
from pymongo import MongoClient

database = 'test'
collection = 'xxxx'


class MongoShunt:

    def __init__(self):
        client = MongoClient()
        db = client.database
        MongoShunt.gs = db.collection

    def find_ip4(self, ip_addr):
        MongoShunt.results = []
        for shunt in MongoShunt.gs.find(ip_addr):
            MongoShunt.results.append(shunt)

    def search(self, ver):
        if ver == "4":
            MongoShunt.ver = "ipv4"
        elif ver == "6":
            MongoShunt.ver = "ipv6"


def main():
    x = MongoShunt()
    srch = sys.argv[1]
    rgx = r'.*' + re.escape(srch) + '.*'
    reg = re.compile(rgx)
    x.find_ip4({'prefixes':reg})


if __name__ == '__main__':
    sys.exit(main())

