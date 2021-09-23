#!/usr/bin/env python

from common.cli.clicommon import CliKeywordBase


class Reboot(CliKeywordBase):
    """Shut down the system to power off and restart."""

    def get_keyword_names(self):
        return ['reboot']

    def reboot(self, delay=None):
        """Reboot.

        Parameters:
        - `delay` - maximum number of seconds to wait for connections
            to close before doing a forceful disconnect. Does not need
            confirmation. Value must be an integer from 0 to 3,600.
            Default - 30.

        Examples:
        | reboot |
        | reboot | delay=20 |
        """
        if delay is not None:
            if not delay.isdigit():
                raise ValueError('Invalid arguments when processing reboot. ' \
                                 'Value must be an integer from 0 to 3,600.')

            else:
                self._cli.reboot(wait_secs=delay)
        else:
            self._cli.reboot()
