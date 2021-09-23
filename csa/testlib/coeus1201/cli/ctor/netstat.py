#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/cli/ctor/netstat.py#1 $

"""
IAF2 CLI command netstat
"""

import re
from sal.exceptions import ConfigError
from sal.containers.yesnodefault import YES, NO
import clictorbase

class netstat(clictorbase.IafCliConfiguratorBase):

    def __call__(self, info_type='all'):
        # dictionary of (info_type: regex to match this type of info in netstat
        # output)
        info_types = {'all': '',
                      'tcp': 'tcp:(.*?)udp:',
                      'udp': 'udp:(.*?)ip:',
                      'ip': 'ip:(.*?)icmp:',
                      'icmp': 'icmp:(.*?)igmp:',
                      'igmp': 'igmp:(.*?)Routing tables',
                      'routing': 'Routing tables(.*?)Active Internet connections',
                      'connections': 'Active Internet connections.*?\r\n(.*)'}

        self.clearbuf()
        self._writeln(self.__class__.__name__)
        out = self._wait_for_prompt()

        if info_type not in info_types:
            raise ConfigError, 'Uknown info type - %s' % (info_type,)

        if info_type == 'all':
            return out

        result = re.search(info_types[info_type], out, re.DOTALL)
        if result:
            return result.group(1)
        else:
            raise ConfigError, 'Could not obtain %s info from netstat' % (info_type,)

if __name__ == '__main__':
    try:
        cli_sess
    except NameError:
        cli_sess = clictorbase.get_sess()

    ns = netstat(cli_sess)
    for info in ('tcp', 'udp', 'ip', 'icmp', 'igmp', 'routing', 'connections'):
        print 'Getting %s info' % (info.upper(),)
        print ns(info_type=info)

