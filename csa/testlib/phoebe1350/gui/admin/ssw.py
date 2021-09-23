#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1350/gui/admin/ssw.py#2 $ $DateTime: 2020/01/09 22:34:35 $ $Author: saurgup5 $

import os
import time

import common.gui.guiexceptions as guiexceptions
from common.gui.guicommon import GuiCommon
from common.util.misc import Misc

from common.util.sarftime import CountDownTimer
from common.cli.clicommon import CliKeywordBase
from credentials import DUT_ADMIN_PASSWORD, DUT_ADMIN_TMP_PASSWORD

DEFAULT_PATH = lambda hostname: 'https://%s' % (hostname,)
NEXT_BUTTON = "xpath=//input[@name='action:Next']"
CONFIRM_DLG = "xpath=//div[@id='confirmation_dialog']"
LDAP_WIZARD_PATH = lambda hostname: 'https://%s/system_administration/ldap_wizard' % (hostname,)
GENERATE_PASSWORD_BUTTON = "//input[@value='Generate']"
SYSTEM_GENERATED_PASSWORD = "//input[@id='sysgen']"


class Passwd(CliKeywordBase):
    def change_default_admin_password(self, old_passwd, new_passwd):
        kwargs = {'old_pwd':old_passwd, 'new_pwd':new_passwd, 'confirm_new_pwd':new_passwd}
        self._cli.passwd(**kwargs)

class SSLConfig(CliKeywordBase):
    def ssl_tls_version_reset(self):
        try:
            kwargs = {'ssl_method':'TLS v1/TLS v1.2'}
            stat = self._cli.sslconfig().gui(**kwargs)
        except Exception:
            try:
                kwargs = {'ssl_method':'TLS v1.0'}
                stat = self._cli.sslconfig().gui(**kwargs)
            except Exception:
                kwargs = {'ssl_method':'3'}
                stat = self._cli.sslconfig().gui(**kwargs)

        self._cli.commit('SSL TLS version is changed..')

class Ssw(GuiCommon):
    """System Setup Wizard interaction class.

    This class designed to interact with GUI elements of System Administration
    -> System Setup Wizard. Use keywords, listed below, to manipulate with
    System Setup wizard.
    """

    # method required by RF
    # return a list with all public methods
    def get_keyword_names(self):
        return ['ssw_run',
                'interface_object_create']

    def _open_page(self):
        self.go_to(DEFAULT_PATH(self.dut))
        self._navigate_to('System Administration', 'System Setup Wizard')

    def _click_checkbox(self, check, cb_locator):
        if check:
            if not self._is_checked(cb_locator):
                self.select_checkbox(cb_locator)
        else:
            self.unselect_checkbox(cb_locator)

    def is_already_configured(self):
        return self._is_element_present(
            "xpath=//input[@value='Reset Configuration']")

    def _cancel_active_dir_wizard(self):
        if self._is_text_present("Active Directory Wizard"):
            self.click_button("name=action:Cancel")
            self._info("Cancelling Active Directory Wizard")


    def _reset_config(self):
        if self.is_already_configured():
            self._info('Resetting all configurations.')
            self.click_element(NEXT_BUTTON)
            self.close_browser()
            Passwd(self.dut, self.dut_version).change_default_admin_password(old_passwd=DUT_ADMIN_PASSWORD,
                                                                             new_passwd=DUT_ADMIN_TMP_PASSWORD)
            SSLConfig(self.dut, self.dut_version).ssl_tls_version_reset()
            self.launch_dut_browser()
            self.log_into_dut()
            self._open_page()
        else:
            self._info('Reset configuration is not required.')

    def _accept_license_agreement(self, accept_license):
        AGREE_CHECKBOX = "xpath=//input[@id='license_agree']"

        if accept_license:
            if not self._is_checked(AGREE_CHECKBOX):
                self.click_element(AGREE_CHECKBOX, "don't wait")
                self.click_button("xpath=//input[@id='begin_setup']")
        else:
            self.unselect_checkbox(AGREE_CHECKBOX)
            raise guiexceptions.ConfigError('Licenses agreement should be'\
                ' accepted to begin setup process')

    def _system_page(self,
                     alerts_rcpts=None,
                     hostname=None,
                     scheduled_report_rcpts=None,
                     region=None,
                     country=None,
                     timezone=None,
                     ntp_server=None,
                     password_option=None,
                     admin_password=None,
                     enable_sbnp=None,
                     enable_auto_support=None):

        password = None
        if hostname:
            self.input_text("xpath=//input[@name='hostname']", hostname)

        if alerts_rcpts:
            self.input_text("xpath=//input[@name='alerts']", alerts_rcpts)

        if scheduled_report_rcpts:
            self.input_text("xpath=//input[@name='reports']",
                            scheduled_report_rcpts)

        if region:
            self.select_from_list("xpath=//select[@id='region']",
                                  "label=%s" % region)
        if country:
            self.select_from_list("xpath=//select[@id='country']",
                                  "label=%s" % country)
        if timezone:
            self.select_from_list("xpath=//select[@id='timezone']",
                                  "label=glob:%s*" % timezone)

        if ntp_server:
            self.input_text("xpath=//input[@id='timeservers_0']", ntp_server)

