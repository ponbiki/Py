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
                       "score_penalty": dc['score-penalty'],
                       "city": dc['city'],
                       "state": dc['state-or-province'],
                       "country": dc['country'],
                       "latitude": dc['latitude'],
                       "longitude": dc['longitude']}            
            self.data_centers.append({dc['@name']: dc_dict})
        self.properties = []
        for prop in obj['domain']['property']:
            ass_list = []
            for ass in prop['assignment']:
                ass_name = ass['@name']
                ass_dict = {"status": ass['status'],
                            "traffic_weight": ass['traffic-weight'],
                            "servers": ass['servers']} # may require another for loop(does this take multiples?)
                ass_list.append({ass_name: ass_dict})
            if 'liveness-test' in prop:
                test_type = prop['liveness-test']['@name']
                test_dict = {"test_type": test_type,
                             "test_interval": prop['liveness-test']['test.interval'],
                             "test_timeout": prop['liveness-test']['test.timeout'],
                             "test_protocol": prop['liveness-test']['test.protocol'],
                             "test_port": prop['liveness-test']['test.port'],
                             "test_object": prop['liveness-test']['test.object'],
                             "test_suppress_warn": prop['liveness-test']['test.suppress-non-standard-port-warnings'],
                             "test_password": prop['liveness-test']['test.password'],
                             "test_username": prop['liveness-test']['test.username'],
                             "test_host_header": prop['liveness-test']['test.http.use-host-header'],
                             "test_fail_code": prop['liveness-test']['test.http.failures-codes']}
            else:
                test_dict = {"test_type": "none"}
            prop_dict = {"comments": prop['comments'],
                         "map_type": prop['map.type'],
                         "ttl": prop['ttl'],
                         "cname": prop['cname'], # probably will need a key grab on this to get type, but only one example to go on
                         "failover_delay": prop['failover-delay'],
                         "failback_delay": prop['failback-delay'],
                         "persistent_assignment": prop['persistent-assignment'],
                         "load_imbalance_factor": prop['load-imbalance-factor'],
                         "dca_threshold_percent": prop['dca-threshold-percent'],
                         "dca_threshold_constant": prop['dca-threshold-constant'],
                         "assignments": ass_list,
                         "test": test_dict}
            self.properties.append({prop['@name']: prop_dict})

tester = Ripper('e.xx.openx.com.akadns.net.xsd')

pprint(tester.properties)