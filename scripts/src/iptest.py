#!/usr/bin/python

import time
import sys
import re
import iptc

INTERVAL = 1

def err(msg):
  print >>sys.stderr, msg

def debug(msg):
  if DEBUG:
    err(msg)

class IpTabler():
    """Capture IPTables ststistics: Rules matched, Packets/Bytes dropped, Packets/Bytes passed"""

    def __init__(self):
        self.table = iptc.Table(iptc.Table.FILTER)
        self.input_chain = iptc.Chain()



def main():
    while True:
        time.sleep(INTERVAL)

if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/python

import time
import iptc
import re

INTERVAL = 60
PARAMS = [iptc.Table.FILTER, iptc.Table.NAT, iptc.Table.MANGLE, iptc.Table.RAW]

filter_def_input_accept_pkt = 0
filter_def_input_accept_byt = 0
filter_def_input_mark_pkt = 0
filter_def_input_mark_byt = 0
filter_def_input_drop_pkt = 0
filter_def_input_drop_byt = 0
filter_def_forward_accept_pkt = 0
filter_def_forward_accept_byt = 0
filter_def_forward_mark_pkt = 0
filter_def_forward_mark_byt = 0
filter_def_forward_drop_pkt = 0
filter_def_forward_drop_byt = 0
filter_def_output_accept_pkt = 0
filter_def_output_accept_byt = 0
filter_def_output_mark_pkt = 0
filter_def_output_mark_byt = 0
filter_def_output_drop_pkt = 0
filter_def_output_drop_byt = 0
filter_ns1_input_accept_pkt = 0
filter_ns1_input_accept_byt = 0
filter_ns1_input_mark_pkt = 0
filter_ns1_input_mark_byt = 0
filter_ns1_input_drop_pkt = 0
filter_ns1_input_drop_byt = 0
filter_ns1_forward_accept_pkt = 0
filter_ns1_forward_accept_byt = 0
filter_ns1_forward_mark_pkt = 0
filter_ns1_forward_mark_byt = 0
filter_ns1_forward_drop_pkt = 0
filter_ns1_forward_drop_byt = 0
filter_ns1_output_accept_pkt = 0
filter_ns1_output_accept_byt = 0
filter_ns1_output_mark_pkt = 0
filter_ns1_output_mark_byt = 0
filter_ns1_output_drop_pkt = 0
filter_ns1_output_drop_byt = 0
nat_def_input_accept_pkt = 0
nat_def_input_accept_byt = 0
nat_def_input_mark_pkt = 0
nat_def_input_mark_byt = 0
nat_def_input_drop_pkt = 0
nat_def_input_drop_byt = 0
nat_def_output_accept_pkt = 0
nat_def_output_accept_byt = 0
nat_def_output_mark_pkt = 0
nat_def_output_mark_byt = 0
nat_def_output_drop_pkt = 0
nat_def_output_drop_byt = 0
nat_def_prert_accept_pkt = 0
nat_def_prert_accept_byt = 0
nat_def_prert_mark_pkt = 0
nat_def_prert_mark_byt = 0
nat_def_prert_drop_pkt = 0
nat_def_prert_drop_byt = 0
nat_def_postrt_accept_pkt = 0
nat_def_postrt_accept_byt = 0
nat_def_postrt_mark_pkt = 0
nat_def_postrt_mark_byt = 0
nat_def_postrt_drop_pkt = 0
nat_def_postrt_drop_byt = 0
nat_ns1_postrt_accept_pkt = 0
nat_ns1_postrt_accept_byt = 0
nat_ns1_postrt_mark_pkt = 0
nat_ns1_postrt_mark_byt = 0
nat_ns1_postrt_drop_pkt = 0
nat_ns1_postrt_drop_byt = 0
mangle_def_input_accept_pkt = 0
mangle_def_input_accept_byt = 0
mangle_def_input_mark_pkt = 0
mangle_def_input_mark_byt = 0
mangle_def_input_drop_pkt = 0
mangle_def_input_drop_byt = 0
mangle_def_forward_accept_pkt = 0
mangle_def_forward_accept_byt = 0
mangle_def_forward_mark_pkt = 0
mangle_def_forward_mark_byt = 0
mangle_def_forward_drop_pkt = 0
mangle_def_forward_drop_byt = 0
mangle_def_output_accept_pkt = 0
mangle_def_output_accept_byt = 0
mangle_def_output_mark_pkt = 0
mangle_def_output_mark_byt = 0
mangle_def_output_drop_pkt = 0
mangle_def_output_drop_byt = 0
mangle_def_prert_accept_pkt = 0
mangle_def_prert_accept_byt = 0
mangle_def_prert_mark_pkt = 0
mangle_def_prert_mark_byt = 0
mangle_def_prert_drop_pkt = 0
mangle_def_prert_drop_byt = 0
mangle_def_postrt_accept_pkt = 0
mangle_def_postrt_accept_byt = 0
mangle_def_postrt_mark_pkt = 0
mangle_def_postrt_mark_byt = 0
mangle_def_postrt_drop_pkt = 0
mangle_def_postrt_drop_byt = 0
mangle_ns1_postrt_accept_pkt = 0
mangle_ns1_postrt_accept_byt = 0
mangle_ns1_postrt_mark_pkt = 0
mangle_ns1_postrt_mark_byt = 0
mangle_ns1_postrt_drop_pkt = 0
mangle_ns1_postrt_drop_byt = 0
raw_def_output_accept_pkt = 0
raw_def_output_accept_byt = 0
raw_def_output_mark_pkt = 0
raw_def_output_mark_byt = 0
raw_def_output_drop_pkt = 0
raw_def_output_drop_byt = 0
raw_def_prert_accept_pkt = 0
raw_def_prert_accept_byt = 0
raw_def_prert_mark_pkt = 0
raw_def_prert_mark_byt = 0
raw_def_prert_drop_pkt = 0
raw_def_prert_drop_byt = 0


