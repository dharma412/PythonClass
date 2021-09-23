#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1350/cli/ctor/diagnostic.py#1 $ $DateTime: 2019/09/18 01:46:35 $ $Author: sarukakk $

"""
IAF 2 CLI command: diagnostic
"""

import clictorbase

from sal.containers.yesnodefault import is_no, is_yes, YES, NO
from sal.deprecated.expect import EXACT
from sal.exceptions import ConfigError


class diagnostic(clictorbase.IafCliConfiguratorBase):
    newlines = 1

    def __call__(self):
        """diagnostic utility command"""
        self._restart()
        self._writeln(self.__class__.__name__)
        return self

    def raid(self, action, confirm=YES, confirm_verify=YES):
        self._query_response('RAID')
        self._query_response(confirm)
        if is_no(confirm):
            self._to_the_top(self.newlines)
            return

        self._query_select_list_item(action)

        # if 'Run disk verify' is selected one more confirmation question
        # will be asked
        result = self._expect(['sure you want to proceed',
                               'Please choose the action'], timeout=20)
        if self._expectindex == 0:
            self._query_response(confirm_verify)
            self._expect('\n')
            util_result = self._read_until('Please choose the action')
        else:
            util_result = result.string

        self._to_the_top(self.newlines + 1)
        return util_result

    def disk_usage(self):
        """Check disk usage"""
        self._query_response('DISK_USAGE')
        self._expect('\n')
        raw = self._read_until('Choose the operation')
        self._to_the_top(self.newlines)
        return raw

    def network(self):
        self._query_response('network')
        return diagnosticNetwork(self._get_sess())

    def reporting(self):
        self._query_response('reporting')
        return diagnosticReporting(self._get_sess())

    def tracking(self):
        self._query_response('tracking')
        return diagnosticTracking(self._get_sess())

    def reload(self, sure=NO):
        self._query_response('reload')
        self._query('Are you sure you want to continue')
        self._writeln(sure)
        curr_status = self._read_until('Choose the operation')

        # if previous answer is yes, confirmation will be asked one more time
        if is_yes(sure) and \
                self._query('*really* sure you want to continue') == 0:
            self._writeln(sure)
            curr_status = self._read_until('Choose the operation')
            return curr_status

        self._to_the_top(self.newlines)
        return curr_status


class diagnosticNetwork(clictorbase.IafCliConfiguratorBase):

    def flush(self):
        """Flush the ARP, DNS, and LDAP cache"""
        self._query_response('flush')
        self._expect("\n")
        raw = self._read_until('Choose the operation')
        self._restart()
        return raw

    def arpshow(self):
        """Display the ARP cache"""
        self._query_response('arpshow')
        self._expect('\n')
        raw = self._read_until('Choose the operation')
        self._restart()
        return raw

    def smtpping(self, hostname_or_ip='aol.com',
                 network_interface="1", select_mx_host=YES, mx_host="2",
                 send_email=NO, from_email_id='from@aol.com',
                 to_email_id='to@aol.com', subject_message='Test Message',
                 message_body='test Body\r\n.'):
        """utility to check connectivity to another mail server"""
        self._query_response('smtpping')
        self._query_response(hostname_or_ip)
        if is_yes(select_mx_host):
            self._query_response(select_mx_host)
            self._query_select_list_item(mx_host)

        self._query_select_list_item(network_interface)
        self._query_response(send_email)

        if is_yes(send_email):
            self._query_response(from_email_id)
            self._query_response(to_email_id)
            self._query_response(subject_message)
            self._writeln(message_body)
        self._expect('Starting SMTP test')
        raw = self._read_until('Choose the operation')
        self._restart()
        return raw

    def tcpdump(self):
        self._query_response('tcpdump')
        return networkTcpdump(self._get_sess())


class diagnosticReporting(clictorbase.IafCliConfiguratorBase):
    newlines = 2

    def deletedb(self, confirm=NO, timeout=120):
        """Reinitialize the reporting database"""
        self._query_response('DELETEDB')
        self._query_response(confirm)
        curr_status = self._read_until("Choose the operation")
        self._to_the_top(self.newlines, timeout)
        return curr_status

    def disable(self):
        """Disable the reporting system"""
        self._query_response('DISABLE')
        curr_status = self._read_until("Choose the operation")
        self._to_the_top(self.newlines)
        return curr_status

    def enable(self):
        """Enable the reporting system"""
        self._query_response('ENABLE')
        curr_status = self._read_until("Choose the operation")
        self._to_the_top(self.newlines)
        return curr_status


