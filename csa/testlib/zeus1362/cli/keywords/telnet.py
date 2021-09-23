#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1362/cli/keywords/telnet.py#1 $ $DateTime: 2020/06/10 22:29:20 $ $Author: sarukakk $

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
        - `interface`: name of interface on appliance from which you want to
          make connection. String.
        - `hostname`: host to which you want to establish connection. String.
        - `port`: posrt on remote computer. Default 25.
        - `timeout`: how long wait for results in seconds. String. Default 30
          seconds.

        *Return*
        None.

        *Exceptons*
        - `ConfigError`: one of the next messages are returned :
        1. Unable to connect to remote host
        2. Connection refused
        3. `hostname`: No address associated with hostname
        4. Unknown

        *Examples*
        | Telnet Connect | Management | vm10bsd0186.auto | 22 | timeout=3 |
        | Telnet Connect | Auto | c650-05.auto |
        """
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
