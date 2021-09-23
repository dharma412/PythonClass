#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/cli/keywords/dns_config.py#1 $
# $DateTime: 2019/08/14 09:58:47 $
# $Author: uvelayut $

from common.cli.clicommon import CliKeywordBase
import common.Variables

DEFAULT = ''

class DnsConfig(CliKeywordBase):
    """ Configure DNS."""

    def get_keyword_names(self):
        return [
                'dns_config_new_server',
                'dns_config_setup',
                'dns_config_delete_server',
                'dns_config_edit_server',
                'dns_config_search',
                'dns_config_print_settings']

    def dns_config_new_server(self,
                              ip=None,
                              domain=None,
                              priority=None,
                              hostname=None,
                              type=None,
                              dns_set_select=None):
        """Add new server.

        dnsconfig > new

        Parameters:
        - `ip`: string with DNS server IP address. The IP address must be
            4 numbers separated by a period. Each number must be a
            value from 0 to 255.
        - `priority`: priority for DNS server. Value must be an integer
            from 0 to 10,000. A value of 0 has the highest priority. Need to
            be specified for local and internet servers.
        - `domain`: string with domain this server is authoritative for. Don't
            need to specify with local servers.
        - `hostname`: fully qualified hostname of the DNS server for
            the specified domain. (Ex: "dns.example.net"). Need to
            be specified only with internet servers.
        - `type`: nameserver type. Either a local DNS cache server,
            an alternate domain server or an internet domain server.
            Values are: 'local', 'alternate' or 'internet'. Mandatory.
        - `dns_set_select`: DNS server set. Either Primary or Secondary
            '1' for Primary and '2' for Secondary

        Example:
        | DNS Config New Server | type=local | ip_addr=1.1.1.1 | priority=1 | dns_set_select=2 |
        | DNS Config New Server | type=alternate | ip=1.1.1.1 | domain=com | dns_set_select=1 |
        | DNS Config New Server | type=internet | ip=1.1.1.1 | domain=com | hostname=test.com | dns_set_select=1 |
        | DNS Config New Server | type=internet | ip=1.1.1.1 | domain=com | hostname=test.com | dns_set_select=2 |
        """
        if type is not None:
            if dns_set_select not in ('1','2'):
                 raise ValueError('You must specify either 1 or 2')
                 return
            if type.lower() == 'local':
                if all([ip, priority]):
                    kwargs = {'ip_addr': ip,
                              'priority': priority,
                              'dns_set': dns_set_select}
                    ##If secondary DNS server set is chosen, there is no alternate server
                    if int(dns_set_select) == 1:
                        kwargs['which_server'] = 1
                else:
                    raise ValueError('You must specify domain name and IP '\
                                     'address.')
            elif type.lower() == 'alternate':
                if all([domain, ip]):
                    kwargs = {'domain_name': domain,
                              'ip_addr': ip,
                              'dns_set': dns_set_select}
                    ##If secondary DNS server set is chosen, domain name is not needed and is no alternate servers
                    if int(dns_set_select) == 1:
                        kwargs['which_server'] = 2
                        kwargs['domain_name'] = domain
                else:
                    raise ValueError('You must specify domain name and IP '\
                                     'address.')
            elif type.lower() == 'internet':
                if all([ip, domain, hostname, priority]):
                    kwargs = {'ip_addr': ip,
                              'dns_set': dns_set_select}
                    ##If secondary DNS server set is chosen, domain name and host name is not needed.
                    if int(dns_set_select) == 1:
                              kwargs['auth_domain'] = domain
                              kwargs['hostname'] = hostname

                    ##Only if secondary DNS server set is chosen, priority is needed
                    if int(dns_set_select) == 2:
                              kwargs['priority'] = priority

                else:
                    raise ValueError('You must specify ip, domain and '\
                                     'hostname.')
            else:
                raise ValueError('Type must be local, alternate or internet.')
            self._cli.dnsconfig().new(**kwargs)
        else:
            raise ValueError('You must specify server type you want to add.')

    def dns_config_setup(self,
                         dns_server_type=DEFAULT,
                         routing_table=DEFAULT,
                         timeout=DEFAULT,
                         ip=None,
                         failed_attempts=DEFAULT,
                         polling_interval=DEFAULT,
                         priority=None,
                         preference=None,
    ):
        """Configure general settings.

        dnsconfig > setup

        Parameters:
        - `dns_server_type`: specify either Internet's root DNS server or
            your own DNS server usage. Value are: 'internet' or
            'local'.
        - `routing_table`: routing table to use. Either 'Data' or
            'Management'.
        - `timeout`: string with number of seconds to wait
            before timing out reverse DNS lookups. Value must be an
            integer from 1 to 300.
        - `failed_attempts`: string with number of failed atttempts
           before considering a local DNS server offline. Value must be
           an integer from 1 to 65,536.
        - `polling_interval`: string for the interval in seconds for polling an
           offline local DNS server. Value must be an integer from 5 to 86,400.
        - `ip`: string with DNS server IP address. Mandatory when switching
            from internet to your own. The IP address must be 4 numbers
            separated by a period. Each number must be a value from 0 to 255.
        - `priority`: priority for DNS server. Value must be an integer
            from 0 to 10,000. A value of 0 has the highest priority. Need to
            be specified only with local servers.
        - `preference` - answer to question: Choose a preference for cases
          when DNS results provide both IPv4 and IPv6 addresses for a host:
          1. Prefer IPv4
          2. Prefer IPv6
          3. Use only IPv4

        Examples:
        | DNS Config Setup | dns_server_type=internet | routing_table=Data | timeout=20 |
        | DNS Config Setup | dns_server_type=local | timeout=40 | ip=1.1.1.1 |
        | DNS Config Setup | dns_server_type=internet | preference=Use only IPv4 |
        """
        if dns_server_type.lower() == 'local':
            dns_server_type = 'own'

        if timeout != '':
            if not timeout.isdigit():
                raise ValueError('Timeout value must be an integer'\
                                 'from 0 to 300.')
            else:
                timeout = int(timeout)

        if failed_attempts != '':
            if not failed_attempts.isdigit():
                raise ValueError('Failed attempts value must be an integer'\
                                 'from 1 to 65,536.')
            else:
                failed_attempts = int(failed_attempts)

        if polling_interval != '':
            if not polling_interval.isdigit():
                raise ValueError('Polling integer value must be an integer'\
                                 'from 5 to 86,400.')
            else:
                polling_interval = int(polling_interval)

        if ip is None and priority is None:
            variables = common.Variables.get_variables()
            SSW_MODE = variables["${SSW_MODE}"]
            if SSW_MODE is "M1":
                kwargs = {'use_own': dns_server_type,
                          'rev_dns_timeout': timeout}
            else:
                kwargs = {'use_own': dns_server_type,
                          'routing_table': routing_table,
                          'rev_dns_timeout': timeout}
        else:
            kwargs = {'use_own': dns_server_type,
                      'routing_table': routing_table,
                      'rev_dns_timeout': timeout,
                      'ip_addr': ip,
                      'priority': priority}

        if dns_server_type.lower() == 'own':
            kwargs['failed_attempts'] = failed_attempts
            kwargs['polling_interval'] = polling_interval

        if preference:
            kwargs['preference'] = preference

        self._cli.dnsconfig().setup(**kwargs)

    def dns_config_delete_server(self, ip=None, type=None, dns_set_select=None):
        """Delete domain server.

        dnsconfig > delete

        Parameters:
        - `ip`: string with server IP address to delete.
            The IP address must be 4 numbers separated by a period.
            Each number must be a value from 0 to 255.
        - `type`: nameserver type. Either a local DNS cache server,
            an alternate domain server or an internet domain server.
            Value are: 'local', 'alternate' or 'internet'.
        - `dns_set_select`: DNS server set. Either Primary or Secondary
            '1' for Primary and '2' for Secondary

        Note: You must configure DNS to use the Internet root nameservers
            for using this keyword for deleting internet domain servers.

        Example:
        | DNS Config Delete Server | ip=5.5.5.5 | type=local | dns_set_select=2 |
        | DNS Config Delete Server | ip=1.1.1.1 | type=internet | dns_set_select=1 |#with Internet root nameservers
        """

        if ip is not None and type is not None:
            if dns_set_select not in ('1','2'):
                 raise ValueError('You must specify either 1 or 2')
                 return
            if type.lower() == 'local':
                kwargs = {'ip_addr': ip, 'dns_set': dns_set_select, 'which_server': 1 }
            elif type.lower() == 'alternate':
                kwargs = {'ip_addr': ip, 'dns_set': dns_set_select, 'which_server': 2 }
            elif type.lower() == 'internet':
                kwargs = {'ip_addr': ip, 'dns_set': dns_set_select}
            else:
                raise ValueError('Type must be local, alternate or internet.')
            self._cli.dnsconfig().delete(**kwargs)
        else:
            raise ValueError('You must specify IP address to delete.')

    def dns_config_edit_server(self,
                               ip=None,
                               new_ip=DEFAULT,
                               priority=DEFAULT,
                               domain=DEFAULT,
                               hostname=DEFAULT,
                               dns_set_select=None,
                               type=None):
        """Edit domain server information.

        dnsconfig > edit

        - `ip`: string with DNS server IP address. The IP address must be
            4 numbers separated by a period. Each number must be a value
            from 0 to 255. The IP address cannot start with "0".
            (Ex: 192.168.1.1). Mandatory.
        - `new_ip`: string with new IP address of your DNS server.
            Requirements are the same as for 'ip'.
        - `domain`: string with domain this server is authoritative for.
            (Ex: "com"). Don't need to specify domain for local servers.
        - `hostname`: fully qualified hostname of the DNS server for
            the specified domain. (Ex: "dns.example.net"). Need to be
            specified only with internet nameservers.
        - `type`: nameserver type. Either a local DNS cache server,
            an alternate domain server or an internet domain server.
            Values are: 'local', 'alternate' or 'internet'. Mandatory.
        - `dns_set_select`: DNS server set. Either Primary or Secondary
            '1' for Primary and '2' for Secondary

        Note: You must configure DNS to use the Internet root nameservers
            for using this keyword for editing internet domain servers.

        Example:
        | DNS Config Edit Server | type=local | ip=1.1.1.1 | new_ip=2.2.2.2 | priority=0 | dns_set_select=2 |
        | DNS Config Edit Server | type=alternate | ip=1.1.1.1 | new_ip=2.2.2.2 | domain=com | dns_set_select=1 |
        | DNS Config Edit Server | type=internet | ip=1.1.1.1 | new_ip=2.2.2.2 | domain=com | hostname=test.com | dns_set_s        elect=1 |
         """
        if ip is not None and type is not None:
            if dns_set_select not in ('1','2'):
                 raise ValueError('You must specify either 1 or 2')
                 return
            if type.lower() == 'local':
                kwargs = {'ip_addr': ip,
                          'priority': priority,
                          'new_ip_addr': new_ip,
                          'dns_set': dns_set_select,
                          'which_server': '1'}
            elif type.lower() == 'alternate':
                kwargs = {'ip_addr': ip,
                          'domain_name': domain,
                          'new_ip_addr': new_ip,
                          'dns_set': dns_set_select,
                          'which_server': '2'}
            elif type.lower() == 'internet':
                kwargs = {'ip_addr': ip,
                          'dns_set': dns_set_select,
                          'auth_domain': domain,
                          'hostname': hostname,
                          'priority': priority,
                          'new_ip_addr': new_ip}
            else:
                raise ValueError('Type must be local, alternate or internet.')
            self._cli.dnsconfig().edit(**kwargs)
        else:
            raise ValueError('You must specify IP address to delete.')

    def dns_config_search(self, domains=None):
        """Configure the DNS domain search list.

        Parameters:
        - `domains`: string with comma separated DNS domain search list.
            (host names with no '.'s). If specified with the string
            'delete' as its argument, keyword clears the DNS domain
            search list.

        Examples:
        | DNS Config Search | domains=test1, test2 |
        | DNS Config Search | domains=delete | #to delete search list |
        """
        if domains is not None:
            self._cli.dnsconfig().search(domains.replace(', ', ' '))

    def dns_config_print_settings(self):
        """Display the current DNS settings.
        Return dictionary with DNS Settings.

        dnsconfig > print

        Example:
        | ${command_output}= | DNS Config Print Settings |
        """
        output = self._cli.dnsconfig('print settings').current()
        self._info(output)
        return output

