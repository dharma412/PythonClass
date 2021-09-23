#!/usr/bin/python
# $Id: //prod/main/sarf_centos/testlib/sal/net/socket.py#1 $
"""Some convenient sockets functions used by IAF tests."""

from __future__ import absolute_import
from sal.exceptions import TimeoutError

__all__ = ["connect_inet", "connect_tcp", "connect_udp",
           "connect_unix", "check_port", "wait_for_port"]

#: Reference Symbols: iafsocket

import errno
import socket
import time
import sal.time


def connect_inet(host, port, socktype, sobject=socket.socket,
                 inet_family=socket.AF_INET):
    """Create a socket and attempt a connection.
    Return: socket object
    Error: raise socket.error if could not connect.
    """
    args = socket.getaddrinfo(str(host), int(port), inet_family, socktype)
    for family, socktype, proto, canonname, sockaddr in args:
        try:
            s = sobject(family, socktype, proto)
            s.connect(sockaddr)
        except:
            continue
        else:
            return s
    raise socket.error, "could not connect, no connections found."


def connect_tcp(host, port, sobject=socket.socket, inet_family=socket.AF_INET):
    """Create a TCP socket and connect to host:port.
    Return socket object.
    Error: raise socket.error if could not connect."""
    return connect_inet(host, port, socket.SOCK_STREAM, sobject, inet_family)


def connect_udp(host, port, sobject=socket.socket, inet_family=socket.AF_INET):
    """Create a UDP socket and connect to host:port. Connecting
    a UDP socket just sets the socket's address association.
    Return socket object.
    Error: raise socket.error if could not connect."""
    return connect_inet(host, port, socket.SOCK_DGRAM, sobject, inet_family)


def connect_unix(path, sobject=socket.socket):
    """Create a Unix socket and connect to 'path'.
    Return socket object."""
    s = sobject(socket.AF_UNIX, socket.SOCK_STREAM)
    s.connect(path)
    return s


def check_port(host, port, inet_family=socket.AF_INET):
    """Checks a TCP port on a remote host for a listener. Returns true if a
    connection is possible, false otherwise."""
    try:
        s = connect_tcp(host, port, inet_family=inet_family)
        s.close()
        return True
    except socket.error, err:
        return False


def wait_for_port(host, port, timeout=60, inet_family=socket.AF_INET):
    """Attempt to TCP connect to (host, port) for timeout seconds.
        Useful when waiting for a rebooted system.
    Raise a RuntimeError if connection is not established in time.
    """
    # The following changes of sleep time calculation on port 22 is done for the changes introduced in WSA.
    # ipblockd deamon blacklists ssh connections from a client if ssh connections from the same client fails 10 times in a 240 seconds rolling window.
    sleep_time = 1
    if int(port) == 22:
        if int(timeout) >= 240:
            sleep_time = 30
        else:
            sleep_time = (timeout / 9) + 1

    tmr = sal.time.CountDownTimer(timeout).start()
    i = 0
    while tmr.is_active():
        if check_port(host, port, inet_family=inet_family):
            break
        time.sleep(sleep_time)
    else:
        raise TimeoutError, "wait_for_port: timed out trying to " \
                            "connect to %s:%s" % (host, port)
