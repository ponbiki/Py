#!/usr/bin/env python
#
# bgp_status.py -- a collector for tcollector/OpenTSDB
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

''' BGP Up Down Status Collector'''

import sys
import time
import os
import psutil

INTERVAL = 30
BGP_CONF = '/etc/nsone/bgp.conf'
BGP_CONF_V6 = '/etc/nsone/bgp.conf-v6'
BGP_UP = 'bgp-up.conf'
BGP_UP_v6 = 'bgp-up.conf-v6'
PUERTO = 179


def check_BGP():
    '''
    Checks bgp.conf for up / down, and the sockets for IPv4 BGP established.
    Returns in the format of:
    bgp.status <time> <0|1> protocol=IPv4
    '''
    thyme = int(time.time())
    v4_up = 0
    if os.readlink(BGP_CONF) != BGP_UP:
        print 'bgp.status %d %d protocol=IPv4' % (thyme, v4_up)
    else:
        for c in psutil.net_connections(kind='inet'):
            if c.raddr:
                if c.raddr[1] == PUERTO:
                    if c.status == 'ESTABLISHED':
                        v4_up = 1
                    else:
                        print >> sys.stderr, 'IPv4 not ESTABLISHED: ', c
        print 'bgp.status %d %d protocol=IPv4' % (thyme, v4_up)


def check_BGP6():
    '''
    Checks bgp.conf for up / down, and the sockets for IPv6 BGP established.
    Returns in the format of:
    bgp.status <time> <0|1> protocol=IPv6
    '''
    thyme = int(time.time())
    v6_up = 0
    if os.readlink(BGP_CONF_V6) != BGP_UP_v6:
        print 'bgp.status %d %d protocol=IPv6' % (thyme, v6_up)
    else:
        for c in psutil.net_connections(kind='inet'):
            if c.raddr:
                if c.raddr[1] == PUERTO:
                    if ':' in c.raddr[0]:
                        if c.status == 'ESTABLISHED':
                            v6_up = 1
                        else:
                            print >> sys.stderr, 'IPv6 not ESTABLISHED: ', c
        print 'bgp.status %d %d protocol=IPv6' % (thyme, v6_up)


def main():
    while True:
        check_BGP()
        check_BGP6()
        sys.stdout.flush()
        if not INTERVAL or INTERVAL < 1:
            break
        else:
            time.sleep(INTERVAL)

if __name__ == '__main__':
    sys.exit(main())
