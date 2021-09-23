#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1100/cli/keywords/websecurityconfig_urlscanning_enable.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $

from common.cli.clicommon import CliKeywordBase


class websecurityconfig_urlscanning_enable(CliKeywordBase):
    """
    cli -> websecurityconfig urlscanning enable
    """

    def get_keyword_names(self):
        return ['websecurityconfig_urlscanning_enable']

    def websecurityconfig_urlscanning_enable(self):
        """
        *Example:*
        | Websecurityconfig urlscanning enable |
        """
        return (self._cli.websecurityconfig_urlscanning_enable())
