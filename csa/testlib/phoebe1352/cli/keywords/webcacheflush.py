#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1350/cli/keywords/webcacheflush.py#1 $ $DateTime: 2020/01/06 01:25:43 $ $Author: saurgup5 $

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