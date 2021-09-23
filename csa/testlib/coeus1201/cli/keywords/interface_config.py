#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/cli/keywords/interface_config.py#1 $
# $DateTime: 2019/08/14 09:58:47 $
# $Author: uvelayut $

import re
from common.cli.clicommon import CliKeywordBase, DEFAULT

class InterfaceConfig(CliKeywordBase):
    """Interface Configuration."""

    def get_keyword_names(self):
        return [
            'interface_config_new',
            'interface_config_edit',
            'interface_config_delete',
        ]

    def interface_config_new(self,
        configure_ipv4=DEFAULT,
        ipv4_address=DEFAULT,
        netmask=DEFAULT,

        configure_ipv6=DEFAULT,
        ipv6_address=DEFAULT,
        prefix_len=DEFAULT,

        interface=DEFAULT,
        hostname=DEFAULT,
        ftp_enable=DEFAULT,
        ssh_enable=DEFAULT,
        http_enable=DEFAULT,
        https_enable=DEFAULT,
        ftp_port=DEFAULT,
        ssh_port=DEFAULT,
        http_port=DEFAULT,
        https_port=DEFAULT,
        demo_cert=DEFAULT,
        http_redirection=DEFAULT):
        """Create a new interface.

        interfaceconfig > new

        Parameters:
        - `configure_ipv4`: answer to question Would you like to configure an
         IPv4 address for this interface (y/n)? [Y]>
        - `ipv4_address`: IPv4 address.
        - `netmask`: netmask for IPv4 address. Must be a dotted octet
                (255.255.255.0) or a hexadecimal (0xffffff00) value.

        - `configure_ipv6`: answer to question Would you like to configure an
         IPv6 address for this interface (y/n)? [N]>
        - `ipv6_address`: IPv6 address.
        - `prefix_len`: prefix length for IPv6 address. Default 64.

        - `interface`: interface name. Either 'Management',
                'P1' or 'P2'.
        - `hostname`: a hostname value for specified interface.
        - `ftp_enable`: enable or disable ftp for Management interface.
                Either 'Yes' or 'No'.
        - `ftp_port`: ftp port value.
        - `ssh_enable`: enable or disable ssh for Management interface.
                Either 'Yes' or 'No'.
        - `ssh_port`: ssh port value.
        - `http_enable`: enable or disable http for Management interface.
                Either 'Yes' or 'No'.
        - `http_port`: http port value.
        - `https_enable`: enable or disable https for Management interface.
                Either 'Yes' or 'No'.
        - `https_port`: https port value.
        - `demo_cert`: use demo certificate or disable https for moment.
        - `http_redirection`: should HTTP requests redirect to the secure
                service or no. Either 'Yes' or 'No'.

        Examples:
        | Interface Config New |
        | ... | configure_ipv4=Y |
        | ... | ipv4_address=10.7.8.130 |
        | ... | netmask=255.255.255.0 |
        | ... | configure_ipv6=Y |
        | ... | ipv6_address=2001:db8:1::4 |
        | ... | prefix_len=64 |
        | ... | interface=management |
        | ... | hostname=test.com |
        | ... | ftp_enable=yes |
        | ... | ftp_port=21 |
        | ... | ssh_enable=yes |
        | ... | ssh_port=22 |
        | ... | http_enable=yes |
        | ... | http_port=8080 |
        | ... | https_enable=yes |
        | ... | https_port=8443 |
        | ... | demo_cert=yes |
        | ... | http_redirection=yes |

        | Interface Config New |
        | ... | ip=10.7.8.130 |
        | ... | netmask=255.255.255.0 |
        | ... | interface=p1 |
        """
        kwargs = {
            'configure_ipv4' : configure_ipv4,
            'ipv4_address' : ipv4_address,
            'netmask' : netmask,

            'configure_ipv6' : configure_ipv6,
            'ipv6_address' : ipv6_address,
            'prefix_len' : prefix_len,

            'ethernet' : interface,
            'hostname' : hostname,
            'FTP' : ftp_enable,
            'FTP_port' : ftp_port,
            'SSH' : ssh_enable,
            'SSH_port' : ssh_port,
            'HTTP' : http_enable,
            'HTTP_port' : http_port,
            'HTTPS' : https_enable,
            'HTTPS_port' : https_port,
            'use_demo_cert' : demo_cert,
            'HTTP_redirect' : http_redirection,
        }
        for k in kwargs.keys():
            if not kwargs[k]:
                del kwargs[k]

        self._cli.interfaceconfig().new(**kwargs)

    def interface_config_delete(self,
        interface=DEFAULT,
        snmp=DEFAULT,
        snmp_new=DEFAULT):
        """Remove an interface.

        interfaceconfig > delete

        Parameters:
        - `interface`: interface name to be deleted.
        - `snmp`: must change snmp configuration for management interface.
                Values either 'Delete' (Disable SNMP on this interface),
                'Change' (Choose a new interface), 'Ignore' (Leave the
                SNMP interface set to "Management" (SNMP will not be
                available until you add a new interface named "Management"
                or change the SNMP settings).
        - `snmp_new`: choose a new interface to use for SNMP (P1 or P2).
                Must be used when snmp is set to 'Change'.

        Example:
        | Interface Config Delete |
        | Interface Config Delete | snmp=change | snmp_new=P1 |
        """
        snmps = {
                 'delete': 1,
                 'change': 2,
                 'ignore': 3
                 }
        kwargs = {
                  'if_name': interface.strip(),
                  }
        if snmp in snmps.keys():
            kwargs['SNMP_choice'] = snmps[snmp.split().lower()]
            kwargs['SNMP_new'] = snmp_new.strip()
        self._cli.interfaceconfig().delete(**kwargs)

    def interface_config_edit(self,
        configure_ipv4=None,
        ipv4_address=None,
        netmask=None,

        configure_ipv6=None,
        ipv6_address=None,
        prefix_len=None,

        interface=None,
        hostname=None,
        ftp_enable=None,
        ssh_enable=None,
        http_enable=None,
        https_enable=None,
        ftp_port=None,
        ssh_port=None,
        http_port=None,
        https_port=None,
        demo_cert=None,
        http_redirection=None):
        """Create a new interface.

        interfaceconfig > edit

        Parameters:
        - `configure_ipv4`: answer to question Would you like to configure an
         IPv4 address for this interface (y/n)? [Y]>
        - `ipv4_address`: IPv4 address.
        - `netmask`: netmask for IPv4 address. Must be a dotted octet
                (255.255.255.0) or a hexadecimal (0xffffff00) value.

        - `configure_ipv6`: answer to question Would you like to configure an
         IPv6 address for this interface (y/n)? [N]>
        - `ipv6_address`: IPv6 address.
        - `prefix_len`: prefix length for IPv6 address. Default 64.

        - `interface`: interface name. Possible values:
                'Management', 'P1', 'P2',
                'Management_v6', 'P1_v6' and 'P2_v6'
        - `hostname`: a hostname value for specified interface.
        - `ftp_enable`: enable or disable ftp for Management interface.
                Either 'Yes' or 'No'.
        - `ftp_port`: ftp port value.
        - `ssh_enable`: enable or disable ssh for Management interface.
                Either 'Yes' or 'No'.
        - `ssh_port`: ssh port value.
        - `http_enable`: enable or disable http for Management interface.
                Either 'Yes' or 'No'.
        - `http_port`: http port value.
        - `https_enable`: enable or disable https for Management interface.
                Either 'Yes' or 'No'.
        - `https_port`: https port value.
        - `demo_cert`: use demo certificate or disable https for moment.
        - `http_redirection`: should HTTP requests redirect to the secure
                service or no. Either 'Yes' or 'No'.

        Examples:
        | Interface Config Edit |
        | ... | interface=management |
        | ... | ftp_enable=no |
        | ... | ssh_enable=no |
        | ... | http_enable=no |
        | ... | https_enable=no |
        """
        kwargs = {
            'configure_ipv4' : configure_ipv4,
            'ipv4_address' : ipv4_address,
            'netmask' : netmask,

            'configure_ipv6' : configure_ipv6,
            'ipv6_address' : ipv6_address,
            'prefix_len' : prefix_len,

            'if_name' : interface,
            'hostname' : hostname,
            'FTP' : ftp_enable,
            'FTP_port' : ftp_port,
            'SSH' : ssh_enable,
            'SSH_port' : ssh_port,
            'HTTP' : http_enable,
            'HTTP_port' : http_port,
            'HTTPS' : https_enable,
            'HTTPS_port' : https_port,
            'use_demo_cert' : demo_cert,
            'HTTP_redirect' : http_redirection,
        }
        for k in kwargs.keys():
            if not kwargs[k]:
                del kwargs[k]

        self._cli.interfaceconfig().edit(**kwargs)
