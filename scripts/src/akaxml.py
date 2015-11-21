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





tester = Ripper('e.xx.openx.com.akadns.net.xsd')

pprint(dir(tester))