#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1210/cli/keywords/support_config.py#1 $ $DateTime: 2019/05/07 03:16:10 $ $Author: bimmanue $

from common.cli.clicommon import CliKeywordBase


class SupportConfig(CliKeywordBase):
    """
    CLI command: supportconfig
    """

    def get_keyword_names(self):
        return ['support_config_request', ]

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
