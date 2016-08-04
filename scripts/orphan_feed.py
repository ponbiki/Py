#!/usr/bin/env python

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

client = MongoClient('mongodb://xxx:xxx@localhost:27017')
db = client['xxx']
collection = db.data_feeds

for key, value in holder:
    doc = collection.find_one({"_id":ObjectId(key)})
    new_dest = []
    for dest in doc['destinations']:
        if dest['record'] not in value:
            new_dest.append(dest)
    del doc['destinations']
    doc['destinations'] = new_dest
    db.save(doc)

# cat <file> |cut -d" " -f 4-5| awk '{ print $1 " "$2 }' | cut -c6-29,31-31,36-
