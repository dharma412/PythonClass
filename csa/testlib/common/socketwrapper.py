#!/usr/bin/python
# $Id: //prod/main/sarf_centos/testlib/common/socketwrapper.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $
"""A wrapper on top of python socket module to support ipv6 changes"""

from socket import *
from robot.libraries.BuiltIn import BuiltIn


def gethostbyname(host, inet_mode=None):
    """Overrides gethostbyname unstion of python's socket
    module by internally using getaddrinfo() to support
    ipv6 changes.
    """
    inet_family = _get_inet_family(inet_mode)
    addr_info = getaddrinfo(host, None, inet_family)
    return addr_info[0][4][0]


def _get_inet_family(mode=None):
    robot_vars = BuiltIn().get_variables()
    inet_mode = mode or robot_vars['${INET_MODE}']
    if inet_mode and inet_mode.lower() in 'ipv6':
        return AF_INET6
    return AF_INET