###Need to uncommented onces system generated password option available###
#	if password_option == 'manual' and admin_password:
#            self._click_radio_button("xpath=//input[@id='manual']")
#            self.input_text("xpath=//input[@id='passwdv']", admin_password)
#            self.input_text("xpath=//input[@id='repasswd']",
#                            admin_password)

#	elif password_option == 'generated':
#            self._click_radio_button("xpath=//input[@id='sys_gen']")
#	    self.click_button(GENERATE_PASSWORD_BUTTON, "don't wait")
#            password = self.get_value(SYSTEM_GENERATED_PASSWORD)

###Need to remove this line once system genereated password is available###
        if password_option:
            self.input_text("xpath=//input[@id='passwdv']", admin_password)
            self.input_text("xpath=//input[@id='repasswd']", admin_password)

        if enable_sbnp is not None:
            self._click_checkbox(enable_sbnp,
                                 "xpath=//input[@id='enable_sbnp']")

        if enable_auto_support is not None:
            self._click_checkbox(enable_auto_support,
                                 "xpath=//input[@id='enable_autosupp']")

        self.click_button(NEXT_BUTTON)
        return password

    def _network_page(self,
                      gateway=None,
                      ipv6_gateway=None,
                      dns_servers=None,
                      data1_obj=None,
                      data2_obj=None,
                      mgmt_obj=None):

        if gateway:
            self.input_text("xpath=//input[@id='gateway']", gateway)

        # if you want to use ipv6 gateway, it's require additional verification.
        # it wan't tested.
        if ipv6_gateway:
            self.input_text("xpath=//input[@name='ipv6_gateway']", ipv6_gateway)

        if dns_servers:
            self._click_radio_button("xpath=//input[@id='dns_choiceSelf']")
            counter = 0
            for dns_server in dns_servers:
                self.input_text("xpath=//input[@id='user_dns%s']" % counter,
                                dns_server)
                counter = +1
        else:
            self._click_radio_button("xpath=//input[@id='dns_ChoiceRoot']")

        if data1_obj:
            self._fill_ifc(data1_obj)

        if data2_obj:
            self._fill_ifc(data2_obj, '1')

        if mgmt_obj:
            if self._is_element_present("xpath=//input[@id='interface[3][enabled]']"):
                self._fill_ifc(mgmt_obj, '3')
            else:
                self._fill_ifc(mgmt_obj, '2')

        self.click_button(NEXT_BUTTON)

    def _fill_ifc(self, ifc_obj=None, indx='0'):

        if not self._is_checked(
            "xpath=//input[@id='interface[%s][enabled]']" % indx):
            self.click_element("xpath=//input[@id='interface[%s][enabled]']"
                               % indx, "don't wait")

        if ifc_obj.ip_netmask:
            self.input_text("xpath=//input[@id='interface[%s][ip]']" % indx,
                            ifc_obj.ip_netmask)

        if ifc_obj.ipv6_netmask:
            self.input_text("xpath=//input[@id='interface[%s][ip6]']" % indx,
                            ifc_obj.ipv6_netmask)

        if ifc_obj.hostname:
            self.input_text("xpath=//input[@id='interface[%s][hostname]']"
                            % indx, ifc_obj.hostname)

        if ifc_obj.domain_dest_pairs:
            self.click_element(
                "xpath=//input[@id='interface[%s][accept]']" % indx,
                "don't wait")
            self._fill_domain_dest_pairs(ifc_obj.domain_dest_pairs)

        if ifc_obj.mail_servers:
            self.click_element(
                "xpath=//input[@id='interface[%s][relay]']" % indx,
                "don't wait")
            counter = 0
            for mail_server in ifc_obj.mail_servers:
                self.input_text("xpath=//input[@id='hat[%d][network]']"
                                % counter, mail_server)
                if counter != (len(ifc_obj.mail_servers) - 1):
                    self.click_button("xpath=//input[@id='hat_domtable_AddRow']",
                                      "don't wait")
                counter = +1

    def _fill_domain_dest_pairs(self, domain_dest_pairs):
        for i in xrange(len(domain_dest_pairs)):
            domain, dest = self._convert_to_tuple_from_colon_separated_string(
                                    domain_dest_pairs[i])
            self.input_text("xpath=//input[@id='rat[%d][domain]']" % i, domain)
            self.input_text("xpath=//input[@id='rat[%d][dest]']" % i, dest)
            if i != (len(domain_dest_pairs) - 1):
                self.click_button(
                    "xpath=//input[@id='rat_domtable_AddRow']",
                    "don't wait")

    def _security_page(self,
                       enable_sbrs=None,
                       as_type_isq_pairs=None,
                       antivirus_type=None,
                       enable_vof=None):
        ANTIVIRUS_ENGINE = "xpath=//input[@id='av_engine_%s']"
        ANTISPAM_ENGINE = "xpath=//input[@id='as_engine_%s']"
        as_types = {'ipas':'case', 'ipas_ims': 'ims'}

        if enable_sbrs is not None:
            self._click_checkbox(enable_sbrs,
                                 "xpath=//input[@id='enable_sbrs']")

        if as_type_isq_pairs:
            as_type_isq_pairs = self._convert_to_tuple(as_type_isq_pairs)
            if not (isinstance(as_type_isq_pairs, tuple) and
                len(as_type_isq_pairs) == 2):
                raise ValueError('Antispam engine must be a tuple of length 2')

            antispam_type, spam_quarantine = as_type_isq_pairs

            self._click_radio_button(ANTISPAM_ENGINE % as_types[antispam_type])
            if antispam_type == 'ipas':
                self._click_checkbox(spam_quarantine, "xpath=//input[@id='enable_isq']")
            else:
                self._click_checkbox(spam_quarantine, "xpath=//input[@id='enable_isq_ims']")
        else:
            self._click_radio_button(ANTISPAM_ENGINE % "none")

        if antivirus_type:
            self._click_radio_button(ANTIVIRUS_ENGINE % antivirus_type)
        else:
            self._click_radio_button(ANTIVIRUS_ENGINE % "none")

        if enable_vof is not None:
            self._click_checkbox(enable_vof, "xpath=//input[@id='enable_vof']")

        self.click_button(NEXT_BUTTON)

    def configure_active_dir(self, active_dir_obj=None):
        # TODO: handling active directory wizard will be implemented later

        if active_dir_obj:
            # self._fill_active_dir_page()
            pass
        else:
            self.click_button("name=action:Cancel")
        msg = 'SSW completed successfully'
        self._info(msg)

    def _review_install_configuration(self):
        self.click_button("xpath=//input[@name='action:Install']", "don't wait")
        tmr = CountDownTimer(5).start()
        while tmr.is_active():
            try:
                if self._is_visible(CONFIRM_DLG):
                    self._info('%s is found' % CONFIRM_DLG)
                    self.click_button(CONFIRM_DLG + \
                                      "//button[normalize-space()='Install']",
                                      "don't wait")
                    break
            except Exception as e:
                print e
            time.sleep(1)

        # Workaround: After configuration install redirection to IP based url
        # takes place. Avoid this manually reopen right page
        tmr = CountDownTimer(10).start()
        import urllib2
        while tmr.is_active():
            try:
                status = urllib2.urlopen(LDAP_WIZARD_PATH(self.dut)).getcode()
            except urllib2.URLError:
                status = None
            if status == 200:
                self.go_to(LDAP_WIZARD_PATH(self.dut))
                break
            time.sleep(1)

    def ssw_run(self,
                alerts_rcpts,
                mgmt_obj=None,
                accept_license=True,
                hostname=None,
                scheduled_report_rcpts=None,
                region=None,
                country=None,
                timezone=None,
                ntp_server=None,
		password_option='manual',
                admin_password=None,
                enable_sbnp=None,
                enable_auto_support=False,
                gateway=None,
                ipv6_gateway=None,
                dns_servers=None,
                data1_obj=None,
                data2_obj=None,
                enable_sbrs=None,
                as_type_isq_pairs=None,
                antivirus_types=None,
                enable_vof=None,
                active_dir_obj=None):
        """ Run system setup wizard.

        *Parameters*:
            - `alerts_rcpts`: email system alerts to. Required parameter.
            - `accept_license`: whether accept EULA. Boolean.
            _${True}_ by default
            - `hostname`: hostname of the appliance. String.
            - `scheduled_report_rcpts`: scheduled reports system deliver to.
            - `region`: time zone region.
            - `country`: time zone country.
            - `timezone`: local specific time zone.
            - `ntp_server`: NTP server.
            - `password_option`: Two options - 'manual' or 'generated'.
            Default is 'manual'.
            - `admin_password`: Administrator's password. Applicable only if
	    password_option is manual.
            - `enable_sbnp`: boolean value to enable SenderBase Network
            Participation feature.
            - `enable_auto_support`: boolean value to enable Autosupport
            feature. _${False}_ by default.
            - `gateway`: default gateway for interface.
            - `dns_servers`: array of DNS server(s). Max 2 values. If more than
            2 values specified then first and last values are taken.
            - `mgmt_obj`: object returned by `Interface Object Create` keyword.
            - `data1_obj`: object returned by `Interface Object Create` keyword
            - `data2_obj`: object returned by `Interface Object Create` keyword
            - `enable_sbrs`: boolean value to enable SenderBase Reputation
            Filtering feature.
            - `as_type_isq_pairs`: accepts a comma separated string or list of
            engine Anti-Spam or Intelligent Multi-Scan
            (can be _ipas_ or _ipas_ims_) and Spam Quarantine value
            (can be ${True} or ${False}).
            e.g. ipas_ims, ${True} or ipas, ${False}. By default _none_
            - `antivirus_types`: antivirus name to enable Anti-Virus feature.
            e.g. sophos, mcafee. By default _none_
            - `enable_vof`: boolean value to enable Outbreak Filters feature
            - `active_dir_obj`: obj for configuring active directory.

        *Exceptions*:
            - `ConfigError`: in case terms of license agreement was not
              accepted.

        *Examples*:
        | @{DATA1_DOM_DEST} | Create List | dom.com:destination.com |
        | ... | 10.1.1.1:note.com |
        | @{DATA1_MAILS} | Create List | data1.com | data11.com |
        | ${data1_obj} = | Interface Object Create |
        | ... | ip_address=${DUT_DATA1_IP} |
        | ... | cidr_netmask=${DUT_DATA1_NETMASK} |
        | ... | hostname=${DUT} |
        | ... | domain_dest_pairs=@{DATA1_DOM_DEST} |
        | ... | mail_servers=@{DATA1_MAILS} |

        | ${sys_gen_password}= | SSW Run |
        | ... | ${ALERT_RCPT} |
        | ... | region=${REGION} |
        | ... | country=${COUNTRY |
        | ... | timezone=${TIMEZONE} |
	| ... | password_option=generated |
        | ... | enable_sbnp=${True} |
        | ... | enable_auto_support=${True} |
        | ... | gateway=${DUT_DATA1_GW} |
        | ... | data1_obj=${data1_obj} |
        | ... | enable_sbrs=${True} |
        | ... | as_type_isq_pairs=ipas_ims, ${False} |
        | ... | antivirus_types=sophos |
        | ... | enable_vof=${True} |

        | @{MGMT_DOM_DEST} | Create List | dom.com:destination.com |
        | @{MGMT_MAILS} | Create List | data2.com |
        | @{DNS} | Create List | ${DNS} |
        | ${mgmt_obj} = | Interface Object Create |
        | ... | ip_address=${DUT_DATA2_IP} |
        | ... | cidr_netmask=${DUT_DATA2_NETMASK} |
        | ... | ipv6_address=${DUT_DATA2_IPv6} |
        | ... | ipv6_netmask=${DUT_DATA2_IPv6_NETMASK} |
        | ... | hostname=${DUT} |
        | ... | domain_dest_pairs=@{MGMT_DOM_DEST} |
        | ... | mail_servers=@{MGMT_MAILS} |

        | SSW Run |
        | ... | ${ALERT_RCPT} |
        | ... | accept_license=${True} |
        | ... | hostname=${DUT} |
        | ... | scheduled_report_rcpts=admin@company.com |
        | ... | region=${REGION} |
        | ... | country=${COUNTRY |
        | ... | timezone=${TIMEZONE} |
        | ... | ntp_server=time.ironport.com |
        | ... | gateway=${DUT_DATA2_GW} |
        | ... | dns_servers=@{DNS} |
        | ... | mgmt_obj=${mgmt_obj} |
        | ... | as_type_isq_pairs=ipas, ${True} |

        """
        self._info('Running System Setup Wizard...')
        self._open_page()
        self._cancel_active_dir_wizard()
        self._open_page()
        # increase selenium timeout
        # 60 seconds not enough for reseting config via WebUI
        self.set_selenium_timeout(120)
        self._reset_config()
        # revert timeout to 60 seconds
        self.set_selenium_timeout(60)

        if self._is_element_present("xpath=//input[@id='license_agree']"):
           self._accept_license_agreement(accept_license)

        if (not admin_password and password_option == 'manual'):
            admin_password = Misc(None, None).get_admin_password(self.dut)

        sys_gen_pass = self._system_page(alerts_rcpts, hostname, scheduled_report_rcpts,
                          region, country, timezone, ntp_server, password_option,
                          admin_password, enable_sbnp, enable_auto_support)
        self._check_action_result()

        self._network_page(gateway, ipv6_gateway, dns_servers, data1_obj,
                           data2_obj, mgmt_obj)
        self._check_action_result()

        self._security_page(enable_sbrs, as_type_isq_pairs, antivirus_types,
                            enable_vof)
        self._check_action_result()

        self._review_install_configuration()
        self._check_action_result()

        msg = 'System Setup Wizard is completed, ' \
               'plz cancel or configure AD settings'
        self._info(msg)

        self.configure_active_dir(active_dir_obj)
        Misc(self.dut, self.dut_version).wait_until_ready()
	return sys_gen_pass

    def interface_object_create(self,
                                ip_address=None,
                                cidr_netmask=None,
                                ipv6_address=None,
                                ipv6_netmask=None,
                                hostname=None,
                                domain_dest_pairs=None,
                                mail_servers=None):
        """ Create interface object.

        *Parameters*:
        - `ip_address`: ipv4 address of appliance.
        - `cidr_netmask`: ipv4 netmask for the subnet.
        - `ipv6_address`: ipv6 address of appliance.
        - `ipv6_netmask`: ipv6 netmask for the subnet.
        - `hostname`: fully qualified domain name for this appliance.
        - `domain_dest_pairs`: array of pairs, separated by colon;
        domain for which to accept mail and destination (SMTP Route)
        for each domain, this is optional
        e.g. dom.com:dest.com    dom1.com:dest1.com
        - `mail_servers`: array of mail servers allowed to relay email
        through the appliance

        *Return*:
          interface object with the following attributes:
          `ip_netmask`, `ipv6_netmask`, `hostname`, `domain_dest_pairs`,
          `mail_servers`

        *Examples*:
        | @{DATA1_DOM_DEST} | Create List | dom.com:destination.com |
        | ... | 10.1.1.1:note.com |
        | @{DATA1_MAILS} | Create List | data1.com | data11.com |
        | ${data1_obj} = | Interface Object Create |
        | ... | ip_address=${DUT_DATA1_IP} |
        | ... | cidr_netmask=${DUT_DATA1_NETMASK} |
        | ... | hostname=${DUT} |
        | ... | domain_dest_pairs=@{DATA1_DOM_DEST} |
        | ... | mail_servers=@{DATA1_MAILS} |

        | @{DATA1_DOM_DEST} | Create List | dom.com:destination.com |
        | ... | 10.1.1.1:note.com |
        | @{DATA1_MAILS} | Create List | data1.com | data11.com |
        | ${data1_obj} = | Interface Object Create |
        | ... | ipv6_address=${DUT_DATA1_IP} |
        | ... | ipv6_netmask=${DUT_DATA1_NETMASK} |
        | ... | hostname=${DUT} |
        | ... | domain_dest_pairs=@{DATA1_DOM_DEST} |
        | ... | mail_servers=@{DATA1_MAILS} |

        | @{DATA1_DOM_DEST} | Create List | dom.com:destination.com |
        | @{DATA1_MAILS} | Create List | data1.com |
        | ${data1_obj} = | Interface Object Create |
        | ... | ip_address=${DUT_DATA1_IP} |
        | ... | cidr_netmask=${DUT_DATA1_NETMASK} |
        | ... | ipv6_address=${DUT_DATA1_IPv6} |
        | ... | ipv6_netmask=${DUT_DATA1_IPv6_NETMASK} |
        | ... | hostname=${DUT} |
        | ... | domain_dest_pairs=@{DATA1_DOM_DEST} |
        | ... | mail_servers=@{DATA1_MAILS} |
        """
        interface = Interface(ip_address, cidr_netmask, ipv6_address,
                      ipv6_netmask, hostname, domain_dest_pairs, mail_servers)
        return interface

