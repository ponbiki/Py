#!/usr/bin/env python

import re
import sys
from pymongo import MongoClient

database = 'test'
collection = 'xxxx'

class mongoShunt:

    def __init__(self):
        client = MongoClient()
        db = client.database
        mongoShunt.gs = db.collection

    def findIp4(self, ip_addr):
        mongoShunt.results = []
        for shunt in mongoShunt.gs.find(ip_addr):
            mongoShunt.results.append(shunt)

    def search(self, ver):
        if ver == "4":
            mongoShunt.ver = "ipv4"
        elif ver == "6":
            mongoShunt.ver = "ipv6"

def main():
    x = mongoShunt()
    srch = sys.argv[1]
    rgx = r'.*' + re.escape(srch) + '.*'
    reg = re.compile(rgx)
    x.findIp4({'prefixes':reg})


if __name__ == '__main__':
    sys.exit(main())

