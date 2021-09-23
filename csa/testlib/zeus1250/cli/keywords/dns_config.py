#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1250/cli/keywords/dns_config.py#3 $ $DateTime: 2019/06/07 02:45:52 $ $Author: sarukakk $

from common.cli.clicommon import (CliKeywordBase, DEFAULT)
from common.cli.cliexceptions import ConfigError


class DnsConfig(CliKeywordBase):

    """Keywords for dnsconfig CLI command."""

    def get_keyword_names(self):
        return [
                'dns_config_new',
                'dns_config_setup',
                'dns_config_delete',
                'dns_config_edit',]

    def dns_config_new(self, ip, server_type, priority=None, domain=None,
        hostname=None):
        """Add new server.

        dnsconfig > new

        Parameters:
        - `ip`: string with DNS server IP address. The IP address must be
            4 numbers separated by a period. Each number must be a
            value from 0 to 255.
        - `server_type`: nameserver type. Either a local DNS cache server,
            an alternate domain server or an internet domain server.
            Values are: 'local', 'alternate' or 'internet'. Mandatory.
        - `priority`: priority for DNS server. Value must be an integer
            from 0 to 10,000. A value of 0 has the highest priority. Need to
            be specified only with local servers.
        - `domain`: string with domain this server is authoritative for. Don't
            need to specify with local servers.
        - `hostname`: fully qualified hostname of the DNS server for
            the specified domain. (Ex: "dns.example.net"). Need to
            be specified only with internet servers.

        Exceptions:
        - `ConfigError`: in case not all configuration options were specified.
        - `ValueError`: in case of invalid value for `server_type`.

        Examples:
        | DNS Config New Server | 1.1.1.1 | local | priority=1 |
        | DNS Config New Server | 1.1.1.1 | alternate | domain=com |
        | DNS Config New Server | 1.1.1.1 | internet | domain=com |
        | ... | hostname=test.com |
        """
        if server_type.lower() == 'local':
            if priority is not None:
                kwargs = {'ip_addr': ip,
                          'priority': priority,
                          'which_server': 1}
            else:
                raise ConfigError('Priority for DNS server must be specified.')
        elif server_type.lower() == 'alternate':
            if domain is not None:
                kwargs = {'domain_name': domain,
                          'ip_addr': ip,
                          'which_server': 2}
            else:
                raise ConfigError('Domain name must be specified')
        elif server_type.lower() == 'internet':
            if all([domain, hostname]):
                kwargs = {'ip_addr': ip,
                          'auth_domain': domain,
                          'hostname': hostname}
            else:
                raise ConfigError(
                    'Domain name and hostname must be specified.')
        else:
            raise ValueError(
                'Server type must be local, alternate or internet.')

        self._cli.dnsconfig().new(**kwargs)

    def dns_config_setup(self, server_type=DEFAULT, ip_interface=DEFAULT,
        timeout=DEFAULT, minimum_ttl=DEFAULT, ip=None, priority=DEFAULT):
        """Configure general settings.

        dnsconfig > setup

        Parameters:
        - `server_type`: specify either Internet's root DNS server or
            your own DNS server usage. Value are: 'internet' or
            'local'.
        - `ip_interface`: the IP interface name for DNS traffic.
        - `timeout`: string with number of seconds to wait
            before timing out reverse DNS lookups. Value must be an
            integer from 1 to 300.
        - `minimum_ttl`: the minimum TTL in seconds for DNS cache.
        - `ip`: string with DNS server IP address. Mandatory when switching
            from internet to your own. The IP address must be 4 numbers
            separated by a period. Each number must be a value from 0 to 255.
        - `priority`: priority for DNS server. Value must be an integer
            from 0 to 10,000. A value of 0 has the highest priority. Need to
            be specified only with local servers.

        Examples:
        | DNS Config Setup | server_type=internet | ip_interface=Data 1 |
        | ... | timeout=20 |
        | DNS Config Setup | server_type=local | timeout=40 |
        | .... | minimum_ttl=1800 | ip=1.1.1.1 | priority=1 |
        | DNS Config Setup | server_type=internet |
        """
        if server_type.lower() == 'local':
            server_type = 'own'

        kwargs = {'use_own': server_type,
                  'iface': ip_interface,
                  'minimum_ttl': minimum_ttl,
                  'rev_dns_timeout': timeout}

        if ip is not None:
            kwargs.update({'ip_addr': ip,
                           'priority': priority})

        self._cli.dnsconfig().setup(**kwargs)

    def dns_config_delete(self, ip, server_type):
        """Delete domain server.

        dnsconfig > delete

        Parameters:
        - `ip`: string with server IP address to delete.
            The IP address must be 4 numbers separated by a period.
            Each number must be a value from 0 to 255.
        - `server_type`: nameserver type. Either a local DNS cache server,
            an alternate domain server or an internet domain server.
            Value are: 'local', 'alternate' or 'internet'.

        Note: You must configure DNS to use the Internet root nameservers
            for using this keyword for deleting internet domain servers.

        Exceptions:
        - `ValueError`: in case of invalid value for `server_type`.

        Examples:
        | DNS Config Delete Server | 5.5.5.5 | local |
        | DNS Config Delete Server | 1.1.1.1 | internet |
        """
        if server_type.lower() == 'local':
            kwargs = {'ip_addr': ip, 'which_server': 1}
        elif server_type.lower() == 'alternate':
            kwargs = {'ip_addr': ip, 'which_server': 2}
        elif server_type.lower() == 'internet':
            kwargs = {'ip_addr': ip}
        else:
            raise ValueError('Server type must be local, '\
                'alternate or internet.')

        self._cli.dnsconfig().delete(**kwargs)

    def dns_config_edit(self, ip, server_type, new_ip=DEFAULT,
        priority=DEFAULT, domain=DEFAULT, hostname=DEFAULT):
        """Edit domain server information.

        dnsconfig > edit

        - `ip`: string with DNS server IP address. The IP address must be
            4 numbers separated by a period. Each number must be a value
            from 0 to 255. The IP address cannot start with "0".
            (Ex: 192.168.1.1). Mandatory.
        - `server_type`: nameserver type. Either a local DNS cache server,
            an alternate domain server or an internet domain server.
            Values are: 'local', 'alternate' or 'internet'. Mandatory.
        - `new_ip`: string with new IP address of your DNS server.
            Requirements are the same as for 'ip'.
        - `domain`: string with domain this server is authoritative for.
            (Ex: "com"). Don't need to specify domain for local servers.
        - `hostname`: fully qualified hostname of the DNS server for
            the specified domain. (Ex: "dns.example.net"). Need to be
            specified only with internet nameservers.

        Note: You must configure DNS to use the Internet root nameservers
            for using this keyword for editing internet domain servers.

        Exceptions:
        - `ValueError`: in case of invalid value for `server_type`.

        Examples:
        | DNS Config Edit Server | 1.1.1.1 | local | new_ip=2.2.2.2 |
        | ... | priority=0 |
        | DNS Config Edit Server | 1.1.1.1 | alternate | new_ip=2.2.2.2 |
        | ... | domain=com |
        | DNS Config Edit Server | 1.1.1.1 | internet |new_ip=2.2.2.2 |
        | ... | domain=com | hostname=test.com |
        """
        kwargs = {'ip_addr': ip,
                  'new_ip_addr': new_ip}

        if server_type.lower() == 'local':
            kwargs.update({'priority': priority, 'which_server': '1'})
        elif server_type.lower() == 'alternate':
            kwargs.update({'domain_name': domain, 'which_server': '2'})
        elif server_type.lower() == 'internet':
            kwargs.update({'auth_domain': domain,'hostname': hostname})
        else:
            raise ValueError('Server type must be local, alternate or '\
                'internet.')

        self._cli.dnsconfig().edit(**kwargs)

