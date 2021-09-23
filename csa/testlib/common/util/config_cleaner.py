import importlib
import os

import common.socketwrapper as socket
import re
from collections import OrderedDict
from common.util.misc import Misc
from esa_intf import NETWORKS_MAPPING
from lxml import etree


class ConfigCleaner(object):
    """
    This class provides methods to modify or clean ESA/WSA/SMA configuration files.
    """

    def __init__(self, dut, dut_version = None):
        self.dut = dut
        self.client = socket.getfqdn()
        self.client_ipv4 = self._get_ipv4_address(self.client)
        self.client_ipv6 = self._get_ipv6_address(self.client)
        self.domain = self._get_domain()
        self.src_config_file = None
        self.dst_config_file = None
        self.xml_tree = None
        self.xml_root = None
        self.lab_env_file = 'environment.%s_lab' % self.domain
        self.lab_env = importlib.import_module(self.lab_env_file)

    def get_keyword_names(self):
        return [
            'config_cleaner_initiate',
            'config_cleaner_update_hostname',
            'config_cleaner_remove_hostname',
            'config_cleaner_update_interfaces',
            'config_cleaner_remove_interfaces',
            'config_cleaner_update_dns',
            'config_cleaner_remove_dns',
            'config_cleaner_update_routing',
            'config_cleaner_remove_routing',
            'config_cleaner_update_ethernet',
            'config_cleaner_remove_ethernet',
            'config_cleaner_remove_ports',
            'config_cleaner_save_config',
            # Below methods are specific to ESA
            'config_cleaner_remove_misc_max_disk_size',
            'config_cleaner_remove_euq_total_db_size',
            'config_cleaner_remove_tracking_global_max_db_size',
            'config_cleaner_update_smtp_routes',
            'config_cleaner_remove_smtp_routes',
            'config_cleaner_update_listeners_interface_name',
            'config_cleaner_remove_listeners_interface_name',
            'config_cleaner_update_listeners_hat',
            'config_cleaner_remove_listeners_hat',
            'config_cleaner_update_listeners_rat',
            'config_cleaner_remove_listeners_rat',
            'config_cleaner_update_alert_email_config',
            'config_cleaner_remove_alert_email_config',
            'config_cleaner_update_policy_content_filters',
            'config_cleaner_remove_policy_content_filters',
            'config_cleaner_update_policy_member',
            'config_cleaner_remove_policy_member',
            'config_cleaner_update_filters',
            'config_cleaner_remove_filters',
            'config_cleaner_update_euq_notify',
            'config_cleaner_remove_euq_notify',
            'config_cleaner_update_euq_access',
            'config_cleaner_remove_euq_access',
            'config_cleaner_update_ldap',
            'config_cleaner_remove_ldap',
            'config_cleaner_update_users',
            'config_cleaner_remove_users',
            'config_cleaner_update_aliasconfig',
            'config_cleaner_remove_aliasconfig',
            'config_cleaner_update_altsrchost',
            'config_cleaner_remove_altsrchost',
            'config_cleaner_update_delivery_interface',
            'config_cleaner_remove_delivery_interface',
            'config_cleaner_update_encryption_account_administrator_email',
            'config_cleaner_remove_encryption_account_administrator_email',
            'config_cleaner_update_mar_profiles',
            'config_cleaner_remove_mar_profiles',
            'config_cleaner_update_smtpauth_profiles',
        ]

    def config_cleaner_initiate(self, src_config_file = None,
                                dst_config_file = None):
        """
        This method needs to be called before any other keyword call.
        :param src_config_file: DUT config file location
        :param dst_config_file: Output config file location
        :return: None
        """
        self.src_config_file = src_config_file
        self.dst_config_file = dst_config_file
        self.xml_tree = etree.parse(self.src_config_file)
        self.xml_root = self.xml_tree.getroot()
        print '|  INFO | Source config file - %s' % self.src_config_file
        print '|  INFO | Destination config file - %s' % self.dst_config_file
        print '|  INFO | Successfully opened %s for parsing' % self.src_config_file

    def config_cleaner_update_hostname(self):
        """
        This methods updates the hostname attribute in the XML file.
        <hostname>NEW_HOSTNAME</hostname>
        :return: None
        """
        self.xml_root.find('hostname').text = self.dut
        print '| DEBUG | Successfully updated "hostname" attribute'

    def config_cleaner_remove_hostname(self):
        """
        This method removes the hostname attribute in the XML file.
        :return: None
        """
        self._remove_xml_element('hostname')
        print '| DEBUG | Successfully removed "hostname" attribute'

    def config_cleaner_update_interfaces(self):
        """
        This method  updates the following attributes of the interfaces
         attribute in the XML file:
         interface.interface_name: Interface name
         interface.interface_hostname: Interface hostname
         interface.ip: IPv4 address
         interface.netmask: IPv4 netmask
         interface.ip6: IPv6 address
         interface.ip6_prefix: IPv6 netmask/prefix
        :return: None
        """
        interfaces = self.xml_root.find('interfaces').findall('interface')
        for intf_obj in interfaces:
            interface_name = intf_obj.find('phys_interface').text
            hostname = self._get_hostname(interface_name)
            ipv4_address = self._get_ipv4_address(hostname)
            ipv6_address = self._get_ipv6_address(hostname)
            intf_obj.find('interface_name').text = hostname
            intf_obj.find('interface_hostname').text = hostname
            intf_obj.find('ip').text = ipv4_address
            if interface_name.lower() == 'management':
                intf_obj.find('netmask').text = NETWORKS_MAPPING[self.domain]['NETMASK']
            elif 'data' in interface_name.lower():
                intf_obj.find('netmask').text = NETWORKS_MAPPING[self.domain]['DATA_NETMASK']
            else:
                raise ValueError('Unknown interface - %s' % interface_name)
            if intf_obj.find('ip6') is not None:
                intf_obj.find('ip6').text = ipv6_address
                if interface_name.lower() == 'management':
                    intf_obj.find('ip6_prefix').text = NETWORKS_MAPPING[self.domain]['PREFIX']
                elif 'data' in interface_name.lower():
                    intf_obj.find('ip6_prefix').text = NETWORKS_MAPPING[self.domain]['DATA_PREFIX']
                else:
                    raise ValueError('Unknown interface - %s' % interface_name)
            else:
                print '| DEBUG | %s interface does not have IPv6 config' % interface_name
            print '| DEBUG | Successfully updated "interfaces.interface" ' \
                  ' attribute for %s interface' % interface_name
        print '| DEBUG | Successfully updated "interfaces" attribute'

    def config_cleaner_remove_interfaces(self):
        """
        This method removes the interfaces attribute from the XML file.
        :return: None
        """
        self._remove_xml_element('interfaces')
        print '| DEBUG | Successfully removed "interfaces" attribute'

    def config_cleaner_update_dns(self, dns_type = 'local'):
        """
        This method updates the dns.local_dns attribute in the XML file.
        :param dns_type: root | local
        :return: None
        """
        if dns_type == 'local':
            self.xml_root.find('dns').find('local_dns').find('dns_ip').text = \
                NETWORKS_MAPPING[self.domain]['DNS']
            print '| DEBUG | Successfully updated "dns.local_dns" attribute'
        else:
            print "|  WARN | Only local DNS server config can be updated by" \
                  " using this tool."

    def config_cleaner_remove_dns(self):
        """
        This method removes the dns attribute from the config file.
        :return: None
        """
        self._remove_xml_element('dns')
        print '| DEBUG | Successfully removed "dns" attribute'

    def config_cleaner_update_routing(self, ipv4_route = None, ipv6_route = None):
        """
        This method updates the following attribute of routing_tables attribute
        of the XML file:
        routing_table.routing_table_gateway: IPv4 & IPv6 default gateway.
        :param ipv4_route: IPv4 gateway address
        :param ipv6_route:  IPv6 gateway address
        :return: None
        """
        ipv4_route = ipv4_route or self._get_ipv4_route()
        ipv6_route = ipv6_route or self._get_ipv6_route()
        if self.xml_root.find('routing_tables') is not None:
            routes = self.xml_root.find('routing_tables').findall(
                'routing_table')
            for route_obj in routes:
                if route_obj.find('routing_table_ip_version').text == '6':
                    route_obj.find('routing_table_gateway').text = ipv6_route
                elif route_obj.find('routing_table_ip_version').text == '4':
                    route_obj.find('routing_table_gateway').text = ipv4_route
                else:
                    raise ValueError(
                        'Unknown IP version in routing table - %s' % route_obj.find(
                            'routing_table_ip_version').text)
                print '| DEBUG | Successfully updated "routing_tables.routing' \
                      '_table_gateway" attribute'
        else:
            print "|  WARN | Routing settings not configured"

    def config_cleaner_remove_routing(self):
        """
        This method removes the routing_tables attribute from the XML file.
        :return: None
        """
        self._remove_xml_element('routing_tables')
        print '| DEBUG | Successfully removed "routing_tables" attribute'

    def config_cleaner_update_ethernet(self):
        """
        This method updates the ethernet_settings.ethernet attribute in the
        XML file
        :return: None
        :Todo: Mapping of ethernets to mgmt & data interfaces
        """
        nics = self._get_nic_card_info()
        ethernets = self.xml_root.find('ethernet_settings').findall('ethernet')
        for nic in nics:
            pass

    def config_cleaner_remove_ethernet(self):
        """
        This method removes the ethernet_settings attribute from the XML file.
        :return: None
        """
        self._remove_xml_element('ethernet_settings')
        print '| DEBUG | Successfully removed "ethernet_settings" attribute'

    def config_cleaner_remove_ports(self):
        """
        This method removes the ports attribute from the XML file.
        :return: None
        """
        self._remove_xml_element('ports')
        print '| DEBUG | Successfully removed "ports" attribute'

    def config_cleaner_save_config(self):
        """
        This method saves the modified XML content to a file.
        :return: None
        """
        tree = etree.ElementTree(self.xml_root)
        tree.write(self.dst_config_file, pretty_print=True,
                   xml_declaration=True, encoding="utf-8")
        print '| DEBUG | Successfully saved modified config file - %s' % self.dst_config_file

    # Below methods are very specific to ESA
    def config_cleaner_remove_misc_max_disk_size(self):
        """
        This method removes the misc_max_disk_size attribute from the XML file.
        :return: None
        """
        self._remove_xml_element('misc_max_disk_size')
        print '| DEBUG | Successfully removed "misc_max_disk_size" attribute'

    def config_cleaner_remove_euq_total_db_size(self):
        """
        This method removes the euq_total_db_size attribute from the XML file.
        :return: None
        """
        self._remove_xml_element('euq_total_db_size', 'euq/euq_server')
        print '| DEBUG | Successfully removed "euq/euq_server/' \
              'euq_total_db_size" attribute'

    def config_cleaner_remove_tracking_global_max_db_size(self):
        """
        This method removes the tracking_global_max_db_size attribute from the XML file.
        :return: None
        """
        self._remove_xml_element('tracking_global_max_db_size', 'tracking')
        print '| DEBUG | Successfully removed "tracking/' \
              'tracking_global_max_db_size" attribute'

    def config_cleaner_update_smtp_routes(self, smtp_routes = None):
        """
        This method updates the smtp_routes attribute from the XML file.
        :return: None
        TODO: Take smtp_routes as a parameter and update the XML file
              smtp_routes will be a dictionary with key as domain name and
              value as destination address. Destination address will be a list
              which can hold multiple addresses for a particular domain
        """
        exchange_ip_2016 = self.lab_env.EXCHANGE_IP_2016
        exchange_ip_2013 = self.lab_env.EXCHANGE_IP_2013
        smtp_routes = self.xml_root.find('smtp_routes').findall('smtp_route')
        if smtp_routes:
            for smtp_route in smtp_routes:
                dest_domain = smtp_route.find('route_source_address').text
                dest_addresses = smtp_route.findall('route_destination_address')
                if 'NETWORK' in dest_domain:
                    dest_domain = dest_domain.replace('NETWORK', self.domain)
                    smtp_route.find('route_source_address').text = dest_domain

                for dest_address in dest_addresses:
                    dest_address_value = dest_address.text
                    if 'CLIENT_IPv4' in dest_address_value:
                        dest_address_value = dest_address_value.replace(
                            'CLIENT_IPv4', self.client_ipv4)
                    if 'CLIENT_IPv6' in dest_address:
                        dest_address_value = dest_address_value.replace(
                            'CLIENT_IPv6', self.client_ipv6)
                    if 'EXCHANGE_IP_2016' in dest_address_value:
                        dest_address_value = dest_address_value.replace(
                            'EXCHANGE_IP_2016', exchange_ip_2016)
                    if 'EXCHANGE_IP_2013' in dest_address_value:
                        dest_address_value = dest_address_value.replace(
                            'EXCHANGE_IP_2013', exchange_ip_2013)
                    dest_address.text = dest_address_value
                    print '| dest_domain -> %20s | dest_address -> %30s |' % (
                        dest_domain, dest_address_value)
                print '| DEBUG | Successfully updated "smtp_routes/' \
                      'smtp_route" attribute'
        else:
            print '|  WARN | %s does not have smtp_routes' % self.src_config_file

    def config_cleaner_remove_smtp_routes(self):
        """
        This method removes the smtp_routes attribute from the XML file.
        :return: None
        """
        self._remove_xml_element('smtp_routes')
        print '| DEBUG | Successfully removed "smtp_routes" attribute'

    def config_cleaner_update_listeners_interface_name(self):
        """
        This method updates the "listeners/listener/interface_name" attribute
        of the XML file
        :return: None
        """
        listeners = self.xml_root.find('listeners').findall('listener')
        for listener in listeners:
            if listener.find('listener_name').text.lower() == 'inboundmail':
                listener.find('interface_name').text = 'd1.' + self.dut
            elif listener.find('listener_name').text.lower() == 'outboundmail':
                listener.find('interface_name').text = 'd2.' + self.dut
                print '| DEBUG | Successfully removed "smtp_routes" attribute'
            else:
                raise ValueError('Unrecognized listener name - %s'
                                 % listener.find('listener_name').text)
            print '| DEBUG | Successfully updated "listeners/listener/' \
                  'interface_name" attribute'

    def config_cleaner_remove_listeners_interface_name(self):
        """
        This method removes the "listeners/listener/interface_name" attribute
        from XML file.
        :return: None
        """
        self._remove_xml_element('interface_name', 'listeners/listener')
        print '| DEBUG | Successfully removed "listeners/listener/' \
              'interface_name" attribute'

    def config_cleaner_update_listeners_hat(self, listener_config = None):
        """
        This method updates the listeners attribute from the XML file.
        :param listener_config: TODO
        :return:
        """
        client_d1_ipv4 = self._get_ipv4_address('d1.' + self.client)
        client_d1_ipv6 = self._get_ipv6_address('d1.' + self.client)
        client_d2_ipv4 = self._get_ipv4_address('d2.' + self.client)
        client_d2_ipv6 = self._get_ipv6_address('d2.' + self.client)
        client_data_cidr = NETWORKS_MAPPING[self.domain]['DATA_CIDR']
        client_data_prefix = NETWORKS_MAPPING[self.domain]['DATA_PREFIX']
        listeners = self.xml_root.find('listeners').findall('listener')
        for listener in listeners:
            listener_type = listener.find('type').text
            hat_config = listener.find('hat').text
            if listener_type.lower() == 'public':
                unknown_sender_group = '{client_d1_ipv4}/{client_d1_cidr}\n' \
                                       '{client_d2_ipv4}/{client_d2_cidr}\n' \
                                       '{client_d1_ipv6}/{client_d1_prefix}\n' \
                                       '{client_d2_ipv6}/{client_d2_prefix}'. \
                    format(client_d1_ipv4=client_d1_ipv4,
                           client_d1_cidr=client_data_cidr,
                           client_d2_ipv4=client_d2_ipv4,
                           client_d2_cidr=client_data_cidr,
                           client_d1_ipv6=client_d1_ipv6,
                           client_d1_prefix=client_data_prefix,
                           client_d2_ipv6=client_d2_ipv6,
                           client_d2_prefix=client_data_prefix)
                print '| DEBUG | UNKNOWNLIST Sender Group:\n%s\n' % unknown_sender_group
                new_hat_config = hat_config.replace(
                    'UNKNOWNLIST_SENDER_GROUP', unknown_sender_group)
                listener.find('hat').text = new_hat_config
            elif listener_type.lower() == 'private':
                relay_sender_group = '{client_d1_ipv4}/{client_d1_cidr}\n' \
                                     '{client_d2_ipv4}/{client_d2_cidr}\n' \
                                     '{client_d1_ipv6}/{client_d1_prefix}\n' \
                                     '{client_d2_ipv6}/{client_d2_prefix}'. \
                    format(client_d1_ipv4=client_d1_ipv4,
                           client_d1_cidr=client_data_cidr,
                           client_d2_ipv4=client_d2_ipv4,
                           client_d2_cidr=client_data_cidr,
                           client_d1_ipv6=client_d1_ipv6,
                           client_d1_prefix=client_data_prefix,
                           client_d2_ipv6=client_d2_ipv6,
                           client_d2_prefix=client_data_prefix)
                print '| DEBUG | RELAYLIST Sender Group:\n%s\n' % relay_sender_group
                new_hat_config = hat_config.replace(
                    'RELAYLIST_SENDER_GROUP', relay_sender_group)
                listener.find('hat').text = new_hat_config
            else:
                raise ValueError('Unknown listener type - %s' % listener_type)
            print '| DEBUG | Successfully updated "listeners/listener" attribute'

    def config_cleaner_remove_listeners_hat(self):
        """
        This method removes the listeners attribute from the XML file.
        :return: None
        """
        self._remove_xml_element('listeners')
        print '| DEBUG | Successfully removed "listeners" attribute'

    def config_cleaner_update_listeners_rat(self, rat_entry = None):
        """
        This method updates the "rat" attribute of the XML file.
        :param rat_entry: Dictionary containing existing domain name and new
        domain name.
        :return: None
        """
        listeners = self.xml_root.find('listeners').findall('listener')
        for listener in listeners:
            rat_entries = listener.find('rat').findall('rat_entry')
            for rat in rat_entries:
                rat_address = rat.find('rat_address').text
                if rat_entry:
                    for domain, new_domain in rat_entry.items():
                        if rat_address.lower() == domain.lower():
                            rat.find('rat_address').text = new_domain
                        print '| DEBUG | Successfully updated "rat/rat_entry/' \
                              'rat_address" attribute for domain %s' % domain
                else:
                    if 'NETWORK' in rat_address:
                        new_rat_address = rat_address.replace('NETWORK',
                                                              self.domain)
                        rat.find('rat_address').text = new_rat_address
                        print '| DEBUG | Successfully updated "rat/rat_entry/' \
                              'rat_address" attribute'

    def config_cleaner_remove_listeners_rat(self):
        """
        This method removes the "rat" entry from the XML file.
        :return: None
        """
        self._remove_xml_element('rat')
        print '| DEBUG | Successfully removed "rat" attribute'

    def config_cleaner_update_alert_email_config(self):
        alert_classes = self.xml_root.find('alert_email_config').findall(
            'alert_class')
        for alert_class in alert_classes:
            alert_email = alert_class.find('alert_severity').find(
                'email_address').text
            new_alert_email = alert_email.replace('USERNAME', os.getenv(
                'USER') or 'testuser')
            alert_class.find('alert_severity').find(
                'email_address').text = new_alert_email
            print '| DEBUG | Successfully updated "alert_email_config/' \
                  'alert_class/alert_severity/email_address" attribute'

    def config_cleaner_remove_alert_email_config(self):
        """
        This method removes the alert_email_config attribute from the XML file.
        :return: None
        """
        self._remove_xml_element('alert_email_config')
        print '| DEBUG | Successfully removed "alert_email_config" attribute'

    def config_cleaner_update_policy_content_filters(self, content_filter_type = 'All'):
        """
        This method updates the content_filters attribute of the XML file.
        :param content_filter_type:
        :return: None
        """
        incoming_content_filters = self.xml_root.find('perrcpt_policies').find(
            'inbound_policies').find('content_filters').findall(
            'content_filter')
        outgoing_content_filters = self.xml_root.find('perrcpt_policies').find(
            'outbound_policies').find('content_filters').findall(
            'content_filter')
        if content_filter_type.lower() == 'incoming':
            for cf in incoming_content_filters:
                cf_rule_data = cf.find('rule').find('rule_data').text
                new_cf_rule_data = cf_rule_data.replace('CLIENT_HOSTNAME',
                                                        self.client)
                cf.find('rule').find('rule_data').text = new_cf_rule_data
                print '| DEBUG | Successfully updated "perrcpt_policies/' \
                      'inbound_policies/content_filter" attribute'
        elif content_filter_type.lower() == 'outgoing':
            for cf in outgoing_content_filters:
                cf_rule_data = cf.find('rule').find('rule_data').text
                new_cf_rule_data = cf_rule_data.replace('CLIENT_HOSTNAME',
                                                        self.client)
                cf.find('rule').find('rule_data').text = new_cf_rule_data
                print '| DEBUG | Successfully updated "perrcpt_policies/' \
                      'outbound_policies/content_filter" attribute'
        else:
            for cf in incoming_content_filters + outgoing_content_filters:
                cf_rule_data = cf.find('rule').find('rule_data').text
                if cf_rule_data:
                    new_cf_rule_data = cf_rule_data.replace('CLIENT_HOSTNAME',
                                                        self.client)
                    cf.find('rule').find('rule_data').text = new_cf_rule_data
                    print '| DEBUG | Successfully updated "perrcpt_policies/' \
                      'inbound_policies/content_filter" and "perrcpt_policies/' \
                      'outbound_policies/content_filter" attributes'

    def config_cleaner_remove_policy_content_filters(self, content_filter_type = None):
        """
        This method removes the content_filters attribute from the XML file.
        :return: None
        """
        if content_filter_type.lower() == 'incoming':
            self._remove_xml_element('content_filters',
                                     'perrcpt_policies/inbound_policies')
            print '| DEBUG | Successfully removed the "perrcpt_policies/' \
                  'inbound_policies/content_filters" attribute'
        elif content_filter_type.lower() == 'outgoing':
            self._remove_xml_element('content_filters',
                                     'perrcpt_policies/outbound_policies')
            print '| DEBUG | Successfully removed the "perrcpt_policies/' \
                  'outbound_policies/content_filters" attribute'
        else:
            self._remove_xml_element('content_filters',
                                     'perrcpt_policies/inbound_policies')
            self._remove_xml_element('content_filters',
                                     'perrcpt_policies/outbound_policies')
            print '| DEBUG | Successfully removed the "perrcpt_policies/' \
                  'inbound_policies/content_filters" and "perrcpt_policies/' \
                  'outbound_policies/content_filters" attributes'

    def config_cleaner_update_policy_member(self):
        """
        This method updates the "perrcpt_policies/inbound_policies/policy/
        policy_member/sender", "perrcpt_policies/inbound_policies/policy/
        policy_member/receiver", "perrcpt_policies/outbound_policies/policy/
        policy_member/sender" and perrcpt_policies/outbound_policies/policy/
        policy_member/receiver" attributes
        :return: None
        """
        incoming_policies = self.xml_root.find('perrcpt_policies').find(
            'inbound_policies').findall('policy')
        outgoing_policies = self.xml_root.find('perrcpt_policies').find(
            'outbound_policies').findall('policy')
        for policy in incoming_policies + outgoing_policies:
            policy_name = policy.find('policy_name').text
            try:
                policy_sender = policy.find('policy_member').find('sender').text
                if 'CLIENT_HOSTNAME' in policy_sender:
                    new_policy_sender = policy_sender.replace('CLIENT_HOSTNAME',
                                                              self.client)
                    policy.find('policy_member').find(
                        'sender').text = new_policy_sender
                    print '| DEBUG | Successfully updated "perrcpt_policies/' \
                          'inbound_policies/policy/policy_member/sender"' \
                          ' attribute'
            except AttributeError:
                print '| DEBUG | Policy %s does not have a sender' % policy_name
            try:
                policy_receiver = policy.find('policy_member').find(
                    'receiver').text
                if 'CLIENT_HOSTNAME' in policy_receiver:
                    new_policy_receiver = policy_receiver.replace(
                        'CLIENT_HOSTNAME',
                        self.client)
                    policy.find('policy_member').find(
                        'receiver').text = new_policy_receiver
                    print '| DEBUG | Successfully updated "perrcpt_policies/' \
                          'inbound_policies/policy/policy_member/receiver"' \
                          ' attribute'
            except AttributeError:
                print '| DEBUG | Policy %s does not have a receiver' % policy_name

    def config_cleaner_remove_policy_member(self):
        """
        TBD
        :return: None
        """
        pass

    def config_cleaner_update_filters(self):
        """
        This method updates the "filters" attribute of the XML file.
        :return:
        """
        filters = self.xml_root.find('filters').text
        new_filters = filters.replace('CLIENT_HOSTNAME', self.client)
        self.xml_root.find('filters').text = new_filters
        print '| DEBUG | Successfully updated the "filters" attribute'

    def config_cleaner_remove_filters(self):
        """
        This method removes the "filters" attribute from the XML file.
        :return: None
        """
        self._remove_xml_element('filters')
        print '| DEBUG | Successfully removed the "filters" attribute'

    def config_cleaner_update_euq_notify(self):
        """
        This method updates the "euq/euq_notify/euq_notify_bounce_address" and
        "euq/euq_notify/euq_notify_from_address" attributes of the XML file.
        :return: None
        """
        euq_notify_bounce_address = self.xml_root.find('euq').find(
            'euq_notify').find('euq_notify_bounce_address').text
        new_euq_notify_bounce_address = euq_notify_bounce_address.replace(
            'CLIENT_HOSTNAME', self.client)
        self.xml_root.find('euq').find(
            'euq_notify').find(
            'euq_notify_bounce_address').text = new_euq_notify_bounce_address
        print '| DEBUG | Successfully updated the "euq/euq_notify/' \
              'euq_notify_bounce_address" attribute'
        euq_notify_from_address = self.xml_root.find('euq').find(
            'euq_notify').find('euq_notify_from_address').text
        new_euq_notify_from_address = euq_notify_from_address.replace(
            'DUT_HOSTNAME', self.dut)
        self.xml_root.find('euq').find(
            'euq_notify').find(
            'euq_notify_from_address').text = new_euq_notify_from_address
        print '| DEBUG | Successfully updated the "euq/euq_notify/' \
              'euq_notify_from_address" attribute'

    def config_cleaner_remove_euq_notify(self):
        """
        This method removes the "euq/euq_notify" attribute from XML file.
        :return:
        """
        self._remove_xml_element('euq_notify', 'euq')
        print '| DEBUG | Successfully removed the "euq/euq_notify" attribute'

    def config_cleaner_update_euq_access(self):
        """
        This method updates the "euq/euq_access/euq_ldap_auth_query" attribute
        of the XML file.
        :return: None
        """
        ldap_server = self.lab_env.LDAP_AUTH_SERVER
        euq_ldap_auth_query = self.xml_root.find('euq').find(
            'euq_access').find('euq_ldap_auth_query').text
        new_euq_ldap_auth_query = euq_ldap_auth_query.replace('LDAP_SERVER',
                                                              ldap_server)
        self.xml_root.find('euq').find(
            'euq_access').find(
            'euq_ldap_auth_query').text = new_euq_ldap_auth_query
        print '| DEBUG | Successfully updated the "euq/euq_access/' \
              'euq_ldap_auth_query" attribute'

    def config_cleaner_remove_euq_access(self):
        """
        This method removes the "euq/euq_access" attribut from the XML file.
        :return: None
        """
        self._remove_xml_element('euq_access', 'euq')
        print '| DEBUG | Successfully removed the "euq/euq_access" attribute'

    def config_cleaner_update_ldap(self):
        """
        This method updates the "ldap/ldap_server/ldap_server_name", "ldap/
        ldap_server/ldap_server_hostname", "ldap/ldap_query/ldap_query_name"
        and "ldap/ldap_query/ldap_query_server" attributes of the XML file.
        :return: None
        """
        ldap_server = self.lab_env.LDAP_AUTH_SERVER
        self.xml_root.find('ldap').find('ldap_server').find(
            'ldap_server_name').text = ldap_server
        print '| DEBUG | Successfully udpated the "ldap/ldap_server/' \
              'ldap_server_name" attribute'
        self.xml_root.find('ldap').find('ldap_server').find(
            'ldap_server_hostname').text = ldap_server
        print '| DEBUG | Successfully udpated the "ldap/ldap_server/' \
              'ldap_server_hostname" attribute'
        ldap_query_name = self.xml_root.find('ldap').find('ldap_query').find(
            'ldap_query_name').text
        new_ldap_query_name = ldap_query_name.replace('LDAP_SERVER',
                                                      ldap_server)
        self.xml_root.find('ldap').find('ldap_query').find(
            'ldap_query_name').text = new_ldap_query_name
        print '| DEBUG | Successfully udpated the "ldap/ldap_query/' \
              'ldap_query_name" attribute'
        self.xml_root.find('ldap').find('ldap_query').find(
            'ldap_query_server').text = ldap_server
        print '| DEBUG | Successfully udpated the "ldap/ldap_query/' \
              'ldap_query_server" attribute'

    def config_cleaner_remove_ldap(self):
        """
        This method removes the "ldap" attribute from XML file.
        :return: None
        """
        self._remove_xml_element('ldap')
        print '| DEBUG | Successfully removed the "ldap" attribute'

    def config_cleaner_update_users(self):
        """
        TBD
        :return:
        """
        pass

    def config_cleaner_remove_users(self):
        """
        This method removes the "users/user" attribute from XML file.
        :return: None
        """
        users = self.xml_root.find('users').findall('user')
        for user in users:
            if user.find('username').text == 'admin':
                continue
            else:
                user.getparent().remove(user)
                print '| DEBUG | Successfully removed the "users/user" attribute'

    def config_cleaner_update_aliasconfig(self, alias_config = None):
        """
        This method updates the aliases attribute of the XML config file.
        :param alias_config: alias config string. eg: @foo.com: test@foo.com
        :return: None
        """
        if not alias_config:
            if 'USERNAME' in self.xml_root.find('aliases').text:
                new_alias_config = self.xml_root.find('aliases').text.replace('USERNAME',
                                                                              os.environ['USER'])
                self.xml_root.find('aliases').text = new_alias_config
                print '| DEBUG | Successfully updated aliases attribute'
        else:
            self.xml_root.find('aliases').text = alias_config
            print '| DEBUG | Successfully updated aliases attribute'

    def config_cleaner_remove_aliasconfig(self):
        """
        This method removes the aliases attribute from the XML config file.
        :return:
        """
        self._remove_xml_element('aliases')

    def config_cleaner_update_altsrchost(self):
        """
        This method updates the altsrchost attribute of the XML config file.
        :return: None
        """
        altsrchosts = self.xml_root.find('altsrchost').findall('altsrchost_entry')
        if altsrchosts:
            for altsrchost in altsrchosts:
                if altsrchost.find('altsrchost_address').text == 'virtual@qa54.qa':
                    altsrchost.find('interface_name').text = self._get_hostname('Data 2')
                    print '| DEBUG | Successfully updated altsrchost attribute'
        else:
            print '| DEBUG | altsrchost config not found'

    def config_cleaner_remove_altsrchost(self):
        """
        This method removes the altsrchost attribute from the XML config file.
        :return:
        """
        self._remove_xml_element('altsrchost')

    def config_cleaner_update_delivery_interface(self, delivery_interface = None):
        """
        This method updates the delivery_interface attribute of the XML config file.
        :param delivery_interface: DUT interface hostname to be used for mail delivery
        :return: None
        """
        if not delivery_interface:
            self.xml_root.find('delivery_interface').text = self._get_hostname('Management')
            print '| DEBUG | Successfully updated delivery_interface attribute'
        else:
            self.xml_root.find('delivery_interface').text = delivery_interface
            print '| DEBUG | Successfully updated delivery_interface attribute'

    def config_cleaner_remove_delivery_interface(self):
        """
        This method removes the delivery_interface attribute from the XML config file.
        :return:
        """
        self._remove_xml_element('delivery_interface')

    def config_cleaner_update_encryption_account_administrator_email(self):
        """
        This method updates the encryption_account_administrator_email attribute of the XML config file.
        :return: None
        """
        encryption_administrator_email = self.xml_root.find('encryption').find(
            'encryption_account_administrator_email').text
        new_encryption_administrator_email = encryption_administrator_email.replace(
            'DUT_HOSTNAME', self.dut)
        self.xml_root.find('encryption').find(
            'encryption_account_administrator_email').text = new_encryption_administrator_email
        print '| DEBUG | Successfully updated encryption_account_administrator_email attribute'

    def config_cleaner_remove_encryption_account_administrator_email(self):
        """
        This method removes the encryption_account_administrator_email attribute from the XML config file.
        :return:
        """
        self._remove_xml_element('encryption_account_administrator_email', 'encryption')

    def config_cleaner_update_mar_profiles(self, mar_profiles = None):
        """
        This method updates the mar_profiles attribute from the XML file.
        :return: None
        """
        exchange_ip_2016 = self.lab_env.EXCHANGE_IP_2016
        exchange_ip_2013 = self.lab_env.EXCHANGE_IP_2013
        mar_profiles = self.xml_root.find('mar_mailbox_config').find('mar_profiles')\
            .findall('mar_profile')
        if mar_profiles:
            for mar_profile in mar_profiles:
                mar_connection_parameters = mar_profile.findall('mar_connection_parameters')
                for mar_connection_parameter in mar_connection_parameters:
                    mar_hosts = mar_connection_parameter.findall('mar_host')
                    for mar_host in mar_hosts:
                        mar_host_value = mar_host.text
                        if 'EXCHANGE_IP_2016' in mar_host_value:
                            mar_host_value = mar_host_value.replace(
                                'EXCHANGE_IP_2016', exchange_ip_2016)
                        if 'EXCHANGE_IP_2013' in mar_host_value:
                            mar_host_value = mar_host_value.replace(
                                'EXCHANGE_IP_2013', exchange_ip_2013)
                        mar_host.text = mar_host_value
            print '| DEBUG | Successfully updated "mar_profiles/' \
                      'mar_host" attribute'
        else:
            print '|  WARN | %s does not have mar_profiles' % self.src_config_file

    def config_cleaner_remove_mar_profiles(self):
        """
        This method removes the mar_profiles attribute from the XML file.
        :return: None
        """
        self._remove_xml_element('mar_mailbox_config')
        print '| DEBUG | Successfully removed "mar_mailbox_config" attribute'

    def config_cleaner_update_smtpauth_profiles(self):
        """
        This method updates the smtpauth_profiles attribute from the XML file.
        :return: None
        """
        smtpauth_forward_hostname = self.xml_root.find('smtpauth_profiles').find(
            'smtpauth_profile').find('smtpauth_forward_server_group').find(
            'smtpauth_forward_server').find('smtpauth_forward_hostname').text
        new_smtpauth_forward_hostname = smtpauth_forward_hostname.replace(
            'DUT_HOSTNAME', self.dut)
        self.xml_root.find('smtpauth_profiles').find('smtpauth_profile').find(
            'smtpauth_forward_server_group').find('smtpauth_forward_server').find(
            'smtpauth_forward_hostname').text = new_smtpauth_forward_hostname
        print
        '| DEBUG | Successfully updated the "smtpauth_profiles/smtpauth_profile/' \
        'smtpauth_forward_hostname" attribute'
        smtpauth_forward_interface = self.xml_root.find('smtpauth_profiles').find(
            'smtpauth_profile').find('smtpauth_forward_server_group').find(
            'smtpauth_forward_server').find('smtpauth_forward_interface').text
        new_smtpauth_forward_interface = smtpauth_forward_interface.replace(
            'DUT_HOSTNAME', self.dut)
        self.xml_root.find('smtpauth_profiles').find(
            'smtpauth_profile').find('smtpauth_forward_server_group').find(
            'smtpauth_forward_server').find(
            'smtpauth_forward_interface').text = new_smtpauth_forward_interface
        print
        '| DEBUG | Successfully updated the "smtpauth_profiles/smtpauth_profile/' \
        'smtpauth_forward_hostname" attribute'

    ########################### Helper Methods ##############################
    def _get_hostname(self, interface_type):
        if interface_type.lower() == 'management':
            hostname = self.dut
        elif interface_type.lower() == 'data 1':
            hostname = 'd1.' + self.dut
        elif interface_type.lower() == 'data 2':
            hostname = 'd2.' + self.dut
        else:
            print "| ERROR | unknow interface type %s" % interface_type
            hostname = None
        print '| INFO | Hostname - %s' % hostname
        return hostname

    def _get_domain(self):
        domain = self.dut.split('.')[-1]
        print '| INFO | Domain - %s' % domain
        return domain

    def _get_ipv4_address(self, hostname = None):
        hostname = hostname or self.dut
        ipv4_address = socket.gethostbyname(hostname, 'ipv4')
        print '| INFO | %s IPv4 address - %s' % (hostname, ipv4_address)
        return ipv4_address

    def _get_ipv6_address(self, hostname = None):
        hostname = hostname or self.dut
        ipv6_address = socket.gethostbyname(hostname, 'ipv6')
        print '| INFO | %s IPv6 address - %s' % (hostname, ipv6_address)
        return ipv6_address

    def _get_ipv4_route(self):
        return '.'.join(self._get_ipv4_address().split('.')[:-1] + ['1'])

    def _get_ipv6_route(self):
        return ":".join(self._get_ipv6_address().split(':')[:-1] + ['1'])

    def _get_nic_cards_info(self):
        mac_addresses = OrderedDict()
        ifconfig_output = Misc(self.dut, None).run_on_dut('ifconfig')
        nics = ifconfig_output.split('status')
        loopback_nic = nics.pop()  ## Discard loopback interface
        for nic in nics:
            nic_name = re.search(r'(\w+):\s+flags', nic).group(1)
            mac_address = re.search(r'ether\s+(.*)\n', nic).group(1)
            mac_addresses[nic_name] = mac_address
        print "| DEBUG | Mac Addresses - %s" % mac_addresses
        return mac_addresses

    def _remove_xml_element(self, element, parent_elements = None):
        if parent_elements:
            parents = parent_elements.split('/')
            pel = self.xml_root.find(parents[0])
            for parent in parents[1:]:
                pel = pel.find(parent)
        else:
            pel = self.xml_root
        el = pel.find(element)
        el.getparent().remove(el)


