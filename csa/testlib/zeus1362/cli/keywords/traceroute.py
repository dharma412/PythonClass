# $Id: //prod/main/sarf_centos/testlib/zeus1362/cli/keywords/traceroute.py#1 $ $DateTime: 2020/06/10 22:29:20 $ $Author: sarukakk $

from common.cli.clicommon import CliKeywordBase
from common.cli import cliexceptions
import re

class Traceroute(CliKeywordBase):

    enabled_options = ['-S', '-v', '-n']
    report_as_string = 'string'
    report_as_list = 'list'

    """
    Returns a route from interface to host
    """
    def get_keyword_names(self):
        return ['traceroute' ]

    def traceroute(self, interface='Auto', host=None, options=None,\
            result_option='string'):
        """
        Returns a route from specified interface to specified host

        *Parameters:*
        - `interface`: the interface name or IP address you want to trace from
        - `host`: the host or IP address you want to trace to
        - `options`: options that can be used during tracing
        - `result_option`: result of tracing can be returned as list or string

        *Example:*
        | ${log}=   | Traceroute | host=${CLIENT_IP} |
        | ${log}=   | Traceroute | interface=Auto | host=${CLIENT_IP} |
        | ${log}=   | Traceroute | interface=Management | host=${CLIENT_IP} |
        | ${log}=   | Traceroute | host=${CLIENT_IP} | options=-S -n -v |
        | ${log}=   | Traceroute | host=${CLIENT_IP} | options=-w 10 |
        | ${log}=   | Traceroute | host=${CLIENT_IP} | result_option=list |
        """
        error_message_time_for_wait = 'time to wait should be integer'

        if host is None or not host:
            raise cliexceptions.ConfigError('Please specify host to trace to.')
        elif options != None:

            option_list = options.split(" ")
            w_has_been_found = False

            for option in option_list:

                if option.lower() == '-w':
                    w_has_been_found = True
                else:

                    if w_has_been_found:
                        if not re.search('^[0-9]+$', option):
                            raise cliexceptions.ConfigError(error_message_time_for_wait)
                    elif option not in self.enabled_options:
                        raise cliexceptions.ConfigError('Please specify correct options.')
                    w_has_been_found = False

            if w_has_been_found:
                raise cliexceptions.ConfigError(error_message_time_for_wait)

        result = self._cli.traceroute(interface, host, options)

        if result_option.lower() == self.report_as_list:
            result = result.parse()
        else:
            result = str(result)
        return result