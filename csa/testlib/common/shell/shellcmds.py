#!/usr/bin/python
__revision = '$Revision: #1 $'
"""
It allows the caller to:
    - control reporting test apps: testd, query_cli, multiple_table_reader,
                                   datagen.misc.tracking_printer
"""

from sal.shell.base import IafUnixShellBase
import re

DEBUG = True


# Beginning with phoebe63, test tool binaries:
#    testd, query_cli, multiple_table_reader, datagen.misc.tracking_printer,
#    datagen.tools.replay_trace, test_tracking_query_api
# are included within DUT's /usr/godspeed/bin/reportd.  Test script that tests
# Reporting should create the soft links for these test tools first in the
# specified 'test_tools_path' below on DUT.  See
# $IAF_HOME/tests/common/reporting20/reportingbase.ReportingTestSuiteBase.initialize() for
# example.
# test_tools_path is now passed in by shell.py  10/23/09

def check_tracebacks(text):
    # Look for explicit traceback or compact traceback
    if text.find('Traceback') != -1 or \
            re.findall('[a-zA-Z_-]+\|[0-9]+', text):
        raise RuntimeError, text


def check_unknown_option(text):
    if text.find('error: no such option') != -1:
        raise RuntimeError, text


class ShellCmdsBase(IafUnixShellBase):
    TOOL_NAME = ''

    def __init__(self, sess, test_tools_path):
        self.test_tools_path = test_tools_path
        IafUnixShellBase.__init__(self, sess)
        self.send_cmd('ln %s/reportd %s/%s ' %
                      (test_tools_path, test_tools_path, self.TOOL_NAME), timeout=180)


class TestdInterface(ShellCmdsBase):
    TOOL_NAME = 'testd'

    def testd(self, command_list):
        cmd = "%s/%s -d %s" % (self.test_tools_path, self.TOOL_NAME, command_list)
        if DEBUG:
            print "DEBUG: %s" % cmd
        out = self.send_cmd(cmd, timeout=300)
        check_tracebacks(out)

    def __call__(self, command_list):
        self.testd(command_list)


class TrackerApi(ShellCmdsBase):
    TOOL_NAME = 'test_tracking_query_api'

    def tracker_api(self, **kwargs):
        opts = ''

        for varname, val in kwargs.items():
            opts += " --%s=%s" % (varname, repr(val))

        cmd = '%s/%s %s' % (self.test_tools_path, self.TOOL_NAME, opts)

        if DEBUG:
            print "DEBUG: %s" % cmd
        out = self.send_cmd(cmd, timeout=180)
        check_tracebacks(out)
        check_unknown_option(out)

        return out

    def __call__(self, **kwargs):
        return self.tracker_api(**kwargs)


class DatagenReplayTrace(ShellCmdsBase):
    TOOL_NAME = 'datagen.tools.replay_trace'

    def datagen_replay_trace(self, qlog_file, eps, max_count,
                             duration, shift_time, floor_time,
                             ignore_timestamps):

        # Do -v and -d by default
        opts = "-v -d"

        for varname, val in (('eps', eps),
                             ('max-count', max_count),
                             ('duration', duration),
                             ('shift-time', shift_time),
                             ('floor-time', floor_time)):
            if val != None:
                opts += " --%s=%s" % (varname, str(val))

        if ignore_timestamps:
            opts += " --ignore-timestamps"

        cmd = '%s/%s %s %s' % (self.test_tools_path, self.TOOL_NAME, opts,
                               qlog_file)
        if DEBUG:
            print "DEBUG: %s" % cmd
        out = self.send_cmd(cmd, timeout=180)
        check_tracebacks(out)

    def __call__(self, qlog_file, eps=None, max_count=None,
                 duration=None, shift_time=None,
                 floor_time=None, ignore_timestamps=None):
        self.datagen_replay_trace(qlog_file, eps, max_count,
                                  duration, shift_time, floor_time,
                                  ignore_timestamps)


class BinaryLogReader(ShellCmdsBase):
    TOOL_NAME = 'datagen.misc.tracking_printer'

    def binary_log_reader(self, log_file):
        if not log_file:
            log_file = '/var/log/godspeed/tracking/tracking/tracking.current'
        cmd = '%s/%s %s' % (self.test_tools_path, self.TOOL_NAME, log_file)
        out = self.send_cmd(cmd, timeout=60)
        check_tracebacks(out)
        return out

    def __call__(self, log_file=None):
        return self.binary_log_reader(log_file)


