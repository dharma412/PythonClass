#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1300/cli/keywords/dlp_status.py#1 $ $DateTime: 2019/06/27 23:26:24 $ $Author: aminath $

from common.cli.clicommon import CliKeywordBase


class DLPStatus(CliKeywordBase):
    """
    cli -> dlpstatus
    """

    def get_keyword_names(self):
        return ['dlp_status', ]

    def dlp_status(self):
        """
        CLI command: dlpstatus

        *Examples*:
        | ${res}= | Dlp Status |
        | Log | ${res} |

        *Return*:
        CLI response(String) - if DLP is disabled.
        Dictionary (CfgHolder) if DLP is enabled.
        Dictionary's keys: version, last_updated.
        """
        return self._cli.dlpstatus()
