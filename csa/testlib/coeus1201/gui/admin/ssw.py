#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/gui/admin/ssw.py#2 $
# $DateTime: 2019/11/20 00:32:44 $
# $Author: uvelayut $

from common.util.misc import Misc
from common.gui.guicommon import (GuiCommon, Wait)
from common.util.systools import SysTools

import os
import common.Variables

class SystemSetupWizard(GuiCommon):

    """GUI configurator for 'System Administration -> System Setup Wizard'
       page.

       *Variable files for interface and networks*

       Two variable files can be imported to provide constants that can
       be used as input to some of the parameters below.  Please refer
       to http://eng.ironport.com/docs/qa/sarf/keyword/common/wsa_intf.rst
       and http://eng.ironport.com/docs/qa/sarf/keyword/common/network.rst
       documents on how to use them.
    """

    def get_keyword_names(self):
        return ['ssw_run']
    # This timeout is required for pages to complete loading
    # https://cdetsng.cisco.com/webui/#view=CSCun08605
    SSW_TIMEOUT = 15

    def _open_page(self):
        """Go to System Setup Wizard page."""

        self._navigate_to('System Administration', 'System Setup Wizard')

    def _reset_config(self, reset_network):
        """Reset configuration if it is required."""

        reset_config_button = 'action:Next'
        reset_config_timeout = 180
        reset_config_text = 'Reset Configuration'
        reset_network_checkbox = 'xpath=//input [@id="reset_network"]'
        reset_network = str(reset_network).lower()

        if self._is_text_present(reset_config_text):
            if reset_network == 'yes':
                self._select_checkbox(reset_network_checkbox)
            elif reset_network == 'no':
                self._unselect_checkbox(reset_network_checkbox)
            else:
                self._info('reset_network parameter should be "yes" or "no". Given: "%s"' % reset_network)

            self.click_button(reset_config_button, 'dont_wait')
            Wait(
                lambda: not (self._is_text_present(reset_config_text)),
                timeout=reset_config_timeout
            ).wait()
            
            self.SSW_TIMEOUT = 60
            try:
                self._wait_until_text_is_present('System Administration',timeout=self.SSW_TIMEOUT)
                self._open_page()
            except:
                self._info("System Administration Text was not present (Old behavior). Continuing with SSW (Hybrid Merge Behavior)")
                pass
            
            self.SSW_TIMEOUT = 15
        else:
            self._info("Reset Config Button was not present.")
        return
            
    def _add_license(self, license_file):
        ' Add license through CLI command loadlicense'

        if not license_file:
            license_file = os.environ["SARF_HOME"] + os.sep + os.path.join('tests','testdata','virtual','super.xml')
        
        filename = license_file.rpartition('/')[2]
        destination = os.sep + os.path.join('data','pub','configuration') + os.sep + filename
        
        Misc(self.dut, self.dut_version).copy_file_to_dut(license_file, destination)
        cli = SysTools(self.dut, self.dut_version)._get_cli()
        self._info('Adding license during SSW...')
        licensetext = cli.loadlicense()._load_license_from_file(filename=filename)
        self._info('Output from loadlicense command(SSW): %s' %licensetext)

    def _process_license_agreement_page(self):
        """Interaction on license agreement page."""
        self._info("Licence agreement page")
        agree_checkbox = 'license_agree'
        begin_button = 'begin_setup'

        self._select_checkbox(agree_checkbox)
        self.click_button(begin_button)

    #<10.5.1 Hybrid: Code changes Merge>
    def _process_appliance_mode_page(self, appliance_mode):
        """ Select Appliance Mode of Operation """
        OPTIONS = {
                                'standard':'xpath=//*[@id="mode_standard"]',
                                'cloud':'xpath=//*[@id="mode_connector"]',
                                'hybrid':'xpath=//*[@id="mode_hybrid"]',
        }

        if appliance_mode != None:
            if appliance_mode in OPTIONS.keys():
                self._click_radio_button(OPTIONS[appliance_mode])
            else:
                raise ValueError("appliance_mode '" + appliance_mode + "' should be in " + str(OPTIONS.keys()))
        self._click_next_button()
    #</10.5.1 Hybrid: Code changes Merge>
    
    def _process_system_setting_page(self, dns, region, country,
                                     timezone,
                                     appliance_mode):
        """Interaction on system settings page."""

        self._info("Licence agreement page")
        dns_field = 'user_dns0'
        region_option_button = 'region'
        country_option_button = 'country'
        timezone_option_button = 'timezone'

        self._wait_until_text_is_present('System Settings',timeout=self.SSW_TIMEOUT)

        self.input_text(dns_field, dns)
        self.select_from_list(region_option_button, region)
        self.select_from_list(country_option_button, country)
        self.select_from_list(timezone_option_button, timezone)
        self._select_appliance_mode(appliance_mode)
        self._click_next_button()

    def _select_appliance_mode(self, appliance_mode):
        """ Select Appliance Mode of Operation """
        #<10.5.1 Hybrid: Code changes Merge>
        APPLIANCE_MODE = "xpath=//*[contains(text(), 'Appliance Mode of Operation')]"
        try:
            if self._is_element_present(APPLIANCE_MODE):
                      
                OPTIONS = {
                                        'standard':'xpath=//input[@id="scansafe_disabled"]',
                                        'cloud':'xpath=//input[@id="scansafe_enabled"]'
                }
                if appliance_mode != None:
                    if appliance_mode in OPTIONS.keys():
                        self._click_radio_button(OPTIONS[appliance_mode])
                    else:
                        raise ValueError("appliance_mode '%s' should be one of the following\n%s" %(appliance_mode, str(OPTIONS.keys())))
        except:
            pass
        #</10.5.1 Hybrid: Code changes Merge>
        
    def _process_cloud_setting_page(self,
        cloud_server1, cloud_server2, cloud_server3,
        cloud_failure_handling,
        cloud_auth_scheme, cloud_auth_key,
        ):
        """Interaction on cloud settings page."""
        self._wait_until_text_is_present("Cloud Web Security Connector Settings",timeout=self.SSW_TIMEOUT)
        self._info("Cloud Settings page")
        self._set_cloud_servers(cloud_server1, cloud_server2, cloud_server3)
        self._set_cloud_failure_handling(cloud_failure_handling)
        self._set_cloud_auth_scheme(cloud_auth_scheme, cloud_auth_key)
        self._click_next_button()

    def _set_cloud_servers(self, cloud_server1, cloud_server2, cloud_server3):
        """ Set Cloud Web Security Proxy Servers"""
        TEXT1 = 'xpath=//input[@id="scansafe_servers[0][host]"]'
        TEXT2 = 'xpath=//input[@id="scansafe_servers[1][host]"]'
        TEXT3 = 'xpath=//input[@id="scansafe_servers[2][host]"]'
        if cloud_server1 != None:
            self.input_text(TEXT1, cloud_server1)
        if cloud_server2 != None:
            self.input_text(TEXT2, cloud_server2)
        if cloud_server3 != None:
            self.input_text(TEXT3, cloud_server3)

    def _set_cloud_failure_handling(self, cloud_failure_handling):
        """ Specify how to handle requests if all specified Cloud Web Security
         Proxy servers fail """
        OPTIONS = {'connect':'xpath=//input[@value="connect"]',
                 'drop':'xpath=//input[@value="drop"]'}
        if cloud_failure_handling != None:
            if cloud_failure_handling in OPTIONS.keys():
                self._click_radio_button(OPTIONS[cloud_failure_handling])
            else:
                raise ValueError("cloud_failure_handling '" + \
                    cloud_failure_handling + \
                    "' should be in " + str(OPTIONS.keys()))

    def _set_cloud_auth_scheme(self, cloud_auth_scheme, cloud_auth_key):
        """ Specify Cloud Web Security Authorization Scheme """
        OPTIONS = {'ip':'xpath=//input[@value="ip"]',
                 'key':'xpath=//input[@value="key"]'}
        TEXT = 'xpath=//input[@id="scansafe_license"]'
        if cloud_auth_scheme != None:
            if cloud_auth_scheme in OPTIONS.keys():
                self._click_radio_button(OPTIONS[cloud_auth_scheme])
            else:
                raise ValueError("cloud_auth_scheme '" + \
                    cloud_auth_scheme + \
                    "' should be in " + str(OPTIONS.keys()))
        if cloud_auth_key != None:
            if self._is_visible(TEXT):
                self.input_text(TEXT, cloud_auth_key)
            else:
                self._info("Can't set cloud_auth_key " + \
                    TEXT + " to " + cloud_auth_key)

    def _process_network_context_page(self):
        """Interaction on network contect page."""

        self._wait_until_text_is_present('Network Context',timeout=self.SSW_TIMEOUT)
        self._info("Network Context page")
        self._click_next_button()

    def _process_network_intf_and_wiring_page(self,
        proxy_port,
        m1_ipv6_addr='',
        p1_hostname='',
        p1_ipv4_addr='',
        p1_ipv6_addr=''
        ):
        """Interaction on network interfaces and wiring page."""

        self._info("Network interfaces and wiring page")
        use_m1_port_for_mgmt_checkbox = 'use_mgmt'
        m1_ipv6_addr_field = 'management_ipv6'
        p1_ipv4_addr_field = 'data_ipv4'
        p1_ipv6_addr_field = 'data_ipv6'
        p1_hostname_field  = 'data_hostname'
        simplex_TAP_radio_button = 'monitor_simplex'

        self._wait_until_text_is_present('Network Interfaces and Wiring',timeout=self.SSW_TIMEOUT)

        self.input_text(m1_ipv6_addr_field, m1_ipv6_addr)
        if proxy_port != 'mgmt':
            self.select_checkbox(use_m1_port_for_mgmt_checkbox)
            self.input_text(p1_ipv4_addr_field, p1_ipv4_addr)
            self.input_text(p1_ipv6_addr_field, p1_ipv6_addr)
            self.input_text(p1_hostname_field, p1_hostname)
        else:
            # clean fields because they can be filled with old info
            self.input_text(p1_ipv4_addr_field, '')
            self.input_text(p1_ipv6_addr_field, '')
            self.input_text(p1_hostname_field, '')

        if self._is_element_present(simplex_TAP_radio_button):
            self._click_radio_button(simplex_TAP_radio_button)
        self._click_next_button()

    def _process_l4tm_wiring_page(self):
        """Interaction on Layer 4 Traffic Monitor Wiring page."""
        simplex_TAP_radio_button = 'monitor_simplex'

        self._wait_until_text_is_present('Layer 4 Traffic Monitor Wiring',timeout=self.SSW_TIMEOUT)

        self._click_radio_button(simplex_TAP_radio_button)
        self._click_next_button()

    def _process_routes_page(self,
        proxy_port,
        p1_gw='',
        route_name='',
        client_subnet='',
        client_gw='',
        m1_ipv6_addr=None,
        m1_ipv6_gw_default=None,
        p1_ipv6_addr=None,
        p1_ipv6_gw_default=None,
        ):
        """Interaction on routes for management and data traffic page."""

        self._info("Routes and Data Traffic page")
        p1_default_gateway_field = 'data_default'
        p1_route_name_field = 'data[0][name]'
        p1_dest_network_field = 'data[0][network]'
        p1_client_gw_field = 'data[0][gateway]'
        m1_v6_default_gateway_field = 'management_v6_default'
        p1_v6_default_gateway_field = 'data_v6_default'

        self._wait_until_text_is_present('Routes for Management',timeout=self.SSW_TIMEOUT)

        if m1_ipv6_addr:
            self.input_text(m1_v6_default_gateway_field, m1_ipv6_gw_default)
        if proxy_port != 'mgmt':
            self.input_text(p1_default_gateway_field, p1_gw)
            self.input_text(p1_route_name_field, route_name)
            self.input_text(p1_dest_network_field, client_subnet)
            self.input_text(p1_client_gw_field, client_gw)
            if p1_ipv6_addr:
                self.input_text(p1_v6_default_gateway_field, p1_ipv6_gw_default)

        self._click_next_button()

    def _process_transparent_connection_settings_page(self):
        """Interaction on transparent connection settings page."""

        self._wait_until_text_is_present('Transparent Connection Settings',timeout=self.SSW_TIMEOUT)
        self._info("Transparent Connections Settings page")
        self._click_next_button()

    def _process_administrative_settings_page(self, alert_rcpt, disable_sbnp, generate_passphrase=None):
        """Interaction on administrative settings page."""
        variables = common.Variables.get_variables()

        password = 'Cisco123$'
        if variables.has_key("${DUT_ADMIN_SSW_PASSWORD}"):
            password = variables["${DUT_ADMIN_SSW_PASSWORD}"]

        self._info("Administrative Settings page")
        RADIO_BUTTON_GENERATE='sys_gen'
        #Manual Password generation is removed from 12.0.1 - 240 and commenting that piece of code
        RADIO_BUTTON_MANUAL='manual'
        BUTTON_GENERATE="//input[@value, 'Generate']"
        pw_field = 'passwdv'                   # 'password'
        pw_confirm_field = 'repasswd'           #'passwordConfirm'
        alert_field = 'alerts'
        enable_autosupp_checkbox = 'enable_autosupp'
        enable_wbnp_checkbox = 'enable_wbnp'

        self._wait_until_text_is_present('Administrative Settings',timeout=self.SSW_TIMEOUT)

        if generate_passphrase is not None and str(generate_passphrase).lower() == 'y':
            self._click_radio_button(RADIO_BUTTON_GENERATE)
            self.click_button(BUTTON_GENERATE)

        else:
            # Manual Password generation is removed from 12.0.1 - 240 and commenting that piece of code
            try:
                self._click_radio_button(RADIO_BUTTON_MANUAL)
            except:
                pass
            self.input_text(pw_field, password)
            self.input_text(pw_confirm_field, password)

        self.input_text(alert_field, alert_rcpt)
        if self._is_element_present(enable_autosupp_checkbox):
            self.unselect_checkbox(enable_autosupp_checkbox)
        if disable_sbnp is not None and disable_sbnp:
            self._select_checkbox(enable_wbnp_checkbox)
        self._click_next_button()

    def _process_security_settings_page(self, disable_sec):
        """Interaction on security settings page."""

        tuple_of_sec_chkbox = (
            'url_filtering_enabled',
            'enable_reputation_filtering',
            'enable_advanced_malware',
            'enable_merlin',
            'enable_mcafee',
            'enable_sophos',
            'dlp_onbox_enabled',
        )
        self._wait_until_text_is_present('Security Settings',timeout=self.SSW_TIMEOUT)
        if disable_sec is not None and disable_sec:
            for chkbox in tuple_of_sec_chkbox:
                self._select_checkbox(chkbox)
        self._click_next_button()

    def _process_review_configuration_page(self):
        """Interaction on review configuration page."""

        self._wait_until_text_is_present('Review Your Configuration',timeout=self.SSW_TIMEOUT)

        install_button = "//input[@name='action:Install']"
        self.click_button(install_button)

    def ssw_run(self,
                alert_rcpt,
                proxy_port='mgmt',
                p1_ip=None,
                p1_netmask=None,
                p1_gw=None,
                p1_netprefix='/28',
                p1_hostname=None,
                route_name='Client',
                client_subnet=None,
                client_gw=None,
                dns='172.29.176.4',
                region='America',
                country='United States',
                timezone='Pacific Time (Los_Angeles)',
                disable_sbnp=None,
                disable_security=None,
                m1_ipv6_addr='',
                m1_ipv6_gw_default='',
                p1_ipv6_addr='',
                p1_ipv6_gw_default='',
                reset_network='yes',
                license_file=None,
                appliance_mode=None,
                # parameters for Cloud Web Security Connector mode
                cloud_server1=None,
                cloud_server2=None,
                cloud_server3=None,
                cloud_failure_handling=None,
                cloud_auth_scheme=None,
                cloud_auth_key=None,
                generate_passphrase=None,
        ):

        """Run system setup wizard.

        Parameters:
           - `alert_rcpt`: recipient to email system alert to.
           - `proxy_port` : port to use for proxy.  Either 'mgmt' or 'data'.
                            Defaulted to 'mgmt'.
           - `p1_ip`: IP address of data 1 port if proxy over data port.
           - `p1_netmask`: netmask of data 1 port if proxy over data port.
           - `p1_hostname`: hostname of data 1 port if proxy over data port.
           - `p1_gw`: gateway to data 1 port if proxy over data port.
           - `p1_netprefix` : network prefix used since coeus80.
              Default value '/28' corresponds to network mask 255.255.255.240
           - `route_name`: name of route for client network.
           - `client_subnet`: subnet where client belonged.
           - `client_gw`: gateway to client network.
           - `dns`: primary DNS to use.  Defaulted to '10.92.144.4'.
           - `region`: time zone region.  Defaulted to 'America'.
           - `country`: time zone country.  Defaulted to 'United States'.
           - `timezone`: local specific time zone.  Defaulted to
                         'Pacific Time (Los_Angeles)'.
           - `disable_sbnp`: specify True to disable SenderBase Network
                             participation during SSW.
           - `disable_security`: specify True to disable all security services
                                 during SSW.
           - `m1_ipv6_addr`: M1 v6 IP
           - `m1_ipv6_gw_default`: Default IPv6 gateway for management interface
           - `p1_ipv6_addr`: P1 v6 IP
           - `p1_ipv6_gw_default`: Default IPv6 gateway for data interface
           - `reset_network` - whether or not check 'Reset Network Settings'
            during Reset Configuration. Accepted values: 'yes' or 'no'
           - `license_file`: Absolute path of the license file present
                             on the client to be copied to
                             /data/pub/configuration directory
                             of the DUT
           - `appliance_mode`: Appliance Mode of Operation;
            'standard' - This appliance will be used for on-premise policy
             enforcement (Standard Web Security Appliance installation) or
            'cloud' - This appliance will be used primarily to direct traffic
             to Cisco Cloud Web Security for cloud policy enforcement and
             threat defense (Cloud Web Security Connector installation) or
             'hybrid' - This appliance will be used with Cisco Cloud Web Security for 
             cloud and on-premise policy enforcement and threat defense (Web Hybrid Installation).
           - `cloud_server1` - Cloud Web Security Proxy Server
           - `cloud_server2` - Cloud Web Security Proxy Server
           - `cloud_server3` - Cloud Web Security Proxy Server
           - `cloud_failure_handling` - Specify how to handle requests if all
            specified Cloud Web Security Proxy servers fail.
            'connect' - connect directly
            'drop' - drop requests
           - `cloud_auth_scheme` - Cloud Web Security Authorization Scheme
           'ip' - Authorize transaction based on IP address
           'key' - Send authorization key information with transaction
           - `cloud_auth_key` - Authorization Key
           - `generate_passphrase` - Generate the password automatically.

        Examples:
        | SSW Run | bar@foo.com | | # proxy over mgmt and use all defaults |
        | SSW Run | foo@bar.com | proxy_port=data | p1_ip=${P1_IP} |
        | | p1_netmask=${P1_NETMASK} | p1_hostname=${P1_HOSTNAME} | p1_gw=${P1_GW} |
        | | p1_netprefix=/28 |
        | | client_subnet=${CLIENT_SUBNET} | client_gw=${CLIENT_GW} | dns=${DNS} |
        | | region=${REGION} | country=${COUNTRY} | timezone=${TIME_ZONE} |
        | SSW Run | appliance_mode=cloud |
        | ... | cloud_server1=1.1.1.1 |
        | ... | cloud_server2=2.2.2.2 |
        | ... | cloud_server3=3.3.3.3 |
        | ... | cloud_failure_handling=connect |
        | ... | cloud_auth_scheme=ip |
        | SSW Run | appliance_mode=cloud |
        | ... | cloud_server1=server.com |
        | ... | cloud_failure_handling=drop |
        | ... | cloud_auth_scheme=key |
        | ... | cloud_auth_key=12345678901234567890123456789012 |
        """

        self._open_page()
        self._reset_config(reset_network)
        LICENSE = 'Please install the license file'
        try:
            self._wait_until_text_is_present(LICENSE,timeout=self.SSW_TIMEOUT)
            self._add_license(license_file=license_file)
            self._open_page()

        except:
            pass

        #if self._is_text_present(LICENSE):
        #    self._add_license(license_file=license_file)
        #    self._open_page()

        EULA = 'xpath=//input[@id="license_agree"]'
        try:
            self._wait_until_element_is_present(EULA,timeout=self.SSW_TIMEOUT)
            self._process_license_agreement_page()
        except:
            pass

        #if self._is_element_present(EULA):
        #    self._process_license_agreement_page()
        
        APPLIANCE_MODE = "xpath=//*[contains(text(), 'Appliance Mode of Operation')]"
        HYBRID = "xpath=//*[@id='mode_hybrid']"
        try:
            self._wait_until_element_is_present(APPLIANCE_MODE, timeout=self.SSW_TIMEOUT)
            #if self._is_element_present(HYBRID):
            self._process_appliance_mode_page(appliance_mode)
        except:
            pass
            
        self._process_system_setting_page(dns, region, country, timezone, appliance_mode)
        
        if appliance_mode == 'cloud':
            self._process_cloud_setting_page(
                cloud_server1, cloud_server2, cloud_server3,
                cloud_failure_handling,
                cloud_auth_scheme, cloud_auth_key,
            )
        else:
            self._process_network_context_page()
        
        if proxy_port != 'mgmt':
            self._process_network_intf_and_wiring_page(
                proxy_port,
                m1_ipv6_addr=m1_ipv6_addr,
                p1_hostname=p1_hostname,
                p1_ipv4_addr=p1_ip + p1_netprefix,
                p1_ipv6_addr=p1_ipv6_addr,
            )
        else:
            self._process_network_intf_and_wiring_page(
                proxy_port,
                m1_ipv6_addr=m1_ipv6_addr,
            )
            
        if appliance_mode != 'cloud':
            self._process_l4tm_wiring_page()
        
        self._process_routes_page(
            proxy_port,
            p1_gw=p1_gw,
            route_name=route_name,
            client_subnet=client_subnet,
            client_gw=client_gw,
            m1_ipv6_addr=m1_ipv6_addr,
            m1_ipv6_gw_default=m1_ipv6_gw_default,
            p1_ipv6_addr=p1_ipv6_addr,
            p1_ipv6_gw_default=p1_ipv6_gw_default,
        )
        
        m1_ipv6_addr=None,
        m1_ipv6_gw_default=None,
        p1_ipv6_addr=None,
        p1_ipv6_gw_default=None,
        self._process_transparent_connection_settings_page()
        self._process_administrative_settings_page(alert_rcpt, disable_sbnp, generate_passphrase)
        
        if appliance_mode != 'cloud':
            self._process_security_settings_page(disable_security)
        
        self._process_review_configuration_page()
        #Need check if below method is reliable
        #self._check_action_result()
        Misc(self.dut, self.dut_version).wait_until_ready()