for param in PARAMS:
    table = iptc.Table(param)
    for chain in table.chains:
        comments = []
        if re.match(r'^NS1', chain.name):
            p = chain.name.split('_')
            chainz = p[0] + '_' + p[1]
        else:
            chainz = chain.name
        for rule in chain.rules:
            if str(rule.target.name).lower() != '':
                for match in rule.matches:
                    if match.name == "comment":
                        comment = match.comment.replace('\s', '_')
                    else:
                        comment = "no_comment_" + str(param)
                match_name = match.name
                if re.match(r'^NS1', rule.target.name):
                    p = rule.target.name.split('_')
                    rule_tgt_name = p[0] + '_' + p[1]
                else:
                    rule_tgt_name = rule.target.name
                (packets, bytes) = rule.get_counters()
                if str(param).lower() == 'filter':
                    if str(chainz).lower() == 'input':
                        if str(rule_tgt_name).lower() == 'accept':
                            fdia = [str(param).lower(), str(chainz).lower(), str(rule_tgt_name).lower()]
                            filter_def_input_accept_pkt += packets
                            filter_def_input_accept_byt += bytes
                        elif str(rule_tgt_name).lower() == 'mark':
                            fdim = [str(param).lower(), str(chainz).lower(), str(rule_tgt_name).lower()]
                            filter_def_input_mark_pkt += packets
                            filter_def_input_mark_byt += bytes
                        elif str(rule_tgt_name).lower() == 'drop':
                            fdid = [str(param).lower(), str(chainz).lower(), str(rule_tgt_name).lower()]
                            filter_def_input_drop_pkt += packets
                            filter_def_input_drop_byt += bytes
                        else:
                            pass
                    elif str(chainz).lower() == 'forward':
                        if str(rule_tgt_name).lower() == 'accept':
                            fdfa = [str(param).lower(), str(chainz).lower(), str(rule_tgt_name).lower()]
                            filter_def_forward_accept_pkt += packets
                            filter_def_forward_accept_byt += bytes
                        elif str(rule_tgt_name).lower() == 'mark':
                            fdfm = [str(param).lower(), str(chainz).lower(), str(rule_tgt_name).lower()]
                            filter_def_forward_mark_pkt += packets
                            filter_def_forward_mark_byt += bytes
                        elif str(rule_tgt_name).lower() == 'drop':
                            fdfd = [str(param).lower(), str(chainz).lower(), str(rule_tgt_name).lower()]
                            filter_def_forward_drop_pkt += packets
                            filter_def_forward_drop_byt += bytes
                        else:
                            pass
                    elif str(chainz).lower() == 'output':
                        if str(rule_tgt_name).lower() == 'accept':
                            fdoa = [str(param).lower(), str(chainz).lower(), str(rule_tgt_name).lower()]
                            filter_def_output_accept_pkt += packets
                            filter_def_output_accept_byt += bytes
                        elif str(rule_tgt_name).lower() == 'mark':
                            fdom = [str(param).lower(), str(chainz).lower(), str(rule_tgt_name).lower()]
                            filter_def_output_mark_pkt += packets
                            filter_def_output_mark_byt += bytes
                        elif str(rule_tgt_name).lower() == 'drop':
                            fdod = [str(param).lower(), str(chainz).lower(), str(rule_tgt_name).lower()]
                            filter_def_output_drop_pkt += packets
                            filter_def_output_drop_byt += bytes
                        else:
                            pass
                    elif str(chainz).lower() == 'ns1_input':
                        if str(rule_tgt_name).lower() == 'accept':
                            fnia = [str(param).lower(), str(chainz).lower(), str(rule_tgt_name).lower()]
                            filter_ns1_input_accept_pkt += packets
                            filter_ns1_input_accept_byt += bytes
                        elif str(rule_tgt_name).lower() == 'mark':
                            fnim = [str(param).lower(), str(chainz).lower(), str(rule_tgt_name).lower()]
                            filter_ns1_input_mark_pkt += packets
                            filter_ns1_input_mark_byt += bytes
                        elif str(rule_tgt_name).lower() == 'drop':
                            fnid = [str(param).lower(), str(chainz).lower(), str(rule_tgt_name).lower()]
                            filter_ns1_input_drop_pkt += packets
                            filter_ns1_input_drop_byt += bytes
                        else:
                            pass
                    elif str(chainz).lower() == 'ns1_forward':
                        if str(rule_tgt_name).lower() == 'accept':
                            fnfa = [str(param).lower(), str(chainz).lower(), str(rule_tgt_name).lower()]
                            filter_ns1_forward_accept_pkt += packets
                            filter_ns1_forward_accept_byt += bytes
                        elif str(rule_tgt_name).lower() == 'mark':
                            fnfm = [str(param).lower(), str(chainz).lower(), str(rule_tgt_name).lower()]
                            filter_ns1_forward_mark_pkt += packets
                            filter_ns1_forward_mark_byt += bytes
                        elif str(rule_tgt_name).lower() == 'drop':
                            fnfd = [str(param).lower(), str(chainz).lower(), str(rule_tgt_name).lower()]
                            filter_ns1_forward_drop_pkt += packets
                            filter_ns1_forward_drop_byt += bytes
                        else:
                            pass
                    elif str(chainz).lower() == 'ns1_output':
                        if str(rule_tgt_name).lower() == 'accept':
                            fnoa = [str(param).lower(), str(chainz).lower(), str(rule_tgt_name).lower()]
                            filter_ns1_output_accept_pkt += packets
                            filter_ns1_output_accept_byt += bytes
                        elif str(rule_tgt_name).lower() == 'mark':
                            fnom = [str(param).lower(), str(chainz).lower(), str(rule_tgt_name).lower()]
                            filter_ns1_output_mark_pkt += packets
                            filter_ns1_output_mark_byt += bytes
                        elif str(rule_tgt_name).lower() == 'drop':
                            fnod = [str(param).lower(), str(chainz).lower(), str(rule_tgt_name).lower()]
                            filter_ns1_output_drop_pkt += packets
                            filter_ns1_output_drop_byt += bytes
                        else:
                            pass
                    else:
                        pass
                elif str(param).lower() == 'nat':
                    if str(chainz).lower() == 'input':
                        if str(rule_tgt_name).lower() == 'accept':
                            ndia = [str(param).lower(), str(chainz).lower(), str(rule_tgt_name).lower()]
                            nat_def_input_accept_pkt += packets
                            nat_def_input_accept_byt += bytes
                        elif str(rule_tgt_name).lower() == 'mark':
                            ndim = [str(param).lower(), str(chainz).lower(), str(rule_tgt_name).lower()]
                            nat_def_input_mark_pkt += packets
                            nat_def_input_mark_byt += bytes
                        elif str(rule_tgt_name).lower() == 'drop':
                            ndid = [str(param).lower(), str(chainz).lower(), str(rule_tgt_name).lower()]
                            nat_def_input_drop_pkt += packets
                            nat_def_input_drop_byt += bytes
                        else:
                            pass
                    elif str(chainz).lower() == 'output':
                        if str(rule_tgt_name).lower() == 'accept':
                            ndoa = [str(param).lower(), str(chainz).lower(), str(rule_tgt_name).lower()]
                            nat_def_output_accept_pkt += packets
                            nat_def_output_accept_byt += bytes
                        elif str(rule_tgt_name).lower() == 'mark':
                            ndom = [str(param).lower(), str(chainz).lower(), str(rule_tgt_name).lower()]
                            nat_def_output_mark_pkt += packets
                            nat_def_output_mark_byt += bytes
                        elif str(rule_tgt_name).lower() == 'drop':
                            ndod = [str(param).lower(), str(chainz).lower(), str(rule_tgt_name).lower()]
                            nat_def_output_drop_pkt += packets
                            nat_def_output_drop_byt += bytes
                        else:
                            pass
                    elif str(chainz).lower() == 'preroute':
                        if str(rule_tgt_name).lower() == 'accept':
                            ndpa = [str(param).lower(), str(chainz).lower(), str(rule_tgt_name).lower()]
                            nat_def_prert_accept_pkt += packets
                            nat_def_prert_accept_byt += bytes
                        elif str(rule_tgt_name).lower() == 'mark':
                            ndpm = [str(param).lower(), str(chainz).lower(), str(rule_tgt_name).lower()]
                            nat_def_prert_mark_pkt += packets
                            nat_def_prert_mark_byt += bytes
                        elif str(rule_tgt_name).lower() == 'drop':
                            ndpd = [str(param).lower(), str(chainz).lower(), str(rule_tgt_name).lower()]
                            nat_def_prert_drop_pkt += packets
                            nat_def_prert_drop_byt += bytes
                        else:
                            pass
                    elif str(chainz).lower() == 'postroute':
                        if str(rule_tgt_name).lower() == 'accept':
                            ndPa = [str(param).lower(), str(chainz).lower(), str(rule_tgt_name).lower()]
                            nat_def_postrt_accept_pkt += packets
                            nat_def_postrt_accept_byt += bytes
                        elif str(rule_tgt_name).lower() == 'mark':
                            ndPm = [str(param).lower(), str(chainz).lower(), str(rule_tgt_name).lower()]
                            nat_def_postrt_mark_pkt += packets
                            nat_def_postrt_mark_byt += bytes
                        elif str(rule_tgt_name).lower() == 'drop':
                            ndPd = [str(param).lower(), str(chainz).lower(), str(rule_tgt_name).lower()]
                            nat_def_postrt_drop_pkt += packets
                            nat_def_postrt_drop_byt += bytes
                        else:
                            pass
                    elif str(chainz).lower() == 'ns1_postroute':
                        if str(rule_tgt_name).lower() == 'accept':
                            nnPa = [str(param).lower(), str(chainz).lower(), str(rule_tgt_name).lower()]
                            nat_def_ns1_postrt_accept_pkt += packets
                            nat_def_ns1_postrt_accept_byt += bytes
                        elif str(rule_tgt_name).lower() == 'mark':
                            nnPm = [str(param).lower(), str(chainz).lower(), str(rule_tgt_name).lower()]
                            nat_def_ns1_postrt_mark_pkt += packets
                            nat_def_ns1_postrt_mark_byt += bytes
                        elif str(rule_tgt_name).lower() == 'drop':
                            nnPd = [str(param).lower(), str(chainz).lower(), str(rule_tgt_name).lower()]
                            nat_def_ns1_postrt_drop_pkt += packets
                            nat_def_ns1_postrt_drop_byt += bytes
                        else:
                            pass
                    else:
                        pass
                elif str(param).lower() == 'mangle':
                    if str(chainz).lower() == 'input':
                        if str(rule_tgt_name).lower() == 'accept':
                            mdia = [str(param).lower(), str(chainz).lower(), str(rule_tgt_name).lower()]
                            mangle_def_input_accept_pkt += packets
                            mangle_def_input_accept_byt += bytes
                        elif str(rule_tgt_name).lower() == 'mark':
                            mdim = [str(param).lower(), str(chainz).lower(), str(rule_tgt_name).lower()]
                            mangle_def_input_mark_pkt += packets
                            mangle_def_input_mark_byt += bytes
                        elif str(rule_tgt_name).lower() == 'drop':
                            mdid = [str(param).lower(), str(chainz).lower(), str(rule_tgt_name).lower()]
                            mangle_def_input_drop_pkt += packets
                            mangle_def_input_drop_byt += bytes
                        else:
                            pass
                    elif str(chainz).lower() == 'forward':
                        if str(rule_tgt_name).lower() == 'accept':
                            mdfa = [str(param).lower(), str(chainz).lower(), str(rule_tgt_name).lower()]
                            mangle_def_forward_accept_pkt += packets
                            mangle_def_forward_accept_byt += bytes
                        elif str(rule_tgt_name).lower() == 'mark':
                            mdfm = [str(param).lower(), str(chainz).lower(), str(rule_tgt_name).lower()]
                            mangle_def_forward_mark_pkt += packets
                            mangle_def_forward_mark_byt += bytes
                        elif str(rule_tgt_name).lower() == 'drop':
                            mdfd = [str(param).lower(), str(chainz).lower(), str(rule_tgt_name).lower()]
                            mangle_def_forward_drop_pkt += packets
                            mangle_def_forward_drop_byt += bytes
                        else:
                            pass
                    elif str(chainz).lower() == 'output':
                        if str(rule_tgt_name).lower() == 'accept':
                            mdoa = [str(param).lower(), str(chainz).lower(), str(rule_tgt_name).lower()]
                            mangle_def_output_accept_pkt += packets
                            mangle_def_output_accept_byt += bytes
                        elif str(rule_tgt_name).lower() == 'mark':
                            mdom = [str(param).lower(), str(chainz).lower(), str(rule_tgt_name).lower()]
                            mangle_def_output_mark_pkt += packets
                            mangle_def_output_mark_byt += bytes
                        elif str(rule_tgt_name).lower() == 'drop':
                            mdod = [str(param).lower(), str(chainz).lower(), str(rule_tgt_name).lower()]
                            mangle_def_output_drop_pkt += packets
                            mangle_def_output_drop_byt += bytes
                        else:
                            pass
                    elif str(chainz).lower() == 'preroute':
                        if str(rule_tgt_name).lower() == 'accept':
                            mdpa = [str(param).lower(), str(chainz).lower(), str(rule_tgt_name).lower()]
                            mangle_def_prert_accept_pkt += packets
                            mangle_def_prert_accept_byt += bytes
                        elif str(rule_tgt_name).lower() == 'mark':
                            mdpm = [str(param).lower(), str(chainz).lower(), str(rule_tgt_name).lower()]
                            mangle_def_prert_mark_pkt += packets
                            mangle_def_prert_mark_byt += bytes
                        elif str(rule_tgt_name).lower() == 'drop':
                            mdpd = [str(param).lower(), str(chainz).lower(), str(rule_tgt_name).lower()]
                            mangle_def_prert_drop_pkt += packets
                            mangle_def_prert_drop_byt += bytes
                        else:
                            pass
                    elif str(chainz).lower() == 'postroute':
                        if str(rule_tgt_name).lower() == 'accept':
                            mdPa = [str(param).lower(), str(chainz).lower(), str(rule_tgt_name).lower()]
                            mangle_def_postrt_accept_pkt += packets
                            mangle_def_postrt_accept_byt += bytes
                        elif str(rule_tgt_name).lower() == 'mark':
                            mdPm = [str(param).lower(), str(chainz).lower(), str(rule_tgt_name).lower()]
                            mangle_def_postrt_mark_pkt += packets
                            mangle_def_postrt_mark_byt += bytes
                        elif str(rule_tgt_name).lower() == 'drop':
                            mdPd = [str(param).lower(), str(chainz).lower(), str(rule_tgt_name).lower()]
                            mangle_def_postrt_drop_pkt += packets
                            mangle_def_postrt_drop_byt += bytes
                        else:
                            pass
                    elif str(chainz).lower() == 'ns1_postroute':
                        if str(rule_tgt_name).lower() == 'accept':
                            mnPa = [str(param).lower(), str(chainz).lower(), str(rule_tgt_name).lower()]
                            mangle_def_ns1_postrt_accept_pkt += packets
                            mangle_def_ns1_postrt_accept_byt += bytes
                        elif str(rule_tgt_name).lower() == 'mark':
                            mnPm = [str(param).lower(), str(chainz).lower(), str(rule_tgt_name).lower()]
                            mangle_def_ns1_postrt_mark_pkt += packets
                            mangle_def_ns1_postrt_mark_byt += bytes
                        elif str(rule_tgt_name).lower() == 'drop':
                            mnPd = [str(param).lower(), str(chainz).lower(), str(rule_tgt_name).lower()]
                            mangle_def_ns1_postrt_drop_pkt += packets
                            mangle_def_ns1_postrt_drop_byt += bytes
                        else:
                            pass
                    else:
                        pass
                elif string(param).lower() == 'raw':
                    if str(chainz).lower() == 'output':
                        if str(rule_tgt_name).lower() == 'accept':
                            ndoa = [str(param).lower(), str(chainz).lower(), str(rule_tgt_name).lower()]
                            nat_def_output_accept_pkt += packets
                            nat_def_output_accept_byt += bytes
                        elif str(rule_tgt_name).lower() == 'mark':
                            ndom = [str(param).lower(), str(chainz).lower(), str(rule_tgt_name).lower()]
                            nat_def_output_mark_pkt += packets
                            nat_def_output_mark_byt += bytes
                        elif str(rule_tgt_name).lower() == 'drop':
                            ndod = [str(param).lower(), str(chainz).lower(), str(rule_tgt_name).lower()]
                            nat_def_output_drop_pkt += packets
                            nat_def_output_drop_byt += bytes
                        else:
                            pass
                    elif str(chainz).lower() == 'preroute':
                        if str(rule_tgt_name).lower() == 'accept':
                            ndpa = [str(param).lower(), str(chainz).lower(), str(rule_tgt_name).lower()]
                            nat_def_prert_accept_pkt += packets
                            nat_def_prert_accept_byt += bytes
                        elif str(rule_tgt_name).lower() == 'mark':
                            ndpm = [str(param).lower(), str(chainz).lower(), str(rule_tgt_name).lower()]
                            nat_def_prert_mark_pkt += packets
                            nat_def_prert_mark_byt += bytes
                        elif str(rule_tgt_name).lower() == 'drop':
                            ndpd = [str(param).lower(), str(chainz).lower(), str(rule_tgt_name).lower()]
                            nat_def_prert_drop_pkt += packets
                            nat_def_prert_drop_byt += bytes
                        else:
                            pass
                    else:
                        pass
                else:
                    pass
            else:
                pass

