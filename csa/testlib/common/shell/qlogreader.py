#!/usr/bin/env python
# $Header: //prod/main/sarf_centos/testlib/common/shell/qlogreader.py#1 $

"""
QlogReader
------------
- grep the WGA log files and search for specific qlog entries.
- return QlogResults object which contains information
  about the grep results.

Restrictions:
- file is restricted to  euq_gui.text/euq_gui.text.current
- pattern is restricted to only qlog_euq_gui_messages_en qcodes

TERMINOLOGY
qcode: short for qlog code. It's the integer value used
       to identify a qlog message. The qlog codes are defined
        in godspeed/qlog/qlog_codes.py.

TODO:
- map qcode to (one or more) logfile(s) (ie. search multiple log files )
- handle freeform search patterns
"""

import re
import types
import time

import sal.time
import qlogmsgs

debug = False
# debug = True

default_timeout = 60


def is_tuple(t):
    return bool(types.TupleType == type(t))


class QlogResults:
    def __init__(self, qcode_name='', cmd='', log_patt='', out=''):
        self.qcode_name = qcode_name
        self.log_patt = log_patt
        self.cmd = cmd
        self.out = out
        self.found_lines = []
        self.match_qty = -1

        # parse the output
        self.parse()

    def __str__(self):
        s = '%-35s %-50s %-s ' % \
            (self.qcode_name, self.log_patt, self.match_qty)
        return s

    def parse(self):
        # cleanup the output
        self.out = self.out.strip()

        # calculate match_qty and found_lines
        self.found_lines = []
        # Skip first line.  It's the grep command and always matches.
        for line in self.out.splitlines():
            line = line.strip()
            if re.search(self.log_patt, line):
                self.found_lines.append(line)
        self.match_qty = len(self.found_lines)


def _is_restricted(qcode, *args):
    """The regex for these qcodes are too generic and will
    match everything in the logs so we require at least one
    arg to be specified."""
    restricted = ('EUQ_INFO', 'EUQ_DEBUG',
                  'EUQ_WARN', 'EUQ_ERROR',
                  'EUQ_CRITICAL', 'GUI_MISC_ERROR')
    if qcode in restricted:
        if len(args) <= 0:
            return True
    return False


