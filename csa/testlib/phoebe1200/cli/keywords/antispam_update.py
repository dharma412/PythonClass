#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1200/cli/keywords/antispam_update.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $

from common.cli.clicommon import CliKeywordBase
import traceback


class AntispamUpdate(CliKeywordBase):
    """
    cli -> antispamupdate

    Provides keywords to update antispam components

    Returns one of the following numbers depending on the status returned:
      - `1` : feature is not activated
      - `2` : can not do Brightmail
      - `3` : CASE restarting
      - `4` : either CASE or VOF must be enabled
      - `5` : update process not running
      - `6` : update in progress
      - `7` : update suspended
      - `8` : requesting forced update
      - `9` : requesting update
    """

    def get_keyword_names(self):
        return ['antispam_update_ironport',
                'antispam_update_cloudmark',
                'antispam_update_multiscan'
                ]

    def antispam_update_ironport(self, force=False):
        """
        Requests updates for IronPort Anti-Spam

        antispamupdate -> ironport

        *Examples*:
        | ${Status}= | Antispam Update Ironport |
        | ${Status}= | Antispam Update Ironport | force=${True} |
        | ${Status}= | Antispam Update Ironport | force=${False} |
        """
        try:
            return self._cli.antispamupdate(vendor='ironport', force=force)
        except Exception, e:
            self._cli.restart()
            traceback.print_exc()
            raise e

    def antispam_update_cloudmark(self, force=False):
        """
        Requests updates for Cloudmark Anti-Spam

        antispamupdate -> cloudmark

        *Examples*:
        | ${Status}= | Antispam Update Cloudmark |
        | ${Status}= | Antispam Update Cloudmark | force=${True} |
        | ${Status}= | Antispam Update Cloudmark | force=${False} |
        """
        try:
            return self._cli.antispamupdate(vendor='cloudmark', force=force)
        except Exception, e:
            self._cli.restart()
            traceback.print_exc()
            raise e

    def antispam_update_multiscan(self, force=False):
        """
        Requests updates for Intelligent Multi-Scan

        antispamupdate -> multiscan

        *Examples*:
        | ${Status}= | Antispam Update Multiscan |
        | ${Status}= | Antispam Update Multiscan | force=${False} |
        | ${Status}= | Antispam Update Multiscan | force=${True} |
        """
        try:
            return self._cli.antispamupdate(vendor='multiscan', force=force)
        except Exception, e:
            self._cli.restart()
            traceback.print_exc()
            raise e
