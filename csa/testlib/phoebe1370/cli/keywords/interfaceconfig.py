#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1350/cli/keywords/interfaceconfig.py#1 $ $DateTime: 2020/01/06 01:25:43 $ $Author: saurgup5 $

from common.cli.clicommon import CliKeywordBase

class Interfaceconfig(CliKeywordBase):
    """
    cli -> interfaceconfig

    Class designed to provide keywords for ESA interfaceconfig command.
    """

    def get_keyword_names(self):
        return [
                'interfaceconfig_new',
                'interfaceconfig_edit',
                'interfaceconfig_delete',
                'interfaceconfig_groups_new',
                'interfaceconfig_groups_edit',
                'interfaceconfig_groups_delete',
                'interfaceconfig_get_details'
               ]


    def interfaceconfig_new(self, *args):
        """
        This is used to create a new interface

        interfaceconfig -> new

        *Parameters*
        - `if_name`: specify a name for the IP interface
        - `configure_ipv4`: configure an IPv4 address. Either 'yes' or 'no'
        - `address`: specify the IPv4 address
        - `netmask`: specify the netmask for the IPv4 address
        - `configure_ipv6`: configure an IPv6 address. Either 'yes' or 'no'
        - `ipv6_address`: specify the IPv6 address
        - `prefix_length`: specify the prefix length for the IPv6 address
        - `ethernet`: specify the ethernet interface to be used
        - `hostname`: specify the hostname
        - `FTP`: enable FTP. Either 'yes' or 'no'
        - `FTP_port`: specify port to be used for FTP
        - `Telnet`: enable Telnet. Either 'yes' or 'no'
        - `Telnet_port`: specify port to be used for Telnet
        - `SSH`: enable SSH. Either 'yes' or 'no'
        - `SSH_port`: specify port to be used for SSH
        - `ccs`: enable Cluster
        - `ccs_port`: specify port to be used for Cluster
        - `HTTP`: enable HTTP. Either 'yes' or 'no'
        - `HTTP_port`: specify port to be used for HTTP
        - `HTTPS`: enable HTTPS. Either 'yes' or 'no'
        - `HTTPS_port`: specify port to be used for HTTPS
        - `EUQ_HTTP`: enable Spam Quarantine HTTP. Either 'yes' or 'no'
        - `EUQ_HTTP_port`: specify port to be used for Spam Quarantine HTTP
        - `EUQ_HTTPS`: enable Spam Quarantine HTTPS. Either 'yes' or 'no'
        - `EUQ_HTTPS_port`: specify port to be used for Spam Quarantine HTTPS
        - `use_demo_cert`: use a demo certificate. Either 'yes' or 'no'
        - `cert_to_use`: the name of certificate profile to be used for the
        interface. Applicable only if there are more than one certificate
        installed on appliance and `use_demo_cert` is set to 'no'.
        "Demo" by default
        - `confirm_demo_use`: whether to use Demo certificate for the
        particular listener or not. Mandatory only if `cert_to_use` is set to
        "Demo" and there are more than one certificate installed.
        Either 'yes' or 'no'
        - `HTTP_redirect`: redirect HTTP requests to the secure service
        - `EUQ_redirect`: redirect Spam Quarantine HTTP requests to the
          secure service
        - `use_def_ipas`: use this interface as default interface for Spam
          Quarantine. Either 'yes' or 'no'
        - `use_custom_base_url`: use custom base URL in your Spam Quarantine
          email notifications. Either 'yes' or 'no'
        - `custom_base_url`: specify the custom base URL
          (Ex: "http://isq.example.url:81/")
        - `RSA_Manager`: whether to enable ESA Enterprise manager feature
        for this interface. Either 'yes' or 'no'
        - `api_http`: enable REST API HTTP. Either 'yes' or 'no'
        - `api_http_port`: specify port to be used for REST API HTTP.
        - `api_https`: enable REST API HTTPS. Either 'yes' or 'no'
        - `api_https_port`: specify port to be used for REST API HTTPS.

        *Examples*:
        | Interfaceconfig New | if_name=test_intf1 | configure_ipv4=yes |
        | ... | ethernet=management | hostname=test.com | FTP=yes |
        | ... | FTP_port=21 | Telnet=yes | Telnet_port=23 | SSH=yes |
        | ... | SSH_port=22 | HTTP=yes | HTTP_port=8080 | HTTPS=yes |
        | ... | EUQ_HTTP=yes | EUQ_HTTP_port=${Empty} | EUQ_HTTPS=yes |
        | ... | api_http=yes | api_http_port=8080 |
        | ... | api_https=yes | api_https_port=8443 |
        | ... | HTTP_redirect=yes | EUQ_redirect=yes | use_def_ipas=yes |
        | ... | use_custom_base_url=yes | address=10.76.68.12 |
        | ... | custom_base_url=http://isq.example.url:81/ |
        | Interfaceconfig New | if_name=test_intf3 | configure_ipv4=no |
        | ... | configure_ipv6=yes | ethernet=Data 1 |
        | ... | hostname=testdomain6.com |
        | ... | ipv6_address=fe80::222:19ff:fe26:e3bf |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.interfaceconfig().new(**kwargs)

    def interfaceconfig_edit(self, if_name, *args):
        """
        This is used to edit an interface settings

        interfaceconfig -> edit

        *Parameters*
        - `if_name`: specify name of the interface to be edited
        - `new_name`: specify new name of the interface
        - `configure_ipv4`: configure an IPv4 address. Either 'yes' or 'no'
        - `address`: specify the IPv4 address
        - `netmask`: specify the netmask for the IPv4 address
        - `configure_ipv6`: configure an IPv6 address. Either 'yes' or 'no'
        - `ipv6_address`: specify the IPv6 address
        - `prefix_length`: specify the prefix length for the IPv6 address
        - `ethernet`: specify the ethernet interface to be used
        - `hostname`: specify the hostname
        - `FTP`: enable FTP. Either 'yes' or 'no'
        - `FTP_port`: specify port to be used for FTP
        - `Telnet`: enable Telnet. Either 'yes' or 'no'
        - `Telnet_port`: specify port to be used for Telnet
        - `SSH`: enable SSH. Either 'yes' or 'no'
        - `SSH_port`: specify port to be used for SSH
        - `ccs`: enable Cluster
        - `ccs_port`: specify port to be used for Cluster
        - `HTTP`: enable HTTP. Either 'yes' or 'no'
        - `HTTP_port`: specify port to be used for HTTP
        - `HTTPS`: enable HTTPS. Either 'yes' or 'no'
        - `HTTPS_port`: specify port to be used for HTTPS
        - `EUQ_HTTP`: enable Spam Quarantine HTTP. Either 'yes' or 'no'
        - `EUQ_HTTP_port`: specify port to be used for Spam Quarantine HTTP
        - `EUQ_HTTPS`: enable Spam Quarantine HTTPS. Either 'yes' or 'no'
        - `EUQ_HTTPS_port`: specify port to be used for Spam Quarantine HTTPS
        - `use_demo_cert`: use a demo certificate. Either 'yes' or 'no'
        - `cert_to_use`: the name of certificate profile to be used for the
        interface. Applicable only if there are more than one certificate
        installed on appliance and `use_demo_cert` is set to 'no'.
        "Demo" by default
        - `confirm_demo_use`: whether to use Demo certificate for the
        particular listener or not. Mandatory only if `cert_to_use` is set to
        "Demo" and there are more than one certificate installed.
        Either 'yes' or 'no'
        - `HTTP_redirect`: redirect HTTP requests to the secure service
        - `EUQ_redirect`: redirect Spam Quarantine HTTP requests to the
          secure service
        - `use_def_ipas`: use this interface as default interface for Spam
          Quarantine. Either 'yes' or 'no'
        - `use_custom_base_url`: use custom base URL in your Spam Quarantine
          email notifications. Either 'yes' or 'no'
        - `custom_base_url`: specify the custom base URL in your Spam Quarantine
          email notifications. (Ex: "http://isq.example.url:81/")
        - `change_confirm`: confirm changes on the logged on interface.
          Either 'Yes' or 'No'.
        - `filter_confirm`: confirm if referenced by one or more filters.
          Either 'Yes' or 'No'.
        - `RSA_Manager`: whether to enable ESA Enterprise manager feature
        for this interface. Either 'yes' or 'no'
        - `api_http`: enable REST API HTTP. Either 'yes' or 'no'
        - `api_http_port`: specify port to be used for REST API HTTP.
        - `api_https`: enable REST API HTTPS. Either 'yes' or 'no'
        - `api_https_port`: specify port to be used for REST API HTTPS.

        *Example*:
        | Interfaceconfig Edit | test_intf | configure_ipv4=yes |
        | ... | address=10.0.131.23 | ethernet=Data 2 |
        | ... | hostname=editdomain.com |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.interfaceconfig().edit(if_name, **kwargs)

    def interfaceconfig_delete(self, if_name, *args):
        """
        This is used to delete an interface

        interfaceconfig -> delete

        *Parameters*
        - `if_name`: specify name of the interface to be deleted
        - `filter_confirm`: confirm if referenced by one or more filters.
          Either 'Yes' or 'No'.
        - `current_confirm`: confirm if logged into. Either 'Yes' or 'No'.
        - `group_confirm`: confirm if one or more IP groups use it.
          Either 'Yes' or 'No'.
        - `omh_choice`:  must change outgoing mail configuration for management
          interface. Values either 'Delete' (Disable outgoing mail on this
          interface), 'Change' (Choose a new interface), 'Ignore' (Leave the
          outgoing mail interface (The service will not be available until you
          add a new interface with the same name or change the settings)
        - `omh_new`: choose a new interface to use for outgoing mail.
          Must be used when omh_choice is set to 'Change'.
        - `altsrchost_choice`: must change Virtual Gateway for management
          interface. Values either 'Delete' (Disable outgoing mail on this
          interface), 'Change' (Choose a new interface), 'Ignore' (Leave the
          outgoing mail interface (The service will not be available until you
          add a new interface with the same name or change the settings)
        - `altsrchost_new`: new interface for Virtual Gateway.
          Must be used when choice option is set to 'Change'.
        - `dns_choice`: must change DNS traffic for management interface.
          Values either 'Delete' (Disable the service on this interface),
          'Change' (Choose a new interface), 'Ignore' (Leave the interface
          for the service (The service will not be available until you add
          a new interface with the same name or change the settings).
        - `dns_new`: new interface for DNS traffic.
          Must be used when choice option is set to 'Change'.
        - `snmp_choice`: must change snmp configuration for management interface
          Values either 'Delete' (Disable SNMP on this interface), 'Change'
          (Choose a new interface), 'Ignore' (Leave the SNMP interface set to
          "Management" (SNMP will not be available until you add a new interface
          named "Management" or change the SNMP settings).
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
          Must be used when choice is set to 'Change'.
        - `cluster_choice`: must change cluster interface.
          Values either 'Delete' (Disable the service on this interface),
          'Change' (Choose a new interface), 'Ignore' (Leave the interface
          for the service (The service will not be available until you add
          a new interface with the same name or change the settings).
        - `cluster_new`: new interface for the route.
          Must be used when choice is set to 'Change'.
        - `upgrade_choice`: must change upgrades interface.
          Values either 'Delete' (Disable the service on this interface),
          'Change' (Choose a new interface), 'Ignore' (Leave the interface
          for the service (The service will not be available until you add
          a new interface with the same name or change the settings).
        - `upgrade_new`: new interface for upgrades.
          Must be used when choice is set to 'Change'.
        - `smtpauth_choice`: must change SMTP Authentication interface.
          Values either 'Delete' (Disable the service on this interface),
          'Change' (Choose a new interface), 'Ignore' (Leave the interface
          for the service (The service will not be available until you add
          a new interface with the same name or change the settings).
        - `smtpauth_new`: new interface for SMTP Auth.
          Must be used when choice is set to 'Change'.

        *Example*:
        | Interfaceconfig Delete | test_intf |

        """
        kwargs = self._convert_to_dict(args)
        self._cli.interfaceconfig().delete(if_name, **kwargs)

    def interfaceconfig_groups_new(self, *args):
        """
        This is used to create a new interface group

        interfaceconfig -> groups -> new

        *Parameters*
        - `group_name`: specify name for the interface group
        - `if_list`: name or number of the interfaces to be included in this
          group. Items should be separated by commas or specified as a range
          with a dash.

        *Examples*:
        | Interfaceconfig Groups New | group_name=test |
        | ... | if_list=1,2 |
        | Interfaceconfig Groups New | group_name=testgrp1 |
        | ... | if_list=a001.d1,a001.d2,Management |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.interfaceconfig().groups().new(**kwargs)

    def interfaceconfig_groups_edit(self, group_name, *args):
        """
        This is used to edit interface groups

        interfaceconfig -> groups -> edit

        *Parameters*
        - `group_name`: specify name of the interface group to be edited
        - `new_name`: new name for this interface group
        - `if_list`: name or number of the interfaces to be included in this
           group. Items should be separated by commas or specified as a range
           with a dash.
        - `filter_confirm`: confrim editing if it is used by a filter.
          Either 'Yes' or 'No'.

        *Example*:
        | Interfaceconfig Groups Edit | test | new_name=test1 |
        | ... | if_list=1,2 |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.interfaceconfig().groups().edit(group_name, **kwargs)

    def interfaceconfig_groups_delete(self, group_name, *args):
        """
        This is used to delete an interface group

        interfaceconfig -> groups -> delete

        *Parameters*
        - `group_name`: specify name of the interface group to be deleted
        - `filter_confirm`: confirm if referenced by one or more filters.
          Either 'Yes' or 'No'.
        - `omh_choice`:  must change outgoing mail configuration for management
          interface. Values either 'Delete' (Disable outgoing mail on this
          interface), 'Change' (Choose a new interface), 'Ignore' (Leave the
          outgoing mail interface (The service will not be available until you
          add a new interface with the same name or change the settings)
        - `omh_new`: choose a new interface to use for outgoing mail.
          Must be used when omh_choice is set to 'Change'.
        - `altsrchost_choice`: must change Virtual Gateway for management
          interface. Values either 'Delete' (Disable outgoing mail on this
          interface), 'Change' (Choose a new interface), 'Ignore' (Leave the
          outgoing mail interface (The service will not be available until you
          add a new interface with the same name or change the settings)
        - `altsrchost_new`: new interface for Virtual Gateway.
          Must be used when choice option is set to 'Change'.

        *Example*:
        | Interfaceconfig Delete | test |

        """
        kwargs = self._convert_to_dict(args)
        self._cli.interfaceconfig().groups().delete(group_name, **kwargs)

    def interfaceconfig_get_details(self):
        """
        This is used to get the interface details

        interfaceconfig
        """

        return self._cli.interfaceconfig().get_details()
