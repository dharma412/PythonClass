#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/common/util/checklogs.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $

# python import
import re
import itertools
import time

# sarf import
from common.util.utilcommon import UtilCommon


class CheckLogsResults:
    """
    initial parameters:

        unique_results - a dict of the followinf structure:
            key - error string
            value - dict of files and numbers of occurances

        other - errors which couldn't be parsed

        err_log - set that stores all errors occured during the run
    """

    err_log = set()

    def __init__(self, unique_results, other, utc_files):
        self.unique_results = unique_results
        self.other = other
        self.utc_files = utc_files

    def __str__(self):
        results = []

        for err in self.unique_results:
            res = ''

            for fname in self.unique_results[err]:
                res += '%s: %s\n' % (fname, self.unique_results[err][fname] \
                    ['occ'])

            res += '\n%s' % err
            results.append(res)

        sep = '\r\n%s\r\n\r\n' % ('-' * 79)
        remote_errors = sep.join(itertools.chain(results, self.other))
        return remote_errors


class CheckLogs(UtilCommon):
    """ Keywords for checking logs for errors

    *Aliaces of log files*

    Note: A parent folder for the following log file is specified in *bold*

    | | |
    | */data/log/heimdall/* | |
    | | |
    | hermes            | hermes/hermes.current |
    | heimdall          | heimdall/heimdall.current |
    | wbrsd             | wbrsd/wbrsd.current |
    | | |
    | */data/log/stdout/* | |
    | | |
    | stdout_heimdall   | stdout_heimdall.log |
    | | |
    | */data/pub/*        | |
    | | |
    | accesslogs        | accesslogs/aclog.current |
    | bypasslogs        | bypasslogs/tmon_bypass.current |
    | configdefragd     | configdefragd_logs/configdefragd_log.current |
    | gui               | gui_logs/gui.current |
    | mcafee            | mcafee_logs/mcafee_log.current |
    | proxylogs         | proxylogs/proxyerrlog.current |
    | authlogs          | authlogs/authlog.current |
    | reportd           | reportd_logs/reportd.current |
    | reportqueryd      | reportqueryd_logs/reportqueryd.current |
    | status            | status/status.log.current |
    | system            | system_logs/system.current |
    | updater           | updater_logs/updater_log.current |
    | wbnp              | wbnp_logs/wbnp_log.current |
    | wbrs              | wbrs_logs/wbrs_log.current |
    | webcat            | webcat_logs/webcat_log.current |
    | webroot           | webrootlogs/webrootlog.current |
    | welcomeack        | welcomeack_logs/welcomeack_log.current |
    | trackstats        | track_stats/prox_track.log |
    """

    def get_keyword_names(self):
        return ['check_logs']

    def check_logs(self, paths=None, patterns=None, exclude_patterns=None):
        """Check logs of Web Security Appliance

        Parameters:

            - `paths`: a string of comma separated values or a list of paths or
              the aliases (for standard log types) the errors should be searched
              in.

              Full list of possible aliases:
                heimdall, hermes, wbrsd, stdout_heimdall, accesslogs,
                bypasslogs, configdefragd, gui, mcafee, proxylogs, authlogs,
                reportd, reportqueryd, status, system, updater, wbnp, wbrs,
                webcat, webroot, welcomeack, trackstats.

              Absolute paths that are used behind these aliases are specified
                in `Introduction` section.

            - `patterns`: string of comma separated value or a list of error
              patterns. Patterns are case sensitive and can be an extended
              regular expression for 'grep' command.

            - `exclude_patterns`: list of exceptional patterns, lines that match
              these patterns are excluded from validation and do not affect
              result of the test case

        Results:
            Print all error lines from log and raise an exception when errors
            are found.
            Print 'No errors found" otherwise.

        Examples:
        | Check Logs |
        | Check Logs | paths=heimdall, gui, /data/log/heimdall/coeuslogd/coeuslogd.current |
        | Check Logs | patterns=.*10:3[0-9], .*22:3[0-9] | exclude_patterns=WARN, Failed |
        """
        fs_paths = self._shell.paths
        grep_results = ''
        traceback_results = []
        # this pattern found in DUT logs will help to list out the log files
        # which are created at UTC
        utc_pat = 'Time offset from UTC: 0 seconds'
        utc_grep_results = ''
        # Traceback should be handled separately
        tb_patt = 'Traceback'

        if patterns is not None:
            # convert from string os comma separated values into list
            if isinstance(patterns, basestring):
                patterns = [str(pattern.strip()) \
                            for pattern in patterns.split(',')]

        patterns = patterns or ['Error', 'Critical', 'Exception', 'appfault',
                                'application.fault', 'failed consistency check',
                                'No module named']
        self._info("Patterns to grep: " + ', '.join(patterns))

        if exclude_patterns is not None:
            # convert from string os comma separated values into list
            if isinstance(exclude_patterns, basestring):
                exclude_patterns = [str(pattern.strip()) \
                                    for pattern in exclude_patterns.split(',')]
            self._info("Patterns excluded from grep: " +
                       ', '.join(exclude_patterns))

        if paths is not None:
            # convert from string os comma separated values into list
            if isinstance(paths, basestring):
                paths = [str(path.strip()) for path in paths.split(',')]

            # replace aliaces with absolute paths
            for i in range(len(paths)):
                if paths[i] in fs_paths.heimdall_logs:
                    paths[i] = fs_paths.heimdall_logs[paths[i]]
                elif paths[i] in fs_paths.user_logs:
                    paths[i] = fs_paths.user_logs[paths[i]]
                elif paths[i] in fs_paths.stdout_logs:
                    paths[i] = fs_paths.stdout_logs[paths[i]]

            # custom paths are specified
            custom_paths = True
        else:
            custom_paths = False

        paths = paths or [fs_paths.heimdall_logs._base,
                          fs_paths.user_logs._base,
                          fs_paths.stdout_logs._base]
        self._info("Paths to be used in grep: " + ', '.join(paths))

        for _path in paths:
            #########
            # Temporarily exclude heimdall/splunkd/splunkd.current and splunkd.c
            #########
            cmd = 'grep -hr -A25 Traceback %s | ' \
                  'sed "/%s.*/p;/^  .*/p;/Error/p;/Interrupt/p;/./d" ' \
                  % (_path, tb_patt)

            traceback_results.append(self._shell.send_cmd(cmd).strip())
            # DUT log files created at UTC
            cmd = """grep -Eri "%s" %s """ % (utc_pat, _path)
            utc_grep_results += (self._shell.send_cmd(cmd).strip())

        for patt in patterns:
            for log_path in paths:
                cmd = """grep -EriI --exclude=prox_track.log """ \
                      """--exclude=configdefragd.current """ \
                      """--exclude="configdefragd\.@[0-9]*\.[cs]" "%s" %s | """ \
                      """grep -v configuration | grep -v "Info: " | """ \
                      """grep -v "INFO: " | grep -v "Warning: " | """ \
                      """grep -v "DEBUG:" | """ \
                      """grep -v "\/tmp\/merlin_query\.sock" | """ \
                      """grep -v "winbind" | grep -v "domain list" | """ \
                      """grep -v "fetch our SID" |  grep -v "ERROR_PAGE" | """ \
                      """grep -v "errorPage*" | grep -v "error_page*" | """ \
                      """grep -v "ManifestAcquisitionError" | """ \
                      """grep -v "Scanning Error" | """ \
                      """grep -v "ERR_INTERNAL_ERROR" | """ \
                      """grep -v "error 22 in LargeFile_BlockWriteDone" | """ \
                      """grep -v "tunnel error" | grep -v "waitpid error" | """ \
                      """grep -v "ads_sasl_spnego_krb5_bind failed" | """ \
                      """grep -v "error_code" | """ \
                      """grep -v "capacity reporting: exception:" | """ \
                      """grep -v "ERROR: <class 'system_health\.coro_snmp\.""" \
                      """NetworkError'>" | """ \
                      """grep -v "ERROR: <class 'system_health\.coro_snmp\.""" \
                      """TimeoutError'>" | """ \
                      """grep -v "AVC_Engine read_thread: packet: 0 bytes:" | """ \
                      """grep -v "AVC_Engine failed to connect to /tmp/""" \
                      """avc_cb_fastrpc\.sock" | """ \
                      """grep -v "exceptions\.client\.xobni\.com/exceptions" | """ \
                      """grep -v "SSL3_READ_BYTES:tlsv1" | """ \
                      """grep -v "ErrorCode=" | """ \
                      """grep -v -E "wbrs traceback.*wbrs_mgmt.py send_to_wbrs_mgmt.*class .wbrs.wbrs_mgmt.WBRSManagementError.*File.*mgmt_server.py.*in __mgmt_server_handler.*No such file or directory" | """ \
                      """grep -v -E "Errno 2.*No such file or directory.*/data/tmp/wbnpd_rpc.sock" | """ \
                      """grep -v "Test Log Message" """ % (patt, log_path)

                # Don't match on any lines matched by an exclude pattern
                if exclude_patterns:
                    for ex_patt in exclude_patterns:
                        cmd += ' | grep -v "%s"' % ex_patt

                # get curl results
                curl_res = self._shell.send_cmd(cmd).strip()
                if custom_paths:
                    # path to log file is not included in grep result
                    if curl_res.strip():
                        grep_results += '\n' + log_path + ': ' + curl_res
                else:
                    # path is included by grep, no need to include them here
                    grep_results += '\n' + curl_res
                self._debug(cmd)

        cmd = "find %s -name '*core'" % fs_paths.core_dumps
        grep_results += '\n' + self._shell.send_cmd(cmd).strip()
        self._debug(grep_results)

        # remove all 'Bogus work queue app fault' errors from the list, we make
        # those ourselves.  Make a copy of grep_results first.
        results = grep_results.splitlines()
        for result_str in grep_results.splitlines():
            # delete our target app faults from the copy, not the original
            # so as not to screw up the loop counter
            if 'Bogus work queue app fault' in result_str:
                results.remove(result_str)
            # exclude PthreadException
            elif 'PthreadException' in result_str:
                results.remove(result_str)
            # ignore Critical: page not found
            elif 'page not found' in result_str:
                results.remove(result_str)
            # ignore relation already exists
            elif re.search(r'relation .* already exists', result_str):
                results.remove(result_str)
            # system_logs are not an issue
            elif 'system_logs' in result_str:
                results.remove(result_str)
            elif 'RPC: OSError' in result_str:
                results.remove(result_str)
            elif re.search(r'a[s|v]archive', result_str):
                results.remove(result_str)
            # Listing configuration variables in stdout_upgrade.log
            elif 'Configuring application' in result_str:
                results.remove(result_str)
            # stdout_upgrade.log has this benign error
            elif 'exit_save_error unknown' in result_str:
                results.remove(result_str)
            # Non-critical RAID errors should not fail checklogs
            elif 'reason other error' in result_str:
                results.remove(result_str)

        # join similar errors
        # unique_results - dict of following structure:
        #   key - error string,
        #   value - dict of files and numbers of occurances
        unique_results = {}
        other = []
        results += traceback_results

        for error in results:
            # check if error is empty string and continue
            if not error.strip():
                continue

            date_patt = '\w+ +\w+ +\d?\d +\d\d:\d\d:\d\d +\d\d\d\d|\d\d\d\d-\d\d-\d\d +\d\d:\d\d:\d\d'
            patt = '(?P<fname>^/data/[pub|log]/.*?)(\s+|:(\d*:\s*|\s*)(?P<date>%s)?\s*(?P<errmsg>.*))' % date_patt
            mo = re.search(patt, error)

            # Add the error message to the set
            CheckLogsResults.err_log.add(error)

            if not mo:
                other.append(error)
                continue

            err_msg = mo.group('errmsg')
            date_string = mo.group('date')
            fname = mo.group('fname')
            if date_string:
                date = self.convert_datestr_to_epoch(date_string)
            elif fname:
                date = self.get_file_modification_time(self._shell, fname)

            # removing unimportant process number
            if err_msg:
                err_msg = re.sub(r'\[\d+\]', '', err_msg)

            if not unique_results.has_key(err_msg):
                unique_results[err_msg] = {fname: {'occ': 1, 'time_stamp': [date]}}
            elif not unique_results[err_msg].has_key(mo.group(1)):
                unique_results[err_msg][fname] = {'occ': 1, 'time_stamp': [date]}
            else:
                unique_results[err_msg][fname]['occ'] += 1
                unique_results[err_msg][fname]['time_stamp'].append(date)

        errors = str(CheckLogsResults(unique_results, other,
                                      utc_grep_results)).strip()
        if errors:
            self._info(errors)
            raise Exception('Errors found in log file(s)')
        else:
            self._info('No errors in log file(s)')

    def get_file_modification_time(self, fname):
        """ Retruns the file creation/modification time.
        """
        cmd = 'ls -lT ' + fname
        ls_output = self._shell.send_cmd(cmd).strip()
        date_patt = '\w+ +\d?\d +\d\d:\d\d:\d\d +\d\d\d\d|\d\d\d\d-\d\d-\d\d +\d\d:\d\d:\d\d'
        patt = '(?P<date>%s)' % date_patt
        mo = re.search(patt, ls_output)
        date_string = mo.group('date')
        return self.convert_datestr_to_epoch(date_string)

    def guess_date_format(self, date_string):
        """ Returns the date format of the given date string.
        """
        if re.search('\w+ +\w+ +\d?\d +\d\d:\d\d:\d\d +\d\d\d\d', date_string):
            return "%a %b %d %H:%M:%S %Y"
        if re.search('\w+ +\d?\d +\d\d:\d\d:\d\d +\d\d\d\d', date_string):
            return "%b %d %H:%M:%S %Y"
        if re.search('\d\d\d\d-\d\d-\d\d +\d\d:\d\d:\d\d', date_string):
            return "%Y-%m-%d %H:%M:%S"

    def convert_datestr_to_epoch(self, date_string):
        """ Returns the time in epoch seconds for the given date string.
        """
        date_format = self.guess_date_format(date_string)
        date = time.strptime(date_string, date_format)
        return time.mktime(date)