class Interface(object):
    """Container class for holding information about interface attributes.

    :Attributes:
    - `ip_address`: ip address of appliance.
    - `cidr_netmask`: netmask for the subnet.
    - `ipv6_address`: ipv6 address of appliance.
    - `ipv6_netmask`: ipv6 netmask for the subnet.
    - `hostname`: fully qualified domain name for this appliance.
    - `domain_dest_pairs`: array of pairs, separated by colon;
    domain for which to accept mail and destination (SMTP Route)
    for each domain, this is optional
    e.g. dom.com:dest.com    dom1.com:dest1.com
    - `mail_servers`: array of mail servers allowed to relay email
    through the appliance
    """
    def __init__(self, ip_address, cidr_netmask, ipv6_address,
                 ipv6_netmask, hostname, domain_dest_pairs, mail_servers):

        self.ip_netmask = None
        self.ipv6_netmask = None
        if ip_address and cidr_netmask:
            self.ip_netmask = '%s/%s' % (ip_address, cidr_netmask)
        elif ip_address and not cidr_netmask:
            raise ValueError('CIDR netmask - 0 through 32 ' + \
                                   'is required for IP address specified')
        elif cidr_netmask and not ip_address:
            raise ValueError('IP address not specified but netmask provided')

        if ipv6_address and ipv6_netmask:
            self.ipv6_netmask = '%s/%s' % (ipv6_address, ipv6_netmask)
        elif ipv6_address and not ipv6_netmask:
            raise ValueError('CIDR netmask - 0 through 128 ' + \
                                   'is required for IPv6 address specified')
        elif ipv6_netmask and not ipv6_address:
            raise ValueError('IPv6 address not specified but netmask provided')

        self.hostname = hostname
        self.domain_dest_pairs = domain_dest_pairs
        self.mail_servers = mail_servers

    def __str__(self):
        interface_str = ('Ip Address: %s' % (self.ip_netmask,),
                         'Ipv6 Address: %s' % (self.ipv6_netmask,),
                         'Hostname: %s' % (self.hostname,),
                         'Domain Destination Pairs: %s'
                                                   % (self.domain_dest_pairs,),
                         'Mail Servers: %s' % (self.mail_servers,),
                         )
        return '; '.join(interface_str)
