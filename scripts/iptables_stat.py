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

        if self.iterations < 1:
            pass
        else:
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
                            pkt_accept_count += packets
                            byt_accept_count += bytes
                        else:
                            pass
                        if rule_tgt_name == 'mark':
                            pkt_mark_count += packets
                            byt_mark_count += bytes
                        else:
                            pass
                        if rule_tgt_name == 'drop':
                            pkt_drop_count += packets
                            byt_drop_count += bytes
                        else:
                            pass
                        for match in rule.matches:
                            if match.name == 'comment':
                                if re.match(r'^tcollector:.*', match.parameters["comment"], re.IGNORECASE):
                                    cmnt = match.parameters["comment"].split(':')[1].strip().split()[0]
                                    if packets >= counter_holder['ipv4_last_pkt_' + cmnt + '_count_' + chainz + '_' + str(param).lower()]:
                                        cmnt_pkt = packets - counter_holder['ipv4_last_pkt_' + cmnt + '_count_' + chainz + '_' + str(param).lower()]
                                    else:
                                        cmnt_pkt = packets
                                    counter_holder['ipv4_last_pkt_' + cmnt + '_count_' + chainz + '_' + str(param).lower()] = cmnt_pkt + counter_holder['ipv4_last_pkt_' + cmnt + '_count_' + chainz + '_' + str(param).lower()]
                                    if bytes >= counter_holder['ipv4_last_byt_' + cmnt + '_count_' + chainz + '_' + str(param).lower()]:
                                        cmnt_byt = bytes - counter_holder['ipv4_last_byt_' + cmnt + '_count_' + chainz + '_' + str(param).lower()]
                                    else:
                                        cmnt_byt = bytes
                                    counter_holder['ipv4_last_byt_' + cmnt + '_count_' + chainz + '_' + str(param).lower()] = cmnt_byt + counter_holder['ipv4_last_pkt_' + cmnt + '_count_' + chainz + '_' + str(param).lower()]
                                    print 'iptables.%s.rules.%s.%s %d %d protocol=%s' % (str(param).lower(), cmnt, 'packets', thyme, cmnt_pkt, 'IPv4')
                                    print 'iptables.%s.rules.%s.%s %d %d protocol=%s' % (str(param).lower(), cmnt, 'bytes', thyme, cmnt_byt, 'IPv4')
                                else:
                                    pass
                            else:
                                pass
                    if pkt_accept_count >= counter_holder['ipv4_last_pkt_accept_count_' + chainz + '_' + str(param).lower()]:
                        pkt_accept_count = pkt_accept_count - counter_holder['ipv4_last_pkt_accept_count_' + chainz + '_' + str(param).lower()]
                    counter_holder['ipv4_last_pkt_accept_count_' + chainz + '_' + str(param).lower()] = pkt_accept_count + counter_holder['ipv4_last_pkt_accept_count_' + chainz + '_' + str(param).lower()]
                    if pkt_mark_count >= counter_holder['ipv4_last_pkt_mark_count_' + chainz + '_' + str(param).lower()]:
                        pkt_mark_count = pkt_mark_count - counter_holder['ipv4_last_pkt_mark_count_' + chainz + '_' + str(param).lower()]
                    counter_holder['ipv4_last_pkt_mark_count_' + chainz + '_' + str(param).lower()] = pkt_mark_count + counter_holder['ipv4_last_pkt_mark_count_' + chainz + '_' + str(param).lower()]
                    if pkt_drop_count >= counter_holder['ipv4_last_pkt_drop_count_' + chainz + '_' + str(param).lower()]:
                        pkt_drop_count = pkt_drop_count - counter_holder['ipv4_last_pkt_drop_count_' + chainz + '_' + str(param).lower()]
                    counter_holder['ipv4_last_pkt_drop_count' + chainz + '_' + str(param).lower()] = pkt_drop_count + counter_holder['ipv4_last_pkt_drop_count_' + chainz + '_' + str(param).lower()]
                    if byt_accept_count >= counter_holder['ipv4_last_byt_accept_count_' + chainz + '_' + str(param).lower()]:
                        byt_accept_count = byt_accept_count - counter_holder['ipv4_last_byt_accept_count_' + chainz + '_' + str(param).lower()]
                    counter_holder['ipv4_last_byt_accept_count_' + chainz + '_' + str(param).lower()] = byt_accept_count + counter_holder['ipv4_last_byt_accept_count_' + chainz + '_' + str(param).lower()]
                    if byt_mark_count >= counter_holder['ipv4_last_byt_mark_count_' + chainz + '_' + str(param).lower()]:
                        byt_mark_count = byt_mark_count - counter_holder['ipv4_last_byt_mark_count_' + chainz + '_' + str(param).lower()]
                    counter_holder['ipv4_last_byt_mark_count_' + chainz + '_' + str(param).lower()] = byt_mark_count + counter_holder['ipv4_last_byt_mark_count_' + chainz + '_' + str(param).lower()]
                    if byt_drop_count >= counter_holder['ipv4_last_byt_drop_count_' + chainz + '_' + str(param).lower()]:
                        byt_drop_count = byt_drop_count - counter_holder['ipv4_last_byt_drop_count_' + chainz + '_' + str(param).lower()]
                    counter_holder['ipv4_last_byt_drop_count' + chainz + '_' + str(param).lower()] = byt_drop_count + counter_holder['ipv4_last_byt_drop_count_' + chainz + '_' + str(param).lower()]
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
                            pkt_accept_count += packets
                            byt_accept_count += bytes
                        else:
                            pass
                        if rule_tgt_name == 'mark':
                            pkt_mark_count += packets
                            byt_mark_count += bytes
                        else:
                            pass
                        if rule_tgt_name == 'drop':
                            pkt_drop_count += packets
                            byt_drop_count += bytes
                        else:
                            pass
                        for match in rule.matches:
                            if match.name == 'comment':
                                if re.match(r'^tcollector:.*', match.parameters["comment"], re.IGNORECASE):
                                    cmnt = match.parameters["comment"].split(':')[1].strip().split()[0]
                                    if packets >= counter_holder['ipv6_last_pkt_' + cmnt + '_count_' + chainz + '_' + str(param).lower()]:
                                        cmnt_pkt = packets - counter_holder['ipv6_last_pkt_' + cmnt + '_count_' + chainz + '_' + str(param).lower()]
                                    else:
                                        cmnt_pkt = packets
                                    counter_holder['ipv6_last_pkt_' + cmnt + '_count_' + chainz + '_' + str(param).lower()] = packets + counter_holder['ipv6_last_pkt_' + cmnt + '_count_' + chainz + '_' + str(param).lower()]
                                    if bytes >= counter_holder['ipv6_last_byt_' + cmnt + '_count_' + chainz + '_' + str(param).lower()]:
                                        cmnt_byt = bytes - counter_holder['ipv6_last_byt_' + cmnt + '_count_' + chainz + '_' + str(param).lower()]
                                    else:
                                        cmnt_byt = bytes
                                    counter_holder['ipv6_last_byt_' + cmnt + '_count_' + chainz + '_' + str(param).lower()] = bytes + counter_holder['ipv6_last_pkt_' + cmnt + '_count_' + chainz + '_' + str(param).lower()]
                                    print 'iptables.%s.rules.%s.%s %d %d protocol=%s' % (str(param).lower(), cmnt, 'packets', thyme, cmnt_pkt, 'IPv6')
                                    print 'iptables.%s.rules.%s.%s %d %d protocol=%s' % (str(param).lower(), cmnt, 'bytes', thyme, cmnt_byt, 'IPv6')
                                else:
                                    pass
                            else:
                                pass
                    if pkt_accept_count >= counter_holder['ipv6_last_pkt_accept_count_' + chainz + '_' + str(param).lower()]:
                        pkt_accept_count = pkt_accept_count - counter_holder['ipv6_last_pkt_accept_count_' + chainz + '_' + str(param).lower()]
                    counter_holder['ipv6_last_pkt_accept_count_' + chainz + '_' + str(param).lower()] = pkt_accept_count + counter_holder['ipv6_last_pkt_accept_count_' + chainz + '_' + str(param).lower()]
                    if pkt_mark_count >= counter_holder['ipv6_last_pkt_mark_count_' + chainz + '_' + str(param).lower()]:
                        pkt_mark_count = pkt_mark_count - counter_holder['ipv6_last_pkt_mark_count_' + chainz + '_' + str(param).lower()]
                    counter_holder['ipv6_last_pkt_mark_count_' + chainz + '_' + str(param).lower()] = pkt_mark_count + counter_holder['ipv6_last_pkt_mark_count_' + chainz + '_' + str(param).lower()]
                    if pkt_drop_count >= counter_holder['ipv6_last_pkt_drop_count_' + chainz + '_' + str(param).lower()]:
                        pkt_drop_count = pkt_drop_count - counter_holder['ipv6_last_pkt_drop_count_' + chainz + '_' + str(param).lower()]
                    counter_holder['ipv6_last_pkt_drop_count' + chainz + '_' + str(param).lower()] = pkt_drop_count + pkt_drop_count - counter_holder['ipv6_last_pkt_drop_count_' + chainz + '_' + str(param).lower()]
                    if byt_accept_count >= counter_holder['ipv6_last_byt_accept_count_' + chainz + '_' + str(param).lower()]:
                        byt_accept_count = byt_accept_count - counter_holder['ipv6_last_byt_accept_count_' + chainz + '_' + str(param).lower()]
                    counter_holder['ipv6_last_byt_accept_count_' + chainz + '_' + str(param).lower()] = byt_accept_count + byt_accept_count - counter_holder['ipv6_last_byt_accept_count_' + chainz + '_' + str(param).lower()]
                    if byt_mark_count >= counter_holder['ipv6_last_byt_mark_count_' + chainz + '_' + str(param).lower()]:
                        byt_mark_count = byt_mark_count - counter_holder['ipv6_last_byt_mark_count_' + chainz + '_' + str(param).lower()]
                    counter_holder['ipv6_last_byt_mark_count_' + chainz + '_' + str(param).lower()] = byt_mark_count + byt_mark_count - counter_holder['ipv6_last_byt_mark_count_' + chainz + '_' + str(param).lower()]
                    if byt_drop_count >= counter_holder['ipv6_last_byt_drop_count_' + chainz + '_' + str(param).lower()]:
                        byt_drop_count = byt_drop_count - counter_holder['ipv6_last_byt_drop_count_' + chainz + '_' + str(param).lower()]
                    counter_holder['ipv6_last_byt_drop_count' + chainz + '_' + str(param).lower()] = byt_drop_count + counter_holder['ipv6_last_byt_drop_count_' + chainz + '_' + str(param).lower()]
                    print 'iptables.%s.%s.%s %d %d chain=%s protocol=%s' % (str(param).lower(), 'accept', 'packets', thyme, pkt_accept_count, chainz, 'IPv6')
                    print 'iptables.%s.%s.%s %d %d chain=%s protocol=%s' % (str(param).lower(), 'accept', 'bytes', thyme, byt_accept_count, chainz, 'IPv6')
                    print 'iptables.%s.%s.%s %d %d chain=%s protocol=%s' % (str(param).lower(), 'mark', 'packets', thyme, pkt_mark_count, chainz, 'IPv6')
                    print 'iptables.%s.%s.%s %d %d chain=%s protocol=%s' % (str(param).lower(), 'mark', 'bytes', thyme, byt_mark_count, chainz, 'IPv6')
                    print 'iptables.%s.%s.%s %d %d chain=%s protocol=%s' % (str(param).lower(), 'drop', 'packets', thyme, pkt_drop_count, chainz, 'IPv6')
                    print 'iptables.%s.%s.%s %d %d chain=%s protocol=%s' % (str(param).lower(), 'drop', 'bytes', thyme, byt_drop_count, chainz, 'IPv6')
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
