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

    PARAMS = [iptc.Table.FILTER, iptc.Table.NAT, iptc.Table.MANGLE, iptc.Table.RAW]
        
    def __init__(self):
        self.table = iptc.Table(iptc.Table.FILTER)
        self.input_chain = iptc.Chain( )



def main():
    while True:
        time.sleep(INTERVAL)

if __name__ == "__main__":
    sys.exit(main())

# <METRIC> <UNIX_TIMESTAMP> <VALUE>
# Rules Matched / drops / packets / bytes
#!/usr/bin/python

import time
import iptc
import re

params = [iptc.Table.FILTER, iptc.Table.NAT, iptc.Table.MANGLE, iptc.Table.RAW]

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


for param in params:
    table = iptc.Table(param)
    for chain in table.chains:
        comments = []
        pkt = 0
        byt = 0
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
                            nat_def_input_accept_pkt += packets
                            nat_def_input_accept_byt += bytes
                        elif str(rule_tgt_name).lower() == 'mark':
                            nat_def_input_mark_pkt += packets
                            nat_def_input_mark_byt += bytes
                        elif str(rule_tgt_name).lower() == 'drop':
                            nat_def_input_drop_pkt += packets
                            nat_def_input_drop_byt += bytes
                        else:
                            pass
                    elif str(chainz).lower() == 'output':
                        if str(rule_tgt_name).lower() == 'accept':
                            nat_def_output_accept_pkt += packets
                            nat_def_output_accept_byt += bytes
                        elif str(rule_tgt_name).lower() == 'mark':
                            nat_def_output_mark_pkt += packets
                            nat_def_output_mark_byt += bytes
                        elif str(rule_tgt_name).lower() == 'drop':
                            nat_def_output_drop_pkt += packets
                            nat_def_output_drop_byt += bytes
                        else:
                            pass
                    elif str(chainz).lower() == 'preroute':
                        if str(rule_tgt_name).lower() == 'accept':
                            nat_def_prert_accept_pkt += packets
                            nat_def_prert_accept_byt += bytes
                        elif str(rule_tgt_name).lower() == 'mark':
                            nat_def_prert_mark_pkt += packets
                            nat_def_prert_mark_byt += bytes
                        elif str(rule_tgt_name).lower() == 'drop':
                            nat_def_prert_drop_pkt += packets
                            nat_def_prert_drop_byt += bytes
                        else:
                            pass
                    elif str(chainz).lower() == 'postroute':
                        if str(rule_tgt_name).lower() == 'accept':
                            nat_def_postrt_accept_pkt += packets
                            nat_def_postrt_accept_byt += bytes
                        elif str(rule_tgt_name).lower() == 'mark':
                            nat_def_postrt_mark_pkt += packets
                            nat_def_postrt_mark_byt += bytes
                        elif str(rule_tgt_name).lower() == 'drop':
                            nat_def_postrt_drop_pkt += packets
                            nat_def_postrt_drop_byt += bytes
                        else:
                            pass
                    elif str(chainz).lower() == 'ns1_postroute':
                        if str(rule_tgt_name).lower() == 'accept':
                            nat_def_ns1_postrt_accept_pkt += packets
                            nat_def_ns1_postrt_accept_byt += bytes
                        elif str(rule_tgt_name).lower() == 'mark':
                            nat_def_ns1_postrt_mark_pkt += packets
                            nat_def_ns1_postrt_mark_byt += bytes
                        elif str(rule_tgt_name).lower() == 'drop':
                            nat_def_ns1_postrt_drop_pkt += packets
                            nat_def_ns1_postrt_drop_byt += bytes
                        else:
                            pass
                    else:
                        pass
                elif str(param).lower() == 'mangle':
                    if str(chainz).lower() == 'input':
                        if str(rule_tgt_name).lower() == 'accept':
                            mangle_def_input_accept_pkt += packets
                            mangle_def_input_accept_byt += bytes
                        elif str(rule_tgt_name).lower() == 'mark':
                            mangle_def_input_mark_pkt += packets
                            mangle_def_input_mark_byt += bytes
                        elif str(rule_tgt_name).lower() == 'drop':
                            mangle_def_input_drop_pkt += packets
                            mangle_def_input_drop_byt += bytes
                        else:
                            pass
                    elif str(chainz).lower() == 'forward':
                        if str(rule_tgt_name).lower() == 'accept':
                            mangle_def_forward_accept_pkt += packets
                            mangle_def_forward_accept_byt += bytes
                        elif str(rule_tgt_name).lower() == 'mark':
                            mangle_def_forward_mark_pkt += packets
                            mangle_def_forward_mark_byt += bytes
                        elif str(rule_tgt_name).lower() == 'drop':
                            mangle_def_forward_drop_pkt += packets
                            mangle_def_forward_drop_byt += bytes
                        else:
                            pass
                    elif str(chainz).lower() == 'output':
                        if str(rule_tgt_name).lower() == 'accept':
                            mangle_def_output_accept_pkt += packets
                            mangle_def_output_accept_byt += bytes
                        elif str(rule_tgt_name).lower() == 'mark':
                            mangle_def_output_mark_pkt += packets
                            mangle_def_output_mark_byt += bytes
                        elif str(rule_tgt_name).lower() == 'drop':
                            mangle_def_output_drop_pkt += packets
                            mangle_def_output_drop_byt += bytes
                        else:
                            pass
                    elif str(chainz).lower() == 'preroute':
                        if str(rule_tgt_name).lower() == 'accept':
                            mangle_def_prert_accept_pkt += packets
                            mangle_def_prert_accept_byt += bytes
                        elif str(rule_tgt_name).lower() == 'mark':
                            mangle_def_prert_mark_pkt += packets
                            mangle_def_prert_mark_byt += bytes
                        elif str(rule_tgt_name).lower() == 'drop':
                            mangle_def_prert_drop_pkt += packets
                            mangle_def_prert_drop_byt += bytes
                        else:
                            pass
                    elif str(chainz).lower() == 'postroute':
                        if str(rule_tgt_name).lower() == 'accept':
                            mangle_def_postrt_accept_pkt += packets
                            mangle_def_postrt_accept_byt += bytes
                        elif str(rule_tgt_name).lower() == 'mark':
                            mangle_def_postrt_mark_pkt += packets
                            mangle_def_postrt_mark_byt += bytes
                        elif str(rule_tgt_name).lower() == 'drop':
                            mangle_def_postrt_drop_pkt += packets
                            mangle_def_postrt_drop_byt += bytes
                        else:
                            pass
                    elif str(chainz).lower() == 'ns1_postroute':
                        if str(rule_tgt_name).lower() == 'accept':
                            mangle_def_ns1_postrt_accept_pkt += packets
                            mangle_def_ns1_postrt_accept_byt += bytes
                        elif str(rule_tgt_name).lower() == 'mark':
                            mangle_def_ns1_postrt_mark_pkt += packets
                            mangle_def_ns1_postrt_mark_byt += bytes
                        elif str(rule_tgt_name).lower() == 'drop':
                            mangle_def_ns1_postrt_drop_pkt += packets
                            mangle_def_ns1_postrt_drop_byt += bytes
                        else:
                            pass
                    else:
                        pass
                elif string(param).lower() == 'raw':
                    if str(chainz).lower() == 'output':
                        if str(rule_tgt_name).lower() == 'accept':
                            nat_def_output_accept_pkt += packets
                            nat_def_output_accept_byt += bytes
                        elif str(rule_tgt_name).lower() == 'mark':
                            nat_def_output_mark_pkt += packets
                            nat_def_output_mark_byt += bytes
                        elif str(rule_tgt_name).lower() == 'drop':
                            nat_def_output_drop_pkt += packets
                            nat_def_output_drop_byt += bytes
                        else:
                            pass
                    elif str(chainz).lower() == 'preroute':
                        if str(rule_tgt_name).lower() == 'accept':
                            nat_def_prert_accept_pkt += packets
                            nat_def_prert_accept_byt += bytes
                        elif str(rule_tgt_name).lower() == 'mark':
                            nat_def_prert_mark_pkt += packets
                            nat_def_prert_mark_byt += bytes
                        elif str(rule_tgt_name).lower() == 'drop':
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
    print fdia[0], fdia[1], fdia[2], 'packets', int(time.time()), filter_def_input_accept_pkt
    print fdia[0], fdia[1], fdia[2], 'bytes', int(time.time()), filter_def_input_accept_byt
