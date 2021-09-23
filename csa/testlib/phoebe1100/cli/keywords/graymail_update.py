#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1100/cli/keywords/graymail_update.py#1 $
# $ $DateTime: 2019/03/22 01:36:06 $
# $ $Author: aminath $

from common.cli.clicommon import CliKeywordBase
import traceback


class GraymailUpdate(CliKeywordBase):
    """
    Provides keywords to update antispam components

    Returns one of the following numbers depending on the status returned:
      - `1` : Requesting check for new Graymail updates
      - `2` : Requesting forced update for Graymail
      - `3` : This feature is not enabled
      - `4` : Updates are currently unavailable
    """

    def get_keyword_names(self):
        return ['graymail_update']

    def graymail_update(self, force=False):
        """
        Requests updates for Graymail Engine

        CLI -> graymailupdate

        *Examples*:
        | ${Status}= | Graymail Update |
        | ${Status}= | Graymail Update | force=${True} |
        | ${Status}= | Graymail Update | force=${False} |
        """
        try:
            return self._cli.graymailupdate(force=force)
        except Exception, e:
            self._cli.restart()
            traceback.print_exc()
            raise e
