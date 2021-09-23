#!/usr/bin/env python

# python import
import re
import itertools
import time

# sarf import
import common.shell.esa_paths
import sal.time
from common.util.utilcommon import UtilCommon

default_timeout = 30


class QlogResults(UtilCommon):
    def __init__(self, cmd='', log_patt='', out='', trace=None):
        self.log_patt = log_patt
        self.cmd = cmd
        self.out = out
        self.found_lines = []
        self.match_qty = -1
        self.trace = trace
        # parse the output
        self.parse()

    def __str__(self):
        s = ' %-50s %-s ' % \
            (self.log_patt, self.match_qty)
        return s

    def parse(self):
        # cleanup the output
        self.out = self.out.strip()

        # calculate match_qty and found_lines
        self.found_lines = []
        # Skip first line.  It's the grep command and always matches.
        for line in self.out.split('\n'):
            line = line.strip()
            if re.search('grep -HEriI ', line):
                self._info('Skipping the grep command from the output')
                continue
            if re.search(self.log_patt, line):
                self.found_lines.append(line)
        if self.trace:
            self._info('\n'.join(self.found_lines))
        self.match_qty = len(self.found_lines)


class LogReader(UtilCommon):
    """ Keywords for searching a file/files inside a path on the MGA for a
        pattern that has been specified

        *Aliases of log files* (for standard log types) which can be used as a
        shortcut for the filename:

        | | |
        | */data/log/heimdall/* | |
        | | |
        | hermes            | hermes/hermes.current |
        | heimdall          | heimdall/heimdall.current |
        | | |
        | */data/log/stdout/* | |
        | | |
        | stdout_brightmail | stdout_brightmail.log |
        | stdout_hermes     | stdout_hermes.log |
        | stdout_mcafee     | stdout_mcafee.log |
        | stdout_sophos     | stdout_sophos.log |
        | stdout_thirdparty | stdout_thirdparty.log |
        | | |
        | */data/pub/*        | |
        | | |
        | antispam          | antispam/antispam.current |
        | antivirus         | antivirus/antivirus.current |
        | asarchive         | asarchive/antispam_archive.mbox.current |
        | avarchive         | avarchive/antivirus_archive.mbox.current |
        | bounces           | bounces/bounces.text.current |
        | brightmail        | brightmail/brightmail.current |
        | case              | case/case.curren |
        | encryption        | encryption/encryption.current |
        | euq               | euq_logs/euq.current |
        | euqgui            | euqgui_logs/euqgui.current |
        | gui               | gui_logs/gui.current |
        | mail              | mail_logs/mail.current |
        | status            | status/status.log.current |
        | system            | system_logs/system.current |
        | trackerd          | trackerd_logs/trackerd.current |
        | reportd           | reportd_logs/reportd.current |
        | reportqueryd      | reportqueryd_logs/reportqueryd.current |
        | updater           | updater_logs/updater_log.current |
        | sntpd             | sntpd_logs/sntpd.current |
        | scanning          | scanning/scanning.text.current |
        | repeng            | repeng/repeng.current |
        | ftpd              | ftpd_logs/ftpd.current |
        | error             | error_logs/errors.current |
        | crash_archive     | crash_archive/crash.current |
        | authentication    | authentication/authentication.current |
        | cli               | cli/cli.current |
        | slbld             | slbld_logs/slbld.current |
        | threatfeeds       | threatfeeds/threatfeeds.current |

        Note: Parent folder for the log files is specified in *bold*
    """

    def get_keyword_names(self):
        return [
            'log_search',
        ]

    def log_search(self, log_pattern, search_path=None,
                   exclude_patterns=None, timeout=default_timeout, trace=None):
        """
        Searches the specified pattern in the file/files inside the
        path specified.

        *Parameters*
        - `log_pattern`: This is the only mandatory parameter.
          Patterns are case sensitive and can be an extended regular
          expression for 'grep' command.
        - `search_path=`: can be alias name (specified in the introduction
          section) or absolute path name.Default is alias name 'mail'.
        - `exclude_patterns=`: comma spearated list of strings which will be
          excluded from the grep result output. If a line matches both
          'log_pattern' & 'exclude_patterns', then line will be excluded.
        - `timeout=`: Time for which pattern will be searched in the specified
          path. Default is 30sec.

        *Return*
        List containing match count of the pattern & a list containing the lines
        matching the pattern. If no matching pattern, then output is (0,[]).
        If an exception is thrown, values returned are:
        ('FAIL', u'<Reason For Failure>').

        *Exceptions*
        - `IOError`: If specified path/alias name  doesn't exist.
        - `ValueError`: If timeout value specified is not float

        *Example*
        | ${output}= | Log Search | User admin commit | search_path= | system |
        | ${output}= | Log Search | score|misses|MID .* ICID .* From: |
        | ... | search_path= | mail | exclude_patterns= | adds |
        """
        fs_paths = {}
        _paths = common.shell.esa_paths.get_paths()
        fs_paths.update(_paths.user_logs)
        fs_paths.update(_paths.heimdall_logs)
        fs_paths.update(_paths.stdout_logs)

        if search_path:
            if fs_paths.has_key(search_path):
                log_path = fs_paths[search_path]
            else:
                log_path = search_path
        else:
            log_path = fs_paths['mail']
        self._info("Path to search: " + log_path)

        out = self._shell.send_cmd("ls %s" % (log_path)).strip()
        if out.find('No such file or directory') != -1:
            raise IOError, "There is no such path"

        self._info("Patterns to grep: " + log_pattern)

        if exclude_patterns is not None:
            # convert from string os comma separated values into list
            if isinstance(exclude_patterns, basestring):
                exclude_patterns = [str(pattern.strip()) \
                                    for pattern in exclude_patterns.split(',')]
            self._info("Patterns excluded from search: " +
                       ', '.join(exclude_patterns))

        cmd = """grep -HEriI "%s" %s""" % (log_pattern, log_path)

        # Don't match on any lines matched by an exclude pattern
        if exclude_patterns:
            for ex_patt in exclude_patterns:
                cmd += ' | grep -v "%s"' % ex_patt
        results = None
        tmr = sal.time.CountDownTimer(timeout).start()
        while tmr.is_active():
            cmd_output = self._shell.send_cmd(cmd).strip()
            results = QlogResults(cmd, log_pattern, cmd_output, trace)
            if results.match_qty > 0:
                break
            time.sleep(1)

        return (results.match_qty, results.found_lines)
