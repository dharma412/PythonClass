#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1300/cli/ctor/netstat.py#1 $ $DateTime: 2019/06/27 23:26:24 $ $Author: aminath $
"""
IAF2 CLI command netstat
"""

from sal.exceptions import ConfigError
import time
from sal.containers.yesnodefault import YES, NO

import clictorbase

REQUIRED = clictorbase.REQUIRED
DEFAULT = clictorbase.DEFAULT


class netstat(clictorbase.IafCliConfiguratorBase):

    def __call__(self, info_type=DEFAULT, ip_version=DEFAULT, \
                 address_as_number=DEFAULT, avoid_truncating=DEFAULT,
                 interface=REQUIRED, bytes=DEFAULT, dropped=DEFAULT,
                 num_sec=DEFAULT, timeout=30,
                 ):

        self._writeln(self.__class__.__name__)
        idx = self._query_select_list_item(info_type)

        if not idx == 5:
            self._query_select_list_item(ip_version)
        if idx in (1, 4):
            # Show network addresses as numbers
            self._query_response(address_as_number)
            # Avoid truncating addresses?
            self._query_response(avoid_truncating)
        elif idx == 2:
            # Select the ethernet interface whose state you wish to display
            self._query_select_list_item(interface)
            # Show the number of bytes in and out?
            self._query_response(bytes)
            # Show the number of dropped packets?
            self._query_response(dropped)
        elif idx == 3:
            # Show network addresses as numbers
            self._query_response(address_as_number)
        elif idx == 5:
            # Enter the number of seconds between displays
            self._query_response(num_sec)
            # Select the ethernet interface whose state you wish to display
            self._query_select_list_item(interface)
            # Show the number of dropped packets?
            self._query_response(dropped)
            time.sleep(timeout)
            self.interrupt()
        else:
            raise ConfigError, 'Invalid info_type value'

        self.clearbuf()
        return '\n'.join(self._wait_for_prompt().splitlines()[2:-1])


if __name__ == '__main__':
    try:
        cli_sess
    except NameError:
        cli_sess = clictorbase.get_sess()

    ns = netstat(cli_sess)
    print ns(info_type='socket', address_as_number=YES, avoid_truncating=YES)
    print ns(info_type='interface', interface='Data 1', bytes=YES, dropped=YES)
    print ns(info_type='routing', address_as_number=YES)
    print ns(info_type='queue', address_as_number=YES, avoid_truncating=NO)
    print ns(info_type='traffic', num_sec=10, interface='Data 1', dropped=NO)
