#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/gui/network/dns.py#1 $
# $DateTime: 2019/08/14 09:58:47 $
# $Author: uvelayut $

import re
from common.gui.guicommon import GuiCommon
from common.gui import guiexceptions

REGEX_USER_DNS = 'user_dns'
REGEX_USER_SEC_DNS = 'user_secondary_dns'
REGEX_USER_ALT = 'user_alt'
REGEX_ROOT_ALT = 'root_alt'
DNS_TBODY_ROW = lambda field: '//tbody[@id=\"%s_rowContainer\"]/tr' % (field,)
DNS_TABLE_FIELD = lambda dns, index, field: '%s[%d][%s]' % (dns, index, field,)
DNS_DEL = lambda dns, index: \
    'xpath=//tr[@id="%s_row%s"]/td/img[contains(@src, "trash.gif")][1]' % \
        (dns, index)
GET_FIELD_REGEX = lambda dns: '%s\[(\d+)\]\[IP\]' % (dns,)

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
    """Keywords for interaction with "Network > DNS" GUI page."""

    # method required by RF
    # return a list with all public methods
    def get_keyword_names(self):
        return [
                'dns_add_local_server',
                'dns_add_sec_server',
                'dns_add_alternate_server',
                'dns_delete_local_servers',
                'dns_delete_sec_servers',
                'dns_delete_alternate_servers',
                'dns_delete_all_local_servers',
                'dns_delete_all_alternate_servers',
                'dns_edit_settings',
                'dns_clear_cache',
                ]

    def _open_page(self):
        """Open 'DNS' """
        self._navigate_to('Network', 'DNS')

    def _get_table_row_values(self, regex_dns=None):
        val_list = []
        row_pattern = re.compile(GET_FIELD_REGEX(regex_dns,))
        text_fields = self._get_all_fields()
        for field in text_fields:
            result = row_pattern.search(field)
            if result:
                value = self.get_value\
                    (DNS_TABLE_FIELD(regex_dns, int(result.group(1)), 'IP'))
                val_list.append(value)
        return val_list

    def _dns_delete(self, dns='Local', dns_ip=None, alt_ip=None):
        """Delete DNS Servers.

        `dns`: - 'Local' to delete DNS server(s) defined under
                'Use these DNS Servers',
               - 'Root' to delete DNS server(s) defined under
                'Use the Internet's Root DNS Servers'
               - 'Sec' to delete Sec DNS server(s) defined under
                'Secondary DNS Servers'

        `dns_ip`: string of comma separated values of 1 or more DNS Server's IP address.
                Apply for 'Use these DNS Servers' option only

        `alt_ip`: string of comma separated values of 1 or more alternate DNS server's
                IP address
        """
        self._open_page()
        self._click_edit_settings_button()
        if dns.lower() == 'sec':
            if dns_ip is not None:
                self._info('Deleting Sec DNS Servers...')
                self._perform_delete_operation(regex_dns=REGEX_USER_SEC_DNS,\
                        ips=dns_ip)
        else:
            self._select_dns(dns)
            if dns_ip is not None:
                self._info('Deleting DNS Servers...')
                self._perform_delete_operation(regex_dns=REGEX_USER_DNS,\
                        ips=dns_ip)
            if alt_ip is not None:
                if dns.lower() == 'root':
                    self._info('Deleting Root Alternate DNS Servers...')
                    self._perform_delete_operation\
                        (regex_dns=REGEX_ROOT_ALT, ips=alt_ip)
                elif dns.lower() == 'local':
                    self._info('Deleting Alternate DNS Servers...')
                    self._perform_delete_operation(regex_dns=REGEX_USER_ALT,\
                            ips=alt_ip)
                else:
                    raise ValueError("Invalid input value  '%s' for "\
                            "'DNS Servers' it should either be 'Local' or "\
                            "'Root'" % (dns,))
        self._click_submit_button()

    def _perform_delete_all_operation(self, regex_dns=None):

        num_entry = int(
                self.get_matching_xpath_count(DNS_TBODY_ROW(regex_dns)))
        for i in range(num_entry):
            self.click_element(DNS_DEL(regex_dns, i),\
                     "don't wait")
        return num_entry

    def _delete_all_servers(self, dns='Local', servers=None):

        self._info('Deleting all DNS servers')
        if dns.lower() == 'local':
            if servers.lower() == 'dns':
                num_entry = self._perform_delete_all_operation(
                        regex_dns=REGEX_USER_DNS)
            else:
                num_entry = self._perform_delete_all_operation(
                        regex_dns=REGEX_USER_ALT)
        elif dns.lower() == 'root':
            num_entry = self._perform_delete_all_operation(
                    regex_dns=REGEX_ROOT_ALT)
        else:
            raise ValueError("Invalid input value  '%s' for 'DNS Servers' "\
                     "it should either be 'Local' or 'Root'" % (dns,))
        self._info('All DNS servers deleted')
        return num_entry

    def _perform_delete_operation(self, regex_dns=None,
                                  ips=None):

        ips = self._convert_to_tuple(ips)
        table_ips = self._get_table_row_values(regex_dns)
        for ip in ips:
            if ip not in table_ips:
                raise guiexceptions.GuiControlNotFoundError(
                        "'%s'" % (ip,), 'DNS')
            self._info('Deleting "%s"' % (ip,))
            for i, table_ip in enumerate(table_ips):
                if ip == table_ip:
                    self.click_element(DNS_DEL(regex_dns, i),\
                            "don't wait")
                    self._info("Deleted '%s'" % (ip,))

    def _add_alt_servers(self, alt_servers=None, dns=None, entry_index=None):

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

            # get number of existing dns servers
            if entry_index is None:
                entry_index = int(self.get_matching_xpath_count(
                    DNS_TBODY_ROW(regex_alt)))
            for i, obj in enumerate(alt_servers):
                # check if new entry should be added
                # if only text field is empty then do not click Add Row
                if entry_index == 1 and \
                        self.get_value(DNS_TABLE_FIELD(regex_alt, 0,
                            'IP')).strip() == '':
                    entry_index = 0
                else:
                    self.click_button(add_row_button, "don't wait")
                    self._info("Clicked 'Add Row' button")
                if type(obj.domain)==tuple:
                    domain_text = ','.join(obj.domain)
                else:
                    domain_text = obj.domain
                self.input_text(DNS_TABLE_FIELD(regex_alt,
                    entry_index, domain_field), domain_text)
                self._info('Added Domain(s) "%s"' % (domain_text,))
                if dns.lower() == 'root':
                    self.input_text(DNS_TABLE_FIELD(regex_alt,
                        entry_index, 'FQDN'), obj.fqdn)
                    self._info('Added DNS Server FQDN "%s"' % (obj.fqdn,))
                self.input_text(DNS_TABLE_FIELD(regex_alt,
                    entry_index, 'IP'), obj.ip)
                self._info('Added IP "%s"' % (obj.ip,))
                entry_index = entry_index + 1

    def _add_dns_servers(self, dns_servers=None, dns=None, entry_index=None):

        dns_add_row_field = 'user_dns_domtable_AddRow'
        if dns_servers is not None:
            self._info('Adding DNS Servers...')
            if dns.lower() == 'local':
                if entry_index is None:
                    entry_index = int(self.get_matching_xpath_count(
                        DNS_TBODY_ROW(REGEX_USER_DNS)
                        ))
                for i, obj in enumerate(dns_servers):
                    # check if new entry should be added
                    # if only text field is empty then do not click Add Row
                    if entry_index == 1 and \
                            self.get_value(DNS_TABLE_FIELD(REGEX_USER_DNS, 0,
                                'IP')).strip() == '':
                        entry_index = 0
                    else:
                        self.click_button(dns_add_row_field, "don't wait")
                        self._info("Clicked 'Add Row' button")
                    self.input_text(DNS_TABLE_FIELD(REGEX_USER_DNS,
                        entry_index, 'Pri'), obj.priority)
                    self._info('Added Priority "%s"' % (obj.priority,))
                    self.input_text(DNS_TABLE_FIELD(REGEX_USER_DNS,
                        entry_index, 'IP'), obj.ip)
                    self._info('Added IP "%s"' % (obj.ip,))
                    entry_index = entry_index + 1
            else:
                raise ValueError('Invalid input value  \'%s\' for \'DNS Servers\' ' \
                                          'it should either be \'Local\'' % (dns,))

    def _add_sec_dns_servers(self, dns_servers=None, dns=None, entry_index=None):

        dns_add_row_field = 'user_secondary_dns_domtable_AddRow'
        if dns_servers is not None:
            self._info('Adding DNS Servers...')
            if dns.lower() == 'sec':
                if entry_index is None:
                    entry_index = int(self.get_matching_xpath_count(
                        DNS_TBODY_ROW(REGEX_USER_SEC_DNS)
                        ))
                for i, obj in enumerate(dns_servers):
                    # check if new entry should be added
                    # if only text field is empty then do not click Add Row
                    if entry_index == 1 and \
                            self.get_value(DNS_TABLE_FIELD(REGEX_USER_SEC_DNS, 0,
                                'IP')).strip() == '':
                        entry_index = 0
                    else:
                        self.click_button(dns_add_row_field, "don't wait")
                        self._info("Clicked 'Add Row' button")
                    self.input_text(DNS_TABLE_FIELD(REGEX_USER_SEC_DNS,
                        entry_index, 'Pri'), obj.priority)
                    self._info('Added Priority "%s"' % (obj.priority,))
                    self.input_text(DNS_TABLE_FIELD(REGEX_USER_SEC_DNS,
                        entry_index, 'IP'), obj.ip)
                    self._info('Added IP "%s"' % (obj.ip,))
                    entry_index = entry_index + 1
            else:
                raise ValueError('Invalid input value  \'%s\' for \'DNS Servers\' ' \
                                          'it should either be \'Sec\'' % (dns,))

    def _select_dns(self, dns=None):

        dns_radio_button = {'local': 'dns_user',
                            'root': 'dns_root1'}
        if dns is not None:
            if dns.lower() == 'local':
                self._click_radio_button(dns_radio_button['local'])
                self._info("Selected to 'Use these DNS Servers'")
            elif dns.lower() == 'root':
                self._click_radio_button(dns_radio_button['root'])
                self._info("Selected to 'Use the Internet Root DNS Servers'")
            else:
                raise ValueError("Invalid input value  '%s' for "\
                        "'DNS Servers' it should either be 'Local' "\
                        "or 'Root'" % (dns,))

    def _select_routing_table(self, routing=None):

        routing_select = 'routing_table'
        routing_option = {'data': 'Data',
                          'management': 'Management'}

        if routing is not None:
            if not self._is_visible(routing_select):
                raise guiexceptions.GuiFeatureDisabledError\
                      ('Cannot select routing table, as disabled')
            if routing.lower() == 'data':
                self.select_from_list(routing_select, routing_option['data'])
                self._info('Selected Routing table: Data')
            elif routing.lower() == 'management':
                self.select_from_list(routing_select,
                        routing_option['management'])
                self._info('Selected Routing table: Management')
            else:
                raise ValueError('Invalid option for \'Routing Table\'')

    def _set_wait_before_timeout(self, timeout=None):

        timeout_field = 'ptr_timeout'
        if timeout is not None:
            self.input_text(timeout_field, timeout)
            self._info("Setting 'Wait Before Timing out Reverse 'DNS Lookups'"\
                    " : %s seconds" % (timeout,))

    def _set_preference(self, preference):
        self._click_radio_button(preference)
        self._info("Setting preference: %s" % preference)

    def _set_domain_search_list(self, domain=None):

        domain_serach_list_field = 'search_domains'
        if domain is not None:
            self.input_text(domain_serach_list_field, domain)
            self._info("Setting domain search list '%s'" % domain)

    def dns_add_local_server(self, dns_ip, priority=0):
        """Add Local DNS Server

        Parameters:
            - `dns_ip`: DNS Server IP Address
            - `priority`: Priority of DNS Server

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

    def dns_add_sec_server(self, dns_ip, priority=0):
        """Add Sec DNS Server

        Parameters:
            - `dns_ip`: Sec DNS Server IP Address
            - `priority`: Priority of Sec DNS Server

        Examples:
        | DNS Add Sec Server | 10.92.144.4 | |
        | DNS Add Sec Server | 192.168.1.1 | priority=10 |
        """
        dns = 'Sec'
        dns_server = DNSServer(dns_ip, priority)
        dns_servers = (dns_server,)

        self._info('Adding Sec DNS server...')
        self._open_page()
        self._click_edit_settings_button()
        self._add_sec_dns_servers(dns_servers, dns)
        self._click_submit_button()

    def dns_delete_local_servers(self, dns_ips):
        """Delete Local DNS Servers

        Parameters:
            - `dns_ips`: string of comma separated IP Addresses

        Examples:
        | DNS Delete Local Servers | 10.92.144.4 |
        | DNS Delete Local Servers | 192.168.1.1, 192.168.1.2 |
        """
        self._dns_delete('Local', dns_ips)

    def dns_delete_sec_servers(self, dns_ips):
        """Delete Secondary DNS Servers

        Parameters:
            - `dns_ips`: string of comma separated IP Addresses

        Examples:
        | DNS Delete Sec Servers | 10.92.144.4 |
        | DNS Delete Sec Servers | 192.168.1.1, 192.168.1.2 |
        """
        self._dns_delete('Sec', dns_ips)

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
            - `FQDN`: DNS Server Fully Qualified Domain Name.
                Apply for Internet's Root DNS Server only.

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

    def dns_delete_alternate_servers(self, dns_ips=None, dns='Local'):
        """Delete Alternate DNS Servers

        Parameters:
            - `dns_ips`: string of comma separated IP Addresses
            - `dns`:
                * 'Local' to add DNS server(s) defined under 'Use these DNS
                    Servers'
                * 'Root' to add DNS server(s) defined under 'Use the
                    Internet's Root DNS Servers'

        Examples:
        | DNS Delete Alternate Servers | 10.92.144.4 | |
        | DNS Delete Alternate Servers | dns_ips=192.168.1.1, 192.168.1.2 | dns=Root |
        """
        self._dns_delete(dns, alt_ip=dns_ips)

    def dns_delete_all_alternate_servers(self, dns='Local'):
        """Delete All Alternate DNS Servers

        Parameters:
            - `dns`:
                * 'Local' to add DNS server(s) defined under 'Use these DNS
                    Servers'
                * 'Root' to add DNS server(s) defined under 'Use the
                    Internet's Root DNS Servers'

        Examples:
        | DNS Delete All Alternate Servers | |
        | DNS Delete All Alternate Servers | dns=Root |
        """
        self._info('Deleting All Alternate DNS Servers...')
        self._open_page()
        self._click_edit_settings_button()
        self._delete_all_servers(dns, 'alt')
        self._click_submit_button()

    def dns_edit_settings(self,
                      dns=None,
                      routing=None,
                      preference='prefer-ipv4',
                      timeout=None,
                      domains=None):
        """Edit DNS settings.

        To add/delete DNS servers please use corresponding keywords:
            - `DNS Add Local Server`
            - `DNS Delete Local Servers`
            - `DNS Add Alternate Server`
            - `DNS Delete Alternate Servers`

        Parameters:
            - `dns`:
                * 'Local' to use Local DNS Servers,
                * 'Root' to use the Internet's Root DNS Servers

            - `routing`: Routing Table for DNS Traffic, 'Management' or 'Data'
            - `preference`: prefer-ipv4, prefer-ipv6 or only-ipv4
            - `timeout`: Wait Before Timing out Reverse DNS Lookups in seconds
            - `domains`: string of comma separated domains for domain search list

        Examples:
        | DNS Edit Settings | routing=Data | timeout=30 | domains=ironport.com, cisco.com |
        | DNS Edit Settings | dns=Root | routing=Management | timeout=30 |
        """
        self._info('Editting DNS settings...')
        self._open_page()
        self._click_edit_settings_button()
        self._select_routing_table(routing)
        self._set_preference(preference)
        self._set_wait_before_timeout(timeout)
        self._set_domain_search_list(domains)
        self._select_dns(dns)
        self._click_submit_button()

    def dns_clear_cache(self):
        """Clear DNS cache

        Example:
        | DNS Clear Cache |
        """
        CLEAR_CACHE="xpath=//input[@value='Clear DNS Cache']"
        CONFIRM_CLEAR_CACHE="xpath=//button[text()='Clear DNS Cache']"

        self._open_page()
        self.click_button(CLEAR_CACHE, "don't wait")
        self.click_button(CONFIRM_CLEAR_CACHE, "don't wait")
        # Validate errors on the page
        self._check_action_result()
