#!/usr/bin/env python

from pprint import pprint
from pymongo import MongoClient
from bson.objectid import ObjectId

holder = {}

with open("client_2016.txt") as fl:
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
collection = db.df

for key in holder:
    try:
        doc = collection.find_one({"_id": ObjectId(key)})
    except Exception as e:
        print "Couldn't load document for %s:\n %s" % (key, e)
        continue
    new_dest = []
    removed = []
    original = 0
    deleted = 0
    for dest in doc['destinations']:
        original += 1
        if (str(dest['record']) not in holder[key]) or (dest['desttype'] != "answer"):
            print "data_feed %s Saving:" % key
            pprint(dest)
            new_dest.append(dest)
        else:
            print "data_feed %s Deleting:" % key
            pprint(dest)
            deleted += 1
            removed.append(dest)
    pprint(new_dest)
    del doc['destinations']
    doc['destinations'] = new_dest
    collection.save(doc)
    print "\n\n================================================================="
    print "There were %d destinations in %s to start" % (original, key)
    print "The following %d destinations were removed from %s, leaving %d destinations\n" % (deleted, key, original-deleted)
    for rem in removed:
        pprint(rem)