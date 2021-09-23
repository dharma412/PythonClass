#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/common/util/reporting_counters.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $

import datetime
import re

from sal.shell.base import IafUnixShellBase
from common.util.utilcommon import UtilCommon
from common.shell.shellcmds import QueryCLI


class QueryCLICheckError(Exception):
    """
        Incorrect values were returned by query_cli
    """

    # The special exception the product page validator
    def __init__(self, msg):
        self.msg = msg

    # Returns formated exception
    def __str__(self):
        return str(self.msg)

    # used by Robot Framework to print message to console and log
    def __unicode__(self):
        return unicode(self.__str__())


class ReportingBase(UtilCommon):
    """
        - Define many verify* functions to test output from test binaries
        - All verify* functions return a 3-tuple:
              (test_result, description of the failure, error output)
        - Remove /var/log/godspeed/reporting/* and restart reportd (in initialize)
    """

    #    def __init__(self, *args, **kwargs):
    #        UtilCommon.__init__(self, *args, **kwargs)
    #        self.start_shell_session()

    def verify_results_file(self, cmd_out, cmp_file):
        """ Do a simple string comparison against a file in the
            $IAF2_HOME/tests/data/reportingXX/resultfiles directory """

        # Load file into string
        cmp_filename = '%s/tests/data/reporting/resultfiles/%s' \
                       '' % (os.environ['IAF2_HOME'], cmp_file)
        fobj = open(cmp_filename)
        exp_list = fobj.readlines()
        fobj.close()

        act_list = cmd_out.splitlines()

        if act_list == exp_list:
            return (True, None, None)
        else:
            # Write actual output file
            out_file = '%s/%s' % (tempfile.gettempdir(),
                                  self.__class__.__name__)
            out_obj = open(out_file, 'w')
            out_obj.write(cmd_out)
            out_obj.close()

            self._info('\nActual query_cli output: %s\nDoes not match ' \
                       'Expected output file: %s' % (out_file, cmp_filename))

            # No need to provide description because we've already reported
            # the error above.
            return (False, None, None)

    def verify_results_object(self, cmd_out, cmp_obj):
        self._debug(("cmd_out:", cmd_out))
        self._debug(("cmp_obj:", cmp_obj))
        # If cmd_out is the empty string, do str compare.
        stripped_cmd = cmd_out.strip()
        stripped_cmd = stripped_cmd.replace("\r\n", ",")
        cmp_obj = str(cmp_obj).replace("\r\n", ",")
        if not stripped_cmd:
            return self.verify_results_string(stripped_cmd, cmp_obj)

        # Do a simple python object comparison
        try:
            if eval(stripped_cmd) == eval(cmp_obj):
                return (True, None, None)
            else:
                return (False, "Does not match", cmd_out)
        except SyntaxError:
            return (False, "^^ Previous Error ^^ does not match", cmd_out)

    def verify_results_string(self, cmd_out, cmp_obj):
        if cmd_out.strip() == cmp_obj:
            return (True, None, None)
        else:
            return (False, "Does not match", cmd_out)

    def verify_results_list(self, cmd_out, cmp_obj):
        """ Create a list of the output rows and compare this list
            to the expected results.
        """
        return self.verify_results_object(cmd_out.splitlines(), cmp_obj)

    def verify_results_len(self, cmd_out, exp_len):
        """ Test to see if the correct number of rows was output from
            test binary.
        """
        if len(cmd_out.splitlines()) == exp_len:
            return (True, None, None)
        else:
            return (False, "Does not contain the correct number of rows:", cmd_out)

    def verify_results_substr(self, cmd_out, exp_substr):
        """ Test to see if the test binary output contains a given string.
            This is most useful for verifying test binary error output,
            Tracebacks, and other negative test cases.
        """
        if exp_substr in cmd_out:
            return (True, None, None)
        else:
            return (False, "Does not contain", cmd_out)


