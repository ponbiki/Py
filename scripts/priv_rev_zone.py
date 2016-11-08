import ipaddress


def priv_rev(zone):
    _ipv4 = '.in-addr.arpa'
    _ipv6 = '.ip6.arpa'
    if zone.rstrip('.').lower().endswith(_ipv4):
        addr_list = [i for i in reversed(zone[:-len(_ipv4)].split('.'))]
        while len(addr_list) < 4:
            addr_list.append('0')
        fwd_addr = unicode('.'.join(addr_list).split('/')[0])
        try:
            return ipaddress.ip_address(fwd_addr).is_private
        except ValueError:
            return False
    elif zone.rstrip('.').lower().endswith(_ipv6):
        flipped_rev6 = ''.join(reversed(zone[:-len(_ipv6)].split('.')))
        rev6_list = [flipped_rev6[i:i + 4] for i in xrange(0, len(flipped_rev6), 4)]
        new_rev6_list = []
        for j in rev6_list:
            while len(j) < 4:
                j += str(0)
            new_rev6_list.append(j)
        if len(new_rev6_list) < 8:
            new_rev6_list.append(':')
        ipv6_final = unicode(':'.join(new_rev6_list))
        try:
            return ipaddress.ip_address(ipv6_final).is_private
        except ValueError:
            return False
    else:
        return False
