#!/usr/bin/env python

import re
import os
import subprocess
import time
from optparse import OptionParser


class APICall():
    """
    API related utility
    """

    def __init__(self, dut, port):
        self.dut = dut
        self.port = port

    def process_line(self, line, var_list):
        flags = {'skip_line': False, 'http_code_provided': False}
        if not line.strip() or line.strip().startswith('#'):
            # Ignoring empty lines and lines starting with '#'(comment lines)
            flags['skip_line'] = True
        for var_name in var_list.keys():
            # Substitute variables
            line = line.replace("${%s}" % (var_name), var_list[var_name])
        line_args = line.strip().split('|')
        if len(line_args) != 2 and len(line_args) != 3:
            flags['skip_line'] = True
        if len(line_args) == 3 and line_args[2] != '':
            flags['http_code_provided'] = True
        return (line_args, flags)

    def call_curl(self, line_args, logfile):
        cmd = "echo -e '\n===================================\nCurl Request with options: %s\nOutput:\n' >> %s" % (
        line_args, logfile)
        subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        cmd = 'curl -m 60 -w "\nAPI_COMMAND_CODE=##%%{http_code}##\n" %s \
        "https://%s:%s/api/v1.0/%s" 2>&1 | tee -a %s' % (line_args[0], self.dut, self.port, line_args[1], logfile)
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output = p.stdout.read()
        if re.compile(r'.*API_COMMAND_CODE=##(.*)##.*').search(output):
            http_code = re.compile(r'.*API_COMMAND_CODE=##(.*)##.*').search(output).group(1)
            return http_code
        # Else some error in getting response, setting response code to None
        return None

    def update_stats(self, http_code, http_code_provided,
                     line_args, passed_uris, failed_uris):
        api_url = "api/v1.0/%s" % (line_args[1])
        if http_code_provided:
            if http_code == line_args[2]:
                passed_uris.append(api_url)
            else:
                failed_uris.append(api_url)
        else:
            if (http_code >= '200' and http_code < '300'):
                passed_uris.append(api_url)
            else:
                failed_uris.append(api_url)
        return passed_uris, failed_uris

    def do_api_curl_calls(self, cmd_file, input_params):
        """
        Does API curl requests to DUT by taking the input api requests
        from the file provided.
        """

        passed_uris = []
        failed_uris = []
        if os.path.isfile(input_params['logfile']):
            os.system("sudo rm -rf %s" % (input_params['logfile']))
        try:
            start = time.time()
            for i in range(0, input_params['repeat_count']):
                with open(cmd_file) as infile:
                    for line in infile:
                        line_args, flags = self.process_line(line,
                                                             input_params['variables'])
                        if not flags['skip_line']:
                            http_code = self.call_curl(line_args,
                                                       input_params['logfile'])
                            passed_uris, failed_uris = self.update_stats(
                                http_code, flags['http_code_provided'],
                                line_args, passed_uris, failed_uris)
                        now = time.time()
                        if now - start > input_params['test_duration']:
                            break
                        # Delay after each curl command
                        time.sleep(input_params['repeat_delay'])
                # Delay after each run of the file contents
                now = time.time()
                if now - start > input_params['test_duration']:
                    break
                time.sleep(input_params['repeat_delay'])
            return {'passed': len(passed_uris),
                    'failed': len(failed_uris),
                    'failed_uris': failed_uris,
                    'passed_uris': passed_uris,
                    'log_file': input_params['logfile'],
                    }
        except Exception:
            raise


if __name__ == '__main__':

    parser = OptionParser(usage='usage: %prog [options] dut_host command_file')
    parser.add_option("--port", dest="port", default="8443",
                      help="DUT port name to connect to")
    parser.add_option("--logfile", dest="logfile", default='/tmp/api_log_file.txt',
                      help="Entire curl log dump file name. Default: /tmp/api_log_file.txt")
    parser.add_option("-r", "--repeat", dest="repeat_count", type='int', default=1,
                      help="number of times to loop around the file contents")
    parser.add_option("-d", "--delay", dest="repeat_delay", type='int', default=4,
                      help="number of seconds to wait before repeating the loop again")
    parser.add_option("-v", "--variable", action='append', dest="variables",
                      help="variables. syntax: -v D1:'16 May 2014' -v D2:'16 June 2014'")
    parser.add_option("-t", "--test-duration", dest="test_duration", type='int',
                      default=1000000,
                      help="Test duration in seconds - 300")

    (options, args) = parser.parse_args()
    option_dict = vars(options)
    if len(args) != 2:
        parser.error("Incorrect number of arguments")
    if not option_dict['variables']:
        option_dict['variables'] = {}
    temp = {}
    for value in option_dict['variables']:
        temp[value.split(':')[0]] = value.split(':')[1]
    option_dict['variables'] = temp

    api_util = APICall(args[0], option_dict['port'])
    final_api_output = api_util.do_api_curl_calls(args[1], option_dict)
    print "API Report= ", final_api_output
