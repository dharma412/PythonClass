#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1210/cli/keywords/show_message.py#1 $ $DateTime: 2019/05/07 03:16:10 $ $Author: bimmanue $

from common.cli.clicommon import CliKeywordBase


class ShowMessage(CliKeywordBase):
    """
    CLI command: showmessage
    """

    def get_keyword_names(self):
        return ['show_message', ]

    def show_message(self, *args):
        """Display the message for the given mid.

        CLI command: showmessage

        *Parameters:*
        - `mid`: The MID to display.

        *Return:*
        Raw output.

        *Examples:*
        | ${message}= | Show Message | mid=7 |
        | Log | ${message} |
        """
        kwargs = self._convert_to_dict(args)
        return self._cli.showmessage(**kwargs)