class ReportingCounters(ReportingBase):
    """
    Keywords for reporting counters.
    """

    def get_keyword_names(self):
        return [
            'interval_time_range_query',
            'interval_time_merge_query',
            'slice_time_merge_query',
            'slice_time_range_query',
            'verify_reporting_counters',
            'get_mail_incomming_clean_recepients_count',
            'get_mail_incomming_spam_count',
            'get_mail_virus_type_count',
            'get_mail_dlp_count',
            'get_mail_marketing_count',
            'get_mail_incoming_total_count',
            'get_web_malware_count',
            'get_web_allowed_count',
            'get_web_blocked_count',
            'get_web_total_count',
            'get_reporting_counters',
        ]

    #    def __init__(self, *args, **kwargs):
    #        ReportingBase.__init__(self, *args, **kwargs)

    def interval_time_range_query(self,
                                  counter_names=None,
                                  period=None, range=None,
                                  key=None, numeric_key=None,
                                  as_period=None, period_num=None,
                                  serial_number=None,
                                  group_id=None,
                                  show_missing=None,
                                  group_by_field_names=None,
                                  field_constraints=None,
                                  return_range=None,
                                  per_host=None,
                                  timeout=None):
        """Gets results of query_cli tool with 'IntervalTimeRangeQuery' type.

        Parameters:
            - `counter_names`: Comma-separated string of counters
            - `period`: rollup period
            - `range`: Comma-separated time range pair.
            - `key`: Comma-separated '<operator> <key>' pairs.
            - `numeric_key`: True if key is numeric
            - `as_period`: Period for aggregation.
            - `period_num`: Period number associated with as_period.
            - `serial_number`: Serial number for per-machine data
            - `group_id`: Group identifier for per-group data.
            - `show_missing`: True if you need to show missing intervals.
            - `group_by_field_names`: Comma-speparated counters for grouping by.
            - `field_constraints`: Comma-separated string of <field_contraints>.
            |    <field_constraint>:   <counter> <operator> [<value>|<value_1>-<value_2>]
            |    <operator>:
            |        '=' - for Equal query, need one value;
            |        '*' - for StartsWith query, need one value;
            |        'range' - for Range query, need two non-numeric values, hyphen sep;
            |        'range_numeric' - for Range query, need two numeric values, hyphen sep.
            |    If value starts with 'raw:', the convert-in function for this field will be skipped.
            |    If value starts with 'not_raw:', the convert-in function for this field will be called.
            |    Otherwise, default to 'not_raw:'.
            - `return_range`: return first n rows for an interval
            - `per_host`: host name for per host data.

        Return:
            Value, returned by query_cli tool for specified parameters.

        Examples:
        | ${query_result}= | Interval Time Range Query |
        | ... | counter_names=WEB_TRANSACTION.USER,WEB_TRANSACTION.TRANSACTIONS_TOTAL,WEB_TRANSACTION.TIME_SPENT |
        | ... | period=day |
        | ... | range=2006 02 01, 2006 04 01 |
        | ... | key=\'* z\' |
        | ... | as_period=day |
        | ... | period_num=1 |
        | ... | serial_number=001143EEC2BA-0000000 |
        | ... | show_missing=${True} |
        | ... | group_by_field_names=\'WEB_TRANSACTION.USER\' |
        | ... | field_constraints=\'WEB_TRANSACTION.USER = Nathan\' |
        | ... | return_range=0,20 |
        | Log | ${query_result} |
        """
        query_cli = self._shell.query_cli
        return query_cli('IntervalTimeRangeQuery',
                         counter_names,
                         period, range,
                         key, numeric_key,
                         as_period, period_num,
                         None,
                         None,
                         serial_number,
                         group_id,
                         group_by_field_names,
                         field_constraints,
                         return_range,
                         per_host,
                         timeout)

    def interval_time_merge_query(self,
                                  counter_names=None,
                                  period=None, range=None,
                                  key=None, numeric_key=None,
                                  as_period=None, period_num=None,
                                  sort_counter_names=None,
                                  sort_ascending=None,
                                  serial_number=None,
                                  group_id=None,
                                  group_by_field_names=None,
                                  field_constraints=None,
                                  return_range=None,
                                  per_host=None,
                                  timeout=None):
        """Gets results of query_cli tool with 'IntervalTimeMergeQuery' type.

        Parameters:
            - `counter_names`: Comma-separated string of counters
            - `period`: rollup period
            - `range`: Comma-separated time range pair.
            - `key`: Comma-separated '<operator> <key>' pairs.
            - `numeric_key`: ${True} if key is numeric
            - `as_period`: Period for aggregation.
            - `period_num`: Period number associated with as_period.
            - `sort_counter_names`: Comma-spepaarted string of sorting counters.
            - `sort_ascending`: ${True} if sort from least to greatest.
            - `serial_number`: Serial number for per-machine data
            - `group_id`: Group identifier for per-group data.
            - `group_by_field_names`: Comma-speparated counters for grouping by.
            - `field_constraints`: Comma-separated string of <field_contraints>.
            |    <field_constraint>:   <counter> <operator> [<value>|<value_1>-<value_2>]
            |    <operator>:
            |        '=' - for Equal query, need one value;
            |        '*' - for StartsWith query, need one value;
            |        'range' - for Range query, need two non-numeric values, hyphen sep;
            |        'range_numeric' - for Range query, need two numeric values, hyphen sep.
            |    If value starts with 'raw:', the convert-in function for this field will be skipped.
            |    If value starts with 'not_raw:', the convert-in function for this field will be called.
            |    Otherwise, default to 'not_raw:'.
            - `return_range`: return first n rows for an interval
            - `per_host`: host name for per host data.

        Return:
            Value, returned by query_cli tool for specified parameters.

        Examples:
        | ${query_result}= | Interval Time Range Query |
        | ... | counter_names=WEB_TRANSACTION.USER,WEB_TRANSACTION.TRANSACTIONS_TOTAL,WEB_TRANSACTION.TIME_SPENT |
        | ... | period=month |
        | ... | range=2006 02 01, 2006 04 01 |
        | ... | key=\'* z\' |
        | ... | as_period=day |
        | ... | period_num=1 |
        | ... | sort_counter_names=WEB_TRANSACTION.TRANSACTIONS_TOTAL |
        | ... | sort_ascending=${True} |
        | ... | serial_number=001143EEC2BA-0000000 |
        | ... | group_by_field_names=\'WEB_TRANSACTION.USER\' |
        | ... | field_constraints=\'WEB_TRANSACTION.USER = Nathan\' |
        | ... | return_range=0,20 |
        | Log | ${query_result} |
        """
        query_cli = self._shell.query_cli
        return query_cli('IntervalTimeMergeQuery',
                         counter_names,
                         period, range,
                         key, numeric_key,
                         as_period, period_num,
                         sort_counter_names,
                         sort_ascending,
                         serial_number,
                         group_id,
                         None,
                         group_by_field_names,
                         field_constraints,
                         return_range,
                         per_host,
                         timeout)

    def slice_time_merge_query(self,
                               counter_names=None,
                               period=None, range=None,
                               key=None, numeric_key=None,
                               as_period=None, period_num=None,
                               sort_counter_names=None,
                               sort_ascending=None,
                               serial_number=None,
                               group_id=None,
                               group_by_field_names=None,
                               field_constraints=None,
                               return_range=None,
                               per_host=None,
                               timeout=None):
        """Gets results of query_cli tool with 'SliceTimeMergeQuery' type.

        Parameters:
            - `counter_names`: Comma-separated string of counters
            - `period`: rollup period
            - `range`: Comma-separated time range pair.
            - `key`: Comma-separated '<operator> <key>' pairs.
            - `numeric_key`: ${True} if key is numeric
            - `as_period`: Period for aggregation.
            - `period_num`: Period number associated with as_period.
            - `sort_counter_names`: Comma-spepaarted string of sorting counters.
            - `sort_ascending`: ${True} if sort from least to greatest.
            - `serial_number`: Serial number for per-machine data
            - `group_id`: Group identifier for per-group data.
            - `group_by_field_names`: Comma-speparated counters for grouping by.
            - `field_constraints`: Comma-separated string of <field_contraints>.
            |    <field_constraint>:   <counter> <operator> [<value>|<value_1>-<value_2>]
            |    <operator>:
            |        '=' - for Equal query, need one value;
            |        '*' - for StartsWith query, need one value;
            |        'range' - for Range query, need two non-numeric values, hyphen sep;
            |        'range_numeric' - for Range query, need two numeric values, hyphen sep.
            |    If value starts with 'raw:', the convert-in function for this field will be skipped.
            |    If value starts with 'not_raw:', the convert-in function for this field will be called.
            |    Otherwise, default to 'not_raw:'.
            - `return_range`: return first n rows for an interval
            - `per_host`: host name for per host data.

        Return:
            Value, returned by query_cli tool for specified parameters.

        Examples:
        | ${query_result}= | Slice Time Range Query |
        | ... | counter_names=WEB_TRANSACTION.USER,WEB_TRANSACTION.TRANSACTIONS_TOTAL,WEB_TRANSACTION.TIME_SPENT |
        | ... | period=month |
        | ... | range=-1, 0 |
        | ... | key=\'* z\' |
        | ... | as_period=day |
        | ... | period_num=1 |
        | ... | sort_counter_names=WEB_TRANSACTION.TRANSACTIONS_TOTAL |
        | ... | sort_ascending=${True} |
        | ... | serial_number=001143EEC2BA-0000000 |
        | ... | group_by_field_names=\'WEB_TRANSACTION.USER\' |
        | ... | field_constraints=\'WEB_TRANSACTION.USER = Nathan\' |
        | ... | return_range=0,20 |
        | Log | ${query_result} |
        """
        query_cli = self._shell.query_cli
        return query_cli('SliceTimeMergeQuery',
                         counter_names,
                         period, range,
                         key, numeric_key,
                         as_period, period_num,
                         sort_counter_names,
                         sort_ascending,
                         serial_number,
                         group_id,
                         None,
                         group_by_field_names,
                         field_constraints,
                         return_range,
                         per_host,
                         timeout)

    def slice_time_range_query(self,
                               counter_names=None,
                               period=None, range=None,
                               key=None, numeric_key=None,
                               as_period=None, period_num=None,
                               serial_number=None,
                               group_id=None,
                               show_missing=None,
                               group_by_field_names=None,
                               field_constraints=None,
                               return_range=None,
                               per_host=None,
                               timeout=None):
        """Gets results of query_cli tool with 'SliceTimeRangeQuery' type.

        Parameters:
            - `counter_names`: Comma-separated string of counters
            - `period`: rollup period
            - `range`: Comma-separated time range pair.
            - `key`: Comma-separated '<operator> <key>' pairs.
            - `numeric_key`: True if key is numeric
            - `as_period`: Period for aggregation.
            - `period_num`: Period number associated with as_period.
            - `serial_number`: Serial number for per-machine data
            - `group_id`: Group identifier for per-group data.
            - `show_missing`: True if you need to show missing intervals.
            - `group_by_field_names`: Comma-speparated counters for grouping by.
            - `field_constraints`: Comma-separated string of <field_contraints>.
            |    <field_constraint>:   <counter> <operator> [<value>|<value_1>-<value_2>]
            |    <operator>:
            |        '=' - for Equal query, need one value;
            |        '*' - for StartsWith query, need one value;
            |        'range' - for Range query, need two non-numeric values, hyphen sep;
            |        'range_numeric' - for Range query, need two numeric values, hyphen sep.
            |    If value starts with 'raw:', the convert-in function for this field will be skipped.
            |    If value starts with 'not_raw:', the convert-in function for this field will be called.
            |    Otherwise, default to 'not_raw:'.
            - `return_range`: return first n rows for an interval
            - `per_host`: host name for per host data.

        Return:
            Value, returned by query_cli tool for specified parameters.

        Examples:
        | ${query_result}= | Slice Time Range Query |
        | ... | counter_names=WEB_TRANSACTION.USER,WEB_TRANSACTION.TRANSACTIONS_TOTAL,WEB_TRANSACTION.TIME_SPENT |
        | ... | period=day |
        | ... | range=-1, 0 |
        | ... | key=\'* z\' |
        | ... | as_period=day |
        | ... | period_num=1 |
        | ... | serial_number=001143EEC2BA-0000000 |
        | ... | group_by_field_names=\'WEB_TRANSACTION.USER\' |
        | ... | field_constraints=\'WEB_TRANSACTION.USER = Nathan\' |
        | ... | return_range=0,20 |
        | Log | ${query_result} |
        """
        query_cli = self._shell.query_cli
        return query_cli('SliceTimeRangeQuery',
                         counter_names,
                         period, range,
                         key, numeric_key,
                         as_period, period_num,
                         None,
                         None,
                         serial_number,
                         group_id,
                         show_missing,
                         group_by_field_names,
                         field_constraints,
                         return_range,
                         per_host,
                         timeout)

    def _get_expected_total(self, *args):
        _exp_total = 0
        _exp_present = False
        for _exp_value in args:
            if _exp_value is not None:
                _exp_present = True
                try:
                    _exp_value = int(_exp_value)
                    _exp_total += _exp_value
                except:
                    pass
        if _exp_present:
            return _exp_total
        else:
            return None

    def make_query_cli_data(self, counter_name, period, range, as_period,
                            period_num, exp_count=None, query_cli_extra_kwargs=None):

        query_cli_kwargs = {'as_period': as_period, 'period_num': period_num}

        if query_cli_extra_kwargs is not None:
            query_cli_kwargs.update(query_cli_extra_kwargs)

        query_cli_data = ()

        if exp_count is not None:
            try:
                exp_count = int(exp_count)
            except:
                pass

            if isinstance(exp_count, int):
                exp_count = "([], [" + str(exp_count) + "])"
            elif isinstance(exp_count, (basestring, str, unicode)):
                if len(exp_count) > 0 and exp_count[0] != '(':
                    exp_count = "([], ['" + exp_count + "'])"

        query_cli_data += ({
                               'query_cli_args': (counter_name, period, range),
                               'query_cli_kwargs': query_cli_kwargs,
                               'query_cli_results': exp_count,
                           },)
        return query_cli_data

    def verify_reporting_counters(self, mail_clean_count=None,
                                  mail_spam_count=None, mail_virus_count=None, mail_virus_type=None,
                                  mail_dlp_count=None, mail_marketing_count=None,
                                  mail_total_count=None,
                                  web_clean_count=None, web_blocked_wbrs_count=None,
                                  web_malware_count=None, web_total_count=None,
                                  period=None, range=None, as_period=None, period_num=None):
        """Verify reporting counters, returned by `query_cli` tool.

        Parameters:
            - `mail_clean_count`:
                Expectation for MAIL_INCOMING_TRAFFIC_SUMMARY.TOTAL_CLEAN_RECIPIENTS counter.
                Either number or string like '([], [expected_count])'.
                The value is not checked if the parameter was skipped.
            - `mail_spam_count`:
                Expectation for MAIL_INCOMING_TRAFFIC_SUMMARY.DETECTED_SPAM counter.
                Either number or string like '([], [expected_count])'.
                The value is not checked if the parameter was skipped.
            - `mail_virus_type`:
                Name of vrus type for filtering virus count.
                All types will be checked if the parameter is skipped.
            - `mail_virus_count`:
                Expectation for MAIL_VIRUS_TYPE_DETAIL.TOTAL_RECIPIENTS counter.
                String of comma-separated tuples like
                '([virus_type1], [expected_count1]), ([virus_type2],
                [expected_count2])', if virus type was not indicated, or
                expected number, if virus type was indicated in
                `mail_virus_type` parameter.
                The value is not checked if the parameter was skipped.
            - `mail_dlp_count`:
                Expectation for MAIL_DLP_OUTGOING_TRAFFIC_SUMMARY.TOTAL_DLP_INCIDENTS counter.
                Either number or string like '([], [expected_count])'.
                The value is not checked if the parameter was skipped.
            - `mail_marketing_count`:
                Expectation for MAIL_INCOMING_TRAFFIC_SUMMARY.MARKETING_MAIL counter.
                Either number or string like '([], [expected_count])'.
                The value is not checked if the parameter was skipped.
            - `mail_total_count`:
                Expectation for MAIL_INCOMING_TRAFFIC_SUMMARY.TOTAL_RECIPIENTS counter.
                Either number or string like '([], [expected_count])'.
                The value is not checked if the parameter was skipped.
            - `web_clean_url_count`:
                Expectation for WEB_SERVICES_SUMMARY.ALLOWED_TRANSACTION_TOTAL counter.
                Either number or string like '([], [expected_count])'.
                The value is not checked if the parameter was skipped.
            - `web_blocked_wbrs_url_count`:
                Expectation for WEB_SERVICES_SUMMARY.BLOCKED_BY_WBRS counter.
                Either number or string like '([], [expected_count])'.
                The value is not checked if the parameter was skipped.
            - `web_malware_url_count`:
                Expectation for WEB_SERVICES_SUMMARY.DETECTED_MALWARE_TOTAL counter.
                Either number or string like '([], [expected_count])'.
                The value is not checked if the parameter was skipped.
            - `web_total_count`:
                Expectation for WEB_SERVICES_SUMMARY.TRANSACTION_TOTAL counter.
                Either number or string like '([], [expected_count])'.
                The value is not checked if the parameter was skipped.
            - `period`: Rollup period. Either 'hour', 'day' or 'month'.
                    'month' is selected by default.
            - `range`: Time range in format 'YYYY MM DD, YYYY MM DD'.
                From yesterday to tomorrow by default.
            - `as_period`: Period for aggregation.
                    Either 'hour', 'day' or 'month'. 'month' by default.
            - `period_num`: Number of aggregated period to use.

        Exceptions:
            - `QueryCLICheckError`: appears if obtained value is not equal to expected value.

        Examples:
        | Verify Reporting Counters |
        | ... | mail_clean_count=NoData |
        | ... | mail_spam_count=NoData |
        | ... | mail_virus_type=EICAR-AV-Test |
        | ... | mail_virus_count=3 |
        | ... | mail_dlp_count=${EMPTY} |
        | ... | mail_marketing_count=NoData |
        | ... | mail_total_count=4 |
        | ... | web_clean_url_count=${EMPTY} |
        | ... | web_blocked_wbrs_url_count=${EMPTY} |
        | ... | web_malware_url_count=${EMPTY} |
        | ... | web_total_count=${EMPTY} |
        """

        ERROR_MESSAGE = ''

        if range is None:
            start_date = datetime.date.today() - datetime.timedelta(1)
            end_date = start_date + datetime.timedelta(2)
            range = '%s,%s' % (start_date.strftime('%Y %m %d'),
                               end_date.strftime('%Y %m %d'))
        if period is None:
            period = 'month'
        if as_period is None:
            as_period = 'month'
        if period_num is None:
            period_num = '1'

        query_cli_data = ()
        if mail_clean_count is not None:
            query_cli_data += self.make_query_cli_data( \
                'MAIL_INCOMING_TRAFFIC_SUMMARY.TOTAL_CLEAN_RECIPIENTS',
                period, range, as_period, period_num,
                mail_clean_count)
        if mail_spam_count is not None:
            query_cli_data += self.make_query_cli_data( \
                'MAIL_INCOMING_TRAFFIC_SUMMARY.DETECTED_SPAM',
                period, range, as_period, period_num,
                mail_spam_count)
        if mail_virus_count is not None:
            if mail_virus_type is None:
                if isinstance(mail_virus_count, dict):
                    _mail_virus_count = ''
                    for _virus_type, _virus_count in mail_virus_count.iteritems():
                        _mail_virus_count += "(['" + _virus_type + "'], [" + \
                                             str(_virus_count) + "])\r\n"
                    if len(_mail_virus_count) > 0:
                        _mail_virus_count = _mail_virus_count[:-2]
                    self._debug("\"" + _mail_virus_count + "\"")
                else:
                    _mail_virus_count = mail_virus_count
            else:
                _mail_virus_count = "(['" + mail_virus_type.strip() + "'], [" + \
                                    str(mail_virus_count) + "])"
            query_cli_data += self.make_query_cli_data( \
                'MAIL_VIRUS_TYPE_DETAIL.TOTAL_RECIPIENTS',
                period, range, as_period, period_num,
                _mail_virus_count)
        if mail_dlp_count is not None:
            query_cli_data += self.make_query_cli_data( \
                'MAIL_DLP_OUTGOING_TRAFFIC_SUMMARY.TOTAL_DLP_INCIDENTS',
                period, range, as_period, period_num,
                mail_dlp_count)
        if mail_marketing_count is not None:
            query_cli_data += self.make_query_cli_data( \
                'MAIL_INCOMING_TRAFFIC_SUMMARY.MARKETING_MAIL',
                period, range, as_period, period_num,
                mail_marketing_count)
        if mail_total_count is not None:
            query_cli_data += self.make_query_cli_data( \
                'MAIL_INCOMING_TRAFFIC_SUMMARY.TOTAL_RECIPIENTS',
                period, range, as_period, period_num,
                mail_total_count)
        if web_malware_count is not None:
            query_cli_data += self.make_query_cli_data( \
                'WEB_SERVICES_SUMMARY.DETECTED_MALWARE_TOTAL',
                period, range, as_period, period_num,
                web_malware_count)
        if web_clean_count is not None:
            query_cli_data += self.make_query_cli_data( \
                'WEB_SERVICES_SUMMARY.ALLOWED_TRANSACTION_TOTAL',
                period, range, as_period, period_num,
                web_clean_count)
        if web_blocked_wbrs_count is not None:
            query_cli_data += self.make_query_cli_data( \
                'WEB_SERVICES_SUMMARY.BLOCKED_BY_WBRS',
                period, range, as_period, period_num,
                web_blocked_wbrs_count)
        if web_total_count is not None:
            query_cli_data += self.make_query_cli_data( \
                'WEB_SERVICES_SUMMARY.TRANSACTION_TOTAL',
                period, range, as_period, period_num,
                web_total_count)

        query_cli = self._shell.query_cli
        verify_func = self.verify_results_object
        query_cli_func = query_cli.interval_time_range_query
        result = True

        for data in query_cli_data:
            query_cli_args = data['query_cli_args']
            query_cli_kwargs = data['query_cli_kwargs']
            expected_results = data['query_cli_results']
            query_res = query_cli_func(*query_cli_args, **query_cli_kwargs)
            # Do we have a match?
            self._debug(("query_res:", query_res))
            self._debug(("expected_results:", expected_results))
            result, desc, cmd_out_obj = verify_func(query_res, expected_results)
            self._debug(("(cmd_out_obj, desc, expected_results):",
                         (cmd_out_obj, desc, expected_results)))
            if result:
                self._info('%s:\r\n   %s' % (query_cli_args, query_res))
                continue
            ERROR_MESSAGE += ('\r\n%s:\r\n   %s %s %s' % \
                              (query_cli_args, cmd_out_obj, desc, expected_results))
            result = False
        if ERROR_MESSAGE != '':
            raise QueryCLICheckError(ERROR_MESSAGE)
        return result

    def _get_counter(self, counter_name, period,
                     range, as_period, period_num):

        query_result = []

        if range is None:
            start_date = datetime.date.today() - datetime.timedelta(1)
            end_date = start_date + datetime.timedelta(2)
            range = '%s,%s' % (start_date.strftime('%Y %m %d'),
                               end_date.strftime('%Y %m %d'))

        query_cli_data = self.make_query_cli_data( \
            counter_name,
            period, range, as_period, period_num)

        query_cli = self._shell.query_cli
        query_cli_func = query_cli.interval_time_range_query

        query_cli_args = (query_cli_data[0])['query_cli_args']
        query_cli_kwargs = (query_cli_data[0])['query_cli_kwargs']
        return query_cli_func(*query_cli_args, **query_cli_kwargs)

    def get_mail_incomming_clean_recepients_count(self, period='month',
                                                  range=None, as_period='month', period_num='1'):
        """Gets value for 'MAIL_INCOMING_TRAFFIC_SUMMARY.TOTAL_CLEAN_RECIPIENTS' by query_cli tool.

        Parameters:
            - `period`: Rollup period. Either 'hour', 'day' or 'month'.
                    'month' is selected by default.
            - `range`: Time range in format 'YYYY MM DD, YYYY MM DD'.
                From yesterday to tomorrow by default.
            - `as_period`: Period for aggregation.
                    Either 'hour', 'day' or 'month'. 'month' by default.
            - `period_num`: Number of aggregated period to use.

        Return:
            Value returned by `query_cli` tool for the counter.

        Examples:
            | ${query_result}= | Get Mail Incomming Clean Recepients Count |
            | Log | ${query_result} |
        """

        query_res = self._get_counter( \
            'MAIL_INCOMING_TRAFFIC_SUMMARY.TOTAL_CLEAN_RECIPIENTS',
            period, range, as_period, period_num)
        if len(query_res) > 0:
            query_count = (eval(query_res)[1])[0]
            if query_count != "NoData":
                return int(query_count)
            else:
                return 0
        else:
            return 0

    def get_mail_incomming_spam_count(self, period='month',
                                      range=None, as_period='month', period_num='1'):
        """Gets value for 'MAIL_INCOMING_TRAFFIC_SUMMARY.DETECTED_SPAM' by query_cli tool.

        Parameters:
            - `period`: Rollup period. Either 'hour', 'day' or 'month'.
                    'month' is selected by default.
            - `range`: Time range in format 'YYYY MM DD, YYYY MM DD'.
                From yesterday to tomorrow by default.
            - `as_period`: Period for aggregation.
                    Either 'hour', 'day' or 'month'. 'month' by default.
            - `period_num`: Number of aggregated period to use.

        Return:
            Value returned by `query_cli` tool for the counter.

        Examples:
            | ${query_result}= | Get Mail Incomming Spam Count |
            | Log | ${query_result} |
        """

        query_res = self._get_counter( \
            'MAIL_INCOMING_TRAFFIC_SUMMARY.DETECTED_SPAM',
            period, range, as_period, period_num)
        self._debug(query_res)
        if len(query_res) > 0:
            query_count = (eval(query_res)[1])[0]
            self._debug(query_count)
            if query_count != "NoData":
                return int(query_count)
            else:
                return 0
        else:
            return 0

    def get_mail_virus_type_count(self, virus_type=None, period='month',
                                  range=None, as_period='month', period_num='1'):
        """Gets value for 'MAIL_VIRUS_TYPE_DETAIL.TOTAL_RECIPIENTS' by query_cli tool.

        Parameters:
            - `virus_type`: Type of interesting viurus. If it is None,
              dictionary of counts for virus types will be returned.
            - `period`: Rollup period. Either 'hour', 'day' or 'month'.
                    'month' is selected by default.
            - `range`: Time range in format 'YYYY MM DD, YYYY MM DD'.
                From yesterday to tomorrow by default.
            - `as_period`: Period for aggregation.
                    Either 'hour', 'day' or 'month'. 'month' by default.
            - `period_num`: Number of aggregated period to use.

        Return:
            Count of specified virus type, or dictionary with counts for virus types, returned by `query_cli` tool.

        Examples:
            | ${query_result}= | Get Mail Virus Type Count | virus_type=EICAR-AV-Test |
            | Log | ${query_result} |
        """

        query_res = self._get_counter( \
            'MAIL_VIRUS_TYPE_DETAIL.TOTAL_RECIPIENTS',
            period, range, as_period, period_num)
        if len(query_res) > 0:
            virus_dict = {}
            for line in query_res.splitlines():
                _virus_type_count = eval(line)
                virus_dict[_virus_type_count[0][0]] = _virus_type_count[1][0]
            if virus_type is None:
                return virus_dict
            else:
                if virus_type in virus_dict:
                    return virus_dict[virus_type]
                else:
                    return 0
        else:
            if virus_type is None:
                return query_res
            else:
                return 0

    def get_mail_dlp_count(self, period='month',
                           range=None, as_period='month', period_num='1'):
        """Gets value for 'MAIL_DLP_OUTGOING_TRAFFIC_SUMMARY.TOTAL_DLP_INCIDENTS' by query_cli tool.

        Parameters:
            - `period`: Rollup period. Either 'hour', 'day' or 'month'.
                    'month' is selected by default.
            - `range`: Time range in format 'YYYY MM DD, YYYY MM DD'.
                From yesterday to tomorrow by default.
            - `as_period`: Period for aggregation.
                    Either 'hour', 'day' or 'month'. 'month' by default.
            - `period_num`: Number of aggregated period to use.

        Return:
            Value returned by `query_cli` tool for the counter.

        Examples:
            | ${query_result}= | Get Mail DLP Count |
            | Log | ${query_result} |
        """

        query_res = self._get_counter( \
            'MAIL_DLP_OUTGOING_TRAFFIC_SUMMARY.TOTAL_DLP_INCIDENTS',
            period, range, as_period, period_num)
        if len(query_res) > 0:
            query_count = (eval(query_res)[1])[0]
            if query_count != "NoData":
                return int(query_count)
            else:
                return 0
        else:
            return 0

    def get_mail_marketing_count(self, period='month',
                                 range=None, as_period='month', period_num='1'):
        """Gets value for 'MAIL_INCOMING_TRAFFIC_SUMMARY.MARKETING_MAIL' by query_cli tool.

        Parameters:
            - `period`: Rollup period. Either 'hour', 'day' or 'month'.
                    'month' is selected by default.
            - `range`: Time range in format 'YYYY MM DD, YYYY MM DD'.
                From yesterday to tomorrow by default.
            - `as_period`: Period for aggregation.
                    Either 'hour', 'day' or 'month'. 'month' by default.
            - `period_num`: Number of aggregated period to use.

        Return:
            Value returned by `query_cli` tool for the counter.

        Examples:
            | ${query_result}= | Get Mail Marketing Count |
            | Log | ${query_result} |
        """

        query_res = self._get_counter( \
            'MAIL_INCOMING_TRAFFIC_SUMMARY.MARKETING_MAIL',
            period, range, as_period, period_num)
        if len(query_res) > 0:
            query_count = (eval(query_res)[1])[0]
            if query_count != "NoData":
                return int(query_count)
            else:
                return 0
        else:
            return 0

    def get_mail_incoming_total_count(self, period='month',
                                      range=None, as_period='month', period_num='1'):
        """Gets value for 'MAIL_INCOMING_TRAFFIC_SUMMARY.TOTAL_RECIPIENTS' by query_cli tool.

        Parameters:
            - `period`: Rollup period. Either 'hour', 'day' or 'month'.
                    'month' is selected by default.
            - `range`: Time range in format 'YYYY MM DD, YYYY MM DD'.
                From yesterday to tomorrow by default.
            - `as_period`: Period for aggregation.
                    Either 'hour', 'day' or 'month'. 'month' by default.
            - `period_num`: Number of aggregated period to use.

        Return:
            Value returned by `query_cli` tool for the counter.

        Examples:
            | ${query_result}= | Get Mail Incoming Total Count |
            | Log | ${query_result} |
        """

        query_res = self._get_counter( \
            'MAIL_INCOMING_TRAFFIC_SUMMARY.TOTAL_RECIPIENTS',
            period, range, as_period, period_num)
        if len(query_res) > 0:
            query_count = (eval(query_res)[1])[0]
            if query_count != "NoData":
                return int(query_count)
            else:
                return 0
        else:
            return 0

    def get_web_malware_count(self, period='month',
                              range=None, as_period='month', period_num='1'):
        """Gets value for 'WEB_SERVICES_SUMMARY.DETECTED_MALWARE_TOTAL' by query_cli tool.

        Parameters:
            - `period`: Rollup period. Either 'hour', 'day' or 'month'.
                    'month' is selected by default.
            - `range`: Time range in format 'YYYY MM DD, YYYY MM DD'.
                From yesterday to tomorrow by default.
            - `as_period`: Period for aggregation.
                    Either 'hour', 'day' or 'month'. 'month' by default.
            - `period_num`: Number of aggregated period to use.

        Return:
            Value returned by `query_cli` tool for the counter.

        Examples:
            | ${query_result}= | Get Web Malware Count |
            | Log | ${query_result} |
        """

        query_res = self._get_counter( \
            'WEB_SERVICES_SUMMARY.DETECTED_MALWARE_TOTAL',
            period, range, as_period, period_num)
        if len(query_res) > 0:
            query_count = (eval(query_res)[1])[0]
            if query_count != "NoData":
                return int(query_count)
            else:
                return 0
        else:
            return 0

    def get_web_allowed_count(self, period='month',
                              range=None, as_period='month', period_num='1'):
        """Gets value for 'WEB_SERVICES_SUMMARY.ALLOWED_TRANSACTION_TOTAL' by query_cli tool.

        Parameters:
            - `period`: Rollup period. Either 'hour', 'day' or 'month'.
                    'month' is selected by default.
            - `range`: Time range in format 'YYYY MM DD, YYYY MM DD'.
                From yesterday to tomorrow by default.
            - `as_period`: Period for aggregation.
                    Either 'hour', 'day' or 'month'. 'month' by default.
            - `period_num`: Number of aggregated period to use.

        Return:
            Value returned by `query_cli` tool for the counter.

        Examples:
            | ${query_result}= | Get Web Allowed Count |
            | Log | ${query_result} |
        """

        query_res = self._get_counter( \
            'WEB_SERVICES_SUMMARY.ALLOWED_TRANSACTION_TOTAL',
            period, range, as_period, period_num)
        if len(query_res) > 0:
            query_count = (eval(query_res)[1])[0]
            if query_count != "NoData":
                return int(query_count)
            else:
                return 0
        else:
            return 0

    def get_web_blocked_count(self, period='month',
                              range=None, as_period='month', period_num='1'):
        """Gets value for 'WEB_SERVICES_SUMMARY.BLOCKED_BY_WBRS' by query_cli tool.

        Parameters:
            - `period`: Rollup period. Either 'hour', 'day' or 'month'.
                    'month' is selected by default.
            - `range`: Time range in format 'YYYY MM DD, YYYY MM DD'.
                From yesterday to tomorrow by default.
            - `as_period`: Period for aggregation.
                    Either 'hour', 'day' or 'month'. 'month' by default.
            - `period_num`: Number of aggregated period to use.

        Return:
            Value returned by `query_cli` tool for the counter.

        Examples:
            | ${query_result}= | Get Web Blocked Count |
            | Log | ${query_result} |
        """

        query_res = self._get_counter( \
            'WEB_SERVICES_SUMMARY.BLOCKED_BY_WBRS',
            period, range, as_period, period_num)
        if len(query_res) > 0:
            query_count = (eval(query_res)[1])[0]
            if query_count != "NoData":
                return int(query_count)
            else:
                return 0
        else:
            return 0

    def get_web_total_count(self, period='month',
                            range=None, as_period='month', period_num='1'):
        """Gets value for 'WEB_SERVICES_SUMMARY.TRANSACTION_TOTAL' by query_cli tool.

        Parameters:
            - `period`: Rollup period. Either 'hour', 'day' or 'month'.
                    'month' is selected by default.
            - `range`: Time range in format 'YYYY MM DD, YYYY MM DD'.
                From yesterday to tomorrow by default.
            - `as_period`: Period for aggregation.
                    Either 'hour', 'day' or 'month'. 'month' by default.
            - `period_num`: Number of aggregated period to use.

        Return:
            Value returned by `query_cli` tool for the counter.

        Examples:
            | ${query_result}= | Get Web Blocked Count |
            | Log | ${query_result} |
        """

        query_res = self._get_counter( \
            'WEB_SERVICES_SUMMARY.TRANSACTION_TOTAL',
            period, range, as_period, period_num)
        if len(query_res) > 0:
            query_count = (eval(query_res)[1])[0]
            if query_count != "NoData":
                return int(query_count)
            else:
                return 0
        else:
            return 0

    def get_reporting_counters(self, period='month',
                               range=None, as_period='month', period_num='1'):
        """Gets value for all reporting counters
            ('MAIL_INCOMING_TRAFFIC_SUMMARY.TOTAL_CLEAN_RECIPIENTS',
            'MAIL_INCOMING_TRAFFIC_SUMMARY.DETECTED_SPAM',
            'MAIL_VIRUS_TYPE_DETAIL.TOTAL_RECIPIENTS',
            'MAIL_DLP_OUTGOING_TRAFFIC_SUMMARY.TOTAL_DLP_INCIDENTS',
            'MAIL_INCOMING_TRAFFIC_SUMMARY.MARKETING_MAIL',
            'MAIL_INCOMING_TRAFFIC_SUMMARY.TOTAL_RECIPIENTS',
            'WEB_SERVICES_SUMMARY.DETECTED_MALWARE_TOTAL',
            'WEB_SERVICES_SUMMARY.ALLOWED_TRANSACTION_TOTAL',
            'WEB_SERVICES_SUMMARY.BLOCKED_BY_WBRS',
            'WEB_SERVICES_SUMMARY.TRANSACTION_TOTAL',
        by query_cli tool.

        Parameters:
            - `period`: Rollup period. Either 'hour', 'day' or 'month'.
                    'month' is selected by default.
            - `range`: Time range in format 'YYYY MM DD, YYYY MM DD'.
                From yesterday to tomorrow by default.
            - `as_period`: Period for aggregation.
                    Either 'hour', 'day' or 'month'. 'month' by default.
            - `period_num`: Number of aggregated period to use.

        Return:
            Value returned by `query_cli` tool.

        Examples:
            | ${query_result}= | Get Web Blocked Count |
            | Log | ${query_result} |
        """
        query_result = []

        if range is None:
            start_date = datetime.date.today() - datetime.timedelta(1)
            end_date = start_date + datetime.timedelta(2)
            range = '%s,%s' % (start_date.strftime('%Y %m %d'),
                               end_date.strftime('%Y %m %d'))

        query_cli_data = ()
        query_cli_data += self.make_query_cli_data( \
            'MAIL_INCOMING_TRAFFIC_SUMMARY.TOTAL_CLEAN_RECIPIENTS',
            period, range, as_period, period_num)
        query_cli_data += self.make_query_cli_data( \
            'MAIL_INCOMING_TRAFFIC_SUMMARY.DETECTED_SPAM',
            period, range, as_period, period_num)
        query_cli_data += self.make_query_cli_data( \
            'MAIL_VIRUS_TYPE_DETAIL.TOTAL_RECIPIENTS',
            period, range, as_period, period_num)
        query_cli_data += self.make_query_cli_data( \
            'MAIL_DLP_OUTGOING_TRAFFIC_SUMMARY.TOTAL_DLP_INCIDENTS',
            period, range, as_period, period_num)
        query_cli_data += self.make_query_cli_data( \
            'MAIL_INCOMING_TRAFFIC_SUMMARY.MARKETING_MAIL',
            period, range, as_period, period_num)
        query_cli_data += self.make_query_cli_data( \
            'MAIL_INCOMING_TRAFFIC_SUMMARY.TOTAL_RECIPIENTS',
            period, range, as_period, period_num)
        query_cli_data += self.make_query_cli_data( \
            'WEB_SERVICES_SUMMARY.DETECTED_MALWARE_TOTAL',
            period, range, as_period, period_num)
        query_cli_data += self.make_query_cli_data( \
            'WEB_SERVICES_SUMMARY.ALLOWED_TRANSACTION_TOTAL',
            period, range, as_period, period_num)
        query_cli_data += self.make_query_cli_data( \
            'WEB_SERVICES_SUMMARY.BLOCKED_BY_WBRS',
            period, range, as_period, period_num)
        query_cli_data += self.make_query_cli_data( \
            'WEB_SERVICES_SUMMARY.TRANSACTION_TOTAL',
            period, range, as_period, period_num)

        query_cli = self._shell.query_cli
        query_cli_func = query_cli.interval_time_range_query

        for _data in query_cli_data:
            query_cli_args = _data['query_cli_args']
            query_cli_kwargs = _data['query_cli_kwargs']
            query_res = query_cli_func(*query_cli_args, **query_cli_kwargs)
            query_result.append([query_cli_args, query_res])
        return query_result