if filter_def_input_accept_pkt > 0:
    print 'iptables.%s.%s.%s %d %d chain=%s' % (fdia[0], fdia[2], 'packets', int(time.time()), filter_def_input_accept_pkt, fdia[1])
    print 'iptables.%s.%s.%s %d %d chain=%s' % (fdia[0], fdia[2], 'bytes', int(time.time()), filter_def_input_accept_byt, fdia[1])
else:
    pass
if filter_def_input_mark_pkt > 0:
    print 'iptables.%s.%s.%s %d %d chain=%s' % (fdim[0], fdim[2], 'packets', int(time.time()), filter_def_input_mark_pkt, fdim[1])
    print 'iptables.%s.%s.%s %d %d chain=%s' % (fdim[0], fdim[2], 'bytes', int(time.time()), filter_def_input_mark_byt, fdim[1])
else:
    pass
if filter_def_input_drop_pkt > 0:
    print 'iptables.%s.%s.%s %d %d chain=%s' % (fdid[0], fdid[2],'packets', int(time.time()), filter_def_input_drop_pkt, fdid[1])
    print 'iptables.%s.%s.%s %d %d chain=%s' % (fdid[0], fdid[2], 'bytes', int(time.time()), filter_def_input_drop_byt, fdid[1])
else:
    pass
