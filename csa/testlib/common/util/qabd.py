#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/common/util/qabd.py#1 $

""" Access the Ironport QA backdoor from Python.  """

__revision = '$Revision: #1 $'

from sal.net.services import commandd
from sal.net.services.qabdbase import QABackdoorBase
from common.util.utilcommon import UtilCommon

LOG_DIRECTORIES = ["", "accesslogs", "cli_logs", "gui_logs", "configuration",
                   "error_logs", "logderrorlogs", "proxyerrorlogs", "reportd_logs", "system_logs",
                   "trafmon_errlogs", "trafmonlogs", "wbnp_logs", "wbrs_logs"]


class QABackdoor(QABackdoorBase):
    """
    Interface to the QA backboor process on the DUT (which is really an
    HTTP/HTML server).
    """
    wga_info = QABackdoorBase.get_info

    def browse_logs(self, d, f, lines=25, offset=-1, do_check=True):
        """Returns number of lines from the log file <f> in directory <d>.

        Parameters:
            - `d`: name of the log directory
            - `f`: filename of the log
            - `lines`: number of lines to return. By default 25
            - `offset`: position starting from which number of lines will be
              returned. If negative then number of lines will be returned from
              the end of the file.  By default -1.
            - `do_check`: whether perform checking of the directory's name. If
              True then directory should be one of following otherwise exception
              will be rised:

              accesslogs, cli_logs, gui_logs, configuration, error_logs,
              logderrorlogs, proxyerrorlogs, reportd_logs, system_logs,
              trafmon_errlogs, trafmonlogs, wbnp_logs, wbrs_logs

        Examples:
        | ${access_log}= | QA Backdoor Browse Logs | accesslogs | aclog.current |
        | ... | lines=3 | offset=-1 |
        | Log | ${access_log} |
        """
        if do_check and (d not in LOG_DIRECTORIES):
            raise RuntimeError, "Directory %s is invalid." % (d,)
        return QABackdoorBase.browse_logs(self, d, f, int(lines), int(offset))

    def whole_log(self, d, f, do_check=True):
        """Returns entire log file <f> in directory <d>.

        Parameters:
            - `d`: name of the log directory
            - `f`: filename of the log
            - `do_check`: whether perform checking of the directory's name. If
              True then directory should be one of following otherwise exception
              will be rised:

              accesslogs, cli_logs, gui_logs, configuration, error_logs,
              logderrorlogs, proxyerrorlogs, reportd_logs, system_logs,
              trafmon_errlogs, trafmonlogs, wbnp_logs, wbrs_logs

        Examples:
        | ${access_log}= | QA Backdoor Whole Log | accesslogs | aclog.current |
        | Log | ${access_log} |
        """
        if do_check and (d not in LOG_DIRECTORIES):
            raise RuntimeError, "Directory %s is invalid." % (d,)
        return QABackdoorBase.whole_log(self, d, f)


class QAVarstoreBackdoor(UtilCommon):
    """ Test Library to interact with the QA backdoor and commandd HTTP server.

        As of right now the only exposed interface is the ability to get and set
        values of commandd variables in the current level."""

    def __init__(self, *args, **kwargs):
        UtilCommon.__init__(self, *args, **kwargs)
        self._qabd = QABackdoor(self.dut)
        self._commandd = commandd.VarstoreHTTPClient(self.dut)

    def get_keyword_names(self):
        return [
            'commandd_get_var',
            'commandd_change_var',
            'commandd_commit',
            'qa_backdoor_top',
            'qa_backdoor_get_info',
            'qa_backdoor_processes',
            'qa_backdoor_reboot',
            'qa_backdoor_netstat_active_sockets',
            'qa_backdoor_netstat_routes',
            'qa_backdoor_netstat_buffers',
            'qa_backdoor_current_interface_config',
            'qa_backdoor_list_open_files',
            'qa_backdoor_browse_logs',
            'qa_backdoor_whole_log',
            'qa_backdoor_cli_status',
            'qa_backdoor_reset_counters',
            'qa_backdoor_config',
            'qa_backdoor_set_qlog_buffer_size',
            'qa_backdoor_add_key',
            'qa_backdoor_replace_keys',
            'qa_backdoor_get_keys',
        ]

    def __getattr__(self, name):
        commandd_prefix = 'commandd_'
        qabd_prefix = 'qa_backdoor_'
        if name.startswith(commandd_prefix):
            return getattr(self._commandd, name[len(commandd_prefix):])
        elif name.startswith(qabd_prefix):
            return getattr(self._qabd, name[len(qabd_prefix):])
        else:
            raise AttributeError
