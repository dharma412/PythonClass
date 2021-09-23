#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1210/cli/keywords/old_message.py#1 $ $DateTime: 2019/05/07 03:16:10 $ $Author: bimmanue $

"""
SARF CLI command: oldmessage
"""

from common.cli.clicommon import CliKeywordBase


class OldMessage(CliKeywordBase):
    """
    Displays the oldest non-quarantine message on the system.
    CLI command: oldmessage
    """

    def get_keyword_names(self):
        return ['oldmessage']

    def oldmessage(self):
        """CLI command: oldmessage

        *Parameters:*
        None

        *Return:*
        Raw output

        *Examples:*
        | ${res}=  | Oldmessage |
        """
        return self._cli.oldmessage()
