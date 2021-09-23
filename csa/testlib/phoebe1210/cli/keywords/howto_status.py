#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1210/cli/keywords/howto_status.py#1 $
# $DateTime: 2019/05/07 03:16:10 $
# $Author: bimmanue $

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
