#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1300/cli/keywords/webcacheflush.py#1 $ $DateTime: 2019/06/27 23:26:24 $ $Author: aminath $

from common.cli.clicommon import CliKeywordBase


class webcacheflush(CliKeywordBase):
    """
    This command flushes the contents of the cache and sets it to default value
    cli -> webcacheflush
    """

    def get_keyword_names(self):
        return ['webcacheflush']

    def webcacheflush(self):
        """
        *Example:*
        | ${webstatus} | Webcacheflush |
        | Log | ${webstatus} |
        """
        return (self._cli.webcacheflush())
