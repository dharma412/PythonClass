#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/phoebe1210/cli/keywords/logconfig.py#1 $ $DateTime: 2019/05/07 03:16:10 $ $Author: bimmanue $

from common.cli.clicommon import CliKeywordBase


class logconfig(CliKeywordBase):
    """
    cli -> logconfig

    Configure log files.
    """

    def get_keyword_names(self):
        return ['log_config_new',
                'log_config_edit',
                'log_config_delete',
                'log_config_setup',
                'log_config_print',
                'log_config_log_headers',
                'log_config_host_key_config_new',
                'log_config_host_key_config_edit',
                'log_config_host_key_config_delete',
                'log_config_host_key_config_scan',
                'log_config_host_key_config_host',
                'log_config_host_key_config_print',
                'log_config_host_key_config_fingerprint',
                'log_config_host_key_config_user']

    def log_config_new(self, *args):
        """Create new log subscription

        logconfg -> new

        *Parameters:*
        - `log_file`: the log file type for this subscription:
        | 1 | IronPort Text Mail Logs |
        | 2 | qmail Format Mail Logs |
        | 3 | Delivery Logs |
        | 4 | Bounce Logs |
        | 5 | Status Logs |
        | 6 | Domain Debug Logs |
        | 7 | Injection Debug Logs |
        | 8 | SMTP Conversation Logs |
        | 9 | System Logs |
        | 10 | CLI Audit Logs |
        | 11 | FTP Server Logs |
        | 12 | HTTP Logs |
        | 13 | NTP logs |
        | 14 | LDAP Debug Logs |
        | 15 | Anti-Spam Logs |
        | 16 | Anti-Spam Archive |
        | 17 | Anti-Virus Logs |
        | 18 | Anti-Virus Archive |
        | 19 | Scanning Logs |
        | 20 | Encryption Logs |
        | 21 | Spam Quarantine Logs |
        | 22 | Spam Quarantine GUI Logs |
        | 23 | Reporting Logs |
        | 24 | Reporting Query Logs |
        | 25 | Updater Logs |
        | 26 | SNMP Logs |
        | 27 | Tracking Logs |
        | 28 | Safe/Block Lists Logs |
        | 29 | Authentication Logs |
        | 30 | Configuration History Logs |
        | 31 | Reputation Engine Logs |
        - `name`: the name for the log, mandatory
        - `log_level`: log level, either:
        | 1 | Critical |
        | 2 | Warning |
        | 3 | Information |
        | 4 | Debug |
        | 5 | Trace |
        - `bytes_bounce`: number of bytes of the bounce message,
        (only for "Bounce Logs")
        - `domain`: the name of the domain for which you want to
        record debug information (only for "Domain Debug Logs"),
        mandatory
        - `smtp_sessions`: the number of SMTP sessions you want
        to record for this hostname (only for "Domain debug logs")
        - `injection_ip`: the hostname, IP address or block of
        IP addresses for which you want to record injection debug information
        (only for "Injection Debug Logs"), mandatory
        - `inj_sessions`: the number of injection sessions you want
        to record for this hostname, IP address or block of IP addresses
        (only for "Injection Debug Logs"), mandatory
        - `retrieval`: the method to retrieve the logs, either:
        | 1 | Download Manually: FTP/HTTP(S)/SCP |
        | 2 | FTP Push |
        | 3 | SCP Push |
        | 4 | Syslog Push |
        - `hostname`: hostname to deliver the logs (for "... Push"
        retrieval type), mandatory
        - `port`: port to connect to on the remote host (for "SCP Push"
        retrieval type), 22 by default
        - `username`: username on the remote host (for "... Push"
        retrieval type), mandatory
        - `password`: password for username on the remote host (for "... Push"
        retrieval type), mandatory
        - `directory`: directory on remote host to place logs (for "... Push"
        retrieval type), mandatory
        - `filename`: filename to use for log files (for "Download Manually"
        retrieval type)
        param_map['max_time'] = ['Maximum time to wait', DEFAULT]
        - `syslog_proto`: which protocol do you want to use to transfer the
        log data (for "Syslog Push" retrieval type):
        | 1 | UDP |
        | 2 | TCP |
        - `facility`: which facility do you want the log data to be sent as
        (for "Syslog Push" retrieval type):
        | 1 | auth |
        | 2 | authpriv |
        | 3 | console |
        | 4 | daemon |
        | 5 | ftp |
        | 6 | local0 |
        | 7 | local1 |
        | 8 | local2 |
        | 9 | local3 |
        | 10 | local4 |
        | 11 | local5 |
        | 12 | local6 |
        | 13 | local7 |
        | 14 | mail |
        | 15 | ntp |
        | 16 | security |
        | 17 | user |
        - `ssh_proto`: SSH protocol (for "SCP Push" retrieval type),
        either:
        | 1 | SSH1 |
        | 2 | SSH2 |
        - `ssh_host_key`: whether you want to enable host key checking (for "SCP Push"
         retrieval type), yes or no
        - `scan_host_SSH_key`: whether you want to automatically scan the host
        for its SSH key, or enter it manually (for "SCP Push" retrieval type), either:
        | 1 | Automatically scan. |
        | 2 | Enter manually. |
        - `max_size_poll`: the maximum file size in bytes (for "Download Manually"
        retrieval type). You can specify suffixes: "m" for megabytes, "k"
        for kilobytes. Suffixes are case-insensitive
        - `max_size_push`: maximum filesize in bytes (for "... Push"
        retrieval type)
        - `max_files`: the maximum number of files (for "Download Manually"
        retrieval type), default is 10
        - `time_based_rollover`: whether to configure time-based log files rollover,
        either yes or no
        - `rollover_setting`: log rollover settings, either:
        | 1 | Custom time interval. |
        | 2 | Weekly rollover. |
        - `interval`: custom time interval in seconds (for "Custom time interval"
        rollover settings), 3600 by default
        - `day`: Choose the day of week to roll over the log files. Separate multiple
        days with comma, or use "*" to specify every day of a week. Also you can use
        dash to secify a range like "1-5":
        | 1 | Monday |
        | 2 | Tuesday |
        | 3 | Wednesday |
        | 4 | Thursday |
        | 5 | Friday |
        | 6 | Saturday |
        | 7 | Sunday |
        This parameter is mandatory for "Weekly rollover" setting.
        - `time`: the time of day to rollover log files in 24-hour format (HH:MM).
        You can specify hour as "*" to match every hour, the same for minutes.
        Separate multiple times of day with comma.
        This parameter is mandatory for "Weekly rollover" setting
        param_map['include_pass'] = ['include passwords', DEFAULT]
        - `alert`: whether to send an alert when files are removed due to the maximum
        number of files allowed (for "Download Manually" retrieval type), yes or no
        - `should_append_ids`: whether you like to append system based unique identifiers
        like $hostname, $serialnumber to the log filename. Either Yes or No
        - `ids_format`: the filename unique identifier format. You can specify system based
        parameters like $hostname or $serialnumber or both $hostname and $serialnumber,
        using "." as delimeter. Eg. $hostname.$serialnumber. Mandatory if `should_append_ids`
        is set to Yes

        *Examples:*
        | Log Config New | name=blah | log_file=Bounce Logs | retrieval=SCP Push |
        | ... | hostname=qa19.qa | username=dang | directory=/tmp/scp_push.qa |
        | ... | filename=blah | ssh_proto=1 | ssh_host_key=Yes |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.logconfig().new(**kwargs)

    def log_config_edit(self, log_to_edit, *args):
        """Edit existing log subscription

        logconfg -> edit

        *Parameters:*
        - `log_to_edit`: the log file number (taken from already configured logs list)
        - `log_file`: the log file type for this subscription:
        | 1 | IronPort Text Mail Logs |
        | 2 | qmail Format Mail Logs |
        | 3 | Delivery Logs |
        | 4 | Bounce Logs |
        | 5 | Status Logs |
        | 6 | Domain Debug Logs |
        | 7 | Injection Debug Logs |
        | 8 | SMTP Conversation Logs |
        | 9 | System Logs |
        | 10 | CLI Audit Logs |
        | 11 | FTP Server Logs |
        | 12 | HTTP Logs |
        | 13 | NTP logs |
        | 14 | LDAP Debug Logs |
        | 15 | Anti-Spam Logs |
        | 16 | Anti-Spam Archive |
        | 17 | Anti-Virus Logs |
        | 18 | Anti-Virus Archive |
        | 19 | Scanning Logs |
        | 20 | Encryption Logs |
        | 21 | Spam Quarantine Logs |
        | 22 | Spam Quarantine GUI Logs |
        | 23 | Reporting Logs |
        | 24 | Reporting Query Logs |
        | 25 | Updater Logs |
        | 26 | SNMP Logs |
        | 27 | Tracking Logs |
        | 28 | Safe/Block Lists Logs |
        | 29 | Authentication Logs |
        | 30 | Configuration History Logs |
        | 31 | Reputation Engine Logs |
        - `name`: the name for the log, mandatory
        - `log_level`: log level, either:
        | 1 | Critical |
        | 2 | Warning |
        | 3 | Information |
        | 4 | Debug |
        | 5 | Trace |
        - `bytes_bounce`: number of bytes of the bounce message,
        (only for "Bounce Logs")
        - `domain`: the name of the domain for which you want to
        record debug information (only for "Domain Debug Logs"),
        mandatory
        - `smtp_sessions`: the number of SMTP sessions you want
        to record for this hostname (only for "Domain debug logs")
        - `injection_ip`: the hostname, IP address or block of
        IP addresses for which you want to record injection debug information
        (only for "Injection Debug Logs"), mandatory
        - `inj_sessions`: the number of injection sessions you want
        to record for this hostname, IP address or block of IP addresses
        (only for "Injection Debug Logs"), mandatory
        - `retrieval`: the method to retrieve the logs, either:
        | 1 | Download Manually: FTP/HTTP(S)/SCP |
        | 2 | FTP Push |
        | 3 | SCP Push |
        | 4 | Syslog Push |
        - `hostname`: hostname to deliver the logs (for "... Push"
        retrieval type), mandatory
        - `port`: port to connect to on the remote host (for "SCP Push"
        retrieval type), 22 by default
        - `username`: username on the remote host (for "... Push"
        retrieval type), mandatory
        - `password`: password for username on the remote host (for "... Push"
        retrieval type), mandatory
        - `directory`: directory on remote host to place logs (for "... Push"
        retrieval type), mandatory
        - `filename`: filename to use for log files (for "Download Manually"
        retrieval type)
        param_map['max_time'] = ['Maximum time to wait', DEFAULT]
        - `syslog_proto`: which protocol do you want to use to transfer the
        log data (for "Syslog Push" retrieval type):
        | 1 | UDP |
        | 2 | TCP |
        - `facility`: which facility do you want the log data to be sent as
        (for "Syslog Push" retrieval type):
        | 1 | auth |
        | 2 | authpriv |
        | 3 | console |
        | 4 | daemon |
        | 5 | ftp |
        | 6 | local0 |
        | 7 | local1 |
        | 8 | local2 |
        | 9 | local3 |
        | 10 | local4 |
        | 11 | local5 |
        | 12 | local6 |
        | 13 | local7 |
        | 14 | mail |
        | 15 | ntp |
        | 16 | security |
        | 17 | user |
        - `ssh_proto`: SSH protocol (for "SCP Push" retrieval type),
        either:
        | 1 | SSH1 |
        | 2 | SSH2 |
        - `ssh_host_key`: whether you want to enable host key checking (for "SCP Push"
         retrieval type), yes or no
        - `scan_host_SSH_key`: whether you want to automatically scan the host
        for its SSH key, or enter it manually (for "SCP Push" retrieval type), either:
        | 1 | Automatically scan. |
        | 2 | Enter manually. |
        - `max_size_poll`: the maximum file size in bytes (for "Download Manually"
        retrieval type). You can specify suffixes: "m" for megabytes, "k"
        for kilobytes. Suffixes are case-insensitive
        - `max_size_push`: maximum filesize in bytes (for "... Push"
        retrieval type)
        - `max_files`: the maximum number of files (for "Download Manually"
        retrieval type), default is 10
        - `time_based_rollover`: whether to configure time-based log files rollover,
        either yes or no
        - `rollover_setting`: log rollover settings, either:
        | 1 | Custom time interval. |
        | 2 | Weekly rollover. |
        - `interval`: custom time interval in seconds (for "Custom time interval"
        rollover settings), 3600 by default
        - `day`: Choose the day of week to roll over the log files. Separate multiple
        days with comma, or use "*" to specify every day of a week. Also you can use
        dash to secify a range like "1-5":
        | 1 | Monday |
        | 2 | Tuesday |
        | 3 | Wednesday |
        | 4 | Thursday |
        | 5 | Friday |
        | 6 | Saturday |
        | 7 | Sunday |
        This parameter is mandatory for "Weekly rollover" setting.
        - `time`: the time of day to rollover log files in 24-hour format (HH:MM).
        You can specify hour as "*" to match every hour, the same for minutes.
        Separate multiple times of day with comma.
        This parameter is mandatory for "Weekly rollover" setting
        param_map['include_pass'] = ['include passwords', DEFAULT]
        - `alert`: whether to send an alert when files are removed due to the maximum
        number of files allowed (for "Download Manually" retrieval type), yes or no
        - `should_append_ids`: whether you like to append system based unique identifiers
        like $hostname, $serialnumber to the log filename. Either Yes or No
        - `ids_format`: the filename unique identifier format. You can specify system based
        parameters like $hostname or $serialnumber or both $hostname and $serialnumber,
        using "." as delimeter. Eg. $hostname.$serialnumber. Mandatory if `should_append_ids`
        is set to Yes

        *Examples:*
        | Log Config Edit | blah | name=blah1 | bytes_bounce=1000 | filename=blah |
        | ... | max_time=1000 | max_size_push=5242880 | ssh_host_key=No |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.logconfig().edit(log_to_edit, **kwargs)

    def log_config_delete(self, log_to_delete):
        """Delete existing log subscription

        logconfg -> delete

        *Parameters:*
        - `log_to_delete`: the existing log file number (taken from already
        configured logs list)

        *Examples:*
        | Log Config Delete | blah1 |
        """
        self._cli.logconfig().delete(log_to_delete)

    def log_config_setup(self, frequency='60', log_message_id='YES',
                         log_subj_header='YES', log_remote_resp='YES'):
        """Setup global parameters for log subscription

        logconfg -> setup

        *Parameters:*
        - `frequency`: system metrics frequency (seconds)
        - `log_message_id`: wheter you want to log Message-ID headers with
        mail logs, yes or no
        - `log_subj_header`: whether you want to log the original subject
        header of each message, yes or no
        - `log_remote_resp`: whther you want to log remote response text
        with mail logs, yes or no

        *Examples:*
        | Log Config Setup | frequency=120 | log_remote_resp=No |
        """
        self._cli.logconfig().setup(frequency, log_message_id,
                                    log_subj_header, log_remote_resp)

    def log_config_print(self):
        """Get current log config table as it is printed by logconfig
        CLI command

        *Examples:*
        | ${logs}= | Log Config Print |
        """
        return self._cli.logconfig().Print()

    def log_config_log_headers(self, headers):
        """Configure the list of headers you wish to record in the log files

        logconfg -> logheaders

        *Parameters:*
        - `headers`: the list of headers you wish to record in the log files.
        Separate multiple headers with commas.

        *Examples:*
        | Log Config Headers | X-blah1,X-blah2 |
        """
        self._cli.logconfig().logheaders(headers)

    def log_config_host_key_config_new(self, hostnames, ssh_key):
        """Add a new public SSH key for specified host(s)

        logconfg -> hostkeyconfig -> new

        *Parameters:*
        - `ssh_key`: the public SSH key for authorization.
        - `hostnames`: the hostnames or IP addresses for this host key.
        Separate the multiple entries with commas.

        *Examples:*
        | Log Config Host Key Config New | blah-host |
        | ... | (RSA/DSA SSH pubkey here) |
        """
        self._cli.logconfig().hostkeyconfig().new(hostnames,
                                                  ssh_key)

    def log_config_host_key_config_edit(self, key_num,
                                        hostnames):
        """Edit exisitng public SSH key

        logconfg -> hostkeyconfig -> edit

        *Parameters:*
        - `key_num`: the public key number, taken from the keys list
        - `hostnames`: the hostnames or IP addresses for this host key.
        Separate the multiple entries with commas.

        *Examples:*
        | Log Config Host Key Config Edit | 1 |
        | ... | blah-host |
        """
        self._cli.logconfig().hostkeyconfig().edit(key_num=key_num,
                                                   hostnames=hostnames)

    def log_config_host_key_config_delete(self, key_num):
        """Delete existing public SSH key

        logconfg -> hostkeyconfig -> delete

        *Parameters:*
        - `key_num`: the public key number, taken from the keys list

        *Examples:*
        | Log Config Host Key Config Delete | key_num=1 |
        """
        self._cli.logconfig().hostkeyconfig().delete(key_num=key_num)

    def log_config_host_key_config_scan(self, *args):
        """Automatically download a host key.

        logconfg -> hostkeyconfig -> scan

        *Parameters:*
        - `hostname`: the host or IP address to lookup, mandatory
        - `ssh_proto`: the ssh protocol type, either:
        | 1 | SSH1:rsa |
        | 2 | SSH2:rsa |
        | 3 | SSH2:dsa |
        | 4 | All |
        - `add_keys`: whether to add the preceding host key(s) to list, yes or no

        *Return:*
        Raw output - result of host key scanning

        *Examples:*
        | ${host_pubkeys}= | Log Config Host Key Config Scan | hostname=10.92.145.140 |
        | ... | add_keys=No |
        """
        kwargs = self._convert_to_dict(args)
        return self._cli.logconfig().hostkeyconfig().scan(**kwargs)

    def log_config_host_key_config_host(self):
        """Display system host keys

        logconfg -> hostkeyconfig -> host

        *Return:*
        Raw output - list of public SSH keys for current host

        *Examples:*
        | ${self_pubkeys}= | Log Config Host Key Config Host |
        | Log | ${self_pubkeys} |
        """
        return self._cli.logconfig().hostkeyconfig().host()

    def log_config_host_key_config_fingerprint(self):
        """Display system host key fingerprints

        logconfg -> hostkeyconfig -> fingerprints

        *Return:*
        Raw output - list of public SSH keys fingerprints for current host

        *Examples:*
        | ${self_fgprints}= | Log Config Host Key Config Fingerprint |
        | Log | ${self_fgprints} |
        """
        return self._cli.logconfig().hostkeyconfig().fingerprint()

    def log_config_host_key_config_user(self):
        """Display system user keys

        logconfg -> hostkeyconfig -> user

        *Return:*
        Raw output - list of public SSH keys for system user

        *Examples:*
        | ${user_keys}= | Log Config Host Key Config User |
        | Log | ${user_keys} |
        """
        return self._cli.logconfig().hostkeyconfig().user()

    def log_config_host_key_config_print(self, key_num):
        """Display a key

        logconfg -> hostkeyconfig -> print

        *Return:*
        Raw output - list of hosts for particular SSH pubkey

        *Examples:*
        | ${key1_host}= | Log Config Host Key Config Print | 1 |
        | Log | ${key1_host} |
        """
        return self._cli.logconfig().hostkeyconfig().Print(key_num=key_num)
