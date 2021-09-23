#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/cli/keywords/log_config.py#1 $

from common.cli.clicommon import CliKeywordBase

class LogConfig(CliKeywordBase):
    """
    cli -> logconfig

    Configure log files.

    """

    def get_keyword_names(self):
        return [
                'log_config_new',
                'log_config_edit',
                'log_config_delete',
                'log_config_hostkey_new',
                'log_config_hostkey_edit',
                'log_config_hostkey_delete',
                'log_config_hostkey_scan',
                'log_config_hostkey_host',
                'log_config_hostkey_print',
                'log_config_hostkey_fingerprint',
                'log_config_userkey_print',
                'log_config_auditlogconfig',
        ]

    def log_config_new(self,
       log_file = None,
       name = None,
       log_level = None,
       retrieval = None,
       hostname = None,
       username = None,
       password = None,
       directory = None,
       filename = None,
       configure_rollover = None,
       settings = None,
       interval = None,
       day_of_week = None,
       time_of_day = None,
       max_size_poll = None,
       max_files = None,
       max_size_push = None,
       ssh_proto = None,
       key_checking = None,
       ssh_scan = None,
       host_key = None,
       alert_when_rollover_files_removed = None,
       compress = None,
       log_style = None,
       http_codes = None,
       transfer_protocol = None,
       msg_size = None,
       facility = None,
       syslog_disk_buffer = None,
       modules = None,
       requests = None,
       criteria = None,
       ip = None,
       domain = None,
       format_string = None,
        ):
        """Create a new log subscription

        logconfig -> new

        Parameters:

        - `log_file` : numeric value of log type.
           Answer to prompt 'Choose the log file type for this subscription:'

        - `name` : name of the log.
           Answer to prompt 'Please enter the name for the log:'

        - `log_level` : 1=Critical, 2=Warning, 3=Information, 4=Debug,
           5=Trace.
           Answer to prompt 'Log level:'

        - `retrieval` : 1=FTP Poll, 2=FTP Push, 3=SCP Push, 4=Syslog Push
           Answer to prompt 'Choose the method to retrieve the logs:'

        - `hostname` : for retrieval methods FTP Push and SCP Push.
           Answer to prompt 'Hostname to deliver the logs:'

        - `username` : for retrieval methods FTP Push and SCP Push.
           Answer to prompt 'Username on the remote host:'

        - `password` : for retrieval methods FTP Push and SCP Push.
           Answer to prompt 'Password for <username>:'

        - `directory` : for retrieval methods FTP Push and SCP Push.
           Answer to prompt 'Directory on remote host to place logs:'

         - `filename :
           Answer to prompt 'Filename to use for log files:'

        - `configure_rollover` : 'y' or 'n'
           Answer to prompt 'Do you want to configure time-based log files
           rollover?'

        - `settings` : 1=Custom time interval.
           2=Weekly rollover.
           3=Daily rollover.
           Answer to prompt 'Configure log rollover settings:'

        - `interval` : Custom time interval
           The rollover interval must be a time interval between 1s and 12d
           (1 - 1036800).  Bare numbers are interpreted as seconds, suffix
           numbers with 'd', 'h', or 'm' as days, hours, or minutes,
           respectively.
           Answer to prompt 'Enter an interval:'

        - `day_of_week` : 1=Monday, 2=Tuesday, 3=Wednesday, 4=Thursday
           5=Friday, 6=Saturday, 7=Sunday
           Answer to prompt 'Choose the day of week to roll over the log
           files.  Separate multiple days with comma, or use "*" to specify
           every day of a week.  Also you can use dash to specify a
           range like "1-5":'

        - `time_of_day :
           Answer to prompt 'Enter the time of day to rollover log files in
           24-hour format (HH:MM).  You can specify hour as "*" to match every
           hour, the same for minutes.  Separate multiple times of day with
           comma:'

        - `max_size_poll` : Value must be an integer in bytes from 100K to 10G.
           Answer to prompt 'Please enter the maximum file size:'

        - `max_files` :
           Answer to prompt 'Please enter the maximum number of files:'

        - `max_size_push` : Value must be an integer in bytes from 100K to 10G.
           Answer to prompt 'Maximum filesize before transferring:'

        - `ssh_proto` : 1=SSH1, 2=SSH2.
           Answer to prompt 'Protocol:'

        - `key_checking` : 'y' or 'n'.
           Answer to prompt 'Do you want to enable host key checking?'

        - `ssh_scan` :
           Answer to prompt 'Do you want to automatically scan the host for
           its SSH key, or enter it manually? 1=Automatically scan.
           2=Enter manually.'

        - `host_key` :
           Answer to prompt 'Enter the public SSH host key for a.s.
           Press enter on a blank line to finish.

        - `alert_when_rollover_files_removed` :
           Answer to prompt 'Should an alert be sent when files are removed
           due to the maximum number of files allowed?'

        - `compress` : 'yes' or 'no'
           Answer to prompt 'Do you want to compress logs (yes/no)'

        parameters for 4. Access Logs
        - `log_style` : 1=Squid, 2=Apache, 3=Squid Details
           Answer to prompt 'Choose the log style for this subscription:'

        - `http_codes` : Enter the HTTP Error Status codes (comma separated
           list of 4xx and 5xx. The HTTP Status codes should be of the form
           4xx(400 - 417) and 5xx(500 - 505).
           Answer to prompt 'Enter the HTTP Error Status codes'

        # parameters for Syslog Push
        - `transfer_protocol` : 1=UDP, 2=TCP
           Answer to prompt 'Which protocol do you want to use to transfer the
            log data?',

        - `msg_size` :
           Answer to prompt 'Maximum message size for ssyslog push:'

        - `facility` :
           1=auth, 2=authpriv, 3=console, 4=daemon, 5=ftp, 6=local0, 7=local1,
           8=local2, 9=local3, 10=local4, 11=local5, 12=local6, 13=local7,
           14=mail, 15=ntp, 16=security, 17=user
           Answer to prompt 'Which facility do you want the log data to be sent
            as?'

        - `syslog_disk_buffer' : yes, no, or None
           answer to question Enable syslog disk buffer (yes/no)

        # parameters for 35. Request Debug Logs
        - `modules` :
           Choose modules where enhanced request logging is to be performed.
           Multiple selections can be made in the form of a comma separated or
           range list (e.g. 1,3,4 or 3-7)
           1=Default Proxy, 2=Access Control Engine, 3=Configuration,
           4=Disk Manager, 5=Memory Manager, 6=McAfee Integration Framework,
           7=Sophos Integration Framework, 8=Webroot Integration Framework,
           9=Webcat Integration Framework, 10=Connection Management,
           11=Authentication Framework, 12=HTTPS, 13=FTP proxy,
           14=WCCP Module, 15=License Module

        - `requests` : Value must be an integer from 1 to 10,000
           Answer to prompt 'Please enter the number of requests for which to
            perform enhanced logging',

        - `criteria` : 1=Client IP Address,
           2=Destination Domain, 3=Destination IP Address
           Answer to prompt 'Choose the request criteria for logging:'

        - `ip` : valid IP address.
           Answer to prompt 'Specify source IP address'

        - `domain` :
           Answer to prompt 'Specify target domain'

        # parameters for 48. W3C Logs
        - `format_string` :
           Answer to prompt 'Enter the format string:'

        Examples:
        | Create a new log subscription |
        | | Log Config Add |
        | | ... | log_file=23 |
        | | ... | name=a01 |
        | | ... | log_level=1 |
        | | ... | retrieval=1 |
        | | ... | filename=bbb |
        | | ... | configure_rollover=y |
        | | ... | settings=1 |
        | | ... | interval=10d |
        | | ... | max_size_poll=10000000000 |
        | | ... | max_files=3 |
        | | ... | alert_when_rollover_files_removed=yes |
        | | ... | compress=no |

        """
        dict = self._drop_none_values(locals())
        self._info('dict=' + str(dict))
        return self._cli.logconfig().new (**dict)

    def log_config_edit(self,
       log_to_edit,
       name = None,
       log_level = None,
       retrieval = None,
       hostname = None,
       username = None,
       password = None,
       directory = None,
       filename = None,
       configure_rollover = None,
       settings = None,
       interval = None,
       day_of_week = None,
       time_of_day = None,
       max_size_poll = None,
       max_files = None,
       max_size_push = None,
       ssh_proto = None,
       key_checking = None,
       ssh_scan = None,
       host_key = None,
       alert_when_rollover_files_removed = None,
       compress = None,
       log_style = None,
       http_codes = None,
       transfer_protocol = None,
       msg_size = None,
       facility = None,
       syslog_disk_buffer = None,
       modules = None,
       requests = None,
       criteria = None,
       ip = None,
       domain = None,
       format_string = None,
        ):
        """Modify a new subscription

        logconfig -> edit

        Parameters:

        - `log_to_edit` : numeric value of log type.
           Answer to prompt 'Enter the number of the log you wish to edit:'

        - `name` : name of the log.
           Answer to prompt 'Please enter the name for the log:'

        - `log_level` : 1=Critical, 2=Warning, 3=Information, 4=Debug,
           5=Trace.
           Answer to prompt 'Log level:'

        - `retrieval` : 1=FTP Poll, 2=FTP Push, 3=SCP Push, 4=Syslog Push
           Answer to prompt 'Choose the method to retrieve the logs:'

        - `hostname` : for retrieval methods FTP Push and SCP Push.
           Answer to prompt 'Hostname to deliver the logs:'

        - `username` : for retrieval methods FTP Push and SCP Push.
           Answer to prompt 'Username on the remote host:'

        - `password` : for retrieval methods FTP Push and SCP Push.
           Answer to prompt 'Password for <username>:'

        - `directory` : for retrieval methods FTP Push and SCP Push.
           Answer to prompt 'Directory on remote host to place logs:'

        - `filename :
           Answer to prompt 'Filename to use for log files:'

        - `configure_rollover` : 'y' or 'n'
           Answer to prompt 'Do you want to configure time-based log files
           rollover?'

        - `settings` : 1=Custom time interval.
           2=Weekly rollover.
           3=Daily rollover.
           Answer to prompt 'Configure log rollover settings:'

        - `interval` : Custom time interval
           The rollover interval must be a time interval between 1s and 12d
           (1 - 1036800).  Bare numbers are interpreted as seconds, suffix
           numbers with 'd', 'h', or 'm' as days, hours, or minutes,
           respectively.
           Answer to prompt 'Enter an interval:'

        - `day_of_week` : 1=Monday, 2=Tuesday, 3=Wednesday, 4=Thursday
           5=Friday, 6=Saturday, 7=Sunday
           Answer to prompt 'Choose the day of week to roll over the log
           files.  Separate multiple days with comma, or use "*" to specify
           every day of a week.  Also you can use dash to specify a
           range like "1-5":'

        - `time_of_day :
           Answer to prompt 'Enter the time of day to rollover log files in
           24-hour format (HH:MM).  You can specify hour as "*" to match every
           hour, the same for minutes.  Separate multiple times of day with
           comma:'

        - `max_size_poll` : Value must be an integer in bytes from 100K to 10G.
           Answer to prompt 'Please enter the maximum file size:'

        - `max_files` :
           Answer to prompt 'Please enter the maximum number of files:'

        - `max_size_push` : Value must be an integer in bytes from 100K to 10G.
           Answer to prompt 'Maximum filesize before transferring:'

        - `ssh_proto` : 1=SSH1, 2=SSH2.
           Answer to prompt 'Protocol:'

        - `key_checking` : 'y' or 'n'.
           Answer to prompt 'Do you want to enable host key checking?'

        - `ssh_scan` :
           Answer to prompt 'Do you want to automatically scan the host for
           its SSH key, or enter it manually? 1=Automatically scan.
           2=Enter manually.'

        - `host_key` :
           Answer to prompt 'Enter the public SSH host key for a.s.
           Press enter on a blank line to finish.

        - `alert_when_rollover_files_removed` :
           Answer to prompt 'Should an alert be sent when files are removed
           due to the maximum number of files allowed?'

        - `compress` : 'yes' or 'no'
           Answer to prompt 'Do you want to compress logs (yes/no)'

        parameters for 4. Access Logs
        - `log_style` : 1=Squid, 2=Apache, 3=Squid Details
           Answer to prompt 'Choose the log style for this subscription:'

        - `http_codes` : Enter the HTTP Error Status codes (comma separated
           list of 4xx and 5xx. The HTTP Status codes should be of the form
           4xx(400 - 417) and 5xx(500 - 505).
           Answer to prompt 'Enter the HTTP Error Status codes'

        # parameters for Syslog Push
        - `transfer_protocol` : 1=UDP, 2=TCP
           Answer to prompt 'Which protocol do you want to use to transfer the
            log data?',

        - `msg_size` :
           Answer to prompt 'Maximum message size for ssyslog push:'

        - `facility` :
           1=auth, 2=authpriv, 3=console, 4=daemon, 5=ftp, 6=local0, 7=local1,
           8=local2, 9=local3, 10=local4, 11=local5, 12=local6, 13=local7,
           14=mail, 15=ntp, 16=security, 17=user
           Answer to prompt 'Which facility do you want the log data to be sent
            as?'

        - `syslog_disk_buffer' : yes, no, or None
           answer to question Enable syslog disk buffer (yes/no)

        # parameters for 35. Request Debug Logs
        - `modules` :
           Choose modules where enhanced request logging is to be performed.
           Multiple selections can be made in the form of a comma separated or
           range list (e.g. 1,3,4 or 3-7)
           1=Default Proxy, 2=Access Control Engine, 3=Configuration,
           4=Disk Manager, 5=Memory Manager, 6=McAfee Integration Framework,
           7=Sophos Integration Framework, 8=Webroot Integration Framework,
           9=Webcat Integration Framework, 10=Connection Management,
           11=Authentication Framework, 12=HTTPS, 13=FTP proxy,
           14=WCCP Module, 15=License Module

        - `requests` : Value must be an integer from 1 to 10,000
           Answer to prompt 'Please enter the number of requests for which to
            perform enhanced logging',

        - `criteria` : 1=Client IP Address,
           2=Destination Domain, 3=Destination IP Address
           Answer to prompt 'Choose the request criteria for logging:'

        - `ip` : valid IP address.
           Answer to prompt 'Specify source IP address'

        - `domain` :
           Answer to prompt 'Specify target domain'

        # parameters for 48. W3C Logs
        - `format_string` :
           Answer to prompt 'Enter the format string:'

        Examples:
        | Modify the new subscription |
        | | Log Config Edit |
        | | ... | 1 |
        | | ... | name=a002 |
        | | ... | log_level=2 |
        | | ... | retrieval=2 |
        | | ... | hostname=qq.aa |
        | | ... | username=guest |
        | | ... | password=guess |
        | | ... | directory=/history |
        | | ... | filename=xxx |
        | | ... | configure_rollover=y |
        | | ... | settings=2 |
        | | ... | day_of_week=1-5 |
        | | ... | time_of_day=23:23 |
        | | ... | max_size_push=123456789 |
        | | ... | compress=yes |

        """
        dict = self._drop_none_values(locals())
        return self._cli.logconfig().edit (**dict)

    def log_config_delete(self, log_to_delete):
        """ Remove a log subscription

        logconfig -> delete

        Parameters:

        - `log_to_delete : numeric value of the log to delete
           Answer to prompt 'Enter the number of the log you wish to delete:'

        Examples:
        | Remove the subscription |
        | | Log Config Delete | 1 |
        """
        return self._cli.logconfig().delete(log_to_delete)

    def log_config_hostkey_new(self, hostname, ssh_key):
        """ Configure SSH host keys. Add a new key.

        logconfig -> HOSTKEYCONFIG -> NEW

        Parameters:

        - `hostname :
           Answer to prompt:
           'Enter the hostnames and IP addresses for this host key.
            Separate the multiple entries with commas:'

        - `ssh_key` : ssh_key.
           Answer to prompt:
           'Please enter the public SSH key for authorization:
            Press enter on a blank line to finish.'

        Examples:
        | *** Settings *** |
        | Library   | WsaCliLibrary |
        | Variables | constants.py  |
        | Configure SSH host keys. Add a new key |
        | | Log Config Hostkey Add           |
        | | ... | www.google.com, 1.2.3.4        |
        | | ... | ${ssh_keys.PUBLIC_KEY}         |
        """
        return self._cli.logconfig().hostkeyconfig().new \
            (hostname, ssh_key)

    def log_config_hostkey_edit(self, key_num, hosts):
        """ Configure SSH host keys. Modify a key.

        logconfig -> HOSTKEYCONFIG -> EDIT

        Parameters:

        - `key_num : Value must be a positive integer.
           Answer to prompt:
           'Enter the number of the key you wish to edit:'

        - `hosts` :
           Answer to prompt:
          'Enter the hostnames and IP addresses for this host key.
            Separate the multiple entries with commas.'

        Examples:

        | Configure SSH host keys. Modify a key |
        | | Log Config Hostkey Edit |
        | | ... | 1 |
        | | ... | 3.3.3.3 |
        """
        return self._cli.logconfig().hostkeyconfig().edit \
            (key_num, hosts)

    def log_config_hostkey_delete(self, key_num):
        """ Configure SSH host keys. Remove a key.

        logconfig -> HOSTKEYCONFIG -> DELETE

        Parameters:

        - `key_num : Value must be a positive integer.
           Answer to prompt:
           'Enter the number of the key you wish to edit:'

        Examples:

        | Configure SSH host keys. Modify a key |
        | | Log Config Hostkey Delete |
        | | ... | 1 |
        """
        return self._cli.logconfig().hostkeyconfig().delete \
            (key_num)

    def log_config_hostkey_scan(self, hostnames, ssh_proto, add_keys='n'):
        """ Configure SSH host keys. Automatically download a host key

        logconfig -> HOSTKEYCONFIG -> SCAN

        Parameters:

        - `hostname : name or IP address of the host
           Answer to prompt 'Please enter the host or IP address to lookup:'

        - `ssh_proto : ssh protocol. 1=SSH1:rsa, 2=SSH2:rsa, 3=SSH2:dsa, 4=All
           Answer to prompt 'Choose the ssh protocol type:'

        - `add_keys : 'y' or 'n'
           Answer to prompt 'Add the preceding host'

        Examples:
        | Configure SSH host keys. Automatically download a host key |
        | | ${result}= | Log Config Hostkey Scan |
        | | ... | ${DUT} |
        | | ... | 4 |
        | | ... | y |
        | | LOG | ${result} |
        """
        return self._cli.logconfig().hostkeyconfig().scan \
            (hostnames, ssh_proto, add_keys)

    def log_config_hostkey_print(self, key_num):
        """Configure SSH host keys. Display a key.

        logconfig -> HOSTKEYCONFIG -> PRINT

        Parameters: None
        - `key_num : Value must be a positive integer.
           Answer to prompt: 'Enter the number of the key you wish to print:'
        Examples:
        | Configure SSH host keys. Display a key. |
        | | ${result}= | Log Config Hostkey Print | 1 |
        | | Log | ${result} |

        """
        return self._cli.logconfig().hostkeyconfig()._print(key_num)

    def log_config_hostkey_host(self):
        """Configure SSH host keys. Return system host keys

        logconfig -> HOSTKEYCONFIG -> HOST

        Parameters: None

        Examples:
        | Configure SSH host keys. Return system host keys |
        | | ${result}= | Log Config Hostkey Host |
        | | Log | ${result} |

        """
        return self._cli.logconfig().hostkeyconfig().host()

    def log_config_hostkey_fingerprint(self):
        """Configure SSH host keys. Return system host key fingerprints

        logconfig -> HOSTKEYCONFIG -> FINGERPRINT

        Parameters: None

        Examples:
        | Configure SSH host keys. Return system host key fingerprints |
        | | ${result}= | Log Config Hostkey Print |
        | | Log | ${result} |

        """
        return self._cli.logconfig().hostkeyconfig().fingerprint()

    def log_config_userkey_print(self):
        """Configure SSH host keys. Return system user keys

        logconfig -> HOSTKEYCONFIG -> USER

        Parameters: None

        Examples:
        | Configure SSH host keys. Return system user keys |
        | | ${result}= | Log Config Userkey Print |
        | | Log | ${result} |
        """
        return self._cli.logconfig().hostkeyconfig().user()

    def _drop_none_values(self, dic):
        """
        Filters a dictionary by removing None values and 'self' key
        """
        result = {}
        for s in dic.keys():
            if dic[s] is not None and s != 'self':
                result[s] = str(dic[s])

        return result

    def log_config_auditlogconfig(self,
        backups = '',
        loadable = '',
        ):
        """
        Adjust settings for audit logging

        logconfig -> auditlogconfig

        Parameters:

        - `backups` : number of auto generated configuration backup files
         to keep between 0 (none) and 100
        - `loadable`: configuration backup files should be loadable.
         Either 'yes' or 'no'

        Examples:
        Log Config AuditLogConfig
        ...    backups=99
        ...    loadable=yes
        """
        loadable_list = ('yes', 'no')
        if loadable:
            if not (loadable in loadable_list):
                raise ValueError(loadable + \
                ' should be in ' + str(loadable_list))
        return self._cli.logconfig().auditlogconfig(backups, loadable)
