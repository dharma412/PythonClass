#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1350/cli/keywords/diagnostic.py#1 $
# $DateTime: 2020/01/06 01:25:43 $
# $Author: saurgup5 $

from common.cli.clicommon import CliKeywordBase
from common.cli.cliexceptions import CliError

class DiagnosticError(CliError):
    """ Incorrect values were entered to the page
    """
    def __init__(self, msg, page_errors=None):
        self.msg = msg
        if page_errors:
            self.page_errors = page_errors
        else:
            self.page_errors = list()
    def __str__(self):
        return str(self.msg) + ':\n\n' + '\n'.join(map(str, self.page_errors))
    # used by Robot Framework to print message to console and log
    def __unicode__(self):
        return unicode(self.__str__())

class Diagnostic(CliKeywordBase):
    """Configure Cisco IronPort system alerts.

    Class designed to provide keywords for Cisco IronPort diagnostic utility
    command.
    """

    def get_keyword_names(self):
        return [
                'diagnostic_raid',
                'diagnostic_disk_usage',
                'diagnostic_network_flush',
                'diagnostic_network_arpshow',
                'diagnostic_network_ndpshow',
                'diagnostic_network_smtpping',
                'diagnostic_network_tcpdump_start',
                'diagnostic_network_tcpdump_stop',
                'diagnostic_network_tcpdump_status',
                'diagnostic_network_tcpdump_setup',
                'diagnostic_reporting_delete_db',
                'diagnostic_reporting_disable',
                'diagnostic_reporting_enable',
                'diagnostic_tracking_delete_db',
                'diagnostic_tracking_debug',
                'diagnostic_reload',
                ]


    def _check_console_error(self, curr_status, message):
        if type(curr_status) is dict:
            if not curr_status:
                raise DiagnosticError(message + "\n" + \
                    'Directory curr_status: %s is empty.' % curr_status)
        else:
            if curr_status.lower().find(' error') > -1:
                raise DiagnosticError(message)


    def diagnostic_raid(self, action, confirm='yes', confirm_verify='yes'):
        """Disk Verify Utility.

        diagnostic > raid

        Parameters:
        - `action`: action to perform:
                    1.  Run disk verify
                    2.  Monitor tasks in progress
                    3.  Display disk verify verdict
                    4.  Check disk firmware
        - `confirm`: confirm raid usage (yes/no).
                     'yes' is default value.
        - `confirm_verify`: confirm disk verification
                            (yes/no) for 'Run disk verify'.
                            'yes' is default value.

        Exceptions:
        - DiagnosticError: if an error appears in CLI during diagnostic test.

        Examples:
        | Diagnostic Raid | action=Run disk verify | confirm=Yes | confirm_verify=Yes |
        """

        curr_status = self._cli.diagnostic().raid(action, confirm, confirm_verify)
        self._info(curr_status)
        self._check_console_error(curr_status, 'Error happened during RAID of diagnostic.')
        return curr_status

    def diagnostic_disk_usage(self):
        """Check Disk Usage.

        diagnostic > disk_usage

        Exceptions:
        - DiagnosticError: if an error appears in CLI during diagnostic test.

        Examples:
        | Diagnostic Disk Usage |
        """

        curr_status = self._cli.diagnostic().disk_usage()
        self._info(curr_status)
        self._check_console_error(curr_status, 'Error happened during Disk Usage of diagnostic.')
        return curr_status

    def diagnostic_network_flush(self):
        """Flush all network related caches.

        diagnostic > network > flush

        Exceptions:
        - DiagnosticError: if an error appears in CLI during diagnostic test.

        Examples:
        | Diagnostic Network Flush |
        """

        curr_status = self._cli.diagnostic().network().flush()
        self._info(curr_status)
        self._check_console_error(curr_status, 'Error happened during Flush of network diagnostic.')
        return curr_status

    def diagnostic_network_arpshow(self):
        """Show system ARP cache.

        diagnostic > network > arpshow

        Exceptions:
        - DiagnosticError: if an error appears in CLI during diagnostic test.

        Examples:
        | Diagnostic Network Arpshow |
        """

        curr_status = self._cli.diagnostic().network().arpshow()
        self._info(curr_status)
        self._check_console_error(curr_status, 'Error happened during ARPShow of network diagnostic.')
        return curr_status

    def diagnostic_network_ndpshow(self):
        """Show system NDP cache.

        diagnostic > network > ndpshow

        Exceptions:
        - DiagnosticError: if an error appears in CLI during diagnostic test.

        Examples:
        | Diagnostic Network Ndpshow |
        """

        curr_status = self._cli.diagnostic().network().ndpshow()
        self._info(curr_status)
        self._check_console_error(curr_status, 'Error happened during NDPShow of network diagnostic.')
        return curr_status

    def diagnostic_network_smtpping(self, hostname_or_ip='cisco.com',
                                        network_interface="1",
                                        send_email='yes',
                                        from_email_id='from@cisco.com',
                                        to_email_id='to@cisco.com',
                                        subject_message='Test Message',
                                        message_body='Test Body\r\n.'):
        """Test a remote SMTP server.

        diagnostic > network > smtpping

        Parameters:
        - `hostname_or_ip`: hostname or IP address of SMTP server.
        - `network_interface`: network interface number to use. '1' by default.
        - `send_email`: whether send e-mail. 'yes' by default.
        - `from_email_id`: sender e-mail address.
        - `to_email_id`: recipient e-mail address.
        - `subject_message`: e-mail subject string.
        - `message_body`: e-mail message body (must be finished by '\r\n.').

        Exceptions:
        - DiagnosticError: if an error occurs in CLI during diagnostic test.

        Examples:
        | Diagnostic Network Smtpping |
        | ... | hostname_or_ip=cisco.com |
        | ... | network_interface=1 |
        | ... | send_email=yes |
        | ... | from_email_id=from@cisco.com |
        | ... | to_email_id=to@cisco.com |
        | ... | subject_message=Test Message |
        | ... | message_body=Test Body\r\n. |
        """

        curr_status = self._cli.diagnostic().network().smtpping(
                            hostname_or_ip, network_interface, send_email,
                            from_email_id, to_email_id, subject_message, message_body)
        self._info(curr_status)
        self._check_console_error(
                curr_status,
                'An error occured during execution SMTPPING of network ' \
                'diagnostic command.')
        return curr_status

    def diagnostic_network_tcpdump_start(self):
        """Start dump ethernet packets.

        diagnostic > network > tcpdumpt > start

        Exceptions:
        - DiagnosticError: if an error appears in CLI during diagnostic test.

        Examples:
        | Diagnostic Network Tcpdump Start |
        """

        curr_status = self._cli.diagnostic().network().tcpdump().start()
        self._info(curr_status)
        self._check_console_error(curr_status, 'Error happened during starting tcpdump.')
        return curr_status

    def diagnostic_network_tcpdump_stop(self):
        """Stop dump ethernet packets.

        diagnostic > network > tcpdumpt > stop

        Exceptions:
        - DiagnosticError: if an error appears in CLI during diagnostic test.

        Returns:
        A dictionary containing below keys
        - file_name
        - file_size
        - duration
        - limit
        - interface
        - filter

        Examples:
        | ${diag_tcpdump_status}= | Diagnostic Network Tcpdump Stop |
        | Log Dictionary | ${diag_tcpdump_status} |
        | ${file_name}= | Get From Dictionary | ${diag_tcpdump_status} | file_name |
        | ${file_size}= | Get From Dictionary | ${diag_tcpdump_status} | file_size |
        """

        curr_status = self._cli.diagnostic().network().tcpdump().stop()
        self._info(curr_status)
        self._check_console_error(curr_status, 'Error happened during stopping tcpdump.')
        return curr_status

    def diagnostic_network_tcpdump_status(self):
        """Status of dump capturing.

        diagnostic > network > tcpdumpt > status

        Exceptions:
        - DiagnosticError: if an error appears in CLI during diagnostic test.

        Examples:
        | Diagnostic Network Tcpdump Status |
        """

        curr_status = self._cli.diagnostic().network().tcpdump().status()
        self._info(curr_status)
        self._check_console_error(curr_status, 'Error happened during tcpdump status.')
        return curr_status

    def diagnostic_network_tcpdump_setup(self,  max_size='', stop='yes', interface='',
            operation='', port='CLEAR', client_ip='CLEAR', server_ip='CLEAR', custom_filter=''):
        """Change packet capture settings.

        diagnostic > network > tcpdumpt > setup

        Parameters:
        - `max_size`: maximum allowable size for the capture file (in MB). 100 by default.
        - `stop`: stop the capture when the file size is reached(yes/no). 'yes' by default.
        - `interface`: interfaces to capture packets from. 'ALL' by default.
        - `operation`: filter operation (PREDEFINED, CUSTOM, CLEAR).
        - `port`: port(s) for PREDEFINED filter (comman-separated list or 'CLEAR' for all ports).
        - `client_ip`: Client IP(s) for PREDEFINED filter (comman-separated list or 'CLEAR' for all ports).
        - `server_ip`: Server IP(s) for PREDEFINED filter (comman-separated list or 'CLEAR' for all ports).
        - `custom_filter`: custom filter using tcpdump syntax for CUSTOM filter.

        Exceptions:
        - DiagnosticError: if an error appears in CLI during diagnostic test.

        Examples:
        | Diagnostic Network Tcpdump Setup | max_size=100 |
        | ... | stop=yes |
        | ... | interface=ALL |
        | ... | operation=PREDEFINED |
        | ... | port=CLEAR |
        | ... | client_ip=CLEAR |
        | ... | server_ip=CLEAR |
        | ... | custom_filter= |
        """

        curr_status = self._cli.diagnostic().network().tcpdump().setup(max_size,
            self._process_yes_no(stop), interface, operation, port, client_ip,
            server_ip, custom_filter)
        self._info(curr_status)
        self._check_console_error(curr_status, 'Error happened during tcpdump setup.')
        return curr_status

    def diagnostic_reporting_delete_db(self, confirm='no'):
        """Reinitialize the reporting database

        diagnostic > reporting > deletedb

        Parameters:
        - `confirm`: answer for confirmation question. Either 'yes' or 'no'.
        Default 'no'.

        Exceptions:
        - DiagnosticError: if an error appears in CLI during diagnostic test.

        Example:
        | Diagnostic Reporting Delete DB | confirm='no' |
        """

        curr_status = self._cli.diagnostic().reporting().deletedb(
            self._process_yes_no(confirm))
        self._info(curr_status)
        self._check_console_error(curr_status, 'Error happened during deleting db of reporting.')
        return curr_status

    def diagnostic_reporting_disable(self):
        """Disable the reporting system

        diagnostic > reporting > disable

        Exceptions:
        - DiagnosticError: if an error appears in CLI during diagnostic test.

        Example:
        | Diagnostic Reporting Disable |
        """

        curr_status = self._cli.diagnostic().reporting().disable()
        self._info(curr_status)
        self._check_console_error(curr_status, 'Error happened during disabling of reporting.')
        return curr_status

    def diagnostic_reporting_enable(self):
        """Enable the reporting system

        diagnostic > reporting > enable

        Exceptions:
        - DiagnosticError: if an error appears in CLI during diagnostic test.

        Example:
        | Diagnostic Reporting Enable |
        """

        curr_status = self._cli.diagnostic().reporting().enable()
        self._info(curr_status)
        self._check_console_error(curr_status, 'Error happened during enabling of reporting.')
        return curr_status

    def diagnostic_tracking_delete_db(self, confirm='no'):
        """Reinitialize the tracking database

        diagnostic > tracking > deletedb

        Parameters:
        - `confirm`: answer for confirmation question. Either 'yes' or 'no'.
        Default 'no'.

        Exceptions:
        - DiagnosticError: if an error appears in CLI during diagnostic test.

        Example:
        | Diagnostic Tracking Delete DB | confirm='no' |
        """

        curr_status = self._cli.diagnostic().tracking().deletedb(
            self._process_yes_no(confirm))
        self._info(curr_status)
        self._check_console_error(curr_status, 'Error happened during deleting db of tracking.')
        return curr_status

    def diagnostic_tracking_debug(self, confirm='no'):
        """Gather debug information.

        diagnostic > tracking > debug

        Parameters:
        - `confirm`: answer for confirmation question. Either 'yes' or 'no'.
        Default 'no'.

        Exceptions:
        - DiagnosticError: if an error appears in CLI during diagnostic test.

        Example:
        | Diagnostic Tracking Debug | confirm='yes' |
        """

        curr_status = self._cli.diagnostic().tracking().debug(
            self._process_yes_no(confirm))
        self._info(curr_status)
        self._check_console_error(curr_status, 'Error happened during tracking debug.')
        return curr_status

    def diagnostic_reload(self, confirm='no', confirm_verify='no', wipe='no'):
        """Reset configuration to the initial manufacturer values.

        diagnostic > reload

        Parameters:
        - `confirm`: answer for confirmation question. Either 'yes' or 'no'.
        Default 'no'.
        - `confirm_verify`: confirmation verification question. Either 'yes' or 'no'
        Default: 'no'
        - `wipe`: answer for wipe question. Either 'yes' or 'no'. Default: 'no'

        Exceptions:
        - DiagnosticError: if an error appears in CLI during diagnostic test.

        Example:
        | Diagnostic Reload | confirm='yes' |
        """

        curr_status = self._cli.diagnostic(self.dut, self.dut_version).reload(
            self._process_yes_no(confirm),
            self._process_yes_no(confirm_verify),
            self._process_yes_no(wipe))
        if curr_status:
            self._info(curr_status)
            self._check_console_error(curr_status, 'Error happened during diagnostic reload.')
            return curr_status
