# $Id: //prod/main/sarf_centos/testlib/zeus1350/cli/keywords/tail.py#1 $ $DateTime: 2019/09/18 01:46:35 $ $Author: sarukakk $
from common.cli.clicommon import CliKeywordBase


class Tail(CliKeywordBase):
    """
    Returns results of tailing of a specified log file.
    Tailing is interrupted after a specified timeout.
    """

    def get_keyword_names(self):
        return ['tail']

    def tail(self, log_name, timeout=5):
        """
        Returns results of tailing of a specified log file.
        Tailing is interrupted after a specified timeout.

        Parameters:
        - `log_name`: name of the log file; the following names are
           currently accepted:
          * authlogs
          * backup_logs
          * cli_logs
          * config_logs
          * ftp_logs
          * http_logs
          * haystackd_logs
          * mail_logs
          * ldap_logs
          * ntp_logs
          * reportd_logs
          * reportqueryd_logs
          * sma_log
          * snmp_logs
          * slbl_logs
          * euq_gui_logs
          * euq_logs
          * status_logs
          * system_logs
          * tracking_logs
          * updater_logs

        - `timeout`:  timeout in seconds. Defaults to 5

        Examples:

        | ${log}= | tail | backup_log |
        | ${log}= | tail | authlogs | timeout=60 |
        | ${log}= | tail | ntp_logs |
        | ${log}= | tail | cli_logs |
        | ${log}= | tail | sma_logs |
        | ${log}= | tail | status_logs | timeout=1 |
        | ${log}= | tail | system_logs |
        | ${log}= | tail | updater_logs |

        Exceptions:
        - ValueError: Invalid value of timeout '<timeout>'; should be a positive
          number
          * that exception is raised when timeout is set to an invalid value
        - ConfigError: Not found: <log_name>
          * that exception is raised when log file can't be found
        """
        try:
            _ftimeout = float(timeout)
            if not _ftimeout > 0:
                raise Exception
        except:
            raise ValueError("Invalid value of timeout '" + str(timeout) \
                             + "'; should be a positive number")
        return str(self._cli.tail(log_name, _ftimeout))
