#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/common/util/api_utils.py#1 $
# $DateTime: 2019/03/22 01:36:06 $
# $Author: aminath $

from common.util.utilcommon import UtilCommon
from common.util.misc import Misc
import re
import base64
import subprocess
from datetime import datetime, timedelta
import time
from api_data import *


class APIUtils(UtilCommon):
    """
    API related utilities
    """

    global found_dict, expected_dict
    found_dict = {}
    expected_dict = {}

    def get_keyword_names(self):
        return [
            'get_swap_usage',
            'base64_encode',
            'send_api_request',
            'get_time_in_utc',
            'verify_api_output',
            'verify_api_entity_output',
        ]

    def send_api_request(self, url, timeout=60, headers='',
                         credentials='', ntlm_mode=''):
        """
        Sends REST API request using curl command

        *Parameters*:
        - `url`: API URL to query
        - `timeout`: max curl command timeout
        - `headers`: comma separated headers to pass to server
        - `credentials`: ESA credentials. Usage: username:password
        - `ntlm_mode`: Authentication mode.

        *Return*:
        Two dictionaries. First dictionary contains http response code
        & error details if any and the second dictionary contains the
        actual API response

        *Example*:
        | ${resp_dict2} | ${api_output2}= | Run Keyword Unless |
        | ${use_base64_auth} | Send API Request | ${final_uri} |
        | credentials=${user}:${pwd} | ntlm_mode=${auth_mode} |

        """
        if ntlm_mode:
            ntlm_mode = "--" + ntlm_mode
        if credentials:
            credentials = "--user '%s'" % (credentials)
        header_opts = ''
        if headers:
            for header in headers.split(','):
                header_opts = header_opts + "-H \"%s\"" % (header) + " "
        cmd = 'curl -s -k -w "HTTP_RESPONSE_CODE=%{http_code}" -m ' + \
              '%s %s %s %s "%s"' % (timeout, header_opts, ntlm_mode, credentials, url)
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        curl_api_output = p.stdout.read()
        output_list = curl_api_output.split('HTTP_RESPONSE_CODE=')
        response_dict = {}
        api_output = {}
        response_dict['http_code'] = int(output_list[1])
        if output_list[0]:
            if response_dict['http_code'] == 200:
                api_output = eval(output_list[0])
            else:
                try:
                    response_dict['http_err_msg'], response_dict['http_err_desc'] = \
                        re.search('<p>Message: (.*)\s+.*<p>Error code explanation: (.*)\s+', \
                                  output_list[0]).groups()
                except AttributeError:
                    err_output = eval(output_list[0])
                    response_dict['http_err_msg'] = err_output['error']['message']
                    response_dict['http_err_desc'] = err_output['error']['explanation']
        return response_dict, api_output

    def verify_api_output(self, group_name=None, api_input_dict={}, counter_name=None):
        """
        Verifies REST API output.

        *Parameters*:
        - `group_name`: Name of the group whose counters need to be verified.
        - `api_input_dict`: Dictionary of API output from curl command.
        - `counter_name`: Name of the counter to be verified.

        *Return*:
        Returns 'Pass' if all the values match else errors out with difference list.

        *Example*:
        | ${verified_result}= | Verify API Output |
        | mail_virus_type_detail | ${api_output} |

        | ${verified_counter_result}= | Verify API Output |
        | mail_virus_type_detail | ${api_output} | incoming_total_recipients |

        """
        found_dict = {}
        expected_dict = {}
        api_input_dict = api_input_dict['data']
        if group_name in globals():
            print "Group is valid"
            compare_dict = globals()[group_name]
        else:
            raise ValueError(group_name + " is an invalid group")
        if counter_name != None:
            found_dict, expected_dict = self._check_dict_values(api_input_dict[counter_name], \
                                                                compare_dict[counter_name])
        else:
            found_dict, expected_dict = self._check_dict_values(api_input_dict, compare_dict)
        if found_dict:
            raise Exception('Mismatch found \nActual: %s \nExpected: %s' % (found_dict, expected_dict))

    def verify_api_entity_output(self, group_name=None, entity=None, api_dict={}):
        """
        Verifies REST API output for a given entity.

        *Parameters*:
        - `group_name`: Name of the group whose counters need to be verified.
        - `entity`: Name of the entity whose output to be verified.
        - `api_dict`: Dictionary of API output from curl command.

        *Return*:
        Returns 'Pass' if all the values match else errors out with difference list.

        *Example*:
        | ${verified_entity_result}= | Verify API Entity Output |
        | mail_virus_type_detail | ${virus_name} | ${api_output} |

        """

        found_dict = {}
        expected_dict = {}
        api_dict = api_dict['data']
        if group_name in globals():
            print "Group is valid"
            compare_dict = globals()[group_name]
        else:
            raise ValueError(group_name + " is an invalid group")
        for key in api_dict[entity].keys():
            if api_dict[entity][key] != compare_dict[key][entity]:
                found_dict[key] = api_dict[entity][key]
                expected_dict[key] = compare_dict[key][entity]
        if found_dict:
            raise Exception('Mismatch found \nActual: %s \nExpected: %s' % (found_dict, expected_dict))

    def _check_dict_values(self, dict1, dict2):
        for key in dict1.keys():
            if isinstance(dict1[key], dict):
                self._check_dict_values(dict1[key], dict2[key])
            elif dict1[key] != dict2[key]:
                found_dict[key] = dict1[key]
                expected_dict[key] = dict2[key]
        return found_dict, expected_dict

    def do_byte_conversion(self, param):
        """
        Converts value to bytes from Mega or Kilobytes.

        *Parameters*:
        - `param`: parameter value to be converted to bytes

        *Return*:
        Returns value in bytes
        """
        if param.endswith('M'):
            param = int(param.split('M')[0]) * 1024 * 1024
        elif param.endswith('K'):
            param = int(param.split('K')[0]) * 1024
        return param

    def get_swap_usage(self):
        """
        Gets system percentage swap utilized from top command.

        *Parameters*:
        None

        *Return*:
        Returns percentage swap utilized

        *Example*:
        | ${percentage_swap_util}= | Get Swap Usage |
        """
        top_output = Misc(self.dut, self.dut_version).run_on_dut("top -bu | grep Swap")
        total = used = ""
        match = re.findall("\s+(\d+\w+)\s+Total", top_output)
        if match:
            total = match[0]
        match = re.findall("\s+(\d+\w+)\s+Used", top_output)
        if match:
            used = match[0]
        total = self.do_byte_conversion(total)
        used = self.do_byte_conversion(used)
        if not total:
            raise Exception("Swap usage values couldn't be retrieved")

        swap_percent_used = 0.0
        if used:
            swap_percent_used = (float(used) * 100) / total
        return swap_percent_used

    def base64_encode(self, decoded_str):
        """
        Returns base64 encoded string

        *Parameters*:
        - `decoded_str` - string to be encoded

        *Return*:
        Returns base 64 encoded string
        """

        b64val = base64.b64encode(decoded_str)
        return b64val

    def get_time_in_utc(self, days_delta=0, offset_format=True):
        """
        Returns UTC time in the requested format

        *Parameters*:
        - `days_delta` - days to be subtracted or added from present date.
        Example: +1 indicates tomorrow's date & -1 indicates yesterday.
        By default returns present date & time.
        - `offset_format` - Return output in offset format or ISO format.

        *Return*:
        Returns UTC time in the requested format
        """

        date = datetime.utcfromtimestamp(time.time())
        date_delta = date - timedelta(days=-int(days_delta))
        if offset_format:
            formatted_date = date_delta.strftime("%Y-%m-%dT%H:00+00:00")
        else:
            formatted_date = date_delta.strftime("%Y-%m-%dT%H:00")
        return formatted_date
