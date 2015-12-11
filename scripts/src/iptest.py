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
        self.input_chain = iptc.Chain( )



def main():
    while True:
        time.sleep(INTERVAL)

if __name__ == "__main__":
    sys.exit(main())

# <METRIC> <UNIX_TIMESTAMP> <VALUE>
# Rules Matched / drops / packets / bytes

params = [iptc.Table.FILTER, iptc.Table.NAT, iptc.Table.MANGLE, iptc.Table.RAW]
for param in params:
    table = iptc.Table(param)
    for chain in table.chains:
        comment_cnt = 0
        pkt = 0
        byt = 0
        if re.match('NS1', chain.name):
            p = chain.name.split('_')
            chainz = p[0] + '_' + p[1]
        else:
            chainz = chain.name
        for rule in chain.rules:
#            print rule.protocol, rule.src, rule.dst, rule.in_interface, rule.out_interface
            for match in rule.matches:
                if match.name == "comment":
                    comment = match.comment.replace('\s', '_')
                else:
                    comment_cnt += 1
                    comment = "no_comment" + str(comment_cnt) + "_" + str(param)
                match_name = match.name
                rule_target_name = rule.target.name
                (packets, bytes) = rule.get_counters()
                pkt += packets
                byt += bytes
                print str(param).lower(), chainz.lower(), comment, 'packets', int(time.time()), byt
                print str(param).lower(), chainz.lower(), comment, 'bytes', int(time.time()), pkt