if filter_def_forward_accept_pkt > 0:
    print 'iptables.%s.%s.%s %d %d chain=%s' % (fdfa[0], fdfa[2], 'packets', int(time.time()), filter_def_forward_accept_pkt, fdfa[1])
    print 'iptables.%s.%s.%s %d %d chain=%s' % (fdfa[0], fdfa[2], 'bytes', int(time.time()), filter_def_forward_accept_byt, fdfa[1])
else:
    pass
if filter_def_forward_mark_pkt > 0:
    print 'iptables.%s.%s.%s %d %d chain=%s' % (fdfm[0], fdfm[2], 'packets', int(time.time()), filter_def_forward_mark_pkt, fdfm[1])
    print 'iptables.%s.%s.%s %d %d chain=%s' % (fdfm[0], fdfm[2], 'bytes', int(time.time()), filter_def_forward_mark_byt, fdfm[1])
else:
    pass
if filter_def_forward_drop_pkt > 0:
    print 'iptables.%s.%s.%s %d %d chain=%s' % (fdfd[0], fdfd[2], 'packets', int(time.time()), filter_def_forward_drop_pkt, fdfd[1])
    print 'iptables.%s.%s.%s %d %d chain=%s' % (fdfd[0], fdfd[2], 'bytes', int(time.time()), filter_def_forward_drop_byt, fdfd[1])
