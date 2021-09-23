from common.cli.clicommon import CliKeywordBase

class Tail(CliKeywordBase):
    """
    Returns results of tailing of a specified log file.
    Tailing is interrupted after a specified timeout.
    """
    def get_keyword_names(self):
        return ['tail' ]

    def tail(self, log_name, timeout=5):
        """
        Returns results of tailing of a specified log file.
        Tailing is interrupted after a specified timeout.

        Parameters:
        - `log_name`: name of the log file; the following names are
           currently accepted:
          * accesslogs
          * authlogs
          * avc_logs
          * bypasslogs
          * cli_logs
          * dca_logs
          * external_auth_logs
          * feedback_logs
          * ftpd_logs
          * gui_logs
          * haystackd_logs
          * idsdataloss_logs
          * logderrorlogs
          * mcafee_logs
          * musd_logs
          * pacd_logs
          * reportd_logs
          * reportqueryd_logs
          * saas_auth_log
          * shd_logs
          * snmp_logs
          * sntpd_logs
          * sophos_logs
          * status
          * system_logs
          * trafmon_errlogs
          * trafmonlogs
          * uds_logs
          * updater_logs
          * wbnp_logs
          * webcat_logs
          * webrootlogs
          * welcomeack_logs

        - `timeout`:  timeout in seconds. Defaults to 5

        Examples:

        | ${log}= | tail | accesslog |
        | ${log}= | tail | authlogs | timeout=60 |
        | ${log}= | tail | bypasslogs |
        | ${log}= | tail | cli_logs |
        | ${log}= | tail | gui_logs |
        | ${log}= | tail | status | timeout=1 |
        | ${log}= | tail | system_logs |
        | ${log}= | tail | webrootlogs |

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

