# $Id: //prod/main/sarf_centos/testlib/common/util/filter.py#1 $
# $DateTime: 2019/03/22 01:36:06 $
# $Author: aminath $

import re
import time

from common.util.utilcommon import UtilCommon
from common.util.misc import Misc


class Filter(UtilCommon):
    """
    Keywords for filtering data
    """
    _errors = ''

    errors_while_filtering = \
        [
            'grep:',
            'Syntax error:',
        ]

    def get_keyword_names(self):
        return [
            'filter_log_create_baseline',
            'filter_log',
            'filter_data',
            'filter_data_compare',
        ]

    def filter_log_create_baseline(self, location):
        """Returns baseline:
        - number of lines in the file, if the file exists
        - 0 if file does not exist.

        The returned value is used to filter data in a file
        from the baseline mark.

        Parameters:

        - `location`: location of a file on the appliance.

        Example:
        | Create a baseline |
        |  ${baseline}= | Filter Log Create Baseline | /data/pub/track_stats/prox_track.log |
        """

        baseline = None
        # In Linux builds, there is no white space before the integer indicating the count. Hence changing the pattern to match both(linux and FreeBSD builds)
        PATTERN = ' *(\d+) +'
        cmd = "wc -l " + str(location)

        resp = Misc(self.dut, self.dut_version).run_on_dut(cmd)
        self._debug("resp = " + resp)
        m = re.match(PATTERN, resp)
        if m:
            baseline = int(m.group(1))

        return baseline

    def filter_log(self,
                   location,

                   # baseline is applicable only to a single file
                   baseline=0,

                   filter_by_log_level=None,

                   skip_patterns=None,
                   match_patterns=None,

                   skip_by_fields=None,
                   match_by_fields=None,
                   field_value_regex=None,

                   limit_return=None,

                   # timeout parameters
                   timeout=None,
                   timeout_interval=1,
                   number_of_matches=1,
                   ):
        """
        Filters the specified log file and returns the results of filtering.

        Parameters:

        - `location`: path to a file on the appliance.

        - `baseline`: that's an alternative to usage of rollover functionality.
           If set, number of first lines that should be skipped
           prior to filtering. The value can be set using keyword
           filter_log_create_baseline

        - `filter_by_log_level`: if set, only lines with the specified or
           higher log_level are filtered
           All other lines including lines with unidentified log level
           are ignored.
           Acceptable values from highest to lowest are:
           - . 'error'
           - . 'warning'
           - . 'info'
           - . 'debug'
           - . 'trace'

        - `skip_patterns`: if set, a string of comma-separated patterns to
           skip or a RF's list of patterns.
           All records that match at list one of the patterns are skipped.
           Each pattern is a grep expression optionally prefixed with grep
           options.
           * Example: skip_patterns=connection closed,
                                    -i -E 'bogus error number [34]\d+'

        - `match_patterns`: if set, a string of comma-separated patterns to
           match or a RF's list of patterns. Only records that match all
           patterns are filtered. Each pattern is a grep expression optionally
           prefixed with grep options.
           * Example: match_patterns=-E '(Login|Logout)'

        - `skip_by_fields`: a list of pairs <field>:<value>
           where
           - . <field> is a constant from a corresponding constants file that
               describe locations in the field in a log file
           - . <value> is a value of the corresponding field
           All records that match at list one of that condition will be
           skipped.
           * Example: skip_by_fields=${proxy_log.MODULE}:PROXY,
            ${proxy_log.TRANSACTION}:-

        - `match_by_fields`: a list of pairs <field>:<value>
           where
           - . <field> is a constant from a corresponding constants file that
               describe locations in the field in a log file
           - . <value> is a value of the corresponding field
           Only records that match all conditions are filtered
           * Example: match_by_fields=${proxy_log.MESSAGE}:failed:

        - `field_value_regex`: whether or not construe <value> in pairs
           <field>:<value> in parameters skip_by_fields and match_by_fields
           as regular expressions. Acceptable values: 'yes' and 'no'.

        - `limit_return`: if set, only first filtered lines are returned.
           Acceptable value - non-negative integer

        The following 3 parameters are used to specify waiting
        until either matching condition is met or timeout is expired

        - `timeout`: if set, max time in seconds to check whether the filtering
           conditions are met.

        - `timeout_interval`: if `timeout` is set, interval in seconds between
           consequent verifications of whether the filtering conditions are met

        - `wait_for_number_of_matches`: if `timeout` is set, number of lines
           that should match the filtering conditions

        Return:
        - filtered lines
        - number of filtered lines

        Examples:

        | Filter log from baseline |
        | |  ${baseline}= | Filter Log Create Baseline |  /data/pub/track_stats/prox_track.log |
        | |  ${filtered_lines} | ${filtered_count}= | Filter Log |
        | |  ... | /data/pub/track_stats/prox_track.log |
        | |  ... | baseline=1 |
        | | ${filtered_lines} | ${filtered_count}= | Filter Log |
        | |  ... | /data/pub/track_stats/prox_track.log |
        | |  ... | limit_return=10 |
        | |  ${base2}= | Evaluate | ${baseline}-5 |
        | |  ${filtered_lines} | ${filtered_count}= | Filter Log |
        | |  ... | /data/pub/track_stats/prox_track.log |
        | |  ... | baseline=${base2} |
        | |  ... | limit_return=10 |
        | Filter by log level |
        | |  ${filtered_lines} | ${filtered_count}= | Filter Log |
        | |  ... | /data/pub/track_stats/prox_track.log |
        | |  ... | filter_by_log_level=info |
        | |  ... | limit_return=10 |
        | |  ${filtered_lines} | ${filtered_count}= | Filter Log |
        | |  ... | /data/pub/track_stats/prox_track.log |
        | |  ... | filter_by_log_level=error |
        | Filter by skip_patterns |
        | |  ${filtered_lines} | ${filtered_count}= | Filter Log |
        | |  ... | /data/pub/track_stats/prox_track.log |
        | |  ... | filter_by_log_level=info |
        | |  ... | skip_patterns='waiting combined' |
        | |  ... | limit_return=10 |
        | |  ${filtered_lines} | ${filtered_count}= | Filter Log |
        | |  ... | /data/pub/track_stats/prox_track.log |
        | |  ... | filter_by_log_level=info |
        | |  ... | skip_patterns=-i waiting,-E -i Combined |
        | Filter using limit_return |
        | |  ${filtered_lines} | ${filtered_count}= | Filter Log |
        | |  ... | /data/pub/track_stats/prox_track.log |
        | |  ... | filter_by_log_level=info |
        | |  ${filtered_lines} | ${filtered_count}= | Filter Log |
        | |  ... | /data/pub/track_stats/prox_track.log |
        | |  ... | filter_by_log_level=info |
        | |  ${filtered_lines} | ${filtered_count}= | Filter Log |
        | |  ... | /data/pub/track_stats/prox_track.log |
        | |  ... | filter_by_log_level=info |
        | |  ... | limit_return=50 |
        | |  ${filtered_lines} | ${filtered_count}= | Filter Log |
        | |  ... | /data/pub/track_stats/prox_track.log |
        | |  ... | filter_by_log_level=info |
        | |  ... | limit_return=1 |
        | Filter by match_patterns |
        | |  ${filtered_lines} | ${filtered_count}= | Filter Log |
        | |  ... | /data/pub/track_stats/prox_track.log |
        | |  ... | filter_by_log_level=info |
        | |  ... | match_patterns='waiting combined' |
        | |  ${filtered_lines} | ${filtered_count}= | Filter Log |
        | |  ... | /data/pub/track_stats/prox_track.log |
        | |  ... | filter_by_log_level=info |
        | |  ... | match_patterns=-i waiting,-E -i Combined |
        | Filter by fields. Fields are described in a constants file below |
            | | @{select_fields}= | Set Variable | ${track_stats.SM_HIT_INACT}:0 | ${track_stats.UNUSED}:66914 |
        | |  ${filtered_lines} | ${filtered_count}= | Filter Log |
        | |  ... | /data/pub/track_stats/prox_track.log |
        | |  ... | filter_by_log_level=info |
        | |  ... | match_by_fields=${select_fields} |
        | |  ... | limit_return=5 |
        | |  Log | ${filtered_lines} |
        | Waiting up to 5 minutes until new 20 records are logged  |
        | |  ${baseline}= | Filter Log Create Baseline   /data/pub/track_stats/prox_track.log |
        | |  ${filtered_lines} | ${filtered_count}= | Filter Log |
        | |  ... | /data/pub/track_stats/prox_track.log |
        | |  ... | baseline=${baseline} |
        | |  ... | timeout=300 |
        | |  ... | number_of_matches=20 |
        | |  ... | timeout_interval=5 |

        """
        return self._filter(
            location=location,
            recurse=None,
            prefix_with_names=None,
            prefix_with_numbers=None,
            baseline=baseline,
            filter_by_log_level=filter_by_log_level,
            skip_patterns=skip_patterns,
            match_patterns=match_patterns,
            skip_by_fields=skip_by_fields,
            match_by_fields=match_by_fields,
            field_value_regex=field_value_regex,

            limit_return=limit_return,
            timeout=timeout,
            timeout_interval=timeout_interval,
            number_of_matches=number_of_matches,
        )

    def filter_data(self,
                    location,

                    # The following 3 parameters are not applicable for a single log file
                    recurse='yes',
                    prefix_with_names='yes',
                    prefix_with_numbers='yes',

                    filter_by_log_level=None,

                    # skip parameters
                    skip_patterns=None,
                    match_patterns=None,

                    limit_return=5,
                    # timeout parameters
                    timeout=None,
                    timeout_interval=1,
                    number_of_matches=1,

                    dut=None,
                    dut_version=None
                    ):

        """
        Filters the specified data and returns the results of filtering.

        Parameters:

        - `location`: string of comma-separated locations of data to filter.
           That's the only required parameter. Acceptable values:
           - . Path to a file on the appliance.
           - . Path to a directory on the appliance.

        - `recurse`: recursive inclusion of all sub-folders of each directory.
           Acceptable values: 'yes' and 'no'.

        - `prefix_with_names`: prefix each match with file name.
           Acceptable values: 'yes' and 'no'.

        - `prefix_with_numbers`: prefix each match with line number within its
           file. Acceptable values: 'yes' and 'no'.

        - `filter_by_log_level`: if set, only lines with the specified or
           higher log_level are considered for filtering.
           All other lines including lines with unidentified log level
           are ignored.
           Acceptable values from highest to lowest are:
           - . 'error'
           - . 'warning'
           - . 'info'
           - . 'debug'
           - . 'trace'

        - `skip_patterns`: if set, a string of comma-separated patterns to
           skip or a RF's list of patterns.
           All records that match at list one of the patterns are skipped.
           Each pattern is a grep expression optionally prefixed with grep
           options.
           * Example: skip_patterns=connection closed,
             -i -E 'bogus error number [34]\d+'

        - `match_patterns`: if set, a string of comma-separated patterns to
           match or a RF's list of patterns. Only records that match all
           patterns are filtered. Each pattern is a grep expression optionally
           prefixed with grep options.
           * Example: match_patterns=-E '(Login|Logout)'

        - `limit_return`: if set, only first filtered lines are returned.
           Acceptable value - non-negative integer

        The following 3 parameters are used to specify waiting
        until either matching condition is met or timeout is expired

        - `timeout`: if set, max time in seconds to check whether the filtering
           conditions are met.

        - `timeout_interval`: if `timeout` is set, interval in seconds between
           consequent verifications of whether the filtering conditions are met

        - `wait_for_number_of_matches`: if `timeout` is set, number of lines
           that should match the filtering conditions

        Examples:

        |  Filter Data |
        |  | ${filtered_lines} | ${filtered_count}= | Filter Data |
        |  | ... | /data/pub/, /data/log |
        |  | ... | filter_by_log_level=warning |
        |  | ... | limit_return=20 |
        |  | Log |  ${filtered_count} |
        |  | ${filtered_lines} | ${filtered_count}= | Filter Data |
        |  | ... | /data/log |
        |  | ... | filter_by_log_level=warning |
        |  | ... | limit_return=20 |
        |  | Log |  ${filtered_count} |
        |  | ${filtered_lines} | ${filtered_count}= | Filter Data |
        |  | ... | /data/pub/ |
        |  | ... | filter_by_log_level=warning |
        |  | ... | limit_return=20 |
        |  | Log |  ${filtered_count} |
        |  | ${filtered_lines} | ${filtered_count}= | Filter Data |
        |  | ... | /data/pub/ |
        |  | ... | filter_by_log_level=debug |
        |  | ... | limit_return=20 |
        |  | Log |  ${filtered_count} |
        """

        return self._filter(
            location=self._convert_to_list(location),
            recurse=recurse,
            prefix_with_names=prefix_with_names,
            prefix_with_numbers=prefix_with_numbers,
            baseline=None,
            filter_by_log_level=filter_by_log_level,
            skip_patterns=skip_patterns,
            match_patterns=match_patterns,
            skip_by_fields=None,
            match_by_fields=None,
            limit_return=limit_return,
            timeout=timeout,
            timeout_interval=timeout_interval,
            number_of_matches=number_of_matches,
            dut=dut,
            dut_version=dut_version,
        )

    def filter_data_compare(self,
                            new_set,
                            old_set):
        """
        Compare 2 sets of data to find new entries
        It is assumed that:
        - both sets of data are produced with filter_data
        - prefix_with_names was set to 'yes'
        - prefix_with_numbers was set to 'yes'

        Parameters:
        - `new_set` filtered lines from last execution of Filter Data
        - `old_set` filtered lines from previous execution of Filter Data

        Algorithm:
        Find and return lines from new_set that are missing in old_set
        and their number

        Examples:

        |  Find only Warnings |
        |  | ${filtered_warn} | ${filtered_count}= | Filter Data |
        |  | ... | /data/pub/, /data/log |
        |  | ... | filter_by_log_level=warning |
        |  | ... | limit_return=${None} |

        |  | ${filtered_err} | ${filtered_count}= | Filter Data |
        |  | ... | /data/pub/, /data/log |
        |  | ... | filter_by_log_level=error |
        |  | ... | limit_return=${None} |

        |  | ${new_entries} | ${new_entries_count}= | Filter Data Compare |
        |  | ... | ${filtered_warn} |
        |  | ... | ${filtered_err} |
        """
        dic = {}
        array = new_set.splitlines()
        pattern = '(?P<location>^[^:]+:[\d]+:)(?P<message>.*)'
        for line in array:
            m = re.match(pattern, line)
            if m:
                if dic.has_key(m.group('message')):
                    dic[m.group('message')].append(m.group('location'))
                else:
                    dic[m.group('message')] = [m.group('location')]

        array = old_set.splitlines()
        for line in array:
            m = re.match(pattern, line)
            if m:
                if dic.has_key(m.group('message')):
                    if m.group('location') in dic[m.group('message')]:
                        dic[m.group('message')].remove(m.group('location'))

        lines = ""
        for key in dic.keys():
            if len(dic[key]) > 0:
                lines += ("\n\n" + key)
                for mem in dic[key]:
                    lines += ("\n\t" + str(mem))
            else:
                dic.__delitem__(key)
        lines += "\n"
        return lines, len(dic)

    def _filter(self,
                location=None,
                recurse=None,
                prefix_with_names=None,
                prefix_with_numbers=None,
                baseline=None,
                filter_by_log_level=None,
                skip_patterns=None,
                match_patterns=None,
                skip_by_fields=None,
                match_by_fields=None,
                field_value_regex=None,
                limit_return=None,
                timeout=None,
                timeout_interval=None,
                number_of_matches=None,
                dut=None,
                dut_version=None,
                ):

        """
        Validation and conversion of input data
        If at least one error is found the script exits after
        reporting all detected issues
        """
        log_levels = {
            'error': "-i -E '( |)Error: '",
            'warning': "-i -E '( |)(Error|Warning): '",
            'info': "-i -E '( |)(Error|Warning|Info): '",
            'debug': "-i -E '( |)(Error|Warning|Info|Debug): '",
            'trace': "-i -E '( |)(Error|Warning|Info|Debug|Trace): '"
        }

        log_levels_avoid_prefix = {
            'error': "-i -E '^[^:]+:.*( |)Error: '",
            'warning': "-i -E '^[^:]+:.*( |)(Error|Warning): '",
            'info': "-i -E '^[^:]+:.*( |)(Error|Warning|Info): '",
            'debug': "-i -E '^[^:]+:.*( |)(Error|Warning|Info|Debug): '",
            'trace': "-i -E '^[^:]+:.*( |)(Error|Warning|Info|Debug|Trace): '"
        }

        cmd = ''

        if location is None:
            self._errors += "location is not specified\n"

        if baseline is not None:
            try:
                baseline = int(baseline)
            except:
                self._errors += "Baseline '%s' should be an integer\n" \
                                % baseline
                baseline = 0

        if baseline is not None and baseline > 0:
            current_lenth = self.filter_log_create_baseline(location)
            if current_lenth is None or current_lenth < baseline:
                self._warn( \
                    "Current length of file is less than baseline\n" + \
                    "Setting baseline to 0")
                baseline = 0

        if baseline is not None and baseline > 0:
            cmd = ("tail -n +" + \
                   str(baseline + 1) + ' ' + str(location))
        else:
            cmd = "grep -a -E "
            if recurse is not None:
                if self._is_yes(recurse) is None:
                    self._errors += \
                        ("recurse '%s' should be 'yes' or 'no'\n" % recurse)
                elif self._is_yes(recurse):
                    cmd += '-r '
            if prefix_with_names is not None:
                if self._is_yes(prefix_with_names) is None:
                    self._errors += \
                        ("prefix_with_names '%s' should be 'yes' or 'no'\n" \
                         % prefix_with_names)
                elif self._is_yes(prefix_with_names):
                    cmd += '-H '
            if prefix_with_numbers is not None:
                if self._is_yes(prefix_with_numbers) is None:
                    self._errors += \
                        ("prefix_with_numbers '%s' should be 'yes' or 'no'\n" \
                         % prefix_with_numbers)
                elif self._is_yes(prefix_with_numbers):
                    cmd += '-n '
            if isinstance(location, list):
                cmd += ("'^' " + ' '.join(location))
            else:
                cmd += ("'^' " + str(location))

        self._debug('pre-filtering cmd = ' + cmd)

        if filter_by_log_level is not None:
            if not log_levels.has_key(filter_by_log_level):
                self._errors += "filter_by_log_level should be in " + \
                                str(log_levels.keys()) + "\n"
            else:
                # filtering by log levels
                if recurse is None:
                    cmd += (" | grep -a " + log_levels[filter_by_log_level])
                else:
                    cmd += (" | grep -a " + \
                            log_levels_avoid_prefix[filter_by_log_level])
                self._debug('filter by log level cmd = ' + cmd)

        if skip_patterns is not None:
            _patterns = self._convert_to_list(skip_patterns)
            for pattern in _patterns:
                cmd += (" | grep -a -v " + pattern)
                self._debug("skip pattern=%s cmd=%s" % (pattern, cmd))

        if match_patterns is not None:
            _patterns = self._convert_to_list(match_patterns)
            for pattern in _patterns:
                cmd += (" | grep -a " + pattern)
                self._debug("match pattern=%s cmd=%s" % (pattern, cmd))

        if skip_by_fields is not None:
            _fields = self._convert_fields(skip_by_fields)
            for field in _fields:
                cmd += (' | grep -a -v ' + \
                        self._get_field_pattern(field, field_value_regex))
                self._debug("skip field pattern=%s cmd=%s" % (field, cmd))

        if match_by_fields is not None:
            _fields = self._convert_fields(match_by_fields)
            for field in _fields:
                cmd += (' | grep -a ' + \
                        self._get_field_pattern(field, field_value_regex))
                self._debug("match field pattern=%s cmd=%s" % (field, cmd))

        if field_value_regex is not None:
            if self._is_yes(field_value_regex) is None:
                self._errors += \
                    ("field_value_regex '%s' should be 'yes' or 'no'\n" \
                     % field_value_regex)
        if limit_return is not None:
            try:
                limit_return = int(limit_return)
                if limit_return < 0:
                    self._errors += \
                        ("limit_return '%s' should be 0 or a positive integer\n" \
                         % limit_return)
            except:
                self._errors += \
                    ("limit_return '%s' should be 0 or a positive integer\n" \
                     % limit_return)

        if timeout is not None:
            try:
                timeout = int(timeout)
                if timeout < 1:
                    self._errors += \
                        ("timeout '%s' should be a positive integer\n" % timeout)
            except:
                self._errors += \
                    ("timeout '%s' should be a positive integer\n" % timeout)

            if timeout_interval is not None:
                try:
                    timeout_interval = int(timeout_interval)
                    if timeout_interval < 1:
                        self._errors += \
                            ("timeout_interval '%s' should be a positive"
                             " integer\n" % timeout_interval)
                except:
                    self._errors += \
                        ("timeout_interval '%s' should be a positive"
                         " integer\n" % timeout_interval)

            if number_of_matches is not None:
                try:
                    number_of_matches = int(number_of_matches)
                    if number_of_matches < 1:
                        self._errors += \
                            ("number_of_matches '%s' should be a positive"
                             " integer\n" % number_of_matches)
                except:
                    self._errors += \
                        ("number_of_matches '%s' should be a positive"
                         " integer\n" % number_of_matches)

        if self._errors != '':
            raise ValueError, self._errors

        if dut == None:
            dut = self.dut

        if dut_version == None:
            dut_version = self.dut_version

        start_time = time.time()

        # cycling until the condition is met or just once if timeout is None
        self._info("Search cmd=%s" % cmd)
        while True:
            start_search = time.time()
            count = Misc(dut, dut_version).run_on_dut(cmd + " | wc -l")
            self._check_resp(count)

            if timeout is None:
                self._info("Search time: %.2f seconds. Matches found: %s" % \
                           ((time.time() - start_search), count))
            else:
                self._info("Elapsed time: %d seconds. Matches found: %s" % \
                           ((time.time() - start_time), count))

            if timeout is None or \
                    time.time() > (start_time + timeout) or \
                    int(count) >= number_of_matches:
                break
            time.sleep(timeout_interval)

        start_search = time.time()
        cmd = cmd + " | grep -v '[^ -~]\+'"
        if limit_return is None:
            resp = Misc(dut, dut_version).run_on_dut(cmd)
        elif limit_return == 0:
            resp = ''
        else:
            resp = Misc(dut, dut_version).run_on_dut(cmd + \
                                                     " | grep -a -m %d '^'" % limit_return)
        self._info("Retrieved filtered lines for %.2f seconds." % \
                   ((time.time() - start_search)))
        return resp, count

    def _check_resp(self, resp):
        """
        Check whether response shows a problem
        If yes, raise an Exception
        """
        for mem in self.errors_while_filtering:
            if resp.startswith(mem):
                raise ValueError, "Error while filtering: '%s'" % mem

    def _get_field_pattern(self, field, field_value_regex):
        """Convert  field to a field pattern
        - `field` - should have format <grep-exp>:<value>
        - . grep-exp expression to filter file by the field.
            It should have a unique occurrence of ({VALUE}) that is replaced
            by <value>. All ':' in grep-exp should be presemted as {COLON}.
            That is necessary to distingish ":" as a separator between
            grep-exp and value.

        - . value is a value of the field. It is construed as a string, not
            as regular expression even when grep-exp has option -E

        Examples:
        " ({VALUE}) sm-hit-inact"
        "-E \'^({VALUE})'",
        "-E -i '^(?[^ ]* +){5}({VALUE}){COLON}'",
        "-E -i \'^(?[^{COLON}]*{COLON}){3} ({VALUE})'",
        "-E -i \'^(?[^{COLON}]*{COLON}){4} ({VALUE}) '",
        "-E -i \'^(?[^{COLON}]*{COLON}){5} ({VALUE})'",
        """
        template = "({VALUE})"
        _index = field.find(':')
        if _index < 0:
            self._errors += ("Field pattern '%s' should have a ':'\n" % field)

        grep_exp = field[:_index].replace("{COLON}", ":")
        if grep_exp.count(template) != 1:
            self._errors += \
                ("'%s' should have a unique match in '%s'; found %d times \n" % \
                 (template, grep_exp, grep_exp.count(template)))

        if (field_value_regex is not None) and not field_value_regex:
            value = re.escape(field[(_index + 1):])
        else:
            value = field[(_index + 1):]

        return grep_exp.replace(template, value)

    def _convert_fields(self, user_input):
        if isinstance(user_input, (str, unicode)):
            user_input = self._process_one_element(user_input)

            result = [item.strip() for item in user_input.split(',')]
        else:
            result = []
            for mem in user_input:
                result.append(self._process_one_element(mem))

        return result

    def _process_one_element(self, user_input):
        user_input = str(user_input)
        if user_input.startswith('("'):
            user_input = user_input[2:].replace('",)', '')

        elif user_input.startswith("('"):
            user_input = user_input[2:].replace("',)", '')
        return user_input

    def _is_yes(self, yes_no):
        """
        - If yes_no starts with y or Y, returns True
        - elif yes_no starts with n or N, returns False
        - else returns None
        """
        if yes_no is None:
            return None

        if yes_no.startswith('y'):
            return True
        elif yes_no.startswith('Y'):
            return True
        elif yes_no.startswith('n'):
            return False
        elif yes_no.startswith('N'):
            return False
        else:
            return None