else:
    pass
if filter_def_output_accept_pkt > 0:
    print 'iptables.%s.%s.%s %d %d chain=%s' % (fdoa[0], fdoa[2], 'packets', int(time.time()), filter_def_output_accept_pkt, fdoa[1])
    print 'iptables.%s.%s.%s %d %d chain=%s' % (fdoa[0], fdoa[2], 'bytes', int(time.time()), filter_def_output_accept_byt, fdoa[1])
else:
    pass
if filter_def_output_mark_pkt > 0:
    print 'iptables.%s.%s.%s %d %d chain=%s' % (fdom[0], fdom[2], 'packets', int(time.time()), filter_def_output_mark_pkt, fdom[1])
    print 'iptables.%s.%s.%s %d %d chain=%s' % (fdom[0], fdom[2], 'bytes', int(time.time()), filter_def_output_mark_byt, fdom[1])
else:
    pass
if filter_def_output_drop_pkt > 0:
    print 'iptables.%s.%s.%s %d %d chain=%s' % (fdod[0], fdod[2], 'packets', int(time.time()), filter_def_output_drop_pkt, fdod[1])
    print 'iptables.%s.%s.%s %d %d chain=%s' % (fdod[0], fdod[2], 'bytes', int(time.time()), filter_def_output_drop_byt, fdod[1])
else:
    pass
if filter_ns1_input_accept_pkt > 0:
    print 'iptables.%s.%s.%s %d %d chain=%s' % (fnia[0], fnia[2], 'packets', int(time.time()), filter_ns1_input_accept_pkt, fnia[1])
    print 'iptables.%s.%s.%s %d %d chain=%s' % (fnia[0], fnia[2], 'bytes', int(time.time()), filter_ns1_input_accept_byt, fnia[1])
else:
    pass
if filter_ns1_input_mark_pkt > 0:
    print 'iptables.%s.%s.%s %d %d chain=%s' % (fnim[0], fnim[2], 'packets', int(time.time()), filter_ns1_input_mark_pkt, fnim[1])
    print 'iptables.%s.%s.%s %d %d chain=%s' % (fnim[0], fnim[2], 'bytes', int(time.time()), filter_ns1_input_mark_byt, fnim[1])
else:
    pass
if filter_ns1_input_drop_pkt > 0:
    print 'iptables.%s.%s.%s %d %d chain=%s' % (fnid[0], fnid[2], 'packets', int(time.time()), filter_ns1_input_drop_pkt, fnid[1])
    print 'iptables.%s.%s.%s %d %d chain=%s' % (fnid[0], fnid[2], 'bytes', int(time.time()), filter_ns1_input_drop_byt, fnid[1])
else:
    pass
if filter_ns1_forward_accept_pkt > 0:
    print 'iptables.%s.%s.%s %d %d chain=%s' % (fnfa[0], fnfa[2], 'packets', int(time.time()), filter_ns1_forward_accept_pkt, fnfa[1])
    print 'iptables.%s.%s.%s %d %d chain=%s' % (fnfa[0], fnfa[2], 'bytes', int(time.time()), filter_ns1_forward_accept_byt, fnfa[1])
else:
    pass
if filter_ns1_forward_mark_pkt > 0:
    print 'iptables.%s.%s.%s %d %d chain=%s' % (fnfm[0], fnfm[2], 'packets', int(time.time()), filter_ns1_forward_mark_pkt, fnfm[1])
    print 'iptables.%s.%s.%s %d %d chain=%s' % (fnfm[0], fnfm[2], 'bytes', int(time.time()), filter_ns1_forward_mark_byt, fnfm[1])
else:
    pass
if filter_ns1_forward_drop_pkt > 0:
    print 'iptables.%s.%s.%s %d %d chain=%s' % (fnfd[0], fnfd[2], 'packets', int(time.time()), filter_ns1_forward_drop_pkt, fnfd[1])
    print 'iptables.%s.%s.%s %d %d chain=%s' % (fnfd[0], fnfd[2], 'bytes', int(time.time()), filter_ns1_forward_drop_byt, fnfd[1])
else:
    pass
if filter_ns1_output_accept_pkt > 0:
    print 'iptables.%s.%s.%s %d %d chain=%s' % (fnoa[0], fnoa[2], 'packets', int(time.time()), filter_ns1_output_accept_pkt, fnoa[1])
    print 'iptables.%s.%s.%s %d %d chain=%s' % (fnoa[0], fnoa[2], 'bytes', int(time.time()), filter_ns1_output_accept_byt, fnoa[1])
