#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1380/cli/keywords/interface_config.py#1 $ $DateTime: 2020/05/25 00:19:30 $ $Author: sarukakk $
from common.cli.clicommon import CliKeywordBase, DEFAULT
class InterfaceConfig(CliKeywordBase):
    """Interface Configuration."""
    def get_keyword_names(self):
        return [
                'interface_config_new',
                'interface_config_edit',
                'interface_config_delete',
                'interface_config_groups_new',
                'interface_config_groups_edit',
                'interface_config_groups_delete',
                ]
    def interface_config_new(self,
                             if_name=DEFAULT,
                             address=DEFAULT,
                             ethernet=DEFAULT,
                             hostname=DEFAULT,
                             netmask=DEFAULT,
                             ftp_enable=DEFAULT,
                             telnet_enable=DEFAULT,
                             ssh_enable=DEFAULT,
                             http_enable=DEFAULT,
                             https_enable=DEFAULT,
                             ftp_port=DEFAULT,
                             telnet_port=DEFAULT,
                             ssh_port=DEFAULT,
                             http_port=DEFAULT,
                             https_port=DEFAULT,
                             spamhttp_enable=DEFAULT,
                             spamhttp_port=DEFAULT,
                             spamhttps_enable=DEFAULT,
                             spamhttps_port=DEFAULT,
                             demo_cert=DEFAULT,
                             http_redirection=DEFAULT,
                             spamhttp_redirection=DEFAULT,
                             spam_default=DEFAULT,
                             spam_custom=DEFAULT,
                             spam_custom_url=DEFAULT,
                             ):
        """Create a new interface.
        ifconfig > new
        Parameters:
        - `if_name`: interface name.
        - `address`: interface IP address. Must be 4 numbers separated by a period.
                Each number must be a value from 0 to 255.
        - `ethernet`: ethernet interface. Either 'Management', 'Data 1' or 'Data 2'.
        - `hostname`: a hostname value for specified interface.
        - `netmask`: netmask for interface address. Must be a dotted octet
                (255.255.255.0) or a hexadecimal (0xffffff00) value.
        - `ftp_enable`: enable or disable ftp for the interface.
                Either 'Yes' or 'No'.
        - `ftp_port`: ftp port value.
        - `telnet_enable`: enable or disable telnet for the interface.
                Either 'Yes' or 'No'.
        - `telnet_port`: telnet port value.
        - `ssh_enable`: enable or disable ssh for the interface.
                Either 'Yes' or 'No'.
        - `ssh_port`: ssh port value.
        - `http_enable`: enable or disable http for the interface.
                Either 'Yes' or 'No'.
        - `http_port`: http port value.
        - `https_enable`: enable or disable https for the interface.
                Either 'Yes' or 'No'.
        - `https_port`: https port value.
        - `spamhttp_enable`: enable or disable Spam Quarantine http for the interface.
                Either 'Yes' or 'No'.
        - `spamhttp_port`: Spam Quarantine http port value.
        - `spamhttps_enable`: enable or disable Spam Quarantine https for the interface.
                Either 'Yes' or 'No'.
        - `spamhttps_port`: Spam Quarantine https port value.
        - `demo_cert`: use demo certificate or disable https for moment.
        - `http_redirection`: should HTTP requests redirect to the secure
                service or no. Either 'Yes' or 'No'.
        - `spamhttp_redirection`: should Spam Quarantine HTTP requests redirect to the secure
                service or no. Either 'Yes' or 'No'.
        - `spam_default`: should the interface be default for Spam Quarantine.
                Either 'Yes' or 'No'.
        - `spam_custom`: use a custom base URL in your Spam Quarantine email notifications.
                Either 'Yes' or 'No'.
        - `spam_custom_url`: the custom base URL in your Spam Quarantine email notifications.
                (Ex: "http://isq.example.url:81/")
        Examples:
        | Interface Config New |
        | ... | if_name=test |
        | ... | address=192.168.1.5 |
        | ... | netmask=255.255.255.0 |
        | ... | ethernet=management |
        | ... | hostname=test.com |
        | ... | ftp_enable=yes |
        | ... | ftp_port=21 |
        | ... | telnet_enable=yes |
        | ... | telnet_port=23 |
        | ... | ssh_enable=yes |
        | ... | ssh_port=22 |
        | ... | http_enable=yes |
        | ... | http_port=8080 |
        | ... | https_enable=no |
        | ... | spamhttp_enable=yes |
        | ... | spamhttp_port=82 |
        | ... | spamhttps_enable=yes |
        | ... | spamhttps_port=83 |
        | ... | spamhttp_redirection=yes |
        | ... | spam_default=yes |
        | ... | spam_custom=yes |
        | ... | spam_custom_url=http://isq.example.url:81/ |
        | Interface Config New |
        | ... | if_name=test1 |
        | ... | address=10.7.8.130 |
        | ... | netmask=255.255.255.0 |
        | ... | ethernet=1 |
        | ... | hostname=test1.com |
        """
        kwargs = {
                  'if_name': if_name,
                  'address': address,
                  'ethernet': ethernet,
                  'netmask': netmask,
                  'hostname': hostname,
                  'FTP': self._process_yes_no(ftp_enable),
                  'Telnet': self._process_yes_no(telnet_enable),
                  'SSH': self._process_yes_no(ssh_enable),
                  'HTTP': self._process_yes_no(http_enable),
                  'HTTPS': self._process_yes_no(https_enable),
                  'EUQ_HTTP': self._process_yes_no(spamhttp_enable),
                  'EUQ_HTTPS': self._process_yes_no(spamhttps_enable),
                  'use_def_ipas': self._process_yes_no(spam_default),
                  'use_custom_url': self._process_yes_no(spam_custom),
                  }
        if ftp_enable.strip().lower() == 'yes':
            kwargs['FTP_port'] = ftp_port
        if telnet_enable.strip().lower() == 'yes':
            kwargs['Telnet_port'] = telnet_port
        if ssh_enable.strip().lower() == 'yes':
            kwargs['SSH_port'] = ssh_port
        if http_enable.strip().lower() == 'yes':
            kwargs['HTTP_port'] = http_port
        if https_enable.strip().lower() == 'yes':
            kwargs['HTTPS_port'] = https_port
            kwargs['use_demo_cert'] = demo_cert
        if http_enable.strip().lower() == 'yes' and\
                 https_enable.strip().lower() == 'yes':
            kwargs['HTTP_redirect'] = self._process_yes_no(http_redirection)
        if spamhttp_enable.strip().lower() == 'yes' and\
                 spamhttps_enable.strip().lower() == 'yes':
            kwargs['EUQ_redirect'] = self._process_yes_no(spamhttp_redirection)
        if spam_custom.strip().lower() == 'yes':
            kwargs['custom_url'] = spam_custom_url
        self._cli.interfaceconfig().new(**kwargs)
    def interface_config_delete(self,
                                if_name=DEFAULT,
                                filter_confirm=DEFAULT,
                                current_confirm=DEFAULT,
                                group_confirm=DEFAULT,
                                omh_choice=DEFAULT,
                                omh_new=DEFAULT,
                                altsrchost_choice=DEFAULT,
                                altsrchost_new=DEFAULT,
                                dns_choice=DEFAULT,
                                dns_new=DEFAULT,
                                SNMP_choice=DEFAULT,
                                SNMP_new=DEFAULT,
                                listener_choice=DEFAULT,
                                listener_new=DEFAULT,
                                tcp_port=DEFAULT,
                                NTP_choice=DEFAULT,
                                NTP_new=DEFAULT,
                                cluster_choice=DEFAULT,
                                cluster_new=DEFAULT,
                                upgrade_choice=DEFAULT,
                                upgrade_new=DEFAULT,
                                smtpauth_choice=DEFAULT,
                                smtpauth_new=DEFAULT,
                                ):
        """Remove an interface.
        interfaceconfig > delete
        Parameters:
        - `if_name`: interface name to be deleted.
        - `filter_confirm`: confirm if referenced by one or more filters. Either 'Yes' or 'No'.
        - `current_confirm`: confirm if logged into. Either 'Yes' or 'No'.
        - `group_confirm`: confirm if one or more IP groups use it. Either 'Yes' or 'No'.
        - `omh_choice`:  must change outgoing mail configuration for management interface.
                Values either 'Delete' (Disable outgoing mail on this interface),
                'Change' (Choose a new interface), 'Ignore' (Leave the
                outgoing mail interface (The service will not be
                available until you add a new interface with the same name or change the settings).
        - `omh_new`: choose a new interface to use for outgoing mail.
                Must be used when omh_choice is set to 'Change'.
        - `altsrchost_choice`: must change Virtual Gateway for management interface.
                Values either 'Delete' (Disable the service on this interface),
                'Change' (Choose a new interface), 'Ignore' (Leave the interface
                for the service (The service will not be available until you add
                a new interface with the same name or change the settings).
        - `altsrchost_new`: new interface for Virtual Gateway.
                Must be used when choice option is set to 'Change'.
        - `dns_choice`: must change DNS traffic for management interface.
                Values either 'Delete' (Disable the service on this interface),
                'Change' (Choose a new interface), 'Ignore' (Leave the interface
                for the service (The service will not be available until you add
                a new interface with the same name or change the settings).
        - `dns_new`: new interface for DNS traffic.
                Must be used when choice option is set to 'Change'.
        - `snmp_choice`: must change snmp configuration for management interface.
                Values either 'Delete' (Disable SNMP on this interface),
                'Change' (Choose a new interface), 'Ignore' (Leave the
                SNMP interface set to "Management" (SNMP will not be
                available until you add a new interface named "Management"
                or change the SNMP settings).
        - `snmp_new`: choose a new interface to use for SNMP (P1 or P2).
                Must be used when snmp is set to 'Change'.
        - `listener_choice`: must change listener interface.
                Values either 'Delete' (Disable the service on this interface),
                'Change' (Choose a new interface), 'Ignore' (Leave the interface
                for the service (The service will not be available until you add
                a new interface with the same name or change the settings).
        - `listener_new`: new interface for listener.
                Must be used when choice option is set to 'Change'.
        - `tcp_port`: enter the TCP port.
                Must be used when choice option of listener is set to 'Change'.
        - `NTP_choice`: must change NTP queries interface.
                Values either 'Delete' (Disable the service on this interface),
                'Change' (Choose a new interface), 'Ignore' (Leave the interface
                for the service (The service will not be available until you add
                a new interface with the same name or change the settings).
        - `NTP_new`: new interface for NTP traffic.
                Must be used when omh_choice is set to 'Change'.
        - `cluster_choice`: must change cluster interface.
                Values either 'Delete' (Disable the service on this interface),
                'Change' (Choose a new interface), 'Ignore' (Leave the interface
                for the service (The service will not be available until you add
                a new interface with the same name or change the settings).
        - `cluster_new`: new interface for the route.
                Must be used when omh_choice is set to 'Change'.
        - `upgrade_choice`: must change upgrades interface.
                Values either 'Delete' (Disable the service on this interface),
                'Change' (Choose a new interface), 'Ignore' (Leave the interface
                for the service (The service will not be available until you add
                a new interface with the same name or change the settings).
        - `upgrade_new`: new interface for upgrades.
                Must be used when omh_choice is set to 'Change'.
        - `smtpauth_choice`: must change SMTP Authentication interface.
                Values either 'Delete' (Disable the service on this interface),
                'Change' (Choose a new interface), 'Ignore' (Leave the interface
                for the service (The service will not be available until you add
                a new interface with the same name or change the settings).
        - `smtpauth_new`: new interface for SMTP Auth.
                Must be used when omh_choice is set to 'Change'.
        Example:
        | Interface Config Delete | if_name=test |
        """
        choices = {
                 'delete': 1,
                 'change': 2,
                 'ignore': 3
                 }
        kwargs = {
                  'if_name': if_name.strip(),
                  }
        if filter_confirm != '':
            kwargs['filter_confirm'] = filter_confirm
        if current_confirm !='':
            kwargs['current_confirm'] = current_confirm
        if group_confirm !='':
            kwargs['group_confirm'] = group_confirm
        if omh_choice in choices.keys():
            kwargs['omh_choice'] = choices[omh_choice.split().lower()]
            if kwargs['omh_choice'] == 2:
                kwargs['omh_new'] = omh_new
        if altsrchost_choice in choices.keys():
            kwargs['altsrchost_choice'] = choices[altsrchost_choice.split().lower()]
            if kwargs['altsrchost_choice'] == 2:
                kwargs['altsrchost_new'] = altsrchost_new
        if dns_choice in choices.keys():
            kwargs['dns_choice'] = choices[dns_choice.split().lower()]
            if kwargs['dns_choice'] == 2:
                kwargs['dns_new'] = dns_new
        if listener_choice in choices.keys():
            kwargs['listener_choice'] = choices[listener_choice.split().lower()]
            if kwargs['listener_choice'] == 2:
                kwargs['listener_new'] = listener_new
                kwargs['tcp_port'] = tcp_port
        if NTP_choice in choices.keys():
            kwargs['NTP_choice'] = choices[NTP_choice.split().lower()]
            if kwargs['NTP_choice'] == 2:
                kwargs['NTP_new'] = NTP_new
        if cluster_choice in choices.keys():
            kwargs['cluster_choice'] = choices[cluster_choice.split().lower()]
            if kwargs['cluster_choice'] == 2:
                kwargs['cluster_new'] = cluster_new
        if upgrade_choice in choices.keys():
            kwargs['upgrade_choice'] = choices[upgrade_choice.split().lower()]
            if kwargs['upgrade_choice'] == 2:
                kwargs['upgrade_new'] = upgrade_new
        if smtpauth_choice in choices.keys():
            kwargs['smtpauth_choice'] = choices[smtpauth_choice.split().lower()]
            if kwargs['smtpauth_choice'] == 2:
                kwargs['smtpauth_new'] = smtpauth_new
        if SNMP_choice in choices.keys():
            kwargs['SNMP_choice'] = choices[SNMP_choice.split().lower()]
            if kwargs['SNMP_choice'] == 2:
                kwargs['SNMP_new'] = SNMP_new.strip()
        self._cli.interfaceconfig().delete(**kwargs)
    def interface_config_edit(self,
                             if_name=DEFAULT,
                             new_name=DEFAULT,
                             address=DEFAULT,
                             ethernet=DEFAULT,
                             hostname=DEFAULT,
                             netmask=DEFAULT,
                             ftp_enable=DEFAULT,
                             telnet_enable=DEFAULT,
                             ssh_enable=DEFAULT,
                             http_enable=DEFAULT,
                             https_enable=DEFAULT,
                             ftp_port=DEFAULT,
                             telnet_port=DEFAULT,
                             ssh_port=DEFAULT,
                             http_port=DEFAULT,
                             https_port=DEFAULT,
                             spamhttp_enable=DEFAULT,
                             spamhttp_port=DEFAULT,
                             spamhttps_enable=DEFAULT,
                             spamhttps_port=DEFAULT,
                             demo_cert=DEFAULT,
                             http_redirection=DEFAULT,
                             spamhttp_redirection=DEFAULT,
                             spam_default=DEFAULT,
                             spam_custom=DEFAULT,
                             spam_custom_url=DEFAULT,
                             asyncos_confirm=DEFAULT,
                             asyncos_https=DEFAULT,
                             asyncos_port=DEFAULT,
                             asyncoshttps_port=DEFAULT
                             ):
        """Edit an interface.
        ifconfig > edit
        Parameters:
        - `if_name`: name of an interface to edit.
        - `new_name`: new name of the interface.
        - `address`: interface IP address. Must be 4 numbers separated by a period.
                Each number must be a value from 0 to 255.
        - `ethernet`: ethernet interface. Either 'Management', 'Data 1' or 'Data 2'.
        - `hostname`: a hostname value for specified interface.
        - `netmask`: netmask for interface address. Must be a dotted octet
                (255.255.255.0) or a hexadecimal (0xffffff00) value.
        - `ftp_enable`: enable or disable ftp for the interface.
                Either 'Yes' or 'No'.
        - `ftp_port`: ftp port value.
        - `telnet_enable`: enable or disable telnet for the interface.
                Either 'Yes' or 'No'.
        - `telnet_port`: telnet port value.
        - `ssh_enable`: enable or disable ssh for the interface.
                Either 'Yes' or 'No'.
        - `ssh_port`: ssh port value.
        - `http_enable`: enable or disable http for the interface.
                Either 'Yes' or 'No'.
        - `http_port`: http port value.
        - `https_enable`: enable or disable https for the interface.
                Either 'Yes' or 'No'.
        - `https_port`: https port value.
        - `spamhttp_enable`: enable or disable Spam Quarantine http for the interface.
                Either 'Yes' or 'No'.
        - `spamhttp_port`: Spam Quarantine http port value.
        - `spamhttps_enable`: enable or disable Spam Quarantine https for the interface.
                Either 'Yes' or 'No'.
        - `spamhttps_port`: Spam Quarantine https port value.
        - `demo_cert`: use demo certificate or disable https for moment.
        - `http_redirection`: should HTTP requests redirect to the secure
                service or no. Either 'Yes' or 'No'.
        - `spamhttp_redirection`: should Spam Quarantine HTTP requests redirect to the secure
                service or no. Either 'Yes' or 'No'.
        - `spam_default`: should the interface be default for Spam Quarantine.
                Either 'Yes' or 'No'.
        - `spam_custom`: use a custom base URL in your Spam Quarantine email notifications.
                Either 'Yes' or 'No'.
        - `spam_custom_url`: the custom base URL in your Spam Quarantine email notifications.
                (Ex: "http://isq.example.url:81/")
        Examples:
        | Interface Config Edit |
        | ... | if_name=test |
        | ... | new_name=test1 |
        | ... | address=192.168.1.5 |
        | ... | netmask=255.255.255.0 |
        | ... | ethernet=management |
        | ... | hostname=test.com |
        | ... | ftp_enable=yes |
        | ... | ftp_port=21 |
        | ... | telnet_enable=yes |
        | ... | telnet_port=23 |
        | ... | ssh_enable=yes |
        | ... | ssh_port=22 |
        | ... | http_enable=yes |
        | ... | http_port=8080 |
        | ... | https_enable=no |
        | ... | spamhttp_enable=yes |
        | ... | spamhttp_port=82 |
        | ... | spamhttps_enable=yes |
        | ... | spamhttps_port=83 |
        | ... | spamhttp_redirection=yes |
        | ... | spam_default=yes |
        | ... | spam_custom=yes |
        | ... | spam_custom_url=http://isq.example.url:81/ |
        """
        kwargs = {
                  'if_name': if_name,
                  'address': address,
                  'ethernet': ethernet,
                  'netmask': netmask,
                  'hostname': hostname,
                  'FTP': self._process_yes_no(ftp_enable),
                  'SSH': self._process_yes_no(ssh_enable),
                  'HTTP': self._process_yes_no(http_enable),
                  'HTTPS': self._process_yes_no(https_enable),
                  'EUQ_HTTP': self._process_yes_no(spamhttp_enable),
                  'EUQ_HTTPS': self._process_yes_no(spamhttps_enable),
                  'use_def_ipas': self._process_yes_no(spam_default),
                  'asyncos_confirm': self._process_yes_no(asyncos_confirm),
                  'asyncos_https': self._process_yes_no(asyncos_https),
                  }
        if if_name != 'Management':
            kwargs['new_name'] = new_name
        if ftp_enable.strip().lower() == 'yes':
            kwargs['FTP_port'] = ftp_port
        if ssh_enable.strip().lower() == 'yes':
            kwargs['SSH_port'] = ssh_port
        if http_enable.strip().lower() == 'yes':
            kwargs['HTTP_port'] = http_port
        if https_enable.strip().lower() == 'yes':
            kwargs['HTTPS_port'] = https_port
            kwargs['use_demo_cert'] = demo_cert
        if http_enable.strip().lower() == 'yes' and\
                 https_enable.strip().lower() == 'yes':
            kwargs['HTTP_redirect'] = self._process_yes_no(http_redirection)
        if spamhttp_enable.strip().lower() == 'yes' and\
                 spamhttps_enable.strip().lower() == 'yes':
            kwargs['EUQ_redirect'] = self._process_yes_no(spamhttp_redirection)
        if spam_default.strip().lower() == 'yes':
            kwargs['use_custom_url'] = use_custom_url
            if spam_custom.strip().lower() == 'yes':
                kwargs['custom_url'] = spam_custom_url
        if asyncos_confirm.strip().lower() == 'yes':
            kwargs['asyncos_port'] = asyncos_port
        if asyncos_https.strip().lower() == 'yes':
            kwargs['asyncoshttps_port'] = asyncoshttps_port
        self._cli.interfaceconfig().edit(**kwargs)
    def interface_config_groups_new(self,
                             group_name=DEFAULT,
                             if_list=DEFAULT,
                            ):
        """Create a new group of interfaces.
        ifconfig > groups > new
        Parameters:
        - `group_name`: group name.
        - `if_list`: name or number of the interfaces to be included in this group.
                Items should be separated by commas or specified as a range with a dash.
        Examples:
        | Interface Config Groups New |
        | ... | group_name=test |
        | ... | if_list=1,2 |
        """
        kwargs = {
                  'group_name': group_name,
                  'if_list': if_list,
                 }
        self._cli.interfaceconfig().groups().new(**kwargs)
    def interface_config_groups_edit(self,
                             group_name=DEFAULT,
                             new_name=DEFAULT,
                             if_list=DEFAULT,
                             filter_confirm=DEFAULT
                             ):
        """Edit a group of interfaces.
        ifconfig > groups > edit
        Parameters:
        - `group_name`: group name.
        - `new_name`: new name for the group.
        - `if_list`: name or number of the interfaces to be included in this group.
                Items should be separated by commas or specified as a range with a dash.
        - `filter_confirm`: confrim editing if it is used by a filter. Either 'Yes' or 'No'.
        Examples:
        | Interface Config Groups Edit |
        | ... | group_name=test |
        | ... | new_name=test1 |
        | ... | if_list=1,2 |
        """
        kwargs = {
                  'group_name': group_name.strip(),
                  'new_name': new_name,
                  'if_list': if_list,
                 }
        if filter_confirm != '':
            kwargs['filter_confirm']= self._process_yes_no(filter_confirm)
        self._cli.interfaceconfig().groups().edit(**kwargs)
    def interface_config_groups_delete(self,
                                group_name=DEFAULT,
                                filter_confirm=DEFAULT,
                                omh_choice=DEFAULT,
                                omh_new=DEFAULT,
                                altsrchost_choice=DEFAULT,
                                altsrchost_new=DEFAULT,
                               ):
        """Remove a group of interfaces.
        ifconfig > delete
        Parameters:
        - `group_name`: name of group to be deleted.
        Example:
        | Interface Config Delete | group_name=test |
        """
        kwargs = {
                  'group_name': group_name.strip(),
                  }
        if filter_confirm != '':
            kwargs['filter_confirm']= self._process_yes_no(filter_confirm)
        if omh_choice != '':
            kwargs['omh_choice']= omh_choice
            kwargs['omh_new']= omh_new
        if altsrchost_choice != '':
            kwargs['altsrchost_choice']= altsrchost_choice
            kwargs['altsrchost_new']= altsrchost_new
        self._cli.interfaceconfig().groups().delete(**kwargs)
