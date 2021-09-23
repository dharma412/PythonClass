#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1362/gui/management/administration/ssw.py#1 $
# $DateTime: 2020/06/10 22:29:20 $
# $Author: sarukakk $

import common.Variables
import common.gui.guiexceptions as guiexceptions
from common.gui.guicommon import GuiCommon
from common.util.misc import Misc
from zeus1250.cli.keywords.reset_config import ResetConfig
from zeus1250.cli.keywords.suspend import Suspend
from common.cli.clicommon import CliKeywordBase
from zeus1250.cli.keywords.passwd import Passwd


import time

NEXT_STEPS_PATH = lambda protocol, hostname: '%s://%s/system_administration/system_setup/euqssw_next_steps' % (protocol, hostname)
DEFAULT_PATH = lambda protocol, hostname: '%s://%s' % (protocol, hostname)
RESET_CONF = "//input[@value='Reset Configuration']"

class SSLConfig(CliKeywordBase):
     def ssl_tls_version_reset(self):
         try:
             kwargs = {'ssl_method':'TLS v1/TLS v1.2','versions':'WebUI','confirm':'Enable for all services'}
             stat = self._cli.sslconfig().gui(**kwargs)
         except Exception:
             try:
                 kwargs = {'ssl_method':'TLSv1.0','versions':'WebUI','confirm':'Enable for all services'}
                 stat = self._cli.sslconfig().gui(**kwargs)
             except Exception:
                 kwargs = {'ssl_method':'SSLv3.0','versions':'WebUI','confirm':'Enable for all services'}
                 stat = self._cli.sslconfig().gui(**kwargs)
         self._cli.commit('SSL TLS version is changed..')

