#!/usr/bin/env python
#
# iptables_stat.py -- a collector for tcollector/OpenTSDB
# Copyright (C) 2016 NSONE, Inc.
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at your
# option) any later version.  This program is distributed in the hope that it
# will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty
# of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser
# General Public License for more details.  You should have received a copy
# of the GNU Lesser General Public License along with this program.  If not,
# see <http://www.gnu.org/licenses/>.

'''IPTables statistics collector'''

import time
import iptc
import re
import sys

INTERVAL = 30
PARAMS = [iptc.Table.FILTER, iptc.Table.NAT, iptc.Table.MANGLE, iptc.Table.RAW]
PARAMS6 = [iptc.Table6.FILTER, iptc.Table6.MANGLE, iptc.Table6.RAW, iptc.Table6.SECURITY]

try:
    from collectors.etc.iptables_stat import *
except ImportError:
    pass

# We no longer clear counters, so this holds the last value seen
counter_holder = {}
ipv6_counter_holder = {}
ipv4_cmnt_counter_holder = {}
ipv6_cmnt_counter_holder = {}


class IPTablesCollector(object):

    def __init__(self):
        self.iterations = 0

    def collect_metrics(self):
        '''
        Using python-iptables, this steps recursively through each table->chain->rule
        It aggregates the packet and byte counts for each rule in a chain that hits an
        accept, mark, or drop rule, and then returns the data for each one in the format of:

        iptables.<table>.<accept|mark|drop>.<packets|bytes> <timestamp> <cnt> chain=<chain> protocol=<IPv6|IPv4>

        There is also a per rule recursion that returns the packet and byte counts for
        any rule containing a comment beginning with "tcollector:" and returns the
        data for each matched rule in the format of:

        iptables.<table>.rules.<rule_marker>.<packets|bytes> <timestamp> <cnt> protocol=<IPv6|IPv4>
        '''

        thyme = int(time.time())

        #  Cleans counter dict once a week to prevent a growing memory leak
        if self.iterations >= 302400:
            counter_holder.clear()
            ipv6_counter_holder.clear()
            ipv4_cmnt_counter_holder.clear()
            ipv6_cmnt_counter_holder.clear()
            self.iterations = 0

        for param in PARAMS:
            table = iptc.Table(param)
            table.refresh()
            ipv4_cmnt = {}
            ipv4_cmnt_diff = {}
            ipv4_metric = {}
            ipv4_metric_diff = {}
            ipv4_metric_print = {}
            for chain in table.chains:
                chainz = str(chain.name).lower()
                for rule in chain.rules:
                    (packets, bytes) = rule.get_counters()
                    rule_tgt_name = str(rule.target.name).lower()
                    if re.match(r'^ns1', rule_tgt_name):
                        s = rule_tgt_name.split('_')
                        if re.match(r'\d{10}', s[-1]):
                            s.pop()
                            s.append('timestamp')
                            rule_tgt_name = '_'.join(s).lower()

                    metric_key = 'iptables.%s.%s-%s' % (param.lower(), rule_tgt_name, chainz)
                    if metric_key in ipv4_metric.keys():
                        ipv4_metric[metric_key]['packets'] += packets
                        ipv4_metric[metric_key]['bytes'] += bytes
                    else:
                        ipv4_metric[metric_key] = {'packets': packets, 'bytes': bytes}

                    for match in rule.matches:
                        if match.name == 'comment':
                            if re.match(r'^tcollector:.*', match.parameters['comment'], re.IGNORECASE):
                                cmnt = match.parameters['comment'].split(':')[1].strip().split()[0]
                                cmnt_key = 'iptables.%s.rules.%s' % (param.lower(), cmnt)
                                if cmnt_key in ipv4_cmnt.keys():
                                    ipv4_cmnt[cmnt_key]['packets'] += packets
                                    ipv4_cmnt[cmnt_key]['bytes'] += bytes
                                else:
                                    ipv4_cmnt[cmnt_key] = {'packets': packets, 'bytes': bytes}

                for key in ipv4_metric.keys():
                    if key in counter_holder.keys():
                        if ipv4_metric[key]['packets'] >= counter_holder[key]['packets']:
                            ipv4_metric_diff[key] = {'packets': ipv4_metric[key]['packets'] -
                                                     counter_holder[key]['packets'],
                                                     'bytes': ipv4_metric[key]['bytes'] -
                                                     counter_holder[key]['bytes']}
                            counter_holder[key]['packets'] = ipv4_metric[key]['packets']
                            counter_holder[key]['bytes'] = ipv4_metric[key]['bytes']
                        else:
                            counter_holder[key] = {'packets': ipv4_metric[key]['packets'],
                                                   'bytes': ipv4_metric[key]['bytes']}
                    else:
                        counter_holder[key] = {'packets': ipv4_metric[key]['packets'],
                                               'bytes': ipv4_metric[key]['bytes']}

                for key in ipv4_metric_diff.keys():
                    pcs = key.split('-')
                    if re.match(r'^ns1', pcs[1]):
                        p = pcs[-1].split('_')
                        if re.match(r'\d{10}', p[-1]):
                            p.pop()
                            p.append('timestamp')
                            new_end = '_'.join(p).lower()
                            pcs.pop()
                            pcs.append(new_end)
                            new_key = '-'.join(pcs).lower()
                        else:
                            new_key = key
                    else:
                        new_key = key

                    if new_key in ipv4_metric_print.keys():
                        ipv4_metric_print[new_key]['packets'] += ipv4_metric_diff[key]['packets']
                        ipv4_metric_print[new_key]['bytes'] += ipv4_metric_diff[key]['bytes']
                    else:
                        ipv4_metric_print[new_key] = {'packets': ipv4_metric_diff[key]['packets'],
                                                      'bytes': ipv4_metric_diff[key]['bytes']}

            if self.iterations > 0:
                for i in ipv4_metric_print:
                    print '%s.packets %d %d chain=%s protocol=IPv4' % (i.split('-')[0], thyme,
                                                                       ipv4_metric_print[i]['packets'], i.split('-')[1])
                    print '%s.bytes %d %d chain=%s protocol=IPv4' % (i.split('-')[0], thyme,
                                                                     ipv4_metric_print[i]['bytes'], i.split('-')[1])

            for key in ipv4_cmnt.keys():
                if key in ipv4_cmnt_counter_holder.keys():
                    if ipv4_cmnt[key]['packets'] >= ipv4_cmnt_counter_holder[key]['packets']:
                        ipv4_cmnt_diff[key] = {'packets': ipv4_cmnt[key]['packets'] -
                                               ipv4_cmnt_counter_holder[key]['packets'],
                                               'bytes': ipv4_cmnt[key]['bytes'] -
                                               ipv4_cmnt_counter_holder[key]['bytes']}
                        ipv4_cmnt_counter_holder[key]['packets'] = ipv4_cmnt[key]['packets']
                        ipv4_cmnt_counter_holder[key]['bytes'] = ipv4_cmnt[key]['bytes']
                    else:
                        ipv4_cmnt_counter_holder[key] = {'packets': ipv4_cmnt[key]['packets'],
                                                         'bytes': ipv4_cmnt[key]['bytes']}

                else:
                    ipv4_cmnt_counter_holder[key] = {'packets': ipv4_cmnt[key]['packets'],
                                                     'bytes': ipv4_cmnt[key]['bytes']}

                if self.iterations > 0 and key in ipv4_cmnt_diff.keys():
                    print '%s.packets %d %d protocol=IPv4' % (key, thyme, ipv4_cmnt_diff[key]['packets'])
                    print '%s.bytes %d %d protocol=IPv4' % (key, thyme, ipv4_cmnt_diff[key]['bytes'])

        for param6 in PARAMS6:
            table = iptc.Table6(param6)
            table.refresh()
            ipv6_cmnt = {}
            ipv6_cmnt_diff = {}
            ipv6_metric = {}
            ipv6_metric_diff = {}
            ipv6_metric_print = {}
            for chain in table.chains:
                chainz = str(chain.name).lower()
                for rule in chain.rules:
                    (packets, bytes) = rule.get_counters()
                    rule_tgt_name = str(rule.target.name).lower()
                    if re.match(r'^ns1', rule_tgt_name):
                        s = rule_tgt_name.split('_')
                        if re.match(r'\d{10}', s[-1]):
                            s.pop()
                            s.append('timestamp')
                            rule_tgt_name = '_'.join(s).lower()

                    metric_key = 'iptables.%s.%s-%s' % (param6.lower(), rule_tgt_name, chainz)
                    if metric_key in ipv6_metric.keys():
                        ipv6_metric[metric_key]['packets'] += packets
                        ipv6_metric[metric_key]['bytes'] += bytes
                    else:
                        ipv6_metric[metric_key] = {"packets": packets, "bytes": bytes}

                    for match in rule.matches:
                        if match.name == 'comment':
                            if re.match(r'^tcollector:.*', match.parameters['comment'], re.IGNORECASE):
                                cmnt = match.parameters['comment'].split(':')[1].strip().split()[0]
                                cmnt_key = 'iptables.%s.rules.%s' % (param6.lower(), cmnt)
                                if cmnt_key in ipv6_cmnt.keys():
                                    ipv6_cmnt[cmnt_key]['packets'] += packets
                                    ipv6_cmnt[cmnt_key]['bytes'] += bytes
                                else:
                                    ipv6_cmnt[cmnt_key] = {'packets': packets, 'bytes': bytes}

                for key in ipv6_metric.keys():
                    if key in ipv6_counter_holder.keys():
                        if ipv6_metric[key]['packets'] >= ipv6_counter_holder[key]['packets']:
                            ipv6_metric_diff[key] = {'packets': ipv6_metric[key]['packets'] -
                                                     ipv6_counter_holder[key]['packets'],
                                                     'bytes': ipv6_metric[key]['bytes'] -
                                                     ipv6_counter_holder[key]['bytes']}
                            ipv6_counter_holder[key]['packets'] = ipv6_metric[key]['packets']
                            ipv6_counter_holder[key]['bytes'] = ipv6_metric[key]['bytes']
                        else:
                            ipv6_counter_holder[key] = {'packets': ipv6_metric[key]['packets'],
                                                        'bytes': ipv6_metric[key]['bytes']}
                    else:
                        ipv6_counter_holder[key] = {'packets': ipv6_metric[key]['packets'],
                                                    'bytes': ipv6_metric[key]['bytes']}

                for key in ipv6_metric_diff.keys():
                    pcs = key.split('-')
                    if re.match(r'^ns1', pcs[1]):
                        p = pcs[-1].split('_')
                        if re.match(r'\d{10}', p[-1]):
                            p.pop()
                            p.append('timestamp')
                            new_end = '_'.join(p).lower()
                            pcs.pop()
                            pcs.append(new_end)
                            new_key = '-'.join(pcs).lower()
                        else:
                            new_key = key
                    else:
                        new_key = key

                    if new_key in ipv6_metric_print.keys():
                        ipv6_metric_print[new_key]['packets'] += ipv6_metric_diff[key]['packets']
                        ipv6_metric_print[new_key]['bytes'] += ipv6_metric_diff[key]['bytes']
                    else:
                        ipv6_metric_print[new_key] = {'packets': ipv6_metric_diff[key]['packets'],
                                                      'bytes': ipv6_metric_diff[key]['bytes']}

            if self.iterations > 0:
                for i in ipv6_metric_print:
                    print '%s.packets %d %d chain=%s protocol=IPv6' % (i.split('-')[0], thyme,
                                                                       ipv6_metric_print[i]['packets'], i.split('-')[1])
                    print '%s.bytes %d %d chain=%s protocol=IPv6' % (i.split('-')[0], thyme,
                                                                     ipv6_metric_print[i]['bytes'], i.split('-')[1])

            for key in ipv6_cmnt.keys():
                if key in ipv6_cmnt_counter_holder.keys():
                    if ipv6_cmnt[key]['packets'] >= ipv6_cmnt_counter_holder[key]['packets']:
                        ipv6_cmnt_diff[key] = {'packets': ipv6_cmnt[key]['packets'] -
                                               ipv6_cmnt_counter_holder[key]['packets'],
                                               'bytes': ipv6_cmnt[key]['bytes'] -
                                               ipv6_cmnt_counter_holder[key]['bytes']}
                        ipv6_cmnt_counter_holder[key]['packets'] = ipv6_cmnt[key]['packets']
                        ipv6_cmnt_counter_holder[key]['bytes'] = ipv6_cmnt[key]['bytes']
                    else:
                        ipv6_cmnt_counter_holder[key] = {'packets': ipv6_cmnt[key]['packets'],
                                                         'bytes': ipv6_cmnt[key]['bytes']}

                else:
                    ipv6_cmnt_counter_holder[key] = {'packets': ipv6_cmnt[key]['packets'],
                                                     'bytes': ipv6_cmnt[key]['bytes']}

                if self.iterations > 0 and key in ipv6_cmnt_diff.keys():
                    print '%s.packets %d %d protocol=IPv6' % (key, thyme, ipv6_cmnt_diff[key]['packets'])
                    print '%s.bytes %d %d protocol=IPv6' % (key, thyme, ipv6_cmnt_diff[key]['bytes'])

        self.iterations += 1


def main():
    ip_t = IPTablesCollector()

    while True:
        ip_t.collect_metrics()
        sys.stdout.flush()

        if not INTERVAL or INTERVAL < 1:
            break
        else:
            time.sleep(INTERVAL)

if __name__ == '__main__':
    sys.exit(main())