class diagnosticTracking(clictorbase.IafCliConfiguratorBase):
    newlines = 2

    def deletedb(self, confirm=NO, timeout=120):
        """Reinitialize the tracking database"""
        self._query_response('DELETEDB')
        self._query_response(confirm)
        curr_status = self._read_until("Choose the operation")
        self._to_the_top(self.newlines, timeout)
        return curr_status

    def debug(self, confirm=NO):
        """Gather debug information"""
        debug_result = None
        self._query_response('DEBUG')
        self._query_response(confirm)
        if is_yes(confirm):
            self._expect('\n')

        debug_result = self._read_until('Choose the operation')

        self._to_the_top(self.newlines)
        return debug_result


class networkTcpdump(clictorbase.IafCliConfiguratorBase):
    newlines = 3

    def __init__(self, sess):
        clictorbase.IafCliConfiguratorBase.__init__(self, sess)
        self._set_local_err_dict(
            {('Capture already running', EXACT): clictorbase.IafCliError,
             ('Capture Not Running', EXACT): clictorbase.IafCliError,
             ('No captures to clear', EXACT): clictorbase.IafCliError})

    def start(self):
        self._query_response('START')
        curr_status = self._read_until("Choose the operation")
        self._to_the_top(self.newlines)
        return curr_status

    def stop(self):
        self._query_response('STOP')
        curr_status = self._read_until("Choose the operation")
        self._to_the_top(self.newlines)
        return curr_status

    def status(self):
        self._query_response('STATUS')
        self._expect('\n')
        curr_status = self._read_until("Choose the operation")
        self._to_the_top(self.newlines)
        return curr_status

    def setup(self, max_size, stop, interface, operation, port, client_ip, server_ip, custom_filter):
        self._query_response('SETUP')
        self._query_response(max_size)
        self._query_response(stop)
        self._query_response(interface)
        self._query_response(operation)
        if (operation == 'PREDEFINED'):
            self._query_response(port)
            self._query_response(client_ip)
            self._query_response(server_ip)
        elif (operation == 'CUSTOM'):
            self._query_response(custom_filter)
        curr_status = self._read_until("Choose the operation")
        self._restart()
        return curr_status

    def filter(self, filter=''):
        self._query_response('FILTER')
        self._writeln(filter)
        self._to_the_top(self.newlines)

    def interface(self, if_name=''):
        self._query_response('INTERFACE')
        self._writeln(if_name)
        self._to_the_top(self.newlines)

    def clear(self, confirm=YES):
        self._query_response('CLEAR')
        self._expect(['Do you want to remove', 'START'])

        # more then one capture file may be present. Remove all
        while self._expectindex == 0:
            self._writeln(confirm)
            self._expect(['Do you want to remove', 'START'])
        self._to_the_top(self.newlines)


if __name__ == '__main__':
    # if cli_sess is already defined, we have a CLI session object from
    # the validator we can use; if not, we must create one
    try:
        cli_sess
    except NameError:
        cli_sess = clictorbase.get_sess()
    ctor = diagnostic(cli_sess)

    print ctor().raid(action='verify')
    print ctor().raid(action='monitor')
    print ctor().raid(action='display')
    print ctor().raid(action='check')

    print ctor().disk_usage()

    print ctor().network().arpshow()
    print ctor().network().flush()
    print ctor().network().smtpping()
    ctor().network().tcpdump().start()
    print ctor().network().tcpdump().status()
    ctor().network().tcpdump().stop()
    ctor().network().tcpdump().start()
    ctor().network().tcpdump().stop()
    ctor().network().tcpdump().filter()
    ctor().network().tcpdump().interface()
    ctor().network().tcpdump().clear()

    ctor().reporting().deletedb()
    ctor().reporting().deletedb(confirm=YES)
    ctor().reporting().disable()
    ctor().reporting().enable()

    ctor().tracking().deletedb()
    ctor().tracking().deletedb(confirm=YES)
    print ctor().tracking().debug()
    print ctor().tracking().debug(confirm=YES)

    ctor().reload(NO)
