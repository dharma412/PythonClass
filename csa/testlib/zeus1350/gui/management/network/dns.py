#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1350/gui/management/network/dns.py#1 $ $DateTime: 2019/09/18 01:46:35 $ $Author: sarukakk $

import re
from common.gui.guicommon import GuiCommon

REGEX_USER_DNS = 'user_dns'
REGEX_USER_ALT = 'user_alt'
REGEX_ROOT_ALT = 'root_alt'
DNS_TBODY_ROW = lambda field: '//tbody[@id=\"%s_rowContainer\"]/tr' % (field,)
DNS_TABLE_FIELD = lambda dns, index, field: '%s[%d][%s]' % (dns, index, field,)
DNS_DEL = lambda dns, index, td: '//tr[@id="%s_row%s"]/td[%d]/img[1]' % \
                                 (dns, index, td,)
GET_FIELD_REGEX = lambda dns: '%s\[(\d+)\]\[IP\]' % (dns,)
LIST_LABEL = lambda item: 'label=%s' % (item,)


class DNSServer(object):
    """Class for DNS Server attributes"""

    def __init__(self, server_ip, priority=0):
        self.ip = server_ip
        self.priority = priority


class AltDNSServer(object):
    """Class for Alternative DNS Server attributes"""

    def __init__(self, server_ip, domain, fqdn=None):
        self.domain = domain
        self.ip = server_ip
        self.fqdn = fqdn