else:
    pass
if filter_ns1_output_mark_pkt > 0:
    print 'iptables.%s.%s.%s %d %d chain=%s' % (fnom[0], fnom[2], 'packets', int(time.time()), filter_ns1_output_mark_pkt, fnom[1])
    print 'iptables.%s.%s.%s %d %d chain=%s' % (fnom[0], fnom[2], 'bytes', int(time.time()), filter_ns1_output_mark_byt, fnom[1])
else:
    pass
if filter_ns1_output_drop_pkt > 0:
    print 'iptables.%s.%s.%s %d %d chain=%s' % (fnod[0], fnod[2], 'packets', int(time.time()), filter_ns1_output_drop_pkt, fnod[1])
    print 'iptables.%s.%s.%s %d %d chain=%s' % (fnod[0], fnod[2], 'bytes', int(time.time()), filter_ns1_output_drop_byt, fnod[1])
else:
    pass
if nat_def_input_accept_pkt > 0:
    print 'iptables.%s.%s.%s %d %d chain=%s' % (ndia[0], ndia[2], 'packets', int(time.time()), nat_def_input_accept_pkt, ndia[1])
    print 'iptables.%s.%s.%s %d %d chain=%s' % (ndia[0], ndia[2], 'bytes', int(time.time()), nat_def_input_accept_byt, ndia[1])
else:
    pass
if nat_def_input_mark_pkt > 0:
    print 'iptables.%s.%s.%s %d %d chain=%s' % (ndim[0], ndim[2], 'packets', int(time.time()), nat_def_input_mark_pkt, ndim[1])
    print 'iptables.%s.%s.%s %d %d chain=%s' % (ndim[0], ndim[2], 'bytes', int(time.time()), nat_def_input_mark_byt, ndim[1])
else:
    pass
if nat_def_input_drop_pkt > 0:
    print 'iptables.%s.%s.%s %d %d chain=%s' % (ndid[0], ndid[2], 'packets', int(time.time()), nat_def_input_drop_pkt, ndid[1])
    print 'iptables.%s.%s.%s %d %d chain=%s' % (ndid[0], ndid[2], 'bytes', int(time.time()), nat_def_input_drop_byt, ndid[1])
else:
    pass
if nat_def_output_accept_pkt > 0:
    print 'iptables.%s.%s.%s %d %d chain=%s' % (ndoa[0], ndoa[2], 'packets', int(time.time()), nat_def_output_accept_pkt, ndoa[1])
    print 'iptables.%s.%s.%s %d %d chain=%s' % (ndoa[0], ndoa[2], 'bytes', int(time.time()), nat_def_output_accept_byt, ndoa[1])
else:
    pass
if nat_def_output_mark_pkt > 0:
    print 'iptables.%s.%s.%s %d %d chain=%s' % (ndom[0], ndom[2], 'packets', int(time.time()), nat_def_output_mark_pkt, ndom[1])
    print 'iptables.%s.%s.%s %d %d chain=%s' % (ndom[0], ndom[2], 'bytes', int(time.time()), nat_def_output_mark_byt, ndom[1])
else:
    pass
if nat_def_output_drop_pkt > 0:
    print 'iptables.%s.%s.%s %d %d chain=%s' % (ndod[0], ndod[2], 'packets', int(time.time()), nat_def_output_drop_pkt, ndod[1])
    print 'iptables.%s.%s.%s %d %d chain=%s' % (ndod[0], ndod[2], 'bytes', int(time.time()), nat_def_output_drop_byt, ndod[1])
else:
    pass
if nat_def_prert_accept_pkt > 0:
    print 'iptables.%s.%s.%s %d %d chain=%s' % (ndpa[0], ndpa[2], 'packets', int(time.time()), nat_def_prert_accept_pkt, ndpa[1])
    print 'iptables.%s.%s.%s %d %d chain=%s' % (ndpa[0], ndpa[2], 'bytes', int(time.time()), nat_def_prert_accept_byt, ndpa[1])
else:
    pass
if nat_def_prert_mark_pkt > 0:
    print 'iptables.%s.%s.%s %d %d chain=%s' % (ndpm[0], ndpm[2], 'packets', int(time.time()), nat_def_prert_mark_pkt, ndpm[1])
    print 'iptables.%s.%s.%s %d %d chain=%s' % (ndpm[0], ndpm[2], 'bytes', int(time.time()), nat_def_prert_mark_byt, ndpm[1])
else:
    pass
if nat_def_prert_drop_pkt > 0:
    print 'iptables.%s.%s.%s %d %d chain=%s' % (ndpd[0], ndpd[2], 'packets', int(time.time()), nat_def_prert_drop_pkt, ndpd[1])
    print 'iptables.%s.%s.%s %d %d chain=%s' % (ndpd[0], ndpd[2], 'bytes', int(time.time()), nat_def_prert_drop_byt, ndpd[1])
else:
    pass
if nat_def_postrt_accept_pkt > 0:
    print 'iptables.%s.%s.%s %d %d chain=%s' % (ndPa[0], ndPa[2], 'packets', int(time.time()), nat_def_postrt_accept_pkt, ndPa[1])
    print 'iptables.%s.%s.%s %d %d chain=%s' % (ndPa[0], ndPa[2], 'bytes', int(time.time()), nat_def_postrt_accept_byt, ndPa[1])
else:
    pass
if nat_def_postrt_mark_pkt > 0:
    print 'iptables.%s.%s.%s %d %d chain=%s' % (ndPm[0], ndPm[2], 'packets', int(time.time()), nat_def_postrt_mark_pkt, ndPm[1])
    print 'iptables.%s.%s.%s %d %d chain=%s' % (ndPm[0], ndPm[2], 'bytes', int(time.time()), nat_def_postrt_mark_byt, ndPm[1])
else:
    pass
if nat_def_postrt_drop_pkt > 0:
    print 'iptables.%s.%s.%s %d %d chain=%s' % (ndPd[0], ndPd[2], 'packets', int(time.time()), nat_def_postrt_drop_pkt, ndPd[1])
    print 'iptables.%s.%s.%s %d %d chain=%s' % (ndPd[0], ndPd[2], 'bytes', int(time.time()), nat_def_postrt_drop_byt, ndPd[1])
