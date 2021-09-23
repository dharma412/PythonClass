#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1210/cli/keywords/shutdown.py#1 $ $DateTime: 2019/05/07 03:16:10 $ $Author: bimmanue $

from common.cli.clicommon import CliKeywordBase


class ShutDown(CliKeywordBase):
    """Keyword for shutdown CLI command."""

    def get_keyword_names(self):
        return ['shutdown']

    def shutdown(self, delay=None):
        """Shut down the system to power off.

        Parameters:
        - `delay` - maximum number of seconds to wait for connections
        to close before doing a forceful disconnect. Does not need
        confirmation. Value must be an integer from 0 to 3,600.
        Default - 30.

        Examples:
        | Shutdown |
        | Shutdown | delay=40 |
        """
        return self._cli.shutdown(delay)
