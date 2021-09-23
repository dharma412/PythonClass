#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1362/cli/keywords/suspend_listener.py#1 $ $DateTime: 2020/06/10 22:29:20 $ $Author: sarukakk $

from common.cli.clicommon import CliKeywordBase

class SuspendListener(CliKeywordBase):

    """Keywords for suspendlistener CLI command."""

    def get_keyword_names(self):
        return ['suspend_listener',]

    def suspend_listener(self, delay=None):
        """Suspend listener.

        Parameters:
        - `delay`: maximum number of seconds to wait for connections to close
           before doing a forceful disconnect.

        Examples:
        | Suspend Listener |
        | Suspend Listener | 10 |
        """

        if delay != None:
            input_dict = {'delay': delay}
            self._cli.suspendlistener(input_dict)
        else:
            self._cli.suspendlistener(delay)

