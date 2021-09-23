#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1350/cli/keywords/antivirus_status.py#1 $ $DateTime: 2020/01/06 01:25:43 $ $Author: saurgup5 $

from common.cli.clicommon import CliKeywordBase
import traceback

class AntivirusStatus(CliKeywordBase):
    """
    cli -> antivirusstatus

    Provides keywords to get antivirus components status
    """

    def get_keyword_names(self):
        return ['antivirus_status_sophos',
                'antivirus_status_mcafee',
               ]

    def antivirus_status_sophos(self):
        """
        Provides Sophos Anti-Virus version information

        antivirusstatus -> sophos

        *Returns*:
          Dictionary with following component as keys:
          - `sav_engine_version`
          - `ide_serial`
          - `last_engine_update`
          - `last_ide_update`
          - `last_update_attempt`
          - `last_update_success`

        *Examples*:
        | ${Status}= | Antivirus Status Sophos |
        | ${sav_eng_ver}= | Get From Dictionary |
        | ... | ${Status} | sav_engine_version |
        """
        try:
            return self._cli.antivirusstatus(vendor='sophos')
        except Exception,e:
            self._cli.restart()
            traceback.print_exc()
            raise e

    def antivirus_status_mcafee(self):
        """
        Provides McAfee Anti-Virus version information

        antivirusstatus -> mcafee

        *Returns*:
          Dictionary with following component as keys:
          - `mcafee_dat_files`
          - `mcafee_engine_version`

        *Examples*:
        | ${Status}= | Antivirus Status Mcafee |
        | ${mcafee_dat_file}= | Get From Dictionary |
        | ... | ${Status} | mcafee_dat_files |
        """
        try:
            return self._cli.antivirusstatus(vendor='mcafee')
        except Exception,e:
            self._cli.restart()
            traceback.print_exc()
            raise e

