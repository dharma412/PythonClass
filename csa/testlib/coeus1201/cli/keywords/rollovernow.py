#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/cli/keywords/rollovernow.py#1 $

from common.cli.clicommon import CliKeywordBase

class RollOverNow(CliKeywordBase):
    """Roll over a log file.

       The following system wide default log names can be used for `logname`
       parameter below:
       | accesslogs | authlogs | avc_logs | bypasslogs | cli_logs |
       | dca_logs | external_auth_logs | feedback_logs | ftpd_logs | gui_logs |
       | haystackd_logs | idsdataloss_logs | logderrorlogs | mcafee_logs | musd_logs |
       | pacd_logs | proxylogs | reportd_logs | reportqueryd_logs | saas_auth_log |
       | shd_logs | snmp_logs | sntpd_logs | sophos_logs | status |
       | system_logs | trafmon_errlogs | trafmonlogs | uds_logs | updater_logs |
       | wbnp_logs | webcat_logs | webrootlogs | welcomeack_logs | All Logs |
    """

    def get_keyword_names(self):
        return [
            'roll_over_now',
        ]

    def roll_over_now(self, logname='All Logs'):
        """Roll over a log file.

        Parameters:
           - `logname`: name of the log subscription to roll over.  Defaulted
                        to 'All Logs' to roll over all log files.

        Examples:
        | Roll Over Now |
        | Roll Over Now | logname=accesslogs |
        | Roll Over Now | logname=proxylogs |
        """
        self._cli.rollovernow(logname)


