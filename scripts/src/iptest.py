#!/usr/bin/python

import time
import sys
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

table = iptc.Table(iptc.Table.FILTER)
chain = iptc.Chain(table, 'INPUT')
for rule in chain.rules:
 (packets, bytes) = rule.get_counters()
 print packets
sys.stdout.flush()
time.sleep(1)
table.refresh()
for rule in chain.rules:
    (packets, bytes) = rule.get_counters()
    print packets

'''
#!/usr/bin/python

import time
import sys
import iptc

table = iptc.Table(iptc.Table.FILTER)
for chain in table.chains:
    print(chain.name)
    print(int(time.time()))




while True:
   for chain in table.chains:
      chain = iptc.Chain(table, chain.name)
      table.refresh()
      for rule in chain.rules:
         (packets, bytes) = rule.get_counters()
         print chain.name
         print packets
         print bytes
   time.sleep(1)
   sys.stdout.flush()
while True:
   table = iptc.Table(iptc.Table.FILTER)
   chain = iptc.Chain(table, 'OUTPUT')
   table.refresh()
   for rule in chain.rules:
      (packets, bytes) = rule.get_counters()
      print packets
   time.sleep(1)
   sys.stdout.flush()

'''