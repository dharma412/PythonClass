#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1210/cli/keywords/webcacheflush.py#1 $ $DateTime: 2019/05/07 03:16:10 $ $Author: bimmanue $

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