if __name__ == "__main__":
    cc = ConfigCleaner('c190q02.cs2')
    cc.config_cleaner_initiate(
        '/home/aminath/public_html/config_cleaner/input/esa004.auto-11.0.1-027-vm51bsd0135.auto.xml',
        '/home/aminath/public_html/config_cleaner/output/esa_upq_config_11.0.1-027_c190q02.cs2_vm09bsd0171.cs2.xml')
    cc.config_cleaner_update_hostname()
    cc.config_cleaner_update_interfaces()
    cc.config_cleaner_update_dns()
    cc.config_cleaner_update_routing()
    cc.config_cleaner_update_smtp_routes()
    cc.config_cleaner_update_mar_profiles()
    cc.config_cleaner_update_smtpauth_profiles()
    cc.config_cleaner_update_listeners_interface_name()
    cc.config_cleaner_update_listeners_hat()
    cc.config_cleaner_update_listeners_rat()
    cc.config_cleaner_update_policy_content_filters()
    cc.config_cleaner_update_policy_member()
    cc.config_cleaner_update_filters()
    cc.config_cleaner_update_alert_email_config()
    cc.config_cleaner_update_euq_notify()
    cc.config_cleaner_update_euq_access()
    cc.config_cleaner_update_ldap()
    cc.config_cleaner_update_aliasconfig()
    cc.config_cleaner_update_altsrchost()
    cc.config_cleaner_update_delivery_interface()
    cc.config_cleaner_remove_ethernet()
    cc.config_cleaner_remove_ports()
    # cc.config_cleaner_remove_users()
    cc.config_cleaner_remove_misc_max_disk_size()
    cc.config_cleaner_remove_euq_total_db_size()
    cc.config_cleaner_remove_tracking_global_max_db_size()
    cc.config_cleaner_save_config()
