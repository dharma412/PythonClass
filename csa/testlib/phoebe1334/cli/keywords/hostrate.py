#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1350/cli/keywords/hostrate.py#1 $ $DateTime: 2020/01/06 01:25:43 $ $Author: saurgup5 $

from common.cli.clicommon import (CliKeywordBase, DEFAULT)


class Hostrate(CliKeywordBase):

    """Keywords for hostrate CLI command."""

    def get_keyword_names(self):
        return ['hostrate',
                'hostrate_batch']

    def hostrate(self, host, delay=DEFAULT, records=2):
        """Run hostrate command and return  host statistics over time.

        Parameters:
        - `host`: host for which to display statistics.
        - `delay`: the number of seconds to wait between displays.
        - `records`: the number of hostrate records to capture.

        Return:
        An output of the command.

        Examples:
        | Hostrate | mail.qa |
        | Hostrate | mail.qa | delay=2 | records=50 |
        """
        return self._cli.hostrate(False, records, host=host, sec=delay)

    def hostrate_batch(self, host, delay=DEFAULT, records=2):
        """Run hostrate command in batch mode and return host statistics
           over time.

        Parameters:
        - `host`: host for which to display statistics.
        - `delay`: the number of seconds to wait between displays.
        - `records`: the number of hostrate records to capture.

        Return:
        An output of the command.

        Examples:
        | Hostrate Batch | mail.qa |
        | Hostrate Batch | mail.qa | delay=2 | records=50 |
        """
        return self._cli.hostrate(True, records, host=host, sec=delay)