else:
    pass
if nat_ns1_postrt_accept_pkt > 0:
    print 'iptables.%s.%s.%s %d %d chain=%s' % (nnPa[0], nnPa[2], 'packets', int(time.time()), nat_ns1_postrt_accept_pkt, nnPa[1])
    print 'iptables.%s.%s.%s %d %d chain=%s' % (nnPa[0], nnPa[2], 'bytes', int(time.time()), nat_ns1_postrt_accept_byt, nnPa[1])
else:
    pass
if nat_ns1_postrt_mark_pkt > 0:
    print 'iptables.%s.%s.%s %d %d chain=%s' % (nnPm[0], nnPm[2], 'packets', int(time.time()), nat_ns1_postrt_mark_pkt, nnPm[1])
    print 'iptables.%s.%s.%s %d %d chain=%s' % (nnPm[0], nnPm[2], 'bytes', int(time.time()), nat_ns1_postrt_mark_byt, nnPm[1])
else:
    pass
if nat_ns1_postrt_drop_pkt > 0:
    print 'iptables.%s.%s.%s %d %d chain=%s' % (nnPd[0], nnPd[2], 'packets', int(time.time()), nat_ns1_postrt_drop_pkt, nnPd[1])
    print 'iptables.%s.%s.%s %d %d chain=%s' % (nnPd[0], nnPd[2], 'bytes', int(time.time()), nat_ns1_postrt_drop_byt, nnPd[1])
else:
    pass
if mangle_def_input_accept_pkt > 0:
    print 'iptables.%s.%s.%s %d %d chain=%s' % (mdia[0], mdia[2], 'packets', int(time.time()), mangle_def_input_accept_pkt, mdia[1])
    print 'iptables.%s.%s.%s %d %d chain=%s' % (mdia[0], mdia[2], 'bytes', int(time.time()), mangle_def_input_accept_byt, mdia[1])
else:
    pass
if mangle_def_input_mark_pkt > 0:
    print 'iptables.%s.%s.%s %d %d chain=%s' % (mdim[0], mdim[2], 'packets', int(time.time()), mangle_def_input_mark_pkt, mdim[1])
    print 'iptables.%s.%s.%s %d %d chain=%s' % (mdim[0], mdim[2], 'bytes', int(time.time()), mangle_def_input_mark_byt, mdim[1])
else:
    pass
if mangle_def_input_drop_pkt > 0:
    print 'iptables.%s.%s.%s %d %d chain=%s' % (mdip[0], mdip[2], 'packets', int(time.time()), mangle_def_input_drop_pkt, mdip[1])
    print 'iptables.%s.%s.%s %d %d chain=%s' % (mdip[0], mdip[2], 'bytes', int(time.time()), mangle_def_input_drop_byt, mdip[1])
else:
    pass
if mangle_def_forward_accept_pkt > 0:
    print 'iptables.%s.%s.%s %d %d chain=%s' % (mdfa[0], mdfa[2], 'packets', int(time.time()), mangle_def_forward_accept_pkt, mdfa[1])
    print 'iptables.%s.%s.%s %d %d chain=%s' % (mdfa[0], mdfa[2], 'bytes', int(time.time()), mangle_def_forward_accept_byt, mdfa[1])
else:
    pass
if mangle_def_forward_mark_pkt > 0:
    print 'iptables.%s.%s.%s %d %d chain=%s' % (mdfm[0], mdfm[2], 'packets', int(time.time()), mangle_def_forward_mark_pkt, mdfm[1])
    print 'iptables.%s.%s.%s %d %d chain=%s' % (mdfm[0], mdfm[2], 'bytes', int(time.time()), mangle_def_forward_mark_byt, mdfm[1])
else:
    pass
if mangle_def_forward_drop_pkt > 0:
    print 'iptables.%s.%s.%s %d %d chain=%s' % (mdfd[0], mdfd[2], 'packets', int(time.time()), mangle_def_forward_drop_pkt, mdfd[1])
    print 'iptables.%s.%s.%s %d %d chain=%s' % (mdfd[0], mdfd[2], 'bytes', int(time.time()), mangle_def_forward_drop_byt, mdfd[1])
else:
    pass
if mangle_def_output_accept_pkt > 0:
    print 'iptables.%s.%s.%s %d %d chain=%s' % (mdoa[0], mdoa[2], 'packets', int(time.time()), mangle_def_output_accept_pkt, mdoa[1])
    print 'iptables.%s.%s.%s %d %d chain=%s' % (mdoa[0], mdoa[2], 'bytes', int(time.time()), mangle_def_output_accept_byt, mdoa[1])
else:
    pass
if mangle_def_output_mark_pkt > 0:
    print 'iptables.%s.%s.%s %d %d chain=%s' % (mdom[0], mdom[2], 'packets', int(time.time()), mangle_def_output_mark_pkt, mdom[1])
    print 'iptables.%s.%s.%s %d %d chain=%s' % (mdom[0], mdom[2], 'bytes', int(time.time()), mangle_def_output_mark_byt, mdom[1])
else:
    pass
if mangle_def_output_drop_pkt > 0:
    print 'iptables.%s.%s.%s %d %d chain=%s' % (mdod[0], mdod[2], 'packets', int(time.time()), mangle_def_output_drop_pkt, mdod[1])
    print 'iptables.%s.%s.%s %d %d chain=%s' % (mdod[0], mdod[2], 'bytes', int(time.time()), mangle_def_output_drop_byt, mdod[1])
else:
    pass
if mangle_def_prert_accept_pkt > 0:
    print 'iptables.%s.%s.%s %d %d chain=%s' % (mdpa[0], mdpa[2], 'packets', int(time.time()), mangle_def_prert_accept_pkt, mdpa[1])
    print 'iptables.%s.%s.%s %d %d chain=%s' % (mdpa[0], mdpa[2], 'bytes', int(time.time()), mangle_def_prert_accept_byt, mdpa[1])
else:
    pass
if mangle_def_prert_mark_pkt > 0:
    print 'iptables.%s.%s.%s %d %d chain=%s' % (mdpm[0], mdpm[2], 'packets', int(time.time()), mangle_def_prert_mark_pkt, mdpm[1])
    print 'iptables.%s.%s.%s %d %d chain=%s' % (mdpm[0], mdpm[2], 'bytes', int(time.time()), mangle_def_prert_mark_byt, mdpm[1])
