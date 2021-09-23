#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1200/cli/keywords/websecurityconfig_urlscanning_disable.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $

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
