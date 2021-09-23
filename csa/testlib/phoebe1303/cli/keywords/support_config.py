#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1350/cli/keywords/support_config.py#1 $ $DateTime: 2020/01/06 01:25:43 $ $Author: saurgup5 $

from common.cli.clicommon import CliKeywordBase

class SupportConfig(CliKeywordBase):
    """
    CLI command: supportconfig
    """
    def get_keyword_names(self):
        return ['support_config_request',]

    def support_config_request(self, *args):
        """Set the destination email address for supportrequest.

        CLI command: supportconfig > SUPPORTREQUEST

        *Parameters:*
        - `email`: The destination email address for supportrequest.

        *Return:*
        None

        *Examples:*
        | Support Config Request | email=supportrequest@mail.qa |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.supportconfig().supportrequest(**kwargs)