#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1350/cli/keywords/log_config.py#1 $
# $DateTime: 2019/09/18 01:46:35 $
# $Author: sarukakk $

from common.cli.clicommon import (CliKeywordBase, DEFAULT)


class LogConfig(CliKeywordBase):
    """Keywords for logconfig CLI command."""

    def get_keyword_names(self):
        return ['log_config_new',
                'log_config_edit',
                'log_config_delete',
                'log_config_setup',
                'log_config_logheaders',
                'log_config_hostkeyconfig_new',
                'log_config_hostkeyconfig_edit',
                'log_config_hostkeyconfig_delete',
                'log_config_hostkeyconfig_print',
                'log_config_hostkeyconfig_scan',
                'log_config_hostkeyconfig_host',
                'log_config_hostkeyconfig_fingerprint',
                'log_config_hostkeyconfig_user',
                ]

    def _get_logconfig_dict(self, **kwargs):
        config_dict = {}

        available_arguments = ('log_file', 'name', 'log_level', 'bytes_bounce',
                               'domain', 'smtp_sessions', 'injection_ip', 'inj_sessions',
                               'retrieval', 'hostname', 'port', 'username', 'password',
                               'directory', 'filename', 'syslog_proto', 'facility', 'ssh_proto',
                               'ssh_host_key', 'scan_host_ssh_key', 'max_size', 'max_files',
                               'time_based_rollover', 'rollover_setting', 'interval', 'day',
                               'time', 'include_pwd',
                               'append_unique_id',
                               'unique_id',
                               )

        for key, value in kwargs.iteritems():
            if key not in available_arguments:
                raise ValueError('Wrong `%s` parameter name' % (key,))

            if value is not None:
                config_dict.update({key: value})

        return config_dict

    def log_config_new(self, *args):
        """Create new log.

        Parameters:
        General log options:
        - `name`: name for the log.
        - `log_file`: log file type to create.
        - `log_level`: log level.
        - `retrieval`: the method to retrieve the logs.
        - `filename`: filename to use for log files.
        - `time_based_rollover`: enable time-based log files rollover.
        - `rollover_setting`: interval for time-based rollover.
        - `interval`: custom time interval for time-based rollover.
        - `day`: the day of week to roll over the log files.
        - `time`: the time of day to rollover log files.
        - `max_size`: maximum file size.
        - `max_files`: maximum number of files.
        - `append_unique_id`: answer to question
        Would you like to append system based unique identifiers like
        $hostname, $serialnumber to the log filename?
        Accepted values: Y and N
        - `unique_id`: filename unique identifier format. You can specify
         system based parameters like $hostname or $serialnumber or both
         $hostname and $serialnumber, using "." as delimeter.
         Eg. $hostname.$serialnumber

        Log delivery options:
        - `hostname`: hostname to deliver logs to.
        - `port`: port to connect to on the remote host.
        - `username`: username on the remote host.
        - `password`: password on the remote host.
        - `directory`: directory on remote host to place logs.
        - `ssh_host_key`: enable host key checking.
        - `scan_host_ssh_key`: automatically scan the host for its SSH key or
           enter it manually.
        - `syslog_proto`: protocol to use for syslog push.
        - `facility`: facility for the log data to be sent as.

        Injection Debug Log options:
        - `injection_ip`: hostname, IP address or block of IP addresses for
           which to record injection debug information.
        - `inj_sessions`: the number of injection sessions you to record.

        Configuration History Log options:
        - `include_pwd`: include passwords.

        SMTP Conversation Log options:
        - `domain`: the domain for which to record debug information.
        - `smtp_sessions`: the number of SMTP sessions to record for the
           domain.

        Bounce Log options:
        - `bytes_bounce`: the number of bytes of the bounce message text you
           want to record.

        Exceptions:
        - `ValueError`: in case of any invalid parameter name.

        Examples:
        | Log Config New | name=my_log |
        | ... | append_unique_id=Y |
        | ... | unique_id=$hostname.$serialnumber |
        | Log Config New | name=conf_history_log_name |
        | ... | log_file=Configuration History | include_pwd=yes |
        | ... | retrieval=FTP Push | hostname=mail.qa |
        | ... | username=someuser | password=somepassword |
        | ... | directory=/home/user | filename=cf_files |
        | Log Config New  | name=ldap_debug_log | log_file=LDAP Debug |
        | ... | retrieval=SCP Push | hostname=mail.qa | port=123 |
        | ... | username=someuser | directory=/home/user |
        | ... | time_based_rollover=yes | rollover_setting=2 | day=1,5 |
        | ... | time=13:15 | max_size=50M | ssh_host_key=no |
        | Log Config New  | name=system_log | log_file=System |
        | ... | log_level=Critical | retrieval=Syslog Push |
        | ... | hostname=mail.qa | syslog_proto=UDP | facility=console |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.logconfig().new(self._get_logconfig_dict(**kwargs))

    def log_config_edit(self, log_to_edit, *args):
        """Edit log subscription.

        Parameters:
        General log options:
        - `log_to_edit`: name or number of the log subscription to edit.
        - `name`: name for the log.
        - `log_file`: log file type to create.
        - `log_level`: log level.
        - `retrieval`: the method to retrieve the logs.
        - `filename`: filename to use for log files.
        - `time_based_rollover`: enable time-based log files rollover.
        - `rollover_setting`: interval for time-based rollover.
        - `interval`: custom time interval for time-based rollover.
        - `day`: the day of week to roll over the log files.
        - `time`: the time of day to rollover log files.
        - `max_size`: maximum file size.
        - `max_files`: maximum number of files.
        - `append_unique_id`: answer to question
        Would you like to append system based unique identifiers like
        $hostname, $serialnumber to the log filename?
        Accepted values: Y and N
        - `unique_id`: filename unique identifier format. You can specify
         system based parameters like $hostname or $serialnumber or both
         $hostname and $serialnumber, using "." as delimeter.
         Eg. $hostname.$serialnumber

        Log delivery options:
        - `hostname`: hostname to deliver logs to.
        - `port`: port to connect to on the remote host.
        - `username`: username on the remote host.
        - `password`: password on the remote host.
        - `directory`: directory on remote host to place logs.
        - `ssh_host_key`: enable host key checking.
        - `scan_host_ssh_key`: automatically scan the host for its SSH key or
           enter it manually.
        - `syslog_proto`: protocol to use for syslog push.
        - `facility`: facility for the log data to be sent as.

        Injection Debug Log options:
        - `injection_ip`: hostname, IP address or block of IP addresses for
           which to record injection debug information.
        - `inj_sessions`: the number of injection sessions you to record.

        Configuration History Log options:
        - `include_pwd`: include passwords.

        SMTP Conversation Log options:
        - `domain`: the domain for which to record debug information.
        - `smtp_sessions`: the number of SMTP sessions to record for the
           domain.

        Bounce Log options:
        - `bytes_bounce`: the number of bytes of the bounce message text you
           want to record.

        Exceptions:
        - `ValueError`: in case of any invalid parameter name.

        Examples:
        | Log Config Edit | log_name |  name=new_name | log_level=Trace |
        | ... | retrieval=FTP Poll | time_based_rollover=yes |
        | ... | rollover_setting=1 | interval=3d | max_size=20M |
        | ... | max_files=20 |
        | ... | append_unique_id=N |
        | Log Config Edit | my_confhist_log_name | include_pwd=no |
        | ... | retrieval=FTP Poll | filename=new_name | max_files=35 |
        | Log Config Edit | mym_sys_log | log_level=Trace |
        | ... | retrieval=SCP Push | hostname=test.com | port=123 |
        | ... | username=username | directory=/home/user |
        | ... | time_based_rollover=no |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.logconfig().edit(log_to_edit,
                                   self._get_logconfig_dict(**kwargs))

    def log_config_delete(self, log_name):
        """Remove a log subscription.

        Parameters:
        - `log_name`: log name or log number to delete.

        Examples:
        | Log Config Delete | system_logs |
        | Log Config Delete | 2 |
        """
        self._cli.logconfig().delete(log_name)

    def log_config_setup(self, metrics_frequency=DEFAULT, log_msg_id=DEFAULT,
                         log_subject=DEFAULT, log_remote_resp=DEFAULT):
        """Edit general log settings.

        Parameters:
        - `metrics_frequency`: system metrics frequency in seconds.
        - `log_msg_id`: log Message-ID headers with mail logs.
        - `log_subject`: log the original subject header of each message.
        - `log_remote_resp`: log remote response text with mail logs.

        Examples:
        | Log Config Setup | 20 | yes | no | yes |
        | Log Config Setup | log_subject=yes |
        """
        self._cli.logconfig().setup(metrics_frequency,
                                    self._process_yes_no(log_msg_id),
                                    self._process_yes_no(log_subject),
                                    self._process_yes_no(log_remote_resp))

    def log_config_logheaders(self, headers):
        """Configure headers to log.

        Parameters:
        - `headers`: a string of comma-separated values of headers to record in
           the log files.

        Examples:
        | Log Config Logheaders | Date, X-Sender |
        | Log Config Logheaders | DELETE |
        """
        self._cli.logconfig().logheaders(headers)

    def log_config_hostkeyconfig_new(self, hosts, key):
        """Add new SSH host key.

        Parameters:
        - `hosts`: a string of comma-separated values of hostnames or IP
           addresses for the host key.
        - `key`: public SSH key for authorization.

        Examples:
        | Log Config Hostkeyconfig New | mail.qa | some_key |
        | Log Config Hostkeyconfig New | mail.qa, example.com |
        | ... | ssh_key_string |
        """
        self._cli.logconfig().hostkeyconfig().new(hosts, key)

    def log_config_hostkeyconfig_edit(self, key_num, hosts):
        """Modify host key.

        Parameters:
        - `key_num`: the number of the key to edit.
        - `hosts`: a string of comma-separated values of hostnames or IP
           addresses for the host key.

        Examples:
        | Log Config Hostkeyconfig Edit | 2 | example.com |
        """
        self._cli.logconfig().hostkeyconfig().edit(key_num, hosts)

    def log_config_hostkeyconfig_delete(self, key_num):
        """Delete SSH host key.

        Parameters:
        - `key_num`: the number of the key to delete.

        Examples:
        | Log Config Hostkeyconfig Delete | 1 |
        """
        self._cli.logconfig().hostkeyconfig().delete(key_num)

    def log_config_hostkeyconfig_scan(self, host, ssh_proto=DEFAULT,
                                      confirm_add=DEFAULT):
        """Download a host key.

        Parameters:
        - `host`: host or IP address to lookup.
        - `ssh_proto`: SSH protocol type.
        - `confirm_add`: confirm tha addition of the host key.

        Examples:
        | Log Config Hostkeyconfig Scan | mail.qa | SSH2:dsa | yes |
        | Log Config Hostkeyconfig Scan | mail.qa |
        """
        self._cli.logconfig().hostkeyconfig().scan(hostname=host,
                                                   ssh_proto=ssh_proto, add_keys=self._process_yes_no(confirm_add))

    def log_config_hostkeyconfig_print(self, key_num):
        """Display a key.

        Parameters:
        - `key_num`: the number of the key to display.

        Return:
        A value of the key.

        Examples:
        | ${key} = | Log Config Hostkeyconfig Print | 2 |
        """
        return self._cli.logconfig().hostkeyconfig().print_key(key_num)

    def log_config_hostkeyconfig_host(self):
        """Display system host keys.

        Return:
        Host keys of the appliance.

        Examples:
        | ${keys} = | Log Config Hostkeyconfig Host |
        """
        return self._cli.logconfig().hostkeyconfig().host()

    def log_config_hostkeyconfig_fingerprint(self):
        """Display system host key fingerprints.

        Return:
        Fingerprint of the host keys of the appliance.

        Examples:
        | ${fingerprints} = | Log Config Hostkeyconfig Fingerprint |
        """
        return self._cli.logconfig().hostkeyconfig().fingerprint()

    def log_config_hostkeyconfig_user(self):
        """Display system user keys.

        Return:
        User host keys of the appliance.

        Examples:
        | ${user_keys} = | Log Config Hostkeyconfig User |
        """
        return self._cli.logconfig().hostkeyconfig().user()
