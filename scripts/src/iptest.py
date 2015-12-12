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
'''
for param in params:
    table = iptc.Table(param)
    for chain in table.chains:
        pkt = 0
        byt = 0
        chn_pkt_accept = 0
        chn_pkt_drop   = 0
        if re.match('NS1', chain.name):
            p = chain.name.split('_')
            chainz = p[0] + '_' + p[1]
        else:
            chainz = chain.name
#        print str(param), chainz.lower()
        for rule in chain.rules:
            rule_target_name = rule.target.name
            print str(param), chainz, rule_target_name
            #pkt = 0
            #byt = 0
            for match in rule.matches:
                if match.name == "comment":
                    #gonna call a second method to hilight this
                    pass
                match_name = match.name
                rule_target_name = rule.target.name
                (packets, bytes) = rule.get_counters()
                if packets <= 0:
                    pass
                else:
                    pkt += packets
                    byt += bytes
                    print chainz
'''
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
            if str(rule.target.name).lower() == 'mark':
                pass
            else:
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
                    print str(param).lower(), chainz.lower(), rule_target_name, 'packets', int(time.time()), byt
#                    print str(param).lower(), chainz.lower(), rule_target_name, 'bytes', int(time.time()), pkt

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
'''

