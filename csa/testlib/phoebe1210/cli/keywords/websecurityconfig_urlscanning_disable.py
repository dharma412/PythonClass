#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1210/cli/keywords/websecurityconfig_urlscanning_disable.py#1 $ $DateTime: 2019/05/07 03:16:10 $ $Author: bimmanue $

from common.cli.clicommon import CliKeywordBase


class websecurityconfig_urlscanning_disable(CliKeywordBase):
    """
    cli -> websecurityconfig urlscanning disable
    """

    def get_keyword_names(self):
        return ['websecurityconfig_urlscanning_disable']

    def websecurityconfig_urlscanning_disable(self):
        """
        *Example:*
        | Websecurityconfig urlscanning disable |
        """
        return (self._cli.websecurityconfig_urlscanning_disable())
