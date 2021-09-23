#!/usr/bin/env python
""" a collection of methods to find out if hosts are up or down

"""
from __future__ import absolute_import

#: Reference Symbols: pinglib

import time
import os
import sal.time
import socket
from sal.exceptions import DutNotRespondingError


class PingError(RuntimeError):
    pass


def ping(hostname, timeout=5):
    cmd = 'ping -c 1 -t %d %s > /dev/null 2>&1' % (timeout, hostname)
    rv = os.system(cmd)
    # returns True if not reachable and false if reachable
    return rv <= 0


is_reachable = ping  # alias


def ping_many(host_list, timeout=5):
    result_list = []
    for hostname in host_list:
        is_reachable = ping(hostname, timeout)
        result_list.append((hostname, is_reachable))
    return result_list


def wait_until_reachable(host, timeout=300):
    tmr = sal.time.CountDownTimer(timeout).start()
    while tmr.is_active():
        if is_reachable(host):
            break
        time.sleep(2)
    else:
        raise PingError, "wait_until_reachable: max tries exceeded."


def wait_until_not_reachable(host, timeout=300):
    tmr = sal.time.CountDownTimer(timeout).start()
    while tmr.is_active():
        if not is_reachable(host):
            break
        time.sleep(2)
    else:
        raise PingError, "wait_until_not_reachable: max tries exceeded."


def wait_for_reboot(host, timeout=300):
    wait_until_not_reachable(host, timeout)
    wait_until_reachable(host, timeout)


# Inserting code to check if hostname is pingable, if pingable check to see if
# port 22 is up

def check_machine_available(hostname):
    # Give machines 15 seconds in case of bad delays across locations
    if not ping(hostname, 15):
        raise DutNotRespondingError, (hostname, DutNotRespondingError.E1)
    elif check_port(hostname):
        raise DutNotRespondingError, (hostname, DutNotRespondingError.E2)


def check_port(hostname):
    server_socket = socket.socket()
    server_socket.settimeout(1)
    try:
        server_socket.connect((hostname, 22))
    except socket.error:
        return 1