class Dns(GuiCommon):
    """Keyword library for menu Management Appliance -> Network -> DNS"""

    def get_keyword_names(self):
        return ['dns_add_local_server',
                'dns_add_alternate_server',
                'dns_edit_settings',
                'dns_clear_cache',
                'dns_delete_local_servers',
                'dns_delete_alternate_servers',
                'dns_delete_all_local_servers',
                'dns_delete_all_alternate_servers',
                ]

    def _open_page(self):
        """Open 'DNS'"""
        self._navigate_to('Management', 'Network', 'DNS')

    def _get_table_row_values(self, regex_dns=None):
        val_list = []
        row_pattern = re.compile(GET_FIELD_REGEX(regex_dns, ))
        text_fields = self._get_all_fields()

        for field in text_fields:
            result = row_pattern.search(field)

            if result:
                value = self.get_value \
                    (DNS_TABLE_FIELD(regex_dns, int(result.group(1)), 'IP'))
                val_list.append(value)

        return val_list

    def _dns_delete(self,
                    dns='Local',
                    dns_ip=None,
                    alt_ip=None):
        self._open_page()
        self._click_edit_settings_button()
        self._select_dns(dns)

        if dns_ip is not None:
            self._info('Deleting DNS Servers...')
            self._perform_delete_operation(regex_dns=REGEX_USER_DNS, ips=dns_ip)

        if alt_ip is not None:
            if dns.lower() == 'root':
                self._info('Deleting Root Alternate DNS Servers...')
                self._perform_delete_operation \
                    (regex_dns=REGEX_ROOT_ALT, table_column=4, ips=alt_ip)
            elif dns.lower() == 'local':
                self._info('Deleting Alternate DNS Servers...')
                self._perform_delete_operation(regex_dns=REGEX_USER_ALT, ips=alt_ip)
            else:
                raise ValueError('Invalid input value  \'%s\' for \'DNS Servers\' ' \
                                 'it should either be \'local\' or \'root\'' % (dns,))

        self._click_submit_button()

    def dns_delete_local_servers(self, dns_ips):
        """Delete Local DNS Servers
        Parameters:
            - `dns_ips`: string of comma separated IP Addresses

        :Exceptions:
            - `ValueError`: in case of invalid value for any of the input
                            parameters.

        Examples:
        | DNS Delete Local Servers | 10.92.144.4 |
        | DNS Delete Local Servers | 192.168.1.1, 192.168.1.2 |
        """
        self._dns_delete('Local', dns_ips)

    def dns_delete_alternate_servers(self, dns_ips=None, dns='Local'):
        """Delete Alternate DNS Servers

        Parameters:
            - `dns_ips`: string of comma separated IP Addresses
            - `dns`:
                * 'Local' to delete DNS server(s) defined under 'Use these DNS
                    Servers'
                * 'Root' to delete DNS server(s) defined under 'Use the
                    Internet's Root DNS Servers'

        :Exceptions:
            - `ValueError`: in case of invalid value for any of the input
                            parameters.

        Examples:
        | DNS Delete Alternate Servers | 10.92.144.4 | |
        | DNS Delete Alternate Servers | dns_ips=192.168.1.1, 192.168.1.2 | dns=Root |
        """
        self._dns_delete(dns, alt_ip=dns_ips)

    def _perform_delete_all_operation(self,
                                      regex_dns=None,
                                      table_column=3):
        num_entry = int(self.get_matching_xpath_count(DNS_TBODY_ROW(regex_dns)))

        for i in range(num_entry):
            self.click_button \
                (DNS_DEL(regex_dns, i, table_column), "don't wait")

        return num_entry

    def _delete_all_servers(self,
                            dns='Local',
                            servers=None):
        self._info('Deleting all DNS servers')

        if dns.lower() == 'local':
            if servers.lower() == 'dns':
                num_entry = self._perform_delete_all_operation(regex_dns=REGEX_USER_DNS)
            else:
                num_entry = self._perform_delete_all_operation(regex_dns=REGEX_USER_ALT)
        elif dns.lower() == 'root':
            num_entry = self._perform_delete_all_operation(
                regex_dns=REGEX_ROOT_ALT, table_column=4)
        else:
            raise ValueError('Invalid input value  \'%s\' for \'DNS Servers\' ' \
                             'it should either be \'local\' or \'root\'' % (dns,))

        self._info('All DNS servers deleted')
        return num_entry

    def dns_delete_all_local_servers(self):
        """Delete All Local DNS Servers
        and use 'Internet's Root DNS Server'

        Examples:
        | DNS Delete All Local Servers |
        """
        self._info('Deleting All Local DNS Servers...')
        self._open_page()
        self._click_edit_settings_button()
        self._delete_all_servers('Local', 'dns')
        self._select_dns('Root')
        self._click_submit_button()

    def dns_delete_all_alternate_servers(self, dns='Local'):
        """Delete All Alternate DNS Servers

        Parameters:
            - `dns`:
                * 'Local' to delete DNS server(s) defined under 'Use these DNS
                    Servers'
                * 'Root' to delete DNS server(s) defined under 'Use the
                    Internet's Root DNS Servers'

        :Exceptions:
            - `ValueError`: in case of invalid value for any of the input
                            parameters.

        Examples:
        | DNS Delete All Alternate Servers | |
        | DNS Delete All Alternate Servers | dns=Root |
        """
        self._info('Deleting All Alternate DNS Servers...')
        self._open_page()
        self._click_edit_settings_button()
        self._delete_all_servers(dns, 'alt')
        self._click_submit_button()

    def _perform_delete_operation(self,
                                  regex_dns=None,
                                  table_column=3,
                                  ips=None):
        ips = self._convert_to_tuple(ips)
        table_ips = self._get_table_row_values(regex_dns)

        for ip in ips:
            if ip not in table_ips:
                raise guiexceptions.GuiControlNotFoundError \
                    ('\'%s\'' % (ip,), 'DNS')
            self._info('Deleting "%s"' % (ip,))

            for i, table_ip in enumerate(table_ips):
                if ip == table_ip:
                    self.click_button(DNS_DEL(regex_dns, i, table_column), "don't wait")
                    self._info('Deleted \'%s\'' % (ip,))

    def _add_alt_servers(self,
                         alt_servers=None,
                         dns=None):
        alt_dns_add_row_field = 'user_alt_domtable_AddRow'
        root_dns_add_row_field = 'root_alt_domtable_AddRow'

        if alt_servers is not None:
            self._info('Adding Alternate DNS Servers...')

            if dns.lower() == 'local':
                regex_alt = REGEX_USER_ALT
                domain_field = 'Domain'
                add_row_button = alt_dns_add_row_field
            else:
                regex_alt = REGEX_ROOT_ALT
                domain_field = 'Dom'
                add_row_button = root_dns_add_row_field

            entry_index = int(self.get_matching_xpath_count(DNS_TBODY_ROW(regex_alt)))

            for i, obj in enumerate(alt_servers):
                if entry_index == 1 and \
                        self.get_value(DNS_TABLE_FIELD(regex_alt, 0,
                                                       'IP')).strip() == '':
                    entry_index = 0
                else:
                    self.click_button(add_row_button, "don't wait")
                    self._info("Clicked 'Add Row' button")

                if type(obj.domain) == tuple:
                    domain_text = ','.join(obj.domain)
                else:
                    domain_text = obj.domain

                self.input_text \
                    (DNS_TABLE_FIELD(regex_alt, entry_index, domain_field), domain_text)
                self._info('Added Domain(s) "%s"' % (domain_text,))
                self.input_text \
                    (DNS_TABLE_FIELD(regex_alt, entry_index, 'IP'), obj.ip)
                self._info('Added IP "%s"' % (obj.ip,))

                if dns.lower() == 'root':
                    self.input_text \
                        (DNS_TABLE_FIELD(regex_alt, entry_index, 'FQDN'),
                         obj.fqdn)
                    self._info('Added DNS Server FQDN "%s"' %
                               (obj.fqdn,))
                    entry_index = entry_index + 1

    def _add_dns_servers(self, dns_servers=None, dns=None):
        dns_add_row_field = 'user_dns_domtable_AddRow'

        if dns_servers is not None:
            if dns.lower() == 'local':
                entry_index = int(self.get_matching_xpath_count(DNS_TBODY_ROW(REGEX_USER_DNS)))

                for i, obj in enumerate(dns_servers):
                    if entry_index == 1 and \
                            self.get_value(DNS_TABLE_FIELD(REGEX_USER_DNS, 0,
                                                           'IP')).strip() == '':
                        entry_index = 0
                    else:
                        self.click_button(dns_add_row_field, "don't wait")
                        self._info("Clicked 'Add Row' button")

                    self._info('Clicked \'Add Row\' button')
                    self.input_text(DNS_TABLE_FIELD(REGEX_USER_DNS, entry_index, 'Pri'), \
                                    obj.priority)
                    self._info('Added Priority "%s"' % (obj.priority,))
                    self.input_text(DNS_TABLE_FIELD(REGEX_USER_DNS,
                                                    entry_index, 'IP'), obj.ip)
                    self._info('Added IP "%s"' % (obj.ip,))
                    entry_index = entry_index + 1
            else:
                raise ValueError('Invalid input value  \'%s\' for \'DNS Servers\' ' \
                                 'it should either be \'local\'' % (dns,))

    def _select_dns(self, dns=None):
        dns_radio_button = {'local': 'dns_user',
                            'root': 'dns_root1'}
        if dns is not None:
            if dns.lower() == 'local':
                self._click_radio_button(dns_radio_button['local'])
                self._info('Selected to \'Use these DNS Servers\'')
            elif dns.lower() == 'root':
                self._click_radio_button(dns_radio_button['root'])
                self._info('Selected to \'Use the Internet Root DNS Servers\'')
            else:
                raise ValueError('Invalid input value  \'%s\' for \'DNS Servers\' ' \
                                 'it should either be \'local\' or \'root\'' % (dns,))

    def dns_add_local_server(self, dns_ip, priority=0):
        """Add Local DNS Server

        Parameters:
            - `dns_ip`: DNS Server IP Address
            - `priority`: Priority of DNS Server

        :Exceptions:
            - `ValueError`: in case of invalid value for any of the input
                            parameters.

        Examples:
        | DNS Add Local Server | 10.92.144.4 | |
        | DNS Add Local Server | 192.168.1.1 | priority=10 |
        """
        dns = 'Local'
        dns_server = DNSServer(dns_ip, priority)
        dns_servers = (dns_server,)

        self._info('Adding Local DNS server...')
        self._open_page()
        self._click_edit_settings_button()
        self._select_dns(dns)
        self._add_dns_servers(dns_servers, dns)
        self._click_submit_button()

    def dns_add_alternate_server(self, dns='Local', dns_ip=None,
                                 domains=None, FQDN=None):
        """Add Alternative DNS Server

        Parameters:
            - `dns`:
                * 'Local' to add DNS server(s) defined under 'Use these DNS
                    Servers'
                * 'Root' to add DNS server(s) defined under 'Use the
                    Internet's Root DNS Servers'

            - `dns_ip`: Alternative DNS Server IP Address
            - `domains`: string of comma separated Domain Names, for
                'Internet's Root DNS Servers' only single domain per server is
                supported
            - `FQDN`: DNS Server Fully Qualified Domain Name
                Apply for Internet's Root DNS Server only

        :Exceptions:
            - `ValueError`: in case of invalid value for any of the input
                            parameters.

        Examples:
        | DNS Add Alternative Server | domains=example.com, example2.com | dns_ip=10.92.144.4 |
        | DNS Add Alternative Server | dns=Root | domains=example.com | FQDN=dns.example.com | dns_ip=10.0.0.3 |
        """
        dns_server = AltDNSServer(dns_ip, domains, FQDN)
        dns_servers = (dns_server,)
        self._info('Adding Alternate DNS server...')
        self._open_page()
        self._click_edit_settings_button()
        self._select_dns(dns)
        self._add_alt_servers(dns_servers, dns)
        self._click_submit_button()

    def _select_interface(self, interface=None):
        if interface is None:
            return
        interface_list = 'name=interface'
        int_list = self.get_list_items(interface_list)

        for int_name in int_list:
            if interface in int_name:
                self.select_from_list(interface_list, LIST_LABEL(int_name))
                self._info('Selected "%s" interface for DNS queries' % \
                           (int_name,))
                break
        else:
            raise ValueError('"%s" interface does not exist' % (interface,))

    def _set_wait_before_timeout(self, timeout=None):
        timeout_field = 'ptr_timeout'

        if timeout is not None:
            self.input_text(timeout_field, timeout)
            self._info('Setting \'Wait Before Timing out Reverse ' \
                       'DNS Lookups\' : %s seconds' % (timeout,))

    def dns_edit_settings(self,
                          interface=None,
                          timeout=None):
        """Edit DNS settings.

        To add/delete DNS servers please use corresponding keywords:
            - `DNS Add Local Server`
            - `DNS Delete Local Servers`
            - `DNS Add Alternate Server`
            - `DNS Delete Alternate Servers`

        Parameters:
            - `interface`: name of the interface to use for DNS traffic
            - `timeout`  : the number of seconds to wait before timing
                           out reverse DNS Lookups

        :Exceptions:
            - `ValueError`: in case of invalid value for any of the input
                            parameters.

        Examples:
        | DNS Edit Settings | interface=Data | timeout=30 |
        | DNS Edit Settings | timeout=30 |
        """
        self._info('Editting DNS settings...')
        self._open_page()
        self._click_edit_settings_button()
        self._select_interface(interface)
        self._set_wait_before_timeout(timeout)
        self._click_submit_button()

    def dns_clear_cache(self):
        """Clear DNS cache

        Example:
        | DNS Clear Cache |
        """
        clear_dns_cache_button = "clearcache"
        self._info('Clearing DNS cache.')
        self._open_page()
        self.click_button(clear_dns_cache_button, "don't wait")
        self._click_continue_button()
        # Validate errors on the page
        self._check_action_result()
