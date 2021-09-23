#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/phoebe1350/cli/keywords/sbstatus.py#1 $ $DateTime: 2020/01/06 01:25:43 $ $Author: saurgup5 $

from common.cli.clicommon import CliKeywordBase


class sbstatus(CliKeywordBase):

    """sbstatus

    Retrieves the status of the most recently performed SenderBase query
    (whether the query succeeded or failed), along with the date and time
    that the query was performed. And returns the display time of last
    successful communication with SenderBase data-sharing server."""

    def get_keyword_names(self):
        return ['sbstatus']

    def sbstatus(self):
        """Returns output of sbstatus CLI command

        Examples:
            | ${status}= | SBStatus |
            | Log | ${status} |
        """
        return self._cli.sbstatus()