else:
    pass
if filter_def_input_mark_pkt > 0:
    print fdim[0], fdim[1], fdim[2], 'packets', int(time.time()), filter_def_input_mark_pkt
    print fdim[0], fdim[1], fdim[2], 'bytes', int(time.time()), filter_def_input_mark_byt
else:
    pass
if filter_def_input_drop_pkt > 0:
    print fdid[0], fdid[1], fdid[2], 'packets', int(time.time()), filter_def_input_drop_pkt
    print fdid[0], fdid[1], fdid[2], 'bytes', int(time.time()), filter_def_input_drop_byt
else:
    pass
if filter_def_forward_accept_pkt > 0:
if filter_def_forward_accept_byt > 0:
if filter_def_forward_mark_pkt > 0:
if filter_def_forward_mark_byt > 0:
if filter_def_forward_drop_pkt > 0:
if filter_def_forward_drop_byt > 0:
if filter_def_output_accept_pkt > 0:
if filter_def_output_accept_byt > 0:
if filter_def_output_mark_pkt > 0:
if filter_def_output_mark_byt > 0:
if filter_def_output_drop_pkt > 0:
if filter_def_output_drop_byt > 0:
if filter_ns1_input_accept_pkt > 0:
if filter_ns1_input_accept_byt > 0:
if filter_ns1_input_mark_pkt > 0:
if filter_ns1_input_mark_byt > 0:
if filter_ns1_input_drop_pkt > 0:
if filter_ns1_input_drop_byt > 0:
if filter_ns1_forward_accept_pkt > 0:
if filter_ns1_forward_accept_byt > 0:
if filter_ns1_forward_mark_pkt > 0:
if filter_ns1_forward_mark_byt > 0:
if filter_ns1_forward_drop_pkt > 0:
if filter_ns1_forward_drop_byt > 0:
if filter_ns1_output_accept_pkt > 0:
if filter_ns1_output_accept_byt > 0:
if filter_ns1_output_mark_pkt > 0:
if filter_ns1_output_mark_byt > 0:
if filter_ns1_output_drop_pkt > 0:
if filter_ns1_output_drop_byt > 0:
if nat_def_input_accept_pkt > 0:
if nat_def_input_accept_byt > 0:
if nat_def_input_mark_pkt > 0:
if nat_def_input_mark_byt > 0:
if nat_def_input_drop_pkt > 0:
if nat_def_input_drop_byt > 0:
if nat_def_output_accept_pkt > 0:
if nat_def_output_accept_byt > 0:
if nat_def_output_mark_pkt > 0:
if nat_def_output_mark_byt > 0:
if nat_def_output_drop_pkt > 0:
if nat_def_output_drop_byt > 0:
if nat_def_prert_accept_pkt > 0:
if nat_def_prert_accept_byt > 0:
if nat_def_prert_mark_pkt > 0:
if nat_def_prert_mark_byt > 0:
if nat_def_prert_drop_pkt > 0:
if nat_def_prert_drop_byt > 0:
if nat_def_postrt_accept_pkt > 0:
if nat_def_postrt_accept_byt > 0:
if nat_def_postrt_mark_pkt > 0:
if nat_def_postrt_mark_byt > 0:
if nat_def_postrt_drop_pkt > 0:
if nat_def_postrt_drop_byt > 0:
if nat_ns1_postrt_accept_pkt > 0:
if nat_ns1_postrt_accept_byt > 0:
if nat_ns1_postrt_mark_pkt > 0:
if nat_ns1_postrt_mark_byt > 0:
if nat_ns1_postrt_drop_pkt > 0:
if nat_ns1_postrt_drop_byt > 0:
if mangle_def_input_accept_pkt > 0:
if mangle_def_input_accept_byt > 0:
if mangle_def_input_mark_pkt > 0:
if mangle_def_input_mark_byt > 0:
if mangle_def_input_drop_pkt > 0:
if mangle_def_input_drop_byt > 0:
if mangle_def_forward_accept_pkt > 0:
if mangle_def_forward_accept_byt > 0:
if mangle_def_forward_mark_pkt > 0:
if mangle_def_forward_mark_byt > 0:
if mangle_def_forward_drop_pkt > 0:
if mangle_def_forward_drop_byt > 0:
if mangle_def_output_accept_pkt > 0:
if mangle_def_output_accept_byt > 0:
if mangle_def_output_mark_pkt > 0:
if mangle_def_output_mark_byt > 0:
if mangle_def_output_drop_pkt > 0:
if mangle_def_output_drop_byt > 0:
if mangle_def_prert_accept_pkt > 0:
if mangle_def_prert_accept_byt > 0:
if mangle_def_prert_mark_pkt > 0:
if mangle_def_prert_mark_byt > 0:
if mangle_def_prert_drop_pkt > 0:
if mangle_def_prert_drop_byt > 0:
if mangle_def_postrt_accept_pkt > 0:
if mangle_def_postrt_accept_byt > 0:
if mangle_def_postrt_mark_pkt > 0:
if mangle_def_postrt_mark_byt > 0:
if mangle_def_postrt_drop_pkt > 0:
if mangle_def_postrt_drop_byt > 0:
if mangle_ns1_postrt_accept_pkt > 0:
if mangle_ns1_postrt_accept_byt > 0:
if mangle_ns1_postrt_mark_pkt > 0:
if mangle_ns1_postrt_mark_byt > 0:
if mangle_ns1_postrt_drop_pkt > 0:
if mangle_ns1_postrt_drop_byt > 0:
if raw_def_output_accept_pkt > 0:
if raw_def_output_accept_byt > 0:
if raw_def_output_mark_pkt > 0:
if raw_def_output_mark_byt > 0:
if raw_def_output_drop_pkt > 0:
if raw_def_output_drop_byt > 0:
if raw_def_prert_accept_pkt > 0:
if raw_def_prert_accept_byt > 0:
if raw_def_prert_mark_pkt > 0:
if raw_def_prert_mark_byt > 0:
if raw_def_prert_drop_pkt > 0:
if raw_def_prert_drop_byt > 0:
'''
'''
params = [iptc.Table.FILTER, iptc.Table.NAT, iptc.Table.MANGLE, iptc.Table.RAW]
for param in params:
    table = iptc.Table(param)
    print '\n\n\n>>>>>>>>' +  str(param).upper()
    for chain in table.chains:
        print "======================="
        print "Chain ", chain.name
        for rule in chain.rules:
            print "Rule", "proto:", rule.protocol, "src:", rule.src, "dst:", \
                  rule.dst, "in:", rule.in_interface, "out:", rule.out_interface,
            print "Matches:",
            for match in rule.matches:
                print match.name,
            print "Target:",
            print rule.target.name
    print "======================="


