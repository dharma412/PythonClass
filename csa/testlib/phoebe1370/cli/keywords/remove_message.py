#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1350/cli/keywords/remove_message.py#1 $ $DateTime: 2020/01/06 01:25:43 $ $Author: saurgup5 $

from common.cli.clicommon import CliKeywordBase
from sal.containers.yesnodefault import YES, NO

class remove_message(CliKeywordBase):
    """
    Removes message with given MID.
    CLI command: removemessage
    """

    def get_keyword_names(self):
        return ['remove_message']

    def remove_message(self, MID, confirm='YES'):
        """CLI command: removemessage

        *Parameters:*
        - `MID`: message ID to be removed
        - `confirm`: whether to confirm message removal. Default - YES

        *Return:*
        Raw output

        *Examples:*
        | Remove Message | 12 |
        """
        return self._cli.removemessage(confirm, MID)
