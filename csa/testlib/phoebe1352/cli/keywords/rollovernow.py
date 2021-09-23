#!/usr/bin/env python

from common.cli.clicommon import CliKeywordBase

class RollOverNow(CliKeywordBase):
    """Roll over a log file.

       The following system wide default log names can be used for `logname`
       parameter below:
       | antispam | antivirus | asarchive | authentication | avarchive |
       | bounces | cli_logs | encryption | error_logs | euq_logs |
       | euqgui_logs | ftpd_logs | gui_logs | mail_logs | repeng |
       | reportd_logs | reportqueryd_logs | scanning | slbld_logs | snmp_logs |
       | sntpd_logs | status | system_logs | trackerd_logs | updater_logs |
       | All Logs |
    """

    def get_keyword_names(self):
        return ['roll_over_now']

    def roll_over_now(self, logname='All Logs'):
        """Roll over a log file.

        Parameters:
           - `logname`: name of the log subscription to roll over.  Defaulted
                        to 'All Logs' to roll over all log files.

        Examples:
        | Roll Over Now |
        | Roll Over Now | logname=mail_logs |
        | Roll Over Now | logname=cli_logs |
        """
        self._cli.rollovernow(logname)