#                print "FilterType: %s\tChain: %10s\tProtocol: %s\tSource: %31s\tDport: %11s\tState: %18s\tTarget: %s\t%s\t%d\t%d" % (str(param).lower(), chainz.lower(), rule.protocol, rule.src, match.dport, match.state, rule_target_name, 'packets', int(time.time()), bytes)
#                print str(param).lower(), chainz.lower(), rule.protocol, rule.src, match.dport, match.state, rule.dst, rule.in_interface, rule.out_interface, rule_target_name, 'packets', int(time.time()), pkt
#                if str(chainz).lower() == 'input' and str(rule_target_name).lower() == 'accept':
#                    print "hai"
#                elif str(chainz).lower() == 'input' and str(rule_target_name).lower() == 'ns1_input':
#                    print "ho"
                print '%s\t%s\t%23s\t%18s\t%15d\t%d' % (str(param).lower(), str(chainz).lower(), str(rule_target_name).lower(), 'packets', int(time.time()), packets)
                print '%s\t%s\t%23s\t%18s\t%15d\t%d' % (str(param).lower(), str(chainz).lower(), str(rule_target_name).lower(), 'bytes', int(time.time()), bytes)
'''

<<<<<<< Upstream, based on origin/master
=======
'''
>>>>>>>>FILTER
=======================
Chain  INPUT
=======================
Chain  FORWARD
=======================
Chain  OUTPUT
=======================
Chain  NS1_FORWARD_1449246906
=======================
Chain  NS1_INPUT_1449246906
=======================
Chain  NS1_OUTPUT_1449246906
=======================

>>>>>>>>NAT
=======================
Chain  PREROUTING
=======================
Chain  INPUT
=======================
Chain  OUTPUT
=======================
Chain  POSTROUTING
=======================
Chain  NS1_POSTROUTING_1449246906
=======================

>>>>>>>>MANGLE
=======================
Chain  PREROUTING
=======================
Chain  INPUT
=======================
Chain  FORWARD
=======================
Chain  OUTPUT
=======================
Chain  POSTROUTING
=======================
Chain  NS1_PREROUTING_1449246906
=======================

>>>>>>>>RAW
=======================
Chain  PREROUTING
=======================
Chain  OUTPUT
=======================

'''
