# !/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1210/cli/keywords/display_alerts.py#1 $
# $DateTime: 2019/05/07 03:16:10 $
# $Author: bimmanue $

from common.cli.clicommon import CliKeywordBase


class DisplayAlerts(CliKeywordBase):
    """
        cli -> displayalerts
    """

    def get_keyword_names(self):
        return ['display_alerts',
                ]

    def display_alerts(self):
        """
        cli -> displayalerts

        *Return:*  Alerts on appliance. Type - string

        *Examples:*

        |  ${alerts_status}= |  Display Alerts |
        |  Log  | ${alerts_status}  |
        """
        return self._cli.displayalerts()
