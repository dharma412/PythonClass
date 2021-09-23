#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1380/cli/keywords/last.py#1 $ $DateTime: 2020/05/25 00:19:30 $ $Author: sarukakk $

from common.cli.clicommon import CliKeywordBase

class Last(CliKeywordBase):
    """Keyword for last CLI command."""

    def get_keyword_names(self):
        return ['last']

    def last(self, option=None):
        """Display who has recently logged into the system.

        Parameters:
        - `option` - specify the username to display.
        By default it shows all users.
        Options:
            -d timestamp
                Show logins for this particular time.
                timestamp format can be:
                YYYY     - Example: 2003
                YYYYMM   - Example: 200306
                YYYYMMDD - Example: 20030603

        Example:
        | ${output} = | Last |
        | ${output} = | Last | admin |
        | ${output} = | Last | admin -d 201202 |
        """
        output = self._cli.last(option)
        self._info(output)
        return output