class QueryCLI(ShellCmdsBase):
    TOOL_NAME = 'query_cli'

    def chop_cruft(self, output):
        """ This function is a product of pain in dealing with the query_cli output:

        - We want to cut out the time report that is appended to all output (last line)
        - If there is any "Invalid X, Doing something" statement, filter it out
        - If there is a traceback, punt and return all of the output
        """
        olines = output.splitlines()[:-1]
        for i in range(len(olines) - 1, -1, -1):
            if olines[i].lstrip().startswith('Invalid'):
                del olines[i]
            elif olines[i].find('Traceback') != -1:
                raise RuntimeError, output
        return '\r\n'.join(olines)

    def __call__(self, type, counter_names, period, range,
                 key=None, numeric_key=None,
                 as_period=None, period_num=None,
                 sort_counter_names=None,
                 sort_ascending=None,
                 serial_number=None,
                 group_id=None,
                 show_missing=None,
                 group_by_field_names=None,
                 field_constraints=None,
                 return_range=None,
                 per_host=None,
                 timeout=None):

        cmd = "%s/%s --type=%s --counter_names=%s " \
              "--period=%s --range='%s' " % (self.test_tools_path, self.TOOL_NAME,
                                             type, counter_names, period, range)
        for varname, val in (('as_period', as_period),
                             ('period_num', period_num),
                             ('key', key),
                             ('sort_counter_names', sort_counter_names),
                             ('group_id', group_id),
                             ('group_by_field_names', group_by_field_names),
                             ('field_constraints', field_constraints),
                             ('return_range', return_range),
                             ('serial_number', serial_number),
                             ('per_host', per_host)):
            if val:
                cmd += "--%s=%s " % (varname, val)
        for varname, val in (('numeric_key', numeric_key),
                             ('sort_ascending', sort_ascending),
                             ('show_missing', show_missing)):
            if val:
                cmd += "--%s " % (varname)
        if DEBUG: print cmd
        return self.chop_cruft(self.send_cmd(cmd, timeout=timeout))

    def interval_time_range_query(self, counter_names, period, range,
                                  key=None, as_period=None, period_num=None,
                                  host=None, serial_number=None, timeout=None):

        cmd = "%s/%s --type=IntervalTimeRangeQuery --counter_names=%s " \
              "--period=%s --range='%s' " % (self.test_tools_path, self.TOOL_NAME,
                                             counter_names, period, range)
        for varname, val in (('key', key),
                             ('as_period', as_period),
                             ('period_num', period_num),
                             ('per_host', host),
                             ('serial_number', serial_number)):
            if val:
                cmd += "--%s=%s " % (varname, val)
        if DEBUG: print cmd
        return self.chop_cruft(self.send_cmd(cmd, timeout=timeout))

    def interval_time_merge_query(self, counter_names, period, range, key=None,
                                  sort_counter_names=None, return_range=None,
                                  sort_ascending=False, host=None,
                                  serial_number=None, timeout=None):
        cmd = "%s/%s --type=IntervalTimeMergeQuery --counter_names=%s " \
              "--period=%s --range='%s' " % (self.test_tools_path, self.TOOL_NAME,
                                             counter_names, period, range)
        for varname, val in (('key', key),
                             ('sort_counter_names', sort_counter_names),
                             ('return_range', return_range),
                             ('per_host', host),
                             ('serial_number', serial_number)):
            if val:
                cmd += "--%s=%s " % (varname, val)
        if sort_ascending:
            cmd += "--sort_ascending"
        if DEBUG: print cmd
        return self.chop_cruft(self.send_cmd(cmd, timeout=timeout))

    def slice_time_merge_query(self, counter_names, period, range, key=None,
                               sort_counter_names=None, return_range=None,
                               sort_ascending=False, numeric_key=None,
                               host=None, serial_number=None, timeout=None):

        cmd = "%s/%s --type=SliceTimeMergeQuery --counter_names=%s " \
              "--period=%s --range='%s' " % (self.test_tools_path, self.TOOL_NAME,
                                             counter_names, period, range)
        for varname, val in (('key', key),
                             ('sort_counter_names', sort_counter_names),
                             ('return_range', return_range),
                             ('per_host', host),
                             ('serial_number', serial_number)):
            if val:
                cmd += "--%s=%s " % (varname, val)
        if sort_ascending:
            cmd += "--sort_ascending "
        if numeric_key:
            cmd += "--numeric_key "
        if DEBUG: print cmd
        return self.chop_cruft(self.send_cmd(cmd, timeout=timeout))

    def slice_time_range_query(self, counter_names, period, range,
                               key=None, numeric_key=None, as_period=None,
                               period_num=None, host=None,
                               serial_number=None, timeout=None):

        cmd = "%s/%s --type=SliceTimeRangeQuery --counter_names=%s " \
              "--period=%s --range='%s' " % (self.test_tools_path, self.TOOL_NAME,
                                             counter_names, period, range)
        for varname, val in (('key', key),
                             ('as_period', as_period),
                             ('period_num', period_num),
                             ('per_host', host),
                             ('serial_number', serial_number)):
            if val:
                cmd += "--%s=%s " % (varname, val)
        if numeric_key:
            cmd += "--numeric_key "
        if DEBUG: print cmd
        return self.chop_cruft(self.send_cmd(cmd, timeout=timeout))


class MultipleTableReader(ShellCmdsBase):
    TOOL_NAME = 'multiple_table_reader'

    def multiple_table_reader(self,
                              counter_group,
                              output=None,
                              counter_manifest=None,
                              counter_def=None,
                              schema_dir=None):

        opts = ''

        for varname, val in (('counter-group', counter_group),
                             ('output', output),
                             ('counter-manifest', counter_manifest),
                             ('counter-def', counter_def),
                             ('schema-dir', schema_dir)):
            if val != None:
                opts += ' --%s=%s' % (varname, str(val))

        cmd = '%s/%s %s' % (self.test_tools_path, self.TOOL_NAME, opts)
        if DEBUG:
            print "DEBUG: %s" % cmd
        self.send_cmd(cmd)
        check_tracebacks(out)
