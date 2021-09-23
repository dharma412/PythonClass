#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1250/cli/keywords/reboot.py#3 $ $DateTime: 2019/06/07 02:45:52 $ $Author: sarukakk $

from common.cli.clicommon import CliKeywordBase

class Reboot(CliKeywordBase):
    """Shut down the system to power off and restart."""

    def get_keyword_names(self):
        return ['reboot']

    def reboot(self, confirm='YES', delay=None):
        """Reboot.

        Parameters:
        - `confirm` - string with answer to confirmation question.
            Either Yes or No. Yes is used by default. Used when delay
            is not specified.
        - `delay` - maximum number of seconds to wait for connections
            to close before doing a forceful disconnect. Does not need
            confirmation. Value must be an integer from 0 to 3,600.
            Default - 30.

        Examples:
        | reboot |
        | reboot | confirm=No |
        | reboot | delay=30 |
        """

        if delay is not None:
            if not delay.isdigit():
                raise ValueError('Invalid arguments when processing reboot. '\
                                 'Value must be an integer from 0 to 3,600.')
            else:
                self._cli.reboot(confirm_continue=self._process_yes_no(confirm),
                    delay=delay)
        else:
            self._cli.reboot(confirm_continue=self._process_yes_no(confirm))
