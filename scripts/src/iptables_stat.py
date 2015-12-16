#!/usr/bin/env python
#
# iptables_stat.py -- a collector for tcollector/OpenTSDB
# Copyright (C) 2015 NSONE, Inc.
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

INTERVAL = 60
PARAMS = [iptc.Table.FILTER, iptc.Table.NAT, iptc.Table.MANGLE, iptc.Table.RAW]

def collect_metrics():
    thyme = int(time.time())
    for param in PARAMS:
        table = iptc.Table(param)
        table.refresh()
        for chain in table.chains:
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
                if rule_tgt_name == 'accept' or rule_tgt_name == 'mark' or rule_tgt_name == 'drop':
                    print 'iptables.%s.%s.%s %d %d chain=%s' % (str(param).lower(), rule_tgt_name, 'packets', thyme, packets, chainz)
                    print 'iptables.%s.%s.%s %d %d chain=%s' % (str(param).lower(), rule_tgt_name, 'bytes', thyme, bytes, chainz)
                    for match in rule.matches:
                        if match.name == 'comment':
                            if re.match(r'^tcollector:.*', match.parameters["comment"], re.IGNORECASE):
                                cmntA = re.sub(r'^tcollector:', '', match.parameters["comment"], re.IGNORECASE)
                                cmnt = re.sub(r'\s', '_', cmntA)
                                print 'iptables.%s.rules.%s %d %d rule=%s' % (str(param).lower(), 'packets', int(time.time()), packets, cmnt)
                                print 'iptables.%s.rules.%s %d %d rule=%s' % (str(param).lower(), 'bytes', int(time.time()), bytes, cmnt)
                            else:
                                pass
                        else:
                            pass
            chain.zero_counters()

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
