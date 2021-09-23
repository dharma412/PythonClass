#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1380/cli/keywords/diagnostic.py#2 $ $DateTime: 2020/05/28 03:18:30 $ $Author: mrmohank $

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
                'diagnostic_services_reporting',
                'diagnostic_services_tracking',
                'diagnostic_services_euqweb',
                'diagnostic_services_webui',
                'diagnostic_services_smartlicense',
                ]


    def _check_console_error(self, curr_status, message):
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

    def diagnostic_network_arpshow(self):
        """Show system ARP cache.

        diagnostic > network > flush

        Exceptions:
        - DiagnosticError: if an error appears in CLI during diagnostic test.

        Examples:
        | Diagnostic Network Arpshow |
        """

        curr_status = self._cli.diagnostic().network().arpshow()
        self._info(curr_status)
        self._check_console_error(curr_status, 'Error happened during ARPShow of network diagnostic.')

    def diagnostic_network_smtpping(self, hostname_or_ip = 'aol.com', network_interface = "1",
            select_mx_host = 'yes', mx_host = "2", send_email = 'no',
            from_email_id = 'from@aol.com', to_email_id = 'to@aol.com',
            subject_message = 'Test Message', message_body = 'test Body\r\n.'):
        """Test a remote SMTP server.

        diagnostic > network > smtpping

        Parameters:
        - `hostname_or_ip`: hostname or IP address of SMTP server ('aol.com' by default).
        - `network_interface`: network interface to use
                               1. Management
                               2. auto
                               ("1" by default)
        - `select_mx_host`: need to select MX host (yes/no). 'yes' by default.
        - `mx_host`: MX host from received list. "2" by default.
        - `send_email`: need to send test e-mail message (yes/no). 'no' by default.
        - `from_email_id`: Froim e-mail address. 'from@aol.com' by default.
        - `to_email_id`: To e-mail address. 'to@aol.com' by default.
        - `subject_message`: Subject of test e-mail message. 'Test Message'by default.
        - `message_body`: Body of test e-mail message (Must be finished by '\r\n.'). 'test Body\r\n.' by default.

        Exceptions:
        - DiagnosticError: if an error appears in CLI during diagnostic test.

        Examples:
        | Diagnostic Network Smtpping | hostname_or_ip=aol.com |
        | ... | network_interface=1 |
        | ... | select_mx_host=yes |
        | ... | mx_host=2 |
        | ... | send_email=yes |
        | ... | from_email_id=from@aol.com |
        | ... | to_email_id=to@aol.com |
        | ... | subject_message=Test Message |
        | ... | message_body=test Body\r\n. |
        """

        curr_status = self._cli.diagnostic().network().smtpping(hostname_or_ip, network_interface,
            select_mx_host, mx_host, send_email, from_email_id, to_email_id, subject_message, message_body )
        self._info(curr_status)
        self._check_console_error(curr_status, 'Error happened during SMTPPing of network diagnostic.')

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

    def diagnostic_network_tcpdump_stop(self):
        """Stop dump ethernet packets.

        diagnostic > network > tcpdumpt > stop

        Exceptions:
        - DiagnosticError: if an error appears in CLI during diagnostic test.

        Examples:
        | Diagnostic Network Tcpdump Stop |
        """

        curr_status = self._cli.diagnostic().network().tcpdump().stop()
        self._info(curr_status)
        self._check_console_error(curr_status, 'Error happened during stopping tcpdump.')

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

    def diagnostic_network_tcpdump_setup(self,  max_size='', stop='yes', interface='',
            operation='', port='CLEAR', client_ip='CLEAR', server_ip='CLLEAR', custom_filter=''):
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
        | ... | server_ip=CLLEAR |
        | ... | custom_filter= |
        """

        curr_status = self._cli.diagnostic().network().tcpdump().setup(max_size,
            self._process_yes_no(stop), interface, operation, port, client_ip,
            server_ip, custom_filter)
        self._info(curr_status)
        self._check_console_error(curr_status, 'Error happened during tcpdump setup.')

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

    def diagnostic_reload(self, confirm='no',wipedata='no'):
        """Reset configuration to the initial manufacturer values.

        diagnostic > reload

        Parameters:
        - `confirm`: answer for confirmation question. Either 'yes' or 'no'.
        Default 'no'.

        Exceptions:
        - DiagnosticError: if an error appears in CLI during diagnostic test.

        Example:
        | Diagnostic Reload | confirm='yes' |
        """

        curr_status = self._cli.diagnostic().reload(self._process_yes_no(confirm),self._process_yes_no(wipedata))
        self._info(curr_status)
        self._check_console_error(curr_status, 'Error happened during diagnostic reload.')

    def diagnostic_services_reporting(self, operation):
        """Perform Diagnostic services status check - Reporting.

                diagnostic > services > reporting

                Applicable Parameters:
                - `operation`: status
                - `operation`: restart

                Exceptions:
                - DiagnosticError: if an error appears in CLI during diagnostic test.

                Example:
                | Diagnostic Services Reporting | operation=status |
                | Diagnostic Services Reporting | operation=restart |
                """

        curr_status = self._cli.diagnostic().services().reporting(operation)
        self._info(curr_status)
        self._check_console_error(curr_status, 'Error happened during diagnostic services reporting.')
        return curr_status

    def diagnostic_services_tracking(self, operation):
        """Perform Diagnostic services status check - Tracking.

                diagnostic > services > tracking

                Applicable Parameters:
                - `operation`: status
                - `operation`: restart

                Exceptions:
                - DiagnosticError: if an error appears in CLI during diagnostic test.

                Example:
                | Diagnostic Services Tracking | operation=status |
                | Diagnostic Services Tracking | operation=restart |
                """

        curr_status = self._cli.diagnostic().services().tracking(operation)
        self._info(curr_status)
        self._check_console_error(curr_status, 'Error happened during diagnostic services tracking.')
        return curr_status

    def diagnostic_services_euqweb(self, operation):
        """Perform Diagnostic services status check - EUQWEB.

                diagnostic > services > euqweb

                Applicable Parameters:
                - `operation`: status
                - `operation`: restart

                Exceptions:
                - DiagnosticError: if an error appears in CLI during diagnostic test.

                Example:
                | Diagnostic Services Euqweb | operation=status |
                | Diagnostic Services Euqweb | operation=restart |
                """

        curr_status = self._cli.diagnostic().services().euqweb(operation)
        self._info(curr_status)
        self._check_console_error(curr_status, 'Error happened during diagnostic services euqweb.')
        return curr_status

    def diagnostic_services_webui(self, operation):
        """Perform Diagnostic services status check - WebUI.

                diagnostic > services > webui

                Applicable Parameters:
                - `operation`: status
                - `operation`: restart

                Exceptions:
                - DiagnosticError: if an error appears in CLI during diagnostic test.

                Example:
                | Diagnostic Services Webui | operation=status |
                | Diagnostic Services Webui | operation=restart |
                """

        curr_status = self._cli.diagnostic().services().webui(operation)
        self._info(curr_status)
        self._check_console_error(curr_status, 'Error happened during diagnostic services webui.')
        return curr_status

    def diagnostic_services_smartlicense(self, operation):
        """Perform Diagnostic services status check - Smart License.

                diagnostic > services > smart_license

                Applicable Parameters:
                - `operation`: status
                - `operation`: restart

                Exceptions:
                - DiagnosticError: if an error appears in CLI during diagnostic test.

                Example:
                | Diagnostic Services Smartlicense | operation=status |
                | Diagnostic Services Smartlicense | operation=restart |
                """

        curr_status = self._cli.diagnostic().services().smart_license(operation)
        self._info(curr_status)
        self._check_console_error(curr_status, 'Error happened during diagnostic services smart license.')
        return curr_status
