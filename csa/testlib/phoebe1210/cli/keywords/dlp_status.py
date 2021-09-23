#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1210/cli/keywords/dlp_status.py#1 $ $DateTime: 2019/05/07 03:16:10 $ $Author: bimmanue $

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
