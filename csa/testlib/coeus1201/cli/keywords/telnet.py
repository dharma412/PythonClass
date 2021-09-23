#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/cli/keywords/telnet.py#1 $
# $DateTime: 2019/08/14 09:58:47 $
# $Author: uvelayut $

from common.cli.clicommon import (CliKeywordBase, DEFAULT)

class Telnet(CliKeywordBase):

    """Keywords for telnet CLI command."""

    def get_keyword_names(self):
        return ['telnet_connect',
                'telnet_close',
                ]

    def telnet_connect(self, interface, hostname, port=None, timeout=30):
        """ Making telnet connection to hostname:port from interface.
            Connection will be left opened and the user is responsible closing
            the session.

        *Parameters*
        - `interface`: Selection from a list of available interfaces:
           1. Auto
           2. Management (172.29.183.44/24: wsa034.wga)
           3. Management_v6 (2001:420:292:2081::2c/64: wsa034.wga)
           4. P1 (10.4.18.20/28: wsa034-p1.wga)
           5. P1_v6 (2001:420:292:20d2:1000::4/68: wsa034-p1.wga)
        value can be either one of [Auto, Management, Management_v6, P1, P1_v6]
        or an uniquely identified part of one choices in the list.
        Please note that actual list of interfaces depends on the configuration
        and differs from the example above.
        Using [Auto, Management, Management_v6, P1, P1_v6] is recommended.
        For example, '2', 'Management (', and '44/24' are equal to 'Management'
        but can be not equal in your settings.
        - `hostname`: host to which you want to establish connection. String.
        - `port`: posrt on remote computer. Default 25.
        - `timeout`: how long wait for results in seconds. String. Default 30
          seconds.

        *Return*
        None.

        *Exceptions*
        - `ConfigError`: one of the next messages are returned :
        1. Unable to connect to remote host
        2. Connection refused
        3. `hostname`: No address associated with hostname
        4. Unknown

        *Examples*
        | Telnet Connect | Management_v6 | vm10bsd0186.auto | 22 | timeout=3 |
        | Telnet Connect | 1 | c650-05.auto | # that way of specifying interface is not recommended |
        | Telnet Connect | Management | vm10bsd0186.auto | 22
        """
        interfaces_map = {
            'Auto' : 'Auto',
            'Management' : 'Management (',
            'Management_v6' : 'Management_v6',
            'P1' : 'P1 (',
            'P1_v6' : 'P1_v6',
            }
        if interface in interfaces_map.keys():
            interface = interfaces_map[interface]
        return self._cli.telnet(interface, hostname, port, int(timeout))

    def telnet_close(self):
        """
        Close previosly opened telnet session.
        This keyword only put ctrl+c to command prompt, so even if connection
        wouldn't be established, using this keyword can't be harmful.

        *Parameters*
        None.

        *Return*
        None.

        *Examples*
        | Telnet Close |
        """
        self._cli.telnet.close()