class SystemSetupWizard(GuiCommon):

    """ Keywords for interaction with Management -> Administration -> System Setup Wizard
    """

    def get_keyword_names(self):
        return ['system_setup_wizard_run',
                'system_setup_wizard_run_password_change',]

    def _open_page(self):
        if self.selenium_server_host == 'localhost':
            protocol = 'https'
        else:
            protocol = 'http'
        self.go_to(DEFAULT_PATH(protocol, self.dut))
        self._navigate_to('Management', 'System Administration',
                            'System Setup Wizard')

    def _is_already_configured(self):
        return self._is_element_present(RESET_CONF)

    def _reset_config(self, old_pwd, new_pwd):
        reset_config_button = 'action:Next'
        oldpw_field = 'old_pwd'
        if self._is_already_configured():
            self._info('Resetting all configurations.')
            try:
               self.click_button(reset_config_button)
               self.input_text(oldpw_field, old_pwd)
               self._process_password(new_pwd,generate_passphrase=None)
               self._click_submit_button()
            except:
               self.close_browser()
               Passwd(self.dut, self.dut_version).passwd(old_pwd, new_pwd)
               SSLConfig(self.dut, self.dut_version).ssl_tls_version_reset()
               self.launch_dut_browser()
               self.log_into_dut()
            self._open_page()
        else:
            self._info('Reset configuration is not required.')

    def _accept_license_agreement(self, accept_eula):
        agree_checkbox = 'id=license_agree'
        begin_button = 'id=begin_setup'

        if accept_eula:
            if not self._is_checked(agree_checkbox):
                self.click_element(agree_checkbox, "don't wait")
                self.click_button(begin_button)
        else:
            self.unselect_checkbox(agree_checkbox)
            raise guiexceptions.ConfigError('Licenses agreement should be'\
                'accepted to begin setup process')

    def _process_system_setting_page(self, alert_rcpt, region, country,
                                timezone, ntp, passwd, autosupport,generate_passphrase=None):
        self._process_alerts_rcpt(alert_rcpt)
        self._process_timezone_settings(region, country, timezone)
        if ntp is not None:
            self._process_ntp_server(ntp)
        self._process_password(passwd,generate_passphrase)
        self._process_autosupport(autosupport)

        self._click_next_button()

    def _process_alerts_rcpt(self, alert_rcpt):
        alerts_combo = 'alerts'
        self.input_text(alerts_combo, alert_rcpt)

    def _process_timezone_settings(self, region, country, timezone):
        region_option_combo = 'region'
        country_option_combo = 'country'
        timezone_option_combo = 'timezone'

        # self.select_from_list(region_option_combo, "value=%s" % region)
        # self.select_from_list(country_option_combo, "value=%s" % country)
        # self.select_from_list(timezone_option_combo, "value=glob:%s*" % timezone)
        self.select_from_list(region_option_combo, region)
        self.select_from_list(country_option_combo, country)
        self.select_from_list(timezone_option_combo, timezone)

    def _process_ntp_server(self, ntp):
        timeserver_box = 'timeservers_0'

        if isinstance(ntp, str):
            self.input_text(timeserver_box, ntp)
        elif isinstance(ntp, object):
            self.input_text(timeserver_box, ntp.name)

    def _process_password(self, passwd,generate_passphrase):
        RADIO_BUTTON_GENERATE='sys_gen'
        RADIO_BUTTON_MANUAL='manual'
        BUTTON_GENERATE="//input[@value, 'Generate']"
        pw_field = 'passwdv'                   # 'password'
        pw_confirm_field = 'repasswd'           #'passwordConfirm'

        if generate_passphrase is not None and str(generate_passphrase).lower() == 'y':
            self._click_radio_button(RADIO_BUTTON_GENERATE)
            self.click_button(BUTTON_GENERATE)

        else:
            if self._is_element_present(RADIO_BUTTON_MANUAL):
                self._click_radio_button(RADIO_BUTTON_MANUAL)
            self.input_text(pw_field, passwd)
            self.input_text(pw_confirm_field, passwd)

    def _process_autosupport(self, autosupport):
        autosupp_box = 'enable_autosupp'

        if autosupport:
            self.select_checkbox(autosupp_box)
        else:
            self.unselect_checkbox(autosupp_box)

    def _process_network_settings_page(self, hostname, ip_address,
                                            netmask, gateway, dns):

        if hostname is not None:
            self._process_hostname(hostname)

        if ip_address is not None:
            self._process_ip_address(ip_address)

        if netmask is not None:
            self._process_netmask(netmask)

        if gateway is not None:
            self._process_gateway(gateway)

        if dns is not None:
            self._process_dns(dns)

        self._click_next_button()

    def _process_ip_address(self, address):
        ip_field = 'interface[0][ip]'
        self.input_text(ip_field, address)

    def _process_hostname(self, hostname):
        hostname_field = 'interface[0][hostname]'
        self.input_text(hostname_field, hostname)

    def _process_netmask(self, mask):
        netmask_field = 'interface[0][netmask]'
        self.input_text(netmask_field, mask)

    def _process_gateway(self, gateway):
        gateway_field = 'gateway'
        self.input_text(gateway_field, gateway)

    def _process_dns(self, dns):
        user_dns = lambda idx: 'user_dns[%i][dns]' % idx
        dns_root_radio = 'dns_ChoiceRoot'
        dns_self_radio = 'dns_choiceSelf'

        if dns is None:
            # Root servers are used
            self._click_radio_button(dns_root_radio)
        else:
            # own servers are used
            self._click_radio_button(dns_self_radio)
            dns = self._convert_to_tuple(dns)
            self._info('dns is %s' % (dns,))
            for i in range(len(dns)):
                self._info('dns server %s' % (dns[i],))
                if not self._is_element_present(user_dns(i+2)):
                    self.click_button('user_dns_addRow',"don't wait")
                self.input_text(user_dns(i+2), dns[i] )

    def _review_install_configuration(self):
        if self.selenium_server_host == 'localhost':
            protocol = 'https'
        else:
            protocol = 'http'
        INSTALL_BTN = "xpath=//input[@name='action:Install']"
        CONFIRM_BTN = 'xpath=//button[text()="Install"]'

        time.sleep(5) # to wait until install button is visible
        if self._is_visible(INSTALL_BTN):
            self.click_button(INSTALL_BTN, "don't wait")
        time.sleep(5) # to avoid time races
        if self._is_visible(CONFIRM_BTN):
            self._info('%s is found' % CONFIRM_BTN)
            self.click_button(CONFIRM_BTN, "don't wait")

        # Workaround: After configuration install redirection to IP based url
        # takes place. Avoid this manually reopen right page
        self.go_to(NEXT_STEPS_PATH(protocol, self.dut))

    def system_setup_wizard_run(self,
                 alert_rcpt,
                 accept_eula=True,
                 region='America',
                 country='United States',
                 timezone='Pacific (Los_Angeles)',
                 ntp=None,
                 passwd='Cisco123$',
                 autosupport=False,
                 hostname=None,
                 ip_address=None,
                 netmask=None,
                 gateway=None,
                 dns=None,
                 skip_cli_resetconfig=True,
                 ):
        """ Run system setup wizard.

        Parameters:
            - `alert_rcpt`: email system alerts to.
            - `accept_eula`: whether accept EULA. Boolean. True by default
            - `region`: time zone region.  Default to 'America'.
            - `country`: time zone country.  Default to 'United States'.
            - `timezone`: local specific time zone.  Default to
                          'Pacific Time (Los_Angeles)'.
            - `ntp`: NTP server.
            - `passwd`: Administrator's password.
            - `autosupport`: boolean value to enable Autosupport feature.
            - `hostname`: fully qualified domain name for this appliance.
            - `ip`: ip address of appliance.
            - `netmask`: netmask for the subnet.
            - `gateway`: default gateway for management interface.
            - `dns`: DNS server(s).
            - `skip_cli_resetconfig`: by default resetconfig is performed from
            cli to save time. If that parameter is set to True, cli method is
            not invoked. That can be needed to check functionality of
            "Reset Configuration" button -Reseting the dafult value to True since this already covered in the UI reset config

        Exceptions:
            - `ConfigError`: in case terms of license agreement was not
              accepted; in case email for system alerts was not specified.

        Examples:
            | System Setup Wizard Run | testuser@mail.qa | accept_eula=${True} | ntp=time.ironport.com |
            | System Setup Wizard Run | testuser@mail.qa | accept_eula=${True} | region=America | country=United States | timezone=Pacific Time (Los_Angeles) |

        """
        userpasswd = passwd


        variables = common.Variables.get_variables()
        # if variables.has_key("${DUT_ADMIN_SSW_PASSWORD}"):
        #     passwd = variables["${DUT_ADMIN_SSW_PASSWORD}"]
        # if variables.has_key("${DUT_ADMIN_PASSWORD}"):
        #     old_pwd = variables["${DUT_ADMIN_PASSWORD}"]
        # if variables.has_key("${DUT_ADMIN_TMP_PASSWORD}"):
        #     new_pwd = variables["${DUT_ADMIN_TMP_PASSWORD}"]

        if "${DUT_ADMIN_SSW_PASSWORD}" in variables:
            passwd = variables["${DUT_ADMIN_SSW_PASSWORD}"]
        if "${DUT_ADMIN_PASSWORD}" in variables:
            old_pwd = variables["${DUT_ADMIN_PASSWORD}"]
        if "${DUT_ADMIN_TMP_PASSWORD}" in variables:
            new_pwd = variables["${DUT_ADMIN_TMP_PASSWORD}"]

        #"""Logic to override default password with user defined password """
        if userpasswd != passwd:
            passwd = userpasswd

        self._info('Running System Setup Wizard...')

        if alert_rcpt is None:
            raise guiexceptions.ConfigError('Email for system alerts should be specified')
        if not skip_cli_resetconfig:
            try:
                Suspend(self.dut, self.dut_version).suspend()
                ResetConfig(self.dut, self.dut_version).reset_config()
            except:
                pass
        self._open_page()
        self._reset_config(old_pwd, new_pwd)
        self._accept_license_agreement(accept_eula)
        self._process_system_setting_page(alert_rcpt, region, country,
                                            timezone, ntp, passwd, autosupport)
        self._process_network_settings_page(hostname, ip_address, netmask,
                                            gateway, dns)
        self._review_install_configuration()
        self._check_action_result()
        self._info( 'System Setup Wizard is completed.' )
        Misc(self.dut, self.dut_version).wait_until_ready()

    def system_setup_wizard_run_password_change(self,
                                alert_rcpt,
                                accept_eula=True,
                                region='America',
                                country='United States',
                                timezone='Pacific (Los_Angeles)',
                                ntp=None,
                                passwd=None,
                                autosupport=False):

        """
        Usage:
        System setup wizard run password change  testuser@mail.qa  passwd=${greater_than_128_char_password}"

        This keyword is to verify error message that occurs in the System setup wizard when the password does not meet
        necessary password length standards"""


        variables = common.Variables.get_variables()
        if variables.has_key("${DUT_ADMIN_SSW_PASSWORD}"):
            if passwd is None:
                passwd = variables["${DUT_ADMIN_SSW_PASSWORD}"]
        if variables.has_key("${DUT_ADMIN_PASSWORD}"):
            old_pwd = variables["${DUT_ADMIN_PASSWORD}"]
        if variables.has_key("${DUT_ADMIN_TMP_PASSWORD}"):
            new_pwd = variables["${DUT_ADMIN_TMP_PASSWORD}"]

            self._open_page()
            self._reset_config(old_pwd, new_pwd)
            self._accept_license_agreement(accept_eula)
            self._process_system_setting_page(alert_rcpt, region, country,
                                              timezone, ntp, passwd, autosupport)
