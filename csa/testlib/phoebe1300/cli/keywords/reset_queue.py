#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/phoebe1300/cli/keywords/reset_queue.py#1 $ $DateTime: 2019/06/27 23:26:24 $ $Author: aminath $

from common.cli.clicommon import CliKeywordBase


class ResetQueue(CliKeywordBase):
    """Resets the whole message queue then shut down the
    system to power off and restart."""

    def get_keyword_names(self):
        return ['reset_queue']

    def reset_queue(self, confirm='Yes'):
        """Reset the message queue and reboot appliance.
        All messages in all queues, including undeliverable messages,
        will be deleted.

        *Parameters:*
        - `confirm`: whether to perform queue reset or not.
        Either 'yes' or 'no'. 'Yes' by default

        *Examples:*
        | Close All Browsers |
        | Reset Queue |
        | Wait until DUT Is Accessible | wait_for_ports=22,443,80 |
        | ... | timeout=360 |
        | Run Keyword If | '${ready}' == 'FAIL' |
        | ... | Fatal Error | Gui became unavailable |
        | Start CLI Session If Not Open |
        | Selenium Login |
        """
        self._cli.resetqueue(self._process_yes_no(confirm))
