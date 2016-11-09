from ipaddress import ip_address


@staticmethod
def is_priv_revdns(input):
    _ipv4 = '.in-addr.arpa'
    _ipv6 = '.ip6.arpa'
    _fqdn = input.rstrip('.').lower()
    if _fqdn.endswith(_ipv4):
        addr_list = [i for i in reversed(_fqdn[:-len(_ipv4)].split('.'))]
        while len(addr_list) < 4:
            addr_list.append('0')
        fwd_addr = unicode('.'.join(addr_list).split('/')[0])
        try:
            return ip_address(fwd_addr).is_private
        except ValueError:
            return False
    elif _fqdn.endswith(_ipv6):
        flipped_rev6 = ''.join(reversed(_fqdn[:-len(_ipv6)].split('.')))
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
            return ip_address(ipv6_final).is_private
        except ValueError:
            return False
    else:
        return False
