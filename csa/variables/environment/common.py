"""
==============================================================================
                        Common Test Environment
==============================================================================
Robot variable file for common (shared) environment between labs.
"""
import socket

NTP = 'time.ironport.com'

CLIENT_HOSTNAME = socket.gethostname()
CLIENT_IP = socket.gethostbyname(CLIENT_HOSTNAME)
CLIENT_IPV6 = 'client ipv6 not set'
if socket.has_ipv6:
    try:
        CLIENT_IPV6 = socket.getaddrinfo(CLIENT_HOSTNAME,
                                         None,
                                         socket.AF_INET6)[0][4][0]
    except Exception, e:
        print 'WARNING: IPv6 is enabled, but %s not found (%s).' \
              ' Some tests may fail.' % (CLIENT_HOSTNAME, e)
