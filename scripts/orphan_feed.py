#!/usr/bin/env python

from pprint import pprint
from pymongo import MongoClient
from bson.objectid import ObjectId

holder = {}

with open("/home/ponbiki/Documents/client_2016.txt") as fl:
    for line in fl:
        x = line.rstrip()
        y = x.split()
        if y:
            if y[0] in holder:
                holder[y[0]].append(y[1])
            else:
                holder[y[0]] = [y[1]]

client = MongoClient('mongodb://***:***@localhost:27017')
db = client['***']
collection = db.d_feeds

for key in holder:
    try:
        doc = collection.find_one({"_id": ObjectId(key)})
    except:
        pass
    new_dest = []
    removed = []
    original = 0
    deleted = 0
    for dest in doc['destinations']:
        original += 1
        if str(dest['record']) not in holder[key]:
            new_dest.append(dest)
        else:
            deleted += 1
            removed.append(dest)
    del doc['destinations']
    doc['destinations'] = new_dest
    collection.save(doc)
    print "\n\n================================================================="
    print "There were %d destinations in %s to start" % (original, key)
    print "The following %d destinations were removed from %s, leaving %d destinations\n" % (deleted, key, original-deleted)
    for rem in removed:
        pprint(rem)


# cat <file> |cut -d" " -f 4-5| awk '{ print $1 " "$2 }' | cut -c6-29,31-31,36-
