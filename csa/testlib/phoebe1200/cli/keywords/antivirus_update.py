#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1200/cli/keywords/antivirus_update.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $

from common.cli.clicommon import CliKeywordBase
import traceback


class AntivirusUpdate(CliKeywordBase):
    """
    cli -> antivirusupdate

    Provides keywords to update antivirus components

    Returns one of the following numbers depending on the status returned:
      - `1` : feature is not activated
      - `2` : for Sophos only
      - `3` : Anti-Virus not enabled (Sophos and McAfee)
      - `4` : update process not running
      - `5` : update in progress
      - `6` : update suspended
      - `7` : requesting forced update
      - `8` : requesting update (Sophos)
      - `9` : requesting update (McAfee)
    """

    def get_keyword_names(self):
        return ['antivirus_update_sophos',
                'antivirus_update_mcafee',
                ]

    def antivirus_update_sophos(self, force=False):
        """
        Request updates for Sophos Anti-Virus

        antivirusupdate -> sophos

        *Examples*:
        | ${Status}= | Antivirus Update Sophos |
        """
        try:
            return self._cli.antivirusupdate(vendor='sophos', force=force)
        except Exception, e:
            self._cli.restart()
            traceback.print_exc()
            raise e

    def antivirus_update_mcafee(self, force=False):
        """
        Requests updates for McAfee Anti-Virus

        antivirusupdate -> mcafee

        *Examples*:
        | ${Status}= | Antivirus Update Mcafee | force=${True} |
        """
        try:
            return self._cli.antivirusupdate(vendor='mcafee', force=force)
        except Exception, e:
            self._cli.restart()
            traceback.print_exc()
            raise e
