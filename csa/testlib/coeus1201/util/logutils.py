#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/util/logutils.py#1 $

# python inport
import types
import os

# sarf import
from common.util.utilcommon import UtilCommon
from accesslogparser import LogCheckException, AccessLogResults

class LogCommon(UtilCommon):
    """ Base class for log checking utilities """

    pass

class AccessLog(LogCommon):
    """Keywords for checking records in access log.

    *Access log fields*

    Any combination of the following fields along with its expected values can
    be passed into `log_check_fields` parameter of `Access Log Check` keyword.

    `log_check_fields` parameter expect a string of comma separated pairs
    'field:value' or a list of such strings. See examples below.

    | *Common values* | utime | elapsed | client | action | wbrs_score | status | bytes | http_line |
    | ... | ident | peer_tag | peerhost | mimetype | acl_dec_tag | policy_group | identity | oms_policy |
    | ... | data_security_policy | dlp_policy | routing_policy | user_agent | url_filt_cat |
    | |
    | *Webroot specific values* | wr_asw_verdict | wr_spyware_name | wr_trr | wr_spyid | wr_traceid |
    | |
    | *Mcafee specific values* | mc_verdict | mc_filename | mc_scan_error | mc_detect_type | mc_virus_type | mc_virus_name |
    | |
    | *Data Loss Prevention specific values* | ids_verdict | icap_verdict |
    | |
    | *Firestones CA specific values* | fs_url_cat_code | fs_req_side_cat |
    | |
    | *Sophos specific values* | sophos_verdict | sophos_code | sophos_class | sophos_name |
    | |
    | *DVS specific values* | dvs_verdict |
    | |
    | *WBRS Threat Type* | wbrs_threat |
    | |
    | *AVC specific values* | avc_app | avc_type | avc_behavior |
    | |
    | *Safe search specific values* | safe_srch_verdict |
    | |
    | *Bandwidth control specific* | bw_avg | bw_throttle |
    | |
    | *Mobile User Security specific values* | mus_tag |
    | |
    | *Outbound AMW scan verdicts* | outbound_dvs_verdict_name | outbound_dvs_threat_name |

    Example (check one access log record):
    | Access Log Check | log_check_fields=status:200, action=TCP_MEM_HIT, mimetype=text/html |

    Example (check few access log record in one shot):
    | @{expected_fields} = | Set Variable |
    | ... | status:301, action=TCP_MEM_HIT, mimetype=text/html |
    | ... | status:200, action=TCP_MISS, mimetype=text/html |
    | Access Log Check | log_check_fields=@{expected_fields} |

    *Sample accesslog entry broken down into its fields*

    1303256707.567 542 10.7.1.41 TCP_HIT/200 528969 GET
    http://services.wga/test-data/SSE/merlin/SpyKeylogger-install.exe - NONE/-
    application/x-dosexec MONITOR_AMW_RESP_11-AccessOrDecryptionPolicy-Identity
    -OutboundMalwareScanningPolicy-DataSecurityPolicy-ExternalDLPPolicy
    -RoutingPolicy <IW_infr,0.0,18,"SpyKeyLogger",0,141112,9477,23,"-",0,1,1,
    "Generic PWS.y",34,262659,"SpyKeylogger-install.exe/FILE:000b",
    "App/SKeyLog-Gen",-,-,IW_infr,-,"PUA","-","Unknown","Unknown","-","-",
    7807.66,0,-,"-","-"> -

    - utime 1303256707
    - elapsed 542
    - client 10.7.1.41
    - action TCP_HIT
    - wbrs_score 0.0
    - status 200
    - bytes 528969
    - http_line GET http://services.wga/test-data/SSE/merlin/SpyKeylogger-install.exe
    - ident -
    - peer_tag NONE
    - peer_host -
    - mimetype application/x-dosexec
    - acl_dec_tag MONITOR_AMW_RESP_11
    - policy_group AccessOrDecryptionPolicy
    - identity Identity
    - oms_policy OutboundMalwareScanningPolicy
    - data_security_policy DataSecurityPolicy
    - dlp_policy ExternalDLPPolicy
    - routing_policy RoutingPolicy
    - user_agent -
    - url_filt_cat IW_infr
    - wr_spyware_name SpyKeyLogger
    - wr_asw_verdict 18
    - wr_trr 0
    - wr_spyid 141112
    - wr_traceid 9477
    - mc_verdict 23
    - mc_filename -
    - mc_scan_error 0
    - mc_detect_type 1
    - mc_virus_type 1
    - mc_virus_name Generic PWS.y
    - sophos_verdict 34
    - sophos_code 262659
    - sophos_class SpyKeylogger-install.exe/FILE:000b
    - sophos_name App/SKeyLog-Gen
    - ids_verdict -
    - icap_verdict -
    - fs_url_cat_code IW_infr
    - fs_req_side_cat -
    - dvs_verdict PUA
    - wbrs_threat -
    - avc_app Unknown
    - avc_type Unknown
    - avc_behavior -
    - safe_srch_verdict -
    - bw_avg 7807.66
    - bw_throttle 0
    - mus_tag -
    - outbound_dvs_verdict_name -
    - outbound_dvs_threat_name -
    """

    def get_keyword_names(self):
        return [
                'access_log_create_baseline',
                'access_log_check',
                'access_log_compare_files',
                ]

    def _get_access_logs(self, patt, filename=None):
        qr = self._shell.logreader.search_now(
                 patt,
                 filename,
                 parse_class=AccessLogResults,
        )
        return qr

    def access_log_create_baseline(self, patt='^'):
        """ Get baseline: current number of records in the access log
        that match pattern `patt`.

        Parameters:
          - `patt`: Specify a specific pattern to look for. Only records that
                    match this pattern will be counted.
                    By default '^' is used and all log records are matched.

        Examples:
        | ${baseline}= | Access Log Create Baseline |
        | ${baseline}= | Access Log Create Baseline | patt=text/plain |
        """
        records_num = self._get_access_logs(patt).match_qty
        self._debug("Created base line: %s" % records_num)
        return records_num

    def access_log_check(self,
                          responses=None,
                          log_check_fields=None,
                          wait_only=False,
                          patt='^',
                          entry_num=0,
                          expect_new_entries=0,
                          baseline=0,
                          wait_timeout=30):
        """ Check the access logs on the WSA

        Verify that the access logs match up with the actual traffic
        that helped to generate them.

        Parameters:
          - `responses`: Response object  returned from `Send Request` keyword.
                         It will contain a list of responses when request were
                         redirected or request is made to few URLs.
                         This list provides HTTP response codes to be
                         checked against the access logs. It also supplies
                         debug information if the log check fails.

          - `log_check_fields`: List of strings of comma separated pairs
                         "field:expected value". If not passed then 'status'
                         fields will be checked in access log record - expected
                         values will be taken from the response object.

                         Possible values are:
                         * a string of comma separated pairs 'field:value'
                         * or list of such strings, in case few access log
                         records should be verified.

                         Field names are listed in `Introduction`. Additionally
                         if custom fields are included in log entry then they
                         can be referred as 'custom_field1, 'custom_field2',
                         etc. Custom fields in log entry are separated by space.
                         Possible values of custom field number (N in
                         'custom_fieldN' field name) are 1 or greater.


          - `wait_only`: Sometimes you need to wait for log entries to show
                         up before you run the next test. Either True or False,
                         False is used by default.

          - `patt`: Specify a specific pattern to look for. Only records that
                         match this pattern will be selected for checking.
                         By default '^' is used and all log records are matched.

          - `entry_num`: For checking access log, without passing in Response
                         object, specify the entry number of the access log to
                         compare `log_check_fields` against.  Default to the
                         very first entry. If `baseline` is passed then the
                         first entry after baseline will be checked by default.
                         Negative values can be passed to check log entries
                         from the end of the log. For example: `entry_num`=-1
                         will check very last log record.

          - `expect_new_entries`: For checking access log, without passing in
                         Response object, number of new entries that are
                         expected to appear can be specified. By default
                         `expect_new_entries`=0 and no new entries are expected
                         and entry with number `entry_num` will be taken from
                         existent log entries.
          - `baseline`: number of old records in the log file. If specified then
                         the keyword will expect 'baseline + expect_new_entries`
                         entries in the access log and will fail otherwise. By
                         default is zero and number of old records will be
                         calculated at the beginning of keyword's execution.

                         Note: If you use custom pattern for matching log
                         records then value of `patt` parameter - the
                         pattern should be the same for two keywords:
                         `Access Log Create Baseline` and `Access Log Check`

          - `wait_timeout`: time in seconds to wait until new records appear in
                         the log. Default time is 30 seconds.

        Examples:
        | ${response}= | Send Request | uri=http://yahoo.com | proxy=${DUT}:80 |
        | Access Log Check | responses=${response} |
        | |
        | ${response}= | Send Request | proxy=${DUT}:80 |
        | ... |  uri_list=http://slashdot.org, http://espn.com, http://craigslist.org |
        | Access Log Check | responses=${response} |
        | |
        | ${response}= | Send Request | uri=http://yahoo.com | proxy=${DUT}:80 |
        | Run Keyword And Expect Error | * | Access Log Check | responses=${response} |
        | ... |  log_check_fields=status:200 |
        | |
        | @{expected_fields}= | Set Variable |
        | ... |  status:200, action:TCP_MISS |
        | ... |  status:301, action:TCP_MISS |
        | ... |  status:200, action:TCP_MISS |
        | ... |  status:302, action:TCP_MISS |
        | ... |  status:302, action:TCP_MISS |
        | ... |  status:302, action:TCP_MISS |
        | ... |  status:200, action:TCP_MISS |
        | ${response}= | Send Request | proxy=${DUT}:80 |
        | ... |  uri_list=http://slashdot.org, http://espn.com, http://craigslist.org |
        | Access Log Check | responses=${response} |
        | ... |  log_check_fields=@{expected_fields} |
        | |
        | rollovernow | accesslogs |
        | ${output}= | Run | curl -v -m 60 -x ${DUT}:80 http://google.com -o /dev/null |
        | Access Log Check | log_check_fields=status:301, policy_group:DefaultGroup |
        | |
        | ${output}= | Run | curl -v -m 60 -x ${DUT}:80 http://google.com -o /dev/null |
        | Run Keyword And Expect Error | * | Access Log Check |
        | ... |  log_check_fields=status:200, action:TCP_MISS | entry_num=-1 | expect_new_entries=1 |
        | ${baseline}= | Access Log Create Baseline |
        | @{expected_fields}= | Set Variable |
        | ... | identity:DefaultGroup |
        | ... | identity:DefaultGroup |
        | ... | identity:DefaultGroup |
        | ${output}= | Run | curl -v -m 60 -x ${DUT}:80 http://www.google.com -o /dev/null |
        | ${output}= | Run | curl -v -m 60 -x ${DUT}:80 http://www.yahoo.com -o /dev/null |
        | ${output}= | Run | curl -v -m 60 -x ${DUT}:80 http://www.cisco.com -o /dev/null |
        | Access Log Check | log_check_fields=@{expected_fields} |
        | ... | expect_new_entries=3 | baseline=${baseline} |
        | |
        | ${output}= | Run | curl -v -m 60 -x ${DUT}:80 http://www.google.com -o /dev/null |
        | Access Log Check | log_check_fields=custom_field1:NONE, custom_field2:- |
        """
        # Convert arguments into lists if needed
        if type(responses) == types.InstanceType:
            responses = [responses]

        if responses:
            # For some reason, 307s are not logged in accesslogs
            filtered_responses = [resp
                    for resp in responses if resp.status != 307]

        # parse integer arguments
        entry_num = int(entry_num)
        expect_new_entries = int(expect_new_entries)
        baseline = int(baseline)
        wait_timeout = int(wait_timeout)

        # update entry_num if baseline specified
        if entry_num >= 0:
            entry_num += baseline

        # parse a list of strings of comma separated pairs
        if log_check_fields is None:
            # If no dictionary is passed, check status for each request
            if responses is not None:
                log_check_dicts = [{'status':resp.status}
                        for resp in filtered_responses]
            else:
                log_check_dicts = None
        else:
            if isinstance(log_check_fields, basestring):
                # string of comma separated pairs
                log_check_dicts = \
                    [self._convert_to_dictionary(str(log_check_fields))]
            elif type(log_check_fields) == types.ListType:
                # list of values
                if isinstance(log_check_fields[-1], basestring):
                    # list of strings
                    log_check_dicts = [self._convert_to_dictionary(str(item))
                            for item in log_check_fields]
                else:
                    # list of dictionaries
                    log_check_dicts = log_check_fields
            elif type(log_check_fields) == types.DictType:
                # left to accept dictionary also
                log_check_dicts = [log_check_fields]
            else:
                raise ValueError('Incorrect value of "log_check_fields" '\
                        'parameter')

        if log_check_dicts is not None:
            # convert string value to float for utime field
            for dict_item in log_check_dicts:
                if dict_item.has_key('utime'):
                    dict_item['utime'] = float(dict_item['utime'])

            # convert string values to integer for elapsed, status, bytes
            # fields
            integer_values = ['elapsed', 'status', 'bytes']
            for value in integer_values:
                for dict_item in log_check_dicts:
                    if dict_item.has_key(value):
                        dict_item[value] = int(dict_item[value])

        if responses:
            self._check_access_logs_with_respone_list(patt,
                                                 filtered_responses,
                                                 log_check_dicts,
                                                 wait_only,
                                                 baseline,
                                                 wait_timeout)
        else:
            self._check_access_logs_with_dict_list(patt,
                                              log_check_dicts,
                                              entry_num,
                                              wait_only,
                                              baseline,
                                              wait_timeout,
                                              expect_new_entries)
        self._info('Fields in access log records matched expected values')

    def _check_access_logs_with_respone_list(self,
                           patt,
                           response_list,
                           log_check_dict_list,
                           wait_only,
                           baseline,
                           timeout):

        # How many log entries should we expect?
        if baseline > 0:
            curr_num_log_entries = baseline
        else:
            curr_num_log_entries = self._get_access_logs(patt).match_qty
        num_new_entries = len(response_list)
        exp_qty = curr_num_log_entries + num_new_entries

        self._info('Waiting for %d (%d new) log entries to appear in ' \
                   'the Access Logs' % (exp_qty, num_new_entries))
        qr = self._shell.logreader.search(
                 patt,
                 exp_qty=exp_qty,
                 parse_class=AccessLogResults,
                 timeout=timeout
        )

        if qr.match_qty != exp_qty:
            self._info('Found access log records:\n' + \
                    '\n'.join(qr.found_lines))
            raise LogCheckException, \
                    'Expected %s log entries, but actually %s entries '\
                    'exist' % (exp_qty, qr.match_qty)

        # print debug info to the log
        self._debug('Found access log entries:\n'
                + '\n'.join(qr.found_lines[:curr_num_log_entries])
                + '\n\nNewly appeared log entries:\n'
                + '\n'.join(qr.found_lines[curr_num_log_entries:]))

        # Sometimes we only want to wait for the log entry to show up
        # because the test already failed and we want the next test to
        # function correctly.
        if wait_only:
            return qr.found_lines

        access_entries = qr.access_entries[curr_num_log_entries:exp_qty]
        # XXX: Is it ever possible to log entries out of order?
        # XXX: If that is not an error case, then this code could break.
        for response, log_check_dict, entry in zip(response_list,
                                                   log_check_dict_list,
                                                   access_entries):
            for check_field, exp_value in log_check_dict.items():
                # get actual value
                act_value = self._get_actual_value(check_field, entry)

                # If actual value from logs does not equal or is not in
                # the expected value, raise an exception
                if not _equal_or_in(act_value, log_check_dict[check_field]):
                    raise LogCheckException, \
                       'Expected %s request to %s to match %s %r, ' \
                       'actually matched %s %r' % (response.method or 'GET',
                                                   response.uri,
                                                   check_field,
                                                   exp_value,
                                                   check_field,
                                                   act_value)

    def _check_access_logs_with_dict_list(self,
                           patt,
                           log_check_dict_list,
                           entry_num,
                           wait_only,
                           baseline,
                           timeout,
                           num_new_entries=0):

        # How many log entries should we expect?
        if baseline > 0:
            curr_num_log_entries = baseline
        else:
            curr_num_log_entries = self._get_access_logs(patt).match_qty
        exp_qty = curr_num_log_entries + num_new_entries

        # if new entries is expected
        if num_new_entries > 0:
            self._info('Waiting for %d (%d new) log entries to appear in ' \
                       'the Access Logs' % (exp_qty, num_new_entries))
            qr = self._shell.logreader.search(
                     patt,
                     exp_qty=exp_qty,
                     parse_class=AccessLogResults,
                     timeout=timeout
            )

            if qr.match_qty != exp_qty:
                self._info('Found access log records:\n' + \
                        '\n'.join(qr.found_lines))
                raise LogCheckException, \
                        'Expected %s log entries, but actually %s entries '\
                        'exist' % (exp_qty, qr.match_qty)
        else:
            qr = self._shell.logreader.search(
                     patt,
                     parse_class=AccessLogResults,
                     timeout=120
            )

        # Sometimes we only want to wait for the log entry to show up
        # because the test already failed and we want the next test to
        # function correctly.
        if wait_only:
            return qr.found_lines

        if not qr.match_qty > 0:
            raise LogCheckException, 'Did not get any access log entry'

        # check whether we have a list of expected values
        if log_check_dict_list is None:
            raise LogCheckException, 'List of expected field:value strings '\
                    'not specified. Use log_check_fields parameter.'

        # check whether entry_num is in log_entries and
        # whether length of log_check_dict_list is less or equal to the
        # length of log_entries minus entry_num
        log_entries = qr.found_lines[:]
        if (entry_num >= 0\
                and len(log_entries) >= entry_num + len(log_check_dict_list))\
            or (-1 * (len(log_entries) + 1) < entry_num < 0\
                   and len(log_check_dict_list) <= -1 * entry_num):

            # highlight the one or more to be checked
            log_entries[entry_num] = '\nEntry that are being checked:\n' + \
                    log_entries[entry_num]
            # end of checked entries
            log_entries[entry_num + len(log_check_dict_list) - 1] += '\n'
            self._debug('Found access log entries:\n'
                    + '\n'.join(log_entries))
        else:
            if entry_num < 0:
                entry_num += len(log_entries)
            entry_nums = entry_num + 1
            if len(log_check_dict_list) > 1:
                entry_nums = str(entry_nums) + '..' + str(entry_nums +
                        len(log_check_dict_list) - 1)
            raise LogCheckException, 'There are %s entries in the access log. '\
                    'Access log entries #%s do not exist' \
                    % (len(log_entries), entry_nums)

        # check all fields specified in log_check_dict_list
        for i in range(len(log_check_dict_list)):
            log_check_dict = log_check_dict_list[i]
            # pick out the specified entry number
            entry = qr.access_entries[entry_num + i]

            for check_field, exp_value in log_check_dict.items():
                # get actual value
                act_value = self._get_actual_value(check_field, entry)

                # If actual value from logs does not equal or is not in
                # the expected value, raise an exception
                if not _equal_or_in(act_value, exp_value):
                    raise LogCheckException, \
                       'Expected access log field "%s" to match %r, ' \
                       'actually matched %r in the entry:\n%s' % (check_field,
                           exp_value, act_value, qr.found_lines[entry_num + i])

    def _get_actual_value(self, check_field, entry):
        if check_field.startswith('custom_field'):
            # parse custom fields
            field_id = int( check_field[len('custom_field'):] )
            if field_id > len(entry.custom_fields):
                raise LogCheckException, \
                        'Custom field %s does not exist, there is %s' \
                        'custom fields' % (field_id, len(entry.custom_fields))
            if field_id <= 0:
                raise LogCheckException, \
                        'Custom field number should be 1 or greater,' \
                        'you are trying to get filed number %s' \
                        % (field_id,)
            act_value = entry.custom_fields[field_id - 1]
        else:
            exec('act_value = entry.%s' % check_field)
        return act_value

    def _get_saved_logs(self, log_dir='/data/pub/', log_type='accesslogs'):

        cmd = 'ls ' + os.path.join(log_dir, log_type, '*.s')
        output = self._shell.send_cmd(cmd)
        files = output.split()
        return files

    def access_log_compare_files(self,
            patt='^',
            check_fields='status',
            check_records_num=True,
            saved_file_id=-1):
        """ Access Log Files Comparing Utility.

        The keyword allows comparing desired list of fields in corresponding
        records of two files: one of the saved (*.s) files and the current one.

        First of all, both files will be checked for same number of records in
        them. If `check_records_num` parameter is True then in case of different
        number of entries - exception will be raised and keyword will fail. If
        `check_records_num` is False then only number of records available in
        both files will be checked.

        Values of all desired fields specified using `check_fields` parameter
        will be compared for every pair of log entries from both file. If values
        of any of desired fields differ then keyword will fail. Every log record
        from current file will be compared to the corresponding log record of
        the saved file. For example the first record in one file will be
        compared to the first one in other file, second to second, etc.

        Parameters:
          - `patt`: Specify a specific pattern to look for. Only records that
                    match this pattern will be selected for checking.
                    By default '^' is used and all log records are matched.
          - `check_fields`: a string of comma separated or a list of fields to
                    be compared in both files. Whole list of possible fields can
                    be found in `Introduction`. By default status field will be
                    checked.
          - `check_records_num`: Specify whether to raise an exception when
                    number of log records are different in files. Either True
                    or False.
          - `saved_file_id`: sequence number of saved log file (*.s) to be used
                    for comparison against the current log file. By default '-1'
                    - the most recently saved log file. 0 - is the oldest saved
                    log file.

        Examples:

        Compare status fields in aclog.current and the most recently
        saved log file
        | Access Log Compare Files |

        Send number of requests two times and compare action taken, status and
        acl_dec_tag fields
        | rollovernow | accesslogs |
        | Send Request | uri=http://yahoo.com | proxy=${DUT}:80 |
        | Send Request | uri=https://google.com | proxy=${DUT}:80 |
        | Send Request | uri=http://cisco.com | proxy=${DUT}:80 |
        | Sleep | 10 | Wait for records to appear in accesslog |
        | rollovernow | accesslogs |
        | Send Request | uri=http://yahoo.com | proxy=${DUT}:80 |
        | Send Request | uri=https://google.com | proxy=${DUT}:80 |
        | Send Request | uri=http://cisco.com | proxy=${DUT}:80 |
        | Sleep | 10 | Wait for records to appear in accesslog |
        | Access Log Compare Files | check_fields=action, status, acl_dec_tag |

        Skip checking number of records and compare with one before the
        recently saved file (the last but one in the list of saved files)
        | Access Log Compare Files | check_fields=action, status, acl_dec_tag |
        | ... | saved_file_id=-2 | check_records_num=${False} |
        """

        # get name of recently saved log file
        saved_file_id = int(saved_file_id)
        saved_log = self._get_saved_logs()[saved_file_id]

        # get AccessLogResults objects
        qr_current = self._get_access_logs(patt)
        qr_saved = self._get_access_logs(patt, filename=saved_log)

        # check number of records
        num_current = len(qr_current.found_lines)
        num_saved = len(qr_saved.found_lines)
        if check_records_num and num_current != num_saved:
            raise LogCheckException, \
                'Number of records in access logs are different: %s in %s '\
                'vs %s in current log' % (num_saved, saved_log, num_current)

        # compare desired fields for all entries
        check_fields = self._convert_to_tuple(check_fields)
        num_entries = min(num_current, num_saved)
        diff_records = 0
        for i in xrange(num_entries):
            diff_count = 0
            diff_desc = []
            entry_current = qr_current.access_entries[i]
            entry_saved = qr_saved.access_entries[i]
            for check_field in check_fields:
                exec('value_current = entry_current.%s' % check_field)
                exec('value_saved = entry_saved.%s' % check_field)
                if value_current != value_saved:
                    diff_count += 1
                    diff_desc.append('Field %s has different values: %s vs %s.'
                            % (check_field, value_saved, value_current))
            if diff_count > 0:
                diff_records += 1
                self._info('Following records are different in %s and current'
                        ' log file:\n%s \n%s'
                        % (saved_log, qr_saved.found_lines[i],
                            qr_current.found_lines[i]))
                self._info('Details:\n' + '\n'.join(diff_desc))


        self._info('Compared fields: %s in %d record(s)' %\
                (', '.join(check_fields), num_entries))
        if diff_records > 0:
            raise LogCheckException, \
                    '%d records has different field(s) values.' % diff_records

def _equal_or_in(a,b):
    if a == b:
        return True
    if type(b) in (types.TupleType, types.ListType) and a in b:
        return True
    # if identity, policy has spaces that they are replaced with underscores
    if isinstance(a, basestring) and isinstance(b, basestring):
        if a.replace(' ', '_') == b.replace(' ', '_'):
            return True
    return False

