#!/usr/bin/python

import xmltodict
import json
import pycurl
from pprint import pprint


class Ripper():
    def __init__(self, file_name):
        '''loads akamai XML configuration file and loads it into manageable dicts'''
        with open(file_name) as xd:
            xmlobj = xmltodict.parse(xd.read())
        obj = xmlobj['configs']['edge-config']
        self.domain_name = obj['domain']['@name']
        self.token = obj['domain']['token']
        self.email_notification = obj['domain']['email-notification']
        self.max_imbalance = obj['domain']['max-imbalance']
        self.load_monitoring_status = obj['domain']['load-monitoring.status']
        self.data_centers = []
        for dc in obj['domain']['datacenter']:
            dc_dict = {"nickname": dc['nickname'],
                       "editable": dc['editable'],
                       "score_penalty": ['score-penalty'],
                       "city": dc['city'],
                       "state": dc['state-or-province'],
                       "country": dc['country'],
                       "latitude": dc['latitude'],
                       "longitude": dc['longitude']}            
            self.data_centers.append({dc['@name']: dc_dict})
        self.properties = []
        for prop in obj['domain']['property']:
            prop_dict = {"comments": prop['comments'],
                         "map_type": prop['map.type']}
            self.properties.append({prop['@name']: prop_dict})


tester = Ripper('e.xx.openx.com.akadns.net.xsd')

pprint(tester.properties)