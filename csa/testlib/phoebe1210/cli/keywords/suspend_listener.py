#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1210/cli/keywords/suspend_listener.py#1 $ $DateTime: 2019/05/07 03:16:10 $ $Author: bimmanue $

from common.cli.clicommon import CliKeywordBase
import traceback


class SuspendListener(CliKeywordBase):
    """Keywords for suspendlistener CLI command."""

    def get_keyword_names(self):
        return ['suspend_listener', ]

    def suspend_listener(self, listener_name='All', delay=None):
        """Suspend listener.

        Parameters:
        - `listener_name` : name of the listener like All,private_qmqp etc..
        - `delay`: maximum number of seconds to wait for connections to close
           before doing a forceful disconnect. Default is 30s

        Examples:
        | Suspend Listener | listener_name=private_qmap |
        | Suspend Listener | 10 |
        """
        try:
            self._cli.suspendlistener(listener_name, delay)
        except Exception, e:
            self._cli.restart()
            traceback.print_exc()
            raise e
