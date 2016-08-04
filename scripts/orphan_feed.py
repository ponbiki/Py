#!/usr/bin/env python

from pymongo import MongoClient
from bson.objectid import ObjectId

feed_id = "read in from file"
record_id = "read in from file"

client = MongoClient('mongodb://xxx:xxx@localhost:27017/xxx')
collection = db.data_feeds
doc = collection.find_one({"_id":ObjectId(feed_id)})
new_dest
for dest in doc['destinations']:
    if dest['record'] != ObjectId(record_id):
        new_dest.append(dest)
del doc['destinations']
doc['destinations'] = new_dest