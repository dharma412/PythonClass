#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1300/cli/keywords/strip_headers.py#1 $ $DateTime: 2019/06/27 23:26:24 $ $Author: aminath $

from common.cli.clicommon import CliKeywordBase


class StripHeaders(CliKeywordBase):
    """
    CLI command: stripheaders
    """

    def get_keyword_names(self):
        return ['strip_headers_setup', ]

    def strip_headers_setup(self, *args):
        """Set message headers to remove.

        CLI command: stripheaders

        *Parameters:*
        - `headers`: The list of headers to strip from the messages before they are delivered.
        Separate multiple headers with commas. String.
        Use the keyword _DELETE_ to clear the list.

        *Return:*
        None

        *Examples:*
        | Strip Headers | headers=from, to |
        | Strip Headers | headers=DELETE |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.stripheaders().setup(**kwargs)
