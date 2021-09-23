
#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1350/cli/keywords/display_alerts.py#1 $
# $DateTime: 2020/01/06 01:25:43 $
# $Author: saurgup5 $

from common.cli.clicommon import CliKeywordBase

class DisplayAlerts(CliKeywordBase):
    """
        cli -> displayalerts
    """
    def get_keyword_names(self):
        return ['display_alerts',
                ]

    def  display_alerts(self):
        """
        cli -> displayalerts

        *Return:*  Alerts on appliance. Type - string

        *Examples:*

        |  ${alerts_status}= |  Display Alerts |
        |  Log  | ${alerts_status}  |
        """
        return self._cli.displayalerts()
