#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/phoebe1210/cli/keywords/sbstatus.py#1 $ $DateTime: 2019/05/07 03:16:10 $ $Author: bimmanue $

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
