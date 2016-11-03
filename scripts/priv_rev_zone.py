import ipaddress


def priv_rev(zone):
    ipv4 = '.in-addr.arpa'
    ipv6 = '.ip6.arpa'
    if zone.rstrip('.').lower().endswith(ipv4):
        addr_list = [i for i in reversed(zone[:-len(ipv4)].split('.'))]
        while len(addr_list) < 4:
            addr_list.append('0')
        try:
            return ipaddress.ip_address(unicode('.'.join(addr_list).split('/')[0])).is_private
        except:
            return False
    elif zone.rstrip('.').lower().endswith(ipv6):
        flipped_rev6 = ''.join(reversed(zone[:-len(ipv6)].split('.')))
        flipped_rev6 = [flipped_rev6[i:i + 4] for i in xrange(0, len(flipped_rev6), 4)]
        new_flipped_rev6 = []
        for j in flipped_rev6:
            while len(j) < 4:
                j += str(0)
            new_flipped_rev6.append(j)
        if len(new_flipped_rev6) < 8:
            new_flipped_rev6.append(':')
        ipv6_final = unicode(':'.join(new_flipped_rev6))
        try:
            return ipaddress.ip_address(ipv6_final).is_private
        except:
            return False