class QlogReader:
    """Search a log file on the WGA for a pattern that has been specified
         in one of the  qlog* godspeed modules.
    """

    def __init__(self, shell, filename=None):
        """
        filename: search this log file located on the wga filesystem
        """
        self.shell = shell
        self.timeout = default_timeout

        # set self.files and self.messages
        self.files = {}

        qlog_dir = '/data/pub/'
        qlog_files = {
            # The dictionary key is the base of the filename (ie. everything
            # but the directory path and .current extension)
            'access': qlog_dir + '/accesslogs/aclog.current',
            'mcafee': qlog_dir + '/mcafee_logs/mcafee_log.current',
            'wbnp': qlog_dir + '/wbnp_logs/wbnp_log.current',
            'wbrs': qlog_dir + '/wbrs_logs/wbrs_log.current',
            'shd': qlog_dir + '/shd_logs/shd.current',
            'welcomeack': qlog_dir + \
                          '/welcomeack_logs/welcomeack_log.current',
            'proxy': qlog_dir + '/proxylogs/proxyerrlog.current',
            'idsdataloss': qlog_dir + \
                           '/idsdataloss_logs/idsdataloss_log.current',
            'status': qlog_dir + '/status/status.log.current',
            'cli': qlog_dir + '/cli_logs/cli.current'
        }
        self.files.update(qlog_files)

        self.all_qlog_msgs = {}
        self.all_qlog_msgs.update(qlogmsgs.messages)

        # set self.filename
        if filename != None:
            self.set_filename(filename)
        else:  # pick a default log file to search
            self.filename = self.files['access']

    def set_filename(self, filename):
        """The following shortcut log names can be used for filename

            'access' : Access Logs
            'wbnp'   : WBNP Logs
            'wbrs'   : WBRS Logs

        The shortcut log names are defined in
        $IAF2_HOME/etc/iaf/dutmodelcfg/wga.cfg
        """
        if self.files.has_key(filename):
            self.filename = self.files[filename]
        else:
            self.filename = filename

    def set_timeout(self, timeout):
        self.timeout = timeout

    def get_qcodes(self):
        """return all known qcodes"""
        return self.all_qlog_msgs.keys()

    def qcode_search(self, qcode, *args):
        """Grep log file specified by self.filename  on the WGA.
        Use the value of qcode as the pattern to search for.

        The ~\d~ variables are replaced with .* in the search pattern.
        Intepreted shell characters are replaced with .* in the search pattern.

        Return a QlogResults object.
        """
        # convert qcode name to qcode integer
        if _is_restricted(qcode, *args):
            # must specify args for restricted qcodes
            results = QlogResults(qcode_name=qcode)  # return empty results
            return results

        # set log_patt
        log_string_or_tuple = self.all_qlog_msgs[qcode]
        log_patt = ''
        if is_tuple(log_string_or_tuple):
            log_patt = log_string_or_tuple[0]
        else:
            log_patt = log_string_or_tuple

        log_patt = log_patt.replace('\n', '.')

        if log_patt.find('~1~') >= 0:
            # replace ~\d~ with *args, if *args exists
            for i in range(len(args)):
                log_patt = re.sub('~%d~' % (i + 1), str(args[i]), log_patt)
        elif log_patt.find('$') >= 0:
            assert qcode.find('.') >= 0  # make sure it's a new-format qlog entry
            # replace $<varname> with *args, if *args exists
            for i in range(len(args)):
                arg = str(args[i])
                try:
                    # treat arg as a number
                    float(arg)
                except ValueError:
                    # treat arg as a string.
                    # Enclose in single quotes (actually use wildchard).
                    arg = '.' + arg + '.'

                log_patt = re.sub('\$\w+', arg, log_patt, count=1)

        # replace remaining ~\d~ with wildcard (.*)
        log_patt = re.sub('~\d~', '.*', log_patt)

        # replace remaining $<varname> with wildcard (.*)
        log_patt = re.sub('\$\w+', '.*', log_patt)

        # replace problematic shell characters with wildchard('.')
        problem_characters = ("'",)  # allow []`|\\" to go unprocessed
        for pc in problem_characters:
            log_patt = log_patt.replace(pc, ".")

        if qcode != 'ANY':
            log_patt = log_patt + '$'

        results = self.search(log_patt, qcode_name=qcode)
        return results

    def search_now(self, log_patt, filename=None, parse_class=QlogResults,
                   quote_str="'"):
        return self.search(log_patt, filename, timeout=1,
                           parse_class=parse_class, quote_str=quote_str)

    def search(self, log_patt, filename=None, timeout=None,
               qcode_name=None, exp_qty=None, parse_class=QlogResults,
               quote_str="'", skip_hashed=True):
        """Grep log file specified by self.filename  on the WGA.
        Use the value of log_patt as the pattern to search for.
        Return a QlogResults object."""

        results = None
        fname = self.files.get(filename, filename) or self.filename

        cmd = "grep -E -i %s%s%s " % (quote_str, log_patt, quote_str) + fname + " 2> /dev/null"
        if skip_hashed:
            cmd += " | grep -v '#'"

        tmr = sal.time.CountDownTimer(timeout or self.timeout).start()
        while tmr.is_active():
            # grep log
            out = self.shell.send_cmd(cmd)

            # return parse_class
            results = parse_class(qcode_name or 'NO_QCODE', cmd, log_patt, out)

            if exp_qty != None:
                if results.match_qty == exp_qty:
                    break
            else:
                if results.match_qty > 0:
                    break

            time.sleep(1)

        if debug:
            print 'qlogreader.search():', results

        return results


if __name__ == '__main__':
    import shell

    logreader = QlogReader(shell.get_shell(iafcfg.get_cfg()))

    logreader.set_timeout(1)
    logreader.set_filename('access')

    match_by_string = True
    if match_by_string:
        results = logreader.search('text/html')
        print results
