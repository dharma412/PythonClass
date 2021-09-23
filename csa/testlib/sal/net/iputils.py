"""These functions are useful for dealing with CIDR notation.

Some take a CIDR-notation string ('IP/bits'), and return
an IP address and mask

Others take an IP address and mask, and return CIDR string.

mask == 0 -> '/bits' and no '/bits' -> mask = 0."""
from __future__ import absolute_import


#: Reference Symbols: iputils

class IPFormatError(Exception):
    pass


import socket, struct


def inet_atohm(net):
    """inet_atohm(net) -> long int int
    accepts IP/bits string
    returns IP address and netmask in host byte order
    type(ip) is long int and type(mask) is int
    """
    mask = 0
    ip_bits = net.split('/')
    ip = ip_bits[0]
    if ip == '255.255.255.255':
        ip = 0xffffffffL
    else:
        ip = socket.inet_aton(ip)
        ip = struct.unpack("!I", ip)[0]
    if len(ip_bits) > 1:
        bits = int(ip_bits[1])
        if bits > 32:
            raise Exception, "%s has invalid number of bits" % net
        if bits > 1:
            mask = ~(2 ** (32 - bits) - 1)
        elif bits == 1:
            mask = 0x80000000L
        ip = ip & mask
    return ip, mask


def inet_atonm(net):
    """inet_atohm(net) -> long int int
    accepts IP/bits string
    returns IP address and netmask in network byte order
    """
    ip, mask = inet_atohm(net)
    ip = ntohl(ip)
    mask = ntohl(mask)
    return ip, mask


def inet_hmtoa(ip, mask=0L):
    """inet_atohm(ip, mask=0) -> string
    accepts IP address and netmask in host byte order
    returns IP/bits string
    """
    p = struct.pack('!I', ip & 0xffffffff)
    net = socket.inet_ntoa(p)
    if mask:
        bits = 32
        mask = ~mask
        mask &= 0xffffffffL  # paranoia?
        while mask:
            bits = bits - 1
            mask = mask >> 1
            if bits == 0:
                break
        net += '/%d' % bits
    return net


def inet_nmtoa(ip, mask=0L):
    """inet_atohm(ip, mask=0) -> string
    accepts IP address and netmask in network byte order
    returns IP/bits string
    """
    ip = htonl(ip)
    mask = htonl(mask)
    return inet_hmtoa(ip, mask)


# In general, python likes to use Long ints, but the socket
# module functions like to use ints.  These functions both
# swap bytes (if necessary) and convert from Long int to int.

def htonl(ip):
    """htonl(ip) -> int
    accepts IP address in host byte order as long int
    returns IP address in network byte order as int
    """
    p = struct.pack('!I', ip & 0xffffffff)
    return struct.unpack('i', p)[0]


def ntohl(ip):
    """ntohl(ip) -> int
    accepts IP address in network byte order as long int
    returns IP address in host byte order as int
    """
    p = struct.pack('I', ip & 0xffffffff)
    return struct.unpack('!i', p)[0]


def make_ip_range(ip1, num_ips):
    """ Take one IP and the number of IPs in the range, and output
        an IP range. This function only works within /24 address ranges.
    """
    if num_ips == 0:
        raise ValueError, "num_ips cannot be 0, as an IP range " \
                          "cannot have 0 IPs"
    ret_range = []

    int_ip1 = inet_atohm(ip1)[0]
    int_ip2 = int_ip1 + num_ips
    ip2 = inet_hmtoa(int_ip2, 0)

    ip1_quad = ip1.split('.')
    ip2_quad = ip2.split('.')

    i = 0
    while i < 3:
        if ip1_quad[i] != ip2_quad[i]:
            raise ValueError, "make_ip_range() only works within " \
                              "/24 network addresses"
        ret_range.append(ip1_quad[i])
        i += 1

    ret_range.append('%s-%s' % (ip1_quad[i], ip2_quad[i]))
    return '.'.join(ret_range)


def make_cidr_range(ip1, num_ips):
    """ Take one IP and the number of IPs in the range, and output
        a CIDR range. The number of IPs must be a power of 2.
    """
    int_ip1 = inet_atohm(ip1)[0]
    return inet_hmtoa(int_ip1, -num_ips)


# Simple class to store a range of IPs
# TODO: This currently does not handle bad input well
import random


### TODO: This really could use some algorithmic improvements
###       as certain inputs like IPs('1.0.0.0/8') lead to massive
###       amounts of stored IPs and take forever to compute

class IPs:
    """ Simple class to store a range of IPs or CIDR ranges"""

    def __init__(self, ip):
        """ Take an ip or range of ips and break them out into a list that's
            stored in this object. Also connect unconnected IP ranges with
            commas like: 1.2.3-4.4-5,2.3.5-6.23-34 """
        self._ip_list = []
        ip_ranges = ip.split(',')
        for ip_range in ip_ranges:
            if '/' in ip_range:
                low, num_ips = inet_atohm(ip_range)
                range_len = (-num_ips - 1)
                high = low + range_len
                for addr in range(low, high + 1):
                    self._ip_list.append(inet_hmtoa(addr))
            elif ip_range.count('.') == 3:
                range_fields = self.parse_ip(ip_range)
                self.compile_ip_list(range_fields)
            elif '/' in ip_range:
                low, num_ips = inet_atohm(ip_range)
                range_len = (-num_ips - 1)
                high = low + range_len
                for addr in range(low, high + 1):
                    self._ip_list.append(inet_hmtoa(addr))
            else:
                raise IPFormatError, "%s: bad ip format" % ip_range

        self.num_ips = len(self._ip_list)
        self.curr_ip = 0

    def rand_ip(self):
        """ Grab a random IP from the IP list """
        return self._ip_list[random.randrange(0, self.num_ips)]

    def next_ip(self):
        """ Grab the next IP from the list, going in a round-robin
            like fashion. """
        retval = self._ip_list[self.curr_ip]
        self.curr_ip = (self.curr_ip + 1) % self.num_ips
        return retval

    def parse_ip(self, ip):
        """ Break up the psuedo cidr notation into a list of 4 ranges (tuples) """
        fields = ip.split('.')
        range_fields = []
        if len(fields) != 4: raise Exception, "%s: bad ip format" % ip
        for field in fields:
            if field.find('-') != -1:
                start, end = field.split('-')
            else:
                start, end = field, field
            range_fields.append((int(start), int(end)))
        return range_fields

    def compile_ip_list(self, range_fields, ip_frag=''):
        """ Take the list of 4 ranges, and expand them recursively until all IPs exist in self._ip_list """
        s, e = range_fields[0]
        for i in range(s, e + 1):
            if len(range_fields) == 1 and ip_frag:
                self._ip_list.append('%s%s' % (ip_frag, str(i)))
            else:
                self.compile_ip_list(range_fields[1:], '%s%s' % (ip_frag, str(i) + '.'))


def expand_ip_list(ip_list, include_others=True):
    """ Expand a list of IPs, IP ranges, CIDR notation ranges, and hostnames into
        a list of single IPs and a list of hostnames
    """
    ret_ip_list = []
    for ip_hostname in ip_list:
        try:
            ret_ip_list.extend(IPs(ip_hostname)._ip_list)
        except IPFormatError, ipfe:
            # Discard or include other non-IPs in the return list?
            if include_others:
                ret_ip_list.append(ip_hostname)
            else:
                raise ipfe
    return ret_ip_list