else:
    pass
if mangle_def_prert_drop_pkt > 0:
    print 'iptables.%s.%s.%s %d %d chain=%s' % (mdpd[0], mdpd[2], 'packets', int(time.time()), mangle_def_prert_drop_pkt, mdpd[1])
    print 'iptables.%s.%s.%s %d %d chain=%s' % (mdpd[0], mdpd[2], 'bytes', int(time.time()), mangle_def_prert_drop_byt, mdpd[1])
else:
    pass
if mangle_def_postrt_accept_pkt > 0:
    print 'iptables.%s.%s.%s %d %d chain=%s' % (mdPa[0], mdPa[2], 'packets', int(time.time()), mangle_def_postrt_accept_pkt, mdPa[1])
    print 'iptables.%s.%s.%s %d %d chain=%s' % (mdPa[0], mdPa[2], 'bytes', int(time.time()), mangle_def_postrt_accept_byt, mdPa[1])
else:
    pass
if mangle_def_postrt_mark_pkt > 0: 
    print 'iptables.%s.%s.%s %d %d chain=%s' % (mdPm[0], mdPm[2], 'packets', int(time.time()), mangle_def_postrt_mark_pkt, mdPm[1])
    print 'iptables.%s.%s.%s %d %d chain=%s' % (mdPm[0], mdPm[2], 'bytes', int(time.time()), mangle_def_postrt_mark_byt, mdPm[1])
else:
    pass
if mangle_def_postrt_drop_pkt > 0:
    print 'iptables.%s.%s.%s %d %d chain=%s' % (mdPd[0], mdPd[2], 'packets', int(time.time()), mangle_def_postrt_drop_pkt, mdPd[1])
    print 'iptables.%s.%s.%s %d %d chain=%s' % (mdPd[0], mdPd[2], 'bytes', int(time.time()), mangle_def_postrt_drop_byt, mdPd[1])
else:
    pass
if mangle_ns1_postrt_accept_pkt > 0:
    print 'iptables.%s.%s.%s %d %d chain=%s' % (mnPa[0], mnPa[2], 'packets', int(time.time()), mangle_ns1__postrt_accept_pkt, mnPa[1])
    print 'iptables.%s.%s.%s %d %d chain=%s' % (mnPa[0], mnPa[2], 'bytes', int(time.time()), mangle_ns1__postrt_accept_byt, mnPa[1])
else:
    pass
if mangle_ns1_postrt_mark_pkt > 0:
    print 'iptables.%s.%s.%s %d %d chain=%s' % (mnPm[0], mnPm[2], 'packets', int(time.time()), mangle_ns1__postrt_mark_pkt, mnPm[1])
    print 'iptables.%s.%s.%s %d %d chain=%s' % (mnPm[0], mnPm[2], 'bytes', int(time.time()), mangle_ns1__postrt_mark_byt, mnPm[1])
else:
    pass
if mangle_ns1_postrt_drop_pkt > 0:
    print 'iptables.%s.%s.%s %d %d chain=%s' % (mnPd[0], mnPd[2], 'packets', int(time.time()), mangle_ns1__postrt_drop_pkt, mnPd[1])
    print 'iptables.%s.%s.%s %d %d chain=%s' % (mnPd[0], mnPd[2], 'bytes', int(time.time()), mangle_ns1__postrt_drop_byt, mnPd[1])
else:
    pass
if raw_def_output_accept_pkt > 0:
    print 'iptables.%s.%s.%s %d %d chain=%s' % (rdoa[0], rdoa[2], 'packets', int(time.time()), raw_def_output_accept_pkt, rdoa[1])
    print 'iptables.%s.%s.%s %d %d chain=%s' % (rdoa[0], rdoa[2], 'bytes', int(time.time()), raw_def_output_accept_byt, rdoa[1])
else:
    pass
if raw_def_output_mark_pkt > 0:
    print 'iptables.%s.%s.%s %d %d chain=%s' % (rdom[0], rdom[2], 'packets', int(time.time()), raw_def_output_mark_pkt, rdom[1])
    print 'iptables.%s.%s.%s %d %d chain=%s' % (rdom[0], rdom[2], 'bytes', int(time.time()), raw_def_output_mark_byt, rdom[1])
else:
    pass
if raw_def_output_drop_pkt > 0:
    print 'iptables.%s.%s.%s %d %d chain=%s' % (rdod[0], rdod[2], 'packets', int(time.time()), raw_def_output_drop_pkt, rdod[1])
    print 'iptables.%s.%s.%s %d %d chain=%s' % (rdod[0], rdod[2], 'bytes', int(time.time()), raw_def_output_drop_byt, rdod[1])
else:
    pass
if raw_def_prert_accept_pkt > 0:
    print 'iptables.%s.%s.%s %d %d chain=%s' % (rdpa[0], rdpa[2], 'packets', int(time.time()), raw_def_prert_accept_pkt, rdpa[1])
    print 'iptables.%s.%s.%s %d %d chain=%s' % (rdpa[0], rdpa[2], 'bytes', int(time.time()), raw_def_prert_accept_byt, rdpa[1])
else:
    pass
if raw_def_prert_mark_pkt > 0:
    print 'iptables.%s.%s.%s %d %d chain=%s' % (rdpm[0], rdpm[2], 'packets', int(time.time()), raw_def_prert_mark_pkt, rdpm[1])
    print 'iptables.%s.%s.%s %d %d chain=%s' % (rdpm[0], rdpm[2], 'bytes', int(time.time()), raw_def_prert_mark_byt, rdpm[1])
else:
    pass
if raw_def_prert_drop_pkt > 0:
    print 'iptables.%s.%s.%s %d %d chain=%s' % (rdpd[0], rdpd[2], 'packets', int(time.time()), raw_def_prert_drop_pkt, rdpd[1])
    print 'iptables.%s.%s.%s %d %d chain=%s' % (rdpd[0], rdpd[2], 'bytes', int(time.time()), raw_def_prert_drop_byt, rdpd[1])
else:
    pass