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
from collections import defaultdict

INTERVAL = 30
PARAMS = [iptc.Table.FILTER, iptc.Table.NAT, iptc.Table.MANGLE, iptc.Table.RAW]
PARAMS6 = [iptc.Table6.FILTER, iptc.Table6.MANGLE, iptc.Table6.RAW, iptc.Table6.SECURITY]

counter_holder = defaultdict(lambda: 0)


def collect_metrics():
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
    for param in PARAMS:
        thyme = int(time.time())
        table = iptc.Table(param)
        table.refresh()
        for chain in table.chains:
            pkt_accept_count = 0
            byt_accept_count = 0
            pkt_mark_count = 0
            byt_mark_count = 0
            pkt_drop_count = 0
            byt_drop_count = 0
            if re.match(r'^NS1', chain.name):
                p = chain.name.split('_')
                chainz = str(p[0] + '_' + p[1]).lower()
            else:
                chainz = str(chain.name).lower()
            for rule in chain.rules:
                if re.match(r'^NS1', rule.target.name):
                    p = rule.target.name.split('_')
                    rule_tgt_name = str(p[0] + '_' + p[1]).lower()
                else:
                    rule_tgt_name = str(rule.target.name).lower()
                (packets, bytes) = rule.get_counters()
                if rule_tgt_name == 'accept':
                    if packets - counter_holder[str(param).lower() + '_accept_packets_v4_' + chainz] < 0:
                        pkt_accept_count += packets
                    else:
                        pkt_accept_count += packets - counter_holder[str(param).lower() + '_accept_packets_v4_' + chainz]
                    counter_holder[str(param).lower() + '_accept_packets_v4_' + chainz] = packets
                    if bytes - counter_holder[str(param).lower() + '_accept_bytes_v4_' + chainz] < 0:
                        byt_accept_count += bytes
                    else:
                        byt_accept_count += bytes - counter_holder[str(param).lower() + '_accept_bytes_v4_' + chainz]
                    counter_holder[str(param).lower() + '_accept_bytes_v4_' + chainz] = bytes
                elif rule_tgt_name == 'mark':
                    if packets - counter_holder[str(param).lower() + '_mark_packets_v4_' + chainz] < 0:
                        pkt_mark_count += packets
                    else:
                        pkt_mark_count += packets - counter_holder[str(param).lower() + '_mark_packets_v4_' + chainz]
                    counter_holder[str(param).lower() + '_mark_packets_v4_' + chainz] = packets
                    if bytes - counter_holder[str(param).lower() + '_mark_bytes_v4_' + chainz] < 0:
                        byt_mark_count += bytes
                    else:
                        byt_mark_count += bytes - counter_holder[str(param).lower() + '_mark_bytes_v4_' + chainz]
                    counter_holder[str(param).lower() + '_mark_bytes_v4_' + chainz] = bytes
                elif rule_tgt_name == 'drop':
                    if packets - counter_holder[str(param).lower() + '_drop_packets_v4_' + chainz] < 0:
                        pkt_drop_count += packets
                    else:
                        pkt_drop_count += packets - counter_holder[str(param).lower() + '_drop_packets_v4_' + chainz]
                    counter_holder[str(param).lower() + '_drop_packets_v4_' + chainz] = packets
                    if bytes - counter_holder[str(param).lower() + '_drop_bytes_v4_' + chainz] < 0:
                        byt_drop_count += bytes
                    else:
                        byt_drop_count += bytes - counter_holder[str(param).lower() + '_drop_bytes_' + chainz]
                    counter_holder[str(param).lower() + '_drop_bytes_v4_' + chainz] = bytes
                else:
                    pass
                for match in rule.matches:
                    if match.name == 'comment':
                        if re.match(r'^tcollector:.*', match.parameters["comment"], re.IGNORECASE):
                            cmnt = match.parameters["comment"].split(':')[1].strip().split()[0]
                            print 'iptables.%s.rules.%s.%s %d %d protocol=%s' % (str(param).lower(), cmnt, 'packets', thyme, packets, 'IPv4')
                            print 'iptables.%s.rules.%s.%s %d %d protocol=%s' % (str(param).lower(), cmnt, 'bytes', thyme, bytes, 'IPv4')
                        else:
                            pass
                    else:
                        pass
            print 'iptables.%s.%s.%s %d %d chain=%s protocol=%s' % (str(param).lower(), 'accept', 'packets', thyme, pkt_accept_count, chainz, 'IPv4')
            print 'iptables.%s.%s.%s %d %d chain=%s protocol=%s' % (str(param).lower(), 'accept', 'bytes', thyme, byt_accept_count, chainz, 'IPv4')
            print 'iptables.%s.%s.%s %d %d chain=%s protocol=%s' % (str(param).lower(), 'mark', 'packets', thyme, pkt_mark_count, chainz, 'IPv4')
            print 'iptables.%s.%s.%s %d %d chain=%s protocol=%s' % (str(param).lower(), 'mark', 'bytes', thyme, byt_mark_count, chainz, 'IPv4')
            print 'iptables.%s.%s.%s %d %d chain=%s protocol=%s' % (str(param).lower(), 'drop', 'packets', thyme, pkt_drop_count, chainz, 'IPv4')
            print 'iptables.%s.%s.%s %d %d chain=%s protocol=%s' % (str(param).lower(), 'drop', 'bytes', thyme, byt_drop_count, chainz, 'IPv4')

    for param6 in PARAMS6:
        thyme = int(time.time())
        table = iptc.Table6(param6)
        table.refresh()
        for chain in table.chains:
            pkt_accept_count = 0
            byt_accept_count = 0
            pkt_mark_count = 0
            byt_mark_count = 0
            pkt_drop_count = 0
            byt_drop_count = 0
            if re.match(r'^NS1', chain.name):
                p = chain.name.split('_')
                chainz = str(p[0] + '_' + p[1]).lower()
            else:
                chainz = str(chain.name).lower()
            for rule in chain.rules:
                if re.match(r'^NS1', rule.target.name):
                    p = rule.target.name.split('_')
                    rule_tgt_name = str(p[0] + '_' + p[1]).lower()
                else:
                    rule_tgt_name = str(rule.target.name).lower()
                (packets, bytes) = rule.get_counters()
                if rule_tgt_name == 'accept':
                    if packets - counter_holder[str(param6).lower() + '_accept_packets_v6_' + chainz] < 0:
                        pkt_accept_count += packets
                    else:
                        pkt_accept_count += packets - counter_holder[str(param6).lower() + '_accept_packets_v6_' + chainz]
                    counter_holder[str(param6).lower() + '_accept_packets_v6_' + chainz] = packets
                    if bytes - counter_holder[str(param6).lower() + '_accept_bytes_v6_' + chainz] < 0:
                        byt_accept_count += bytes
                    else:
                        byt_accept_count += bytes - counter_holder[str(param6).lower() + '_accept_bytes_v6_' + chainz]
                    counter_holder[str(param6).lower() + '_accept_bytes_v6_' + chainz] = bytes
                elif rule_tgt_name == 'mark':
                    if packets - counter_holder[str(param6).lower() + '_mark_packets_v6_' + chainz] < 0:
                        pkt_mark_count += packets
                    else:
                        pkt_mark_count += packets - counter_holder[str(param6).lower() + '_mark_packets_v6_' + chainz]
                    counter_holder[str(param6).lower() + '_mark_packets_v6_' + chainz] = packets
                    if bytes - counter_holder[str(param6).lower() + '_mark_bytes_v6_' + chainz] < 0:
                        byt_mark_count += bytes
                    else:
                        byt_mark_count += bytes - counter_holder[str(param6).lower() + '_mark_bytes_v6_' + chainz]
                    counter_holder[str(param6).lower() + '_mark_bytes_v6_' + chainz] = bytes
                elif rule_tgt_name == 'drop':
                    if packets - counter_holder[str(param6).lower() + '_drop_packets_v6_' + chainz] < 0:
                        pkt_drop_count += packets
                    else:
                        pkt_drop_count += packets - counter_holder[str(param6).lower() + '_drop_packets_v6_' + chainz]
                    counter_holder[str(param6).lower() + '_drop_packets_v6_' + chainz] = packets
                    if bytes - counter_holder[str(param6).lower() + '_drop_bytes_v6_' + chainz] < 0:
                        byt_drop_count += bytes
                    else:
                        byt_drop_count += bytes - counter_holder[str(param6).lower() + '_drop_bytes_v6_' + chainz]
                    counter_holder[str(param6).lower() + '_drop_bytes_v6_' + chainz] = bytes
                else:
                    pass
                for match in rule.matches:
                    if match.name == 'comment':
                        if re.match(r'^tcollector:.*', match.parameters["comment"], re.IGNORECASE):
                            cmnt = match.parameters["comment"].split(':')[1].strip().split()[0]
                            print 'iptables.%s.rules.%s.%s %d %d protocol=%s' % (str(param).lower(), cmnt, 'packets', thyme, packets, 'IPv6')
                            print 'iptables.%s.rules.%s.%s %d %d protocol=%s' % (str(param).lower(), cmnt, 'bytes', thyme, bytes, 'IPv6')
                        else:
                            pass
                    else:
                        pass
            print 'iptables.%s.%s.%s %d %d chain=%s protocol=%s' % (str(param).lower(), 'accept', 'packets', thyme, pkt_accept_count, chainz, 'IPv6')
            print 'iptables.%s.%s.%s %d %d chain=%s protocol=%s' % (str(param).lower(), 'accept', 'bytes', thyme, byt_accept_count, chainz, 'IPv6')
            print 'iptables.%s.%s.%s %d %d chain=%s protocol=%s' % (str(param).lower(), 'mark', 'packets', thyme, pkt_mark_count, chainz, 'IPv6')
            print 'iptables.%s.%s.%s %d %d chain=%s protocol=%s' % (str(param).lower(), 'mark', 'bytes', thyme, byt_mark_count, chainz, 'IPv6')
            print 'iptables.%s.%s.%s %d %d chain=%s protocol=%s' % (str(param).lower(), 'drop', 'packets', thyme, pkt_drop_count, chainz, 'IPv6')
            print 'iptables.%s.%s.%s %d %d chain=%s protocol=%s' % (str(param).lower(), 'drop', 'bytes', thyme, byt_drop_count, chainz, 'IPv6')


def main():
    while True:
        collect_metrics()
        sys.stdout.flush()
        if not INTERVAL or INTERVAL < 1:
            break
        else:
            time.sleep(INTERVAL)

if __name__ == '__main__':
    sys.exit(main())
