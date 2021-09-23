# $Id: //prod/main/sarf_centos/testlib/phoebe1210/cli/keywords/tail.py#1 $ $DateTime: 2019/05/07 03:16:10 $ $Author: bimmanue $
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
        * antispam
        * antivirus
        * asarchive
        * authentication
        * avarchive
        * bounces
        * cli_logs
        * encryption
        * error_logs
        * euq_logs
        * euqgui_logs
        * ftpd_logs
        * gui_logs
        * mail_logs
        * repeng
        * reportd_logs
        * reportqueryd_logs
        * scanning
        * slbld_logs
        * snmp_logs
        * sntpd_logs
        * status
        * system_logs
        * trackerd_logs
        * updater_logs
        - `timeout`:  timeout in seconds. Defaults to 5

        Examples:

        | ${log}= | tail | mail_logs | timeout=60 |
        | ${log}= | tail | cli_logs |
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
