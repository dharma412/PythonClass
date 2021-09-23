#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1200/cli/keywords/antispam_status.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $

from common.cli.clicommon import CliKeywordBase
import traceback


class AntispamStatus(CliKeywordBase):
    """
    cli -> antispamstatus

    Provides keywords to get antispam components status
    """

    def get_keyword_names(self):
        return ['antispam_status_ironport',
                'antispam_status_brightmail',
                'antispam_status_cloudmark',
                'antispam_status_multiscan',
                ]

    def antispam_status_ironport(self):
        """
        Provides IronPort Anti-Spam version and rule information.

        antispamstatus -> ironport

        *Returns*:
          Dictionary with following component as keys:
          - `web_reputation_rules`
          - `case_utilities`
          - `web_reputation_db`
          - `structural_rules`
          - `case_core_files`
          - `content_rules`
          - `content_rules_update`
          - `case_core_files`

          Each key is a dictionary having 'update_date' and 'version' as keys

        *Examples*:
        | ${Status}= | Antispam Status Ironport |
        | ${rules}= | Get From Dictionary | ${Status} | structural_rules |
        | ${rules_ver}= | Get From Dictionary | ${rules} | version |
        | ${rules_date}= | Get From Dictionary | ${rules} | update_date |
        """
        try:
            return dict(self._cli.antispamstatus(vendor='ironport'))
        except Exception, e:
            self._cli.restart()
            traceback.print_exc()
            raise e

    def antispam_status_brightmail(self):
        """
        Provides Symantec Brightmail Anti-Spam version and rule information

        antispamstatus -> brightmail

        *Returns*:
          Dictionary with following rule type as keys:
          - `header_rules`
          - `intsig_rules`
          - `brightsig2_rules`
          - `body_hash_rules`
          - `heuristic_rules`

          Each key is a dictionary having 'update_date' as key

        *Examples*:
        | ${Status}= | Antispam Status Brightmail |
        | ${rules}= | Get From Dictionary | ${Status} | intsig_rules |
        | ${rules_date}= | Get From Dictionary | ${rules} | update_date |
        """
        try:
            return dict(self._cli.antispamstatus(vendor='brightmail'))
        except Exception, e:
            self._cli.restart()
            traceback.print_exc()
            raise e

    def antispam_status_cloudmark(self):
        """
        Provides Cloudmark Service Provider Edition version and rule information

        antispamstatus -> cloudmark

        *Returns*:
          Dictionary with following component as keys:
          - `meta_data_mfl`
          - `categories`
          - `meta_data_dpl`
          - `meta_data_mpl`
          - `meta_data_rpl`
          - `meta_data_ipl`
          - `meta_data_wpl`
          - `meta_data_rplv2`
          - `cartridge`
          - `meta_data_xrl`
          - `meta_data_ebl`
          - `meta_data_impl`
          - `meta_data_fsl`
          - `meta_data_lgl`
          - `meta_data_csl`

          Each key is a dictionary having 'update_date' and 'version' as keys

        *Examples*:
        | ${Status}= | Antispam Status Cloudmark |
        | ${rules}= | Get From Dictionary | ${Status} | meta_data_mfl |
        | ${rules_ver}= | Get From Dictionary | ${rules} | version |
        | ${rules_date}= | Get From Dictionary | ${rules} | update_date |
        """
        try:
            return dict(self._cli.antispamstatus(vendor='cloudmark'))
        except Exception, e:
            self._cli.restart()
            traceback.print_exc()
            raise e

    def antispam_status_multiscan(self):
        """
        Provides Intelligent Multi-Scan version and rule information

        antispamstatus -> multiscan

        *Returns*:
          Dictionary with following component as keys:
          - `web_reputation_rules`
          - `case_utilities`
          - `web_reputation_db`
          - `structural_rules`
          - `content_rules`
          - `content_rules_update`
          - `case_core_files`
          - `meta_data_mfl`
          - `categories`
          - `meta_data_dpl`
          - `meta_data_mpl`
          - `meta_data_rpl`
          - `meta_data_ipl`
          - `meta_data_wpl`
          - `meta_data_rplv2`
          - `cartridge`
          - `meta_data_xrl`
          - `meta_data_ebl`
          - `meta_data_impl`
          - `meta_data_fsl`
          - `meta_data_lgl`
          - `meta_data_csl`

          Each key is a dictionary having 'update_date' and 'version' as keys

          *Examples*:
          | ${Status}= | Antispam Status Multiscan |
          | ${irules}= | Get From Dictionary | ${Status} | structural_rules |
          | ${irules_ver}= | Get From Dictionary | ${irules} | version |
          | ${irules_date}= | Get From Dictionary | ${irules} | update_date |
        """
        try:
            return dict(self._cli.antispamstatus(vendor='multiscan'))
        except Exception, e:
            self._cli.restart()
            traceback.print_exc()
            raise e
