#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1200/cli/keywords/howto_status.py#1 $
# $DateTime: 2019/03/22 01:36:06 $
# $Author: aminath $

from common.cli.clicommon import CliKeywordBase


class HowtoStatus(CliKeywordBase):

    def get_keyword_names(self):
        return ['howto_status']

    def howto_status(self):
        """To get the current how to status
        example:
        ${output}=     Howto Status
        """
        return self._cli.howtostatus()
