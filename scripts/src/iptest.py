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

                
'''
-P INPUT DROP
-P FORWARD DROP
-P OUTPUT ACCEPT
-N NS1_FORWARD_1449246906
-N NS1_INPUT_1449246906
-N q
-A INPUT -s 192.168.50.200/32 -p tcp -m tcp --dport 6379 -m state --state NEW -j ACCEPT
-A INPUT -j NS1_INPUT_1449246906
-A INPUT -p tcp -m tcp --dport 666 -m comment --comment "evil port" -j DROP
-A FORWARD -j NS1_FORWARD_1449246906
-A OUTPUT -j NS1_OUTPUT_1449246906
-A NS1_INPUT_1449246906 -i lo -j ACCEPT
-A NS1_INPUT_1449246906 -p icmp -m icmp --icmp-type 8 -j ACCEPT
-A NS1_INPUT_1449246906 -p icmp -m icmp --icmp-type 11 -j ACCEPT
-A NS1_INPUT_1449246906 -p udp -m udp --dport 33434:33534 -j ACCEPT
-A NS1_INPUT_1449246906 -m state --state RELATED,ESTABLISHED -j ACCEPT
-A NS1_INPUT_1449246906 -p tcp -m tcp --dport 22 -m state --state NEW -j ACCEPT
-A NS1_INPUT_1449246906 -p tcp -m tcp --dport 5099 -m state --state NEW -j ACCEPT
-A NS1_INPUT_1449246906 -s 192.168.50.200/32 -p tcp -m tcp --dport 22 -m state --state NEW -j ACCEPT
-A NS1_INPUT_1449246906 -s 192.168.50.200/32 -p udp -m udp --dport 60000:61000 -j ACCEPT
-A NS1_INPUT_1449246906 -s 192.168.50.200/32 -p tcp -m tcp --dport 5099 -m state --state NEW -j ACCEPT
-A NS1_INPUT_1449246906 -p udp -m udp --dport 60000:61000 -j ACCEPT
-A NS1_INPUT_1449246906 -s 192.168.50.200/32 -p tcp -m tcp --dport 22 -m state --state NEW -j ACCEPT
-A NS1_INPUT_1449246906 -s 192.168.50.201/32 -p tcp -m tcp --dport 22 -m state --state NEW -j ACCEPT
-A NS1_INPUT_1449246906 -s 192.168.50.210/32 -p tcp -m tcp --dport 22 -m state --state NEW -j ACCEPT
-A NS1_INPUT_1449246906 -s 67.208.82.116/32 -p tcp -m tcp --dport 22 -m state --state NEW -j ACCEPT
-A NS1_INPUT_1449246906 -p tcp -m tcp --dport 53 -m state --state NEW -j ACCEPT
-A NS1_INPUT_1449246906 -p udp -m udp --dport 53 -j ACCEPT
-A NS1_INPUT_1449246906 -p tcp -m tcp --dport 53 -m state --state NEW -j ACCEPT
-A NS1_INPUT_1449246906 -p udp -m udp --dport 53 -j ACCEPT
-A NS1_INPUT_1449246906 -p tcp -m tcp --dport 8080 -m state --state NEW -j ACCEPT
-A NS1_INPUT_1449246906 -s 192.168.50.200/32 -p tcp -m tcp --dport 5671:5672 -m state --state NEW -j ACCEPT
-A NS1_INPUT_1449246906 -s 192.168.50.201/32 -p tcp -m tcp --dport 5671:5672 -m state --state NEW -j ACCEPT
-A NS1_INPUT_1449246906 -s 192.168.50.210/32 -p tcp -m tcp --dport 5671:5672 -m state --state NEW -j ACCEPT
-A NS1_INPUT_1449246906 -s 67.208.82.116/32 -p tcp -m tcp --dport 5671:5672 -m state --state NEW -j ACCEPT
-A NS1_INPUT_1449246906 -s 192.168.50.220/32 -p tcp -m tcp --dport 5671:5672 -m state --state NEW -j ACCEPT
-A NS1_INPUT_1449246906 -s 192.168.50.200/32 -p tcp -m tcp --dport 6379 -m state --state NEW -j ACCEPT
-A NS1_INPUT_1449246906 -s 192.168.50.200/32 -p tcp -m tcp --dport 6379 -m state --state NEW -j ACCEPT
-A NS1_INPUT_1449246906 -s 192.168.50.210/32 -p tcp -m tcp --dport 6379 -m state --state NEW -j ACCEPT
-A NS1_INPUT_1449246906 -s 192.168.50.200/32 -p udp -m udp --dport 53000 -j ACCEPT
-A NS1_INPUT_1449246906 -s 192.168.50.210/32 -p udp -m udp --dport 53000 -j ACCEPT
-A NS1_INPUT_1449246906 -s 192.168.50.200/32 -p tcp -m tcp --dport 27017 -m state --state NEW -j ACCEPT
-A NS1_INPUT_1449246906 -s 192.168.50.201/32 -p tcp -m tcp --dport 27017 -m state --state NEW -j ACCEPT
-A NS1_INPUT_1449246906 -s 192.168.50.200/32 -p tcp -m tcp --dport 27017 -m state --state NEW -j ACCEPT
-A NS1_INPUT_1449246906 -s 67.208.82.116/32 -p tcp -m tcp --dport 27017 -m state --state NEW -j ACCEPT
-A NS1_INPUT_1449246906 -s 192.168.50.210/32 -p tcp -m tcp --dport 27017 -m state --state NEW -j ACCEPT
-A NS1_INPUT_1449246906 -s 192.168.50.200/32 -p tcp -m tcp --dport 27017 -m state --state NEW -j ACCEPT
-A NS1_INPUT_1449246906 -s 192.168.50.200/32 -p tcp -m tcp --dport 27017 -m state --state NEW -j ACCEPT
-A NS1_INPUT_1449246906 -s 192.168.50.200/32 -p tcp -m tcp --dport 27017 -m state --state NEW -j ACCEPT
-A NS1_INPUT_1449246906 -s 192.168.50.210/32 -p tcp -m tcp --dport 27017 -m state --state NEW -j ACCEPT
-A NS1_INPUT_1449246906 -s 192.168.50.200/32 -p tcp -m tcp --dport 27017 -m state --state NEW -j ACCEPT
-A NS1_INPUT_1449246906 -s 192.168.50.200/32 -p tcp -m tcp --dport 27017 -m state --state NEW -j ACCEPT
-A NS1_INPUT_1449246906 -s 192.168.50.200/32 -p tcp -m tcp --dport 27017 -m state --state NEW -j ACCEPT
-A NS1_INPUT_1449246906 -s 192.168.50.200/32 -p tcp -m tcp --dport 27017 -m state --state NEW -j ACCEPT
-A NS1_INPUT_1449246906 -s 192.168.50.200/32 -p tcp -m tcp --dport 27017 -m state --state NEW -j ACCEPT
-A NS1_INPUT_1449246906 -s 192.168.50.210/32 -p tcp -m tcp --dport 28017 -m state --state NEW -j ACCEPT
-A NS1_INPUT_1449246906 -s 192.168.50.220/32 -p tcp -m tcp --dport 27017 -m state --state NEW -j ACCEPT
-A NS1_INPUT_1449246906 -p tcp -m tcp --dport 5300 -m state --state NEW -j ACCEPT
-A NS1_INPUT_1449246906 -p udp -m udp --dport 5300 -j ACCEPT
-A NS1_INPUT_1449246906 -p tcp -m tcp --dport 80 -m state --state NEW -j ACCEPT
-A NS1_INPUT_1449246906 -p tcp -m tcp --dport 443 -m state --state NEW -j ACCEPT
-A NS1_INPUT_1449246906 -p tcp -m tcp --dport 10000 -m state --state NEW -j ACCEPT
-A NS1_INPUT_1449246906 -p tcp -m tcp --dport 12000 -m state --state NEW -j ACCEPT
-A NS1_INPUT_1449246906 -p tcp -m tcp --dport 5400 -m state --state NEW -j ACCEPT
-A NS1_INPUT_1449246906 -p udp -m udp --dport 5400 -j ACCEPT
-A NS1_INPUT_1449246906 -s 192.168.50.200/32 -p udp -m udp --dport 11000 -j ACCEPT
-A NS1_INPUT_1449246906 -s 192.168.50.200/32 -p tcp -m tcp --dport 6379 -m state --state NEW -j ACCEPT
-A NS1_INPUT_1449246906 -s 192.168.50.200/32 -p tcp -m tcp --dport 6379 -m state --state NEW -j ACCEPT
-A NS1_INPUT_1449246906 -s 192.168.50.201/32 -p tcp -m tcp --dport 6379 -m state --state NEW -j ACCEPT
-A NS1_INPUT_1449246906 -s 192.168.50.210/32 -p tcp -m tcp --dport 6379 -m state --state NEW -j ACCEPT
-A NS1_INPUT_1449246906 -s 192.168.50.210/32 -p tcp -m tcp --dport 8090 -m state --state NEW -j ACCEPT
-A NS1_INPUT_1449246906 -s 192.168.50.200/32 -p tcp -m tcp --dport 4242 -m state --state NEW -j ACCEPT
-A NS1_INPUT_1449246906 -s 192.168.50.201/32 -p tcp -m tcp --dport 4242 -m state --state NEW -j ACCEPT
-A NS1_INPUT_1449246906 -s 192.168.50.210/32 -p tcp -m tcp --dport 4242 -m state --state NEW -j ACCEPT
-A NS1_INPUT_1449246906 -s 67.208.82.116/32 -p tcp -m tcp --dport 4242 -m state --state NEW -j ACCEPT
-A NS1_INPUT_1449246906 -s 192.168.50.220/32 -p tcp -m tcp --dport 4242 -m state --state NEW -j ACCEPT
-A NS1_INPUT_1449246906 -s 192.168.50.221/32 -p tcp -m tcp --dport 4242 -m state --state NEW -j ACCEPT
-A NS1_INPUT_1449246906 -p tcp -m tcp --dport 80 -m state --state NEW -j ACCEPT
-A NS1_INPUT_1449246906 -p tcp -m tcp --dport 7180 -m state --state NEW -j ACCEPT
-A NS1_INPUT_1449246906 -p tcp -m tcp --dport 80 -m state --state NEW -j ACCEPT
-A NS1_INPUT_1449246906 -p tcp -m tcp --dport 443 -m state --state NEW -j ACCEPT
-A NS1_INPUT_1449246906 -p tcp -m tcp --dport 8899 -m state --state NEW -j ACCEPT
-A NS1_OUTPUT_1449246906 -o lo -j ACCEPT
'''
