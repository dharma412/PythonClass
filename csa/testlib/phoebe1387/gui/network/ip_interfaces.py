#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1350/gui/network/ip_interfaces.py#1 $ $DateTime: 2020/01/06 01:25:43 $ $Author: saurgup5 $

from common.gui.guicommon import GuiCommon
from common.gui.decorators import set_speed

# locators
ADD_INTERFACE_BUTTON="//input[@value='Add IP Interface...']"
INTERFACES_TABLE = "//*/table[@class='cols']"
INTERFACE_DELETE_CONFIRM = "//*[@type='button' and text()='Delete']"
INTERFACE_DELETE_CANCEL = "//*[@type='button' and text()='Cancel']"
# Add/Edit interface. Main locators
INTERFACE_IFC_NAME = "//input[@name='intname']"
INTERFACE_JACK_NAME = "//select[@name='jackname']"
INTERFACE_IPV4_ADDRESS = "//input[@name='ipv4']" # + netmask
INTERFACE_IPV6_ADDRESS = "//input[@name='ipv6']" # + prefix
INTERFACE_HOSTNAME = "//input[@name='hostname']"
INTERFACE_HTTPS_CERT = "//select[@id='certificate']"

# Add/Edit interface. Services configuration locators.
SERVICE_FTP = "//*[@id='ftpd']"
SERVICE_SSH = "//*[@id='sshd']"
SERVICE_HTTP = "//*[@id='httpd']"
SERVICE_HTTPS = "//*[@id='httpsd']"
SERVICE_HTTP_HTTPS_REDIRECT = "//*[@id='httpd_redirect']"
SERVICE_API_HTTP = "//*[@id='api_httpd']"
SERVICE_API_HTTPS = "//*[@id='api_httpsd']"
SERVICE_SPAM_HTTP = "//*[@id='euq_httpd']"
SERVICE_SPAM_HTTPS = "//*[@id='euq_httpsd']"
SERVICE_SPAM_HTTP_HTTPS_REDIRECT = "//*[@id='euq_httpd_redirect']"
SERVICE_SPAM_DEFAULT_INTERFACE = "//*[@id='euq_default_interface']"
SERVICE_SPAM_DEFAULT_HOSTNAME = "//*[@id='hostname_url']"
SERVICE_SPAM_DEFAULT_IP = "//*[@id='hostname_ip']"
SERVICE_SPAM_DEFAULT = "//input[@id='notification']"

# Ports
SERVICE_FTP_PORT = "//input[@id='ftpdport']"
SERVICE_SSH_PORT = "//input[@id='sshdport']"
SERVICE_HTTP_PORT = "//input[@id='httpdport']"
SERVICE_HTTPS_PORT = "//input[@id='httpsdport']"
SERVICE_API_HTTP_PORT = "//input[@id='api_httpdport']"
SERVICE_API_HTTPS_PORT = "//input[@id='api_httpsdport']"
SERVICE_SPAM_HTTP_PORT = "//input[@id='euq_httpdport']"
SERVICE_SPAM_HTTPS_PORT = "//input[@id='euq_httpsdport']"

class IpInterfaces(GuiCommon):
    """
    Library to interact with 'Network > IP Interfaces' page.
    """
    def get_keyword_names(self):
        return ['ip_interface_add',
                'ip_interface_edit',
                'ip_interface_delete',
                'ip_interface_get_list',]

    def _open_page(self):
        self._navigate_to('Network', 'IP Interfaces')

    def _open_edit_interface_page(self, interface_name):
        self._open_page()
        interface_link = \
        self._get_element_link(INTERFACES_TABLE, interface_name)
        self.click_element(interface_link)

    def _add_edit_ip_interface(self,
                               name=None,
                               ethernet=None,
                               ipv4=None,
                               ipv6=None,
                               hostname=None,
                               certificate=None,
                               enable_ftp=None,
                               ftp_port=None,
                               enable_ssh=None,
                               ssh_port=None,
                               enable_http=None,
                               http_port=None,
                               enable_https=None,
                               https_port=None,
                               enable_http_redirect=None,
                               enable_api_http=None,
                               api_http_port=None,
                               enable_api_https=None,
                               api_https_port=None,
                               enable_spam_http=None,
                               spam_http_port=None,
                               enable_spam_https=None,
                               spam_https_port=None,
                               enable_spam_http_redirect=None,
                               mark_as_default_for_spam=None,
                               url_in_notification=None):
        self._input_text_if_not_none(INTERFACE_IFC_NAME, name)
        self.select_from_dropdown_list(INTERFACE_JACK_NAME, ethernet)
        self._input_text_if_not_none(INTERFACE_IPV4_ADDRESS, ipv4)
        self._input_text_if_not_none(INTERFACE_IPV6_ADDRESS, ipv6)
        self._input_text_if_not_none(INTERFACE_HOSTNAME, hostname)
        self.select_from_dropdown_list(INTERFACE_HTTPS_CERT, certificate)
        self._select_unselect_checkbox(SERVICE_FTP, enable_ftp)
        self._input_text_if_not_none(SERVICE_FTP_PORT, ftp_port)
        self._select_unselect_checkbox(SERVICE_SSH, enable_ssh)
        self._input_text_if_not_none(SERVICE_SSH_PORT, ssh_port)
        self._select_unselect_checkbox(SERVICE_HTTP, enable_http)
        self._input_text_if_not_none(SERVICE_HTTP_PORT, http_port)
        self._select_unselect_checkbox(SERVICE_HTTPS, enable_https)
        self._input_text_if_not_none(SERVICE_HTTPS_PORT, https_port)
        self._select_unselect_checkbox\
            (SERVICE_HTTP_HTTPS_REDIRECT, enable_http_redirect)
        self._select_unselect_checkbox(SERVICE_API_HTTP, enable_api_http)
        self._input_text_if_not_none(SERVICE_API_HTTP_PORT, api_http_port)
        self._select_unselect_checkbox(SERVICE_API_HTTPS, enable_api_https)
        self._input_text_if_not_none(SERVICE_API_HTTPS_PORT, api_https_port)
        self._select_unselect_checkbox(SERVICE_SPAM_HTTP, enable_spam_http)
        self._input_text_if_not_none(SERVICE_SPAM_HTTP_PORT, spam_http_port)
        self._select_unselect_checkbox(SERVICE_SPAM_HTTPS, enable_spam_https)
        self._input_text_if_not_none(SERVICE_SPAM_HTTPS_PORT, spam_https_port)
        self._select_unselect_checkbox\
            (SERVICE_SPAM_HTTP_HTTPS_REDIRECT, enable_spam_http_redirect)
        self._select_unselect_checkbox\
            (SERVICE_SPAM_DEFAULT_INTERFACE, mark_as_default_for_spam)
        if url_in_notification is not None:
            if url_in_notification.lower()=='hostname':
                self._click_radio_button(SERVICE_SPAM_DEFAULT_HOSTNAME)
            else:
                self._click_radio_button(SERVICE_SPAM_DEFAULT_IP)
                self._input_text_if_not_none\
                    (SERVICE_SPAM_DEFAULT, url_in_notification)
        self._click_submit_button()

    @set_speed(0)
    def ip_interface_add(self,
                         name=None,
                         ethernet=None,
                         ipv4=None,
                         ipv6=None,
                         hostname=None,
                         certificate=None,
                         enable_ftp=None,
                         ftp_port=None,
                         enable_ssh=None,
                         ssh_port=None,
                         enable_http=None,
                         http_port=None,
                         enable_https=None,
                         https_port=None,
                         enable_http_redirect=None,
                         enable_api_http=None,
                         api_http_port=None,
                         enable_api_https=None,
                         api_https_port=None,
                         enable_spam_http=None,
                         spam_http_port=None,
                         enable_spam_https=None,
                         spam_https_port=None,
                         enable_spam_http_redirect=None,
                         mark_as_default_for_spam=None,
                         url_in_notification=None):
        """
        Create new IP Interface.

        *Parameters*:
        - `name`: The name of the IP Interface. String. Mandatory.
        - `ethernet`: The ethernet(jack) port to bind to. String. Allows regexp.
        - `ipv4`: The IPv4 address/Netmask. Eg: 10.92.145.159/24
        - `ipv6`: The IPv6 address/Prefix.
        - `hostname`: The hostname. String.
        - `certificate`: The certificate to use on Interface. 'System' by default.
        - `enable_ftp`: Enable FTP service. ${True} - enable; ${False} - disable.
         - `ftp_port`: FTP port.
        - `enable_ssh`: Enable SSH service. ${True} - enable; ${False} - disable.
        - `ssh_port`: SSH port.
        - `enable_http`: Enable HTTP service. ${True} - enable; ${False} - disable.
        - `http_port`: HTTP port.
        - `enable_https`: Enable HTTPS service. ${True} - enable; ${False} - disable.
        - `https_port`: HTTPS port.
        - `enable_http_redirect`: Enable HTTP>HTTPS redirect. ${True} - enable; ${False} - disable.
        - `enable_api_http`: Enable API HTTP service. ${True} - enable; ${False} - disable.
        - `api_http_port`: API HTTP port.
        - `enable_api_https`: Enable API HTTPS service. ${True} - enable; ${False} - disable.
        - `api_https_port`: API HTTPS port.
        - `enable_spam_http`: Enable EUQ HTTP service. ${True} - enable; ${False} - disable.
        - `spam_http_port`: EUQ HTTP port.
        - `enable_spam_https`: Enable EUQ HTTPS service. ${True} - enable; ${False} - disable.
        - `spam_https_port`: FEUQ HTTPS port.
        - `enable_spam_http_redirect`: Enable EUQ HTTP>HTTPS redirect. ${True} - enable; ${False} - disable.
        - `mark_as_default_for_spam`: Make the Interface default for EUQ.
        - `url_in_notification`: What URL to use in spam notification.
        Use 'hostname' - to leave hostname or define any other value ending with '/'.
        Example: http://some.url.qa/

        *Return*:
        None

        *Examples*:
        | Ip Interface Add |
        | ... | name=${data2_name} |
        | ... | ethernet=data 2 |
        | ... | ipv4=${DUT_DATA2_IP}/${DUT_DATA2_CIDR} |
        | ... | ipv6=${data2_ipv6} |
        | ... | hostname=${DUT_DATA2} |
        | ... | enable_ftp=${True} |
        | ... | ftp_port=111 |
        | ... | enable_ssh=${True} |
        | ... | ssh_port=333 |
        | ... | enable_http=${True} |
        | ... | http_port=444 |
        | ... | enable_https=${True} |
        | ... | https_port=555 |
        | ... | enable_http_redirect=${True} |
        | ... | enable_api_http=${True} |
        | ... | api_http_port=8080 |
        | ... | enable_api_https=${True} |
        | ... | api_https_port=8443 |
        | ... | enable_spam_http=${True} |
        | ... | spam_http_port=777 |
        | ... | enable_spam_https=${True} |
        | ... | spam_https_port=888 |
        | ... | enable_spam_http_redirect=${True} |
        | ... | mark_as_default_for_spam=${True} |
        | ... | url_in_notification=http://burumburururm.ua/ |

        | Ip Interface Add |
        | ... | name=${data2_name} |
        | ... | ethernet=data 2 |
        | ... | ipv4=${DUT_DATA2_IP}/${DUT_DATA2_CIDR} |
        | ... | hostname=${DUT_DATA2} |
        | ... | enable_ftp=${True} |
        | ... | enable_ssh=${True} |
        | ... | enable_http=${True} |
        | ... | enable_https=${True} |
        | ... | enable_api_http=${True} |
        | ... | enable_api_https=${True} |
        | ... | enable_spam_http=${True} |
        | ... | enable_spam_https=${True} |
        """
        self._info('Add interface: %s' % name)
        self._open_page()
        self.click_button(ADD_INTERFACE_BUTTON)
        self._add_edit_ip_interface(name=name,
            ethernet=ethernet,
            ipv4=ipv4,
            ipv6=ipv6,
            hostname=hostname,
            certificate=certificate,
            enable_ftp=enable_ftp,
            ftp_port=ftp_port,
            enable_ssh=enable_ssh,
            ssh_port=ssh_port,
            enable_http=enable_http,
            http_port=http_port,
            enable_https=enable_https,
            https_port=https_port,
            enable_http_redirect=enable_http_redirect,
            enable_api_http=enable_api_http,
            api_http_port=api_http_port,
            enable_api_https=enable_api_https,
            api_https_port=api_https_port,
            enable_spam_http=enable_spam_http,
            spam_http_port=spam_http_port,
            enable_spam_https=enable_spam_https,
            spam_https_port=spam_https_port,
            enable_spam_http_redirect=enable_spam_http_redirect,
            mark_as_default_for_spam=mark_as_default_for_spam,
            url_in_notification=url_in_notification)

    @set_speed(0)
    def ip_interface_edit(self,
                          interface_name,
                          name=None,
                          ethernet=None,
                          ipv4=None,
                          ipv6=None,
                          hostname=None,
                          certificate=None,
                          enable_ftp=None,
                          ftp_port=None,
                          enable_ssh=None,
                          ssh_port=None,
                          enable_http=None,
                          http_port=None,
                          enable_https=None,
                          https_port=None,
                          enable_http_redirect=None,
                          enable_api_http=None,
                          api_http_port=None,
                          enable_api_https=None,
                          api_https_port=None,
                          enable_spam_http=None,
                          spam_http_port=None,
                          enable_spam_https=None,
                          spam_https_port=None,
                          enable_spam_http_redirect=None,
                          mark_as_default_for_spam=None,
                          url_in_notification=None):
        """
        Edit the IP Interface.

        *Parameters*:
        - `interface_name`: The name of the intarface to edit. Mandatory.
        - `name`: The name of the IP Interface. String. Optional.
        - `ethernet`: The ethernet(jack) port to bind to. String. Allows regexp.
        - `ipv4`: The IPv4 address/Netmask. Eg: 10.92.145.159/24
        - `ipv6`: The IPv6 address/Prefix.
        - `hostname`: The hostname. String.
        - `certificate`: The certificate to use on Interface. 'System' by default.
        - `enable_ftp`: Enable FTP service. ${True} - enable; ${False} - disable.
        - `ftp_port`: FTP port.
        - `enable_ssh`: Enable SSH service. ${True} - enable; ${False} - disable.
        - `ssh_port`: SSH port.
        - `enable_http`: Enable HTTP service. ${True} - enable; ${False} - disable.
        - `http_port`: HTTP port.
        - `enable_https`: Enable HTTPS service. ${True} - enable; ${False} - disable.
        - `https_port`: HTTPS port.
        - `enable_http_redirect`: Enable HTTP>HTTPS redirect. ${True} - enable; ${False} - disable.
        - `enable_api_http`: Enable API HTTP service. ${True} - enable; ${False} - disable.
        - `api_http_port`: API HTTP port.
        - `enable_api_https`: Enable API HTTPS service. ${True} - enable; ${False} - disable.
        - `api_https_port`: API HTTPS port.
        - `enable_spam_http`: Enable EUQ HTTP service. ${True} - enable; ${False} - disable.
        - `spam_http_port`: EUQ HTTP port.
        - `enable_spam_https`: Enable EUQ HTTPS service. ${True} - enable; ${False} - disable.
        - `spam_https_port`: FEUQ HTTPS port.
        - `enable_spam_http_redirect`: Enable EUQ HTTP>HTTPS redirect. ${True} - enable; ${False} - disable.
        - `mark_as_default_for_spam`: Make the Interface default for EUQ.
        - `url_in_notification`: What URL to use in spam notification.
        Use 'hostname' - to leave hostname or define any other value ending with '/'.
        Example: http://some.url.qa/

        *Return*:
        None

        *Examples*:
        | Ip Interface Edit | ${data1_name} |
        | ... | name=${data1_name}_modified |
        | ... | ethernet=data 1 |
        | ... | ipv4=${DUT_DATA1_IP}/${DUT_DATA1_CIDR} |
        | ... | ipv6=${EMPTY} |
        | ... | hostname=${DUT_DATA1} |
        | ... | enable_ftp=${False} |
        | ... | enable_ssh=${False} |
        | ... | enable_http=${False} |
        | ... | enable_https=${False} |
        | ... | enable_http_redirect=${False} |
        | ... | enable_api_http=${True} |
        | ... | enable_api_https=${True} |
        | ... | enable_spam_http=${False} |
        | ... | enable_spam_https=${False} |
        | ... | enable_spam_http_redirect=${False} |
        | ... | mark_as_default_for_spam=${False} |
        """
        self._info('Edit interface: %s' % interface_name)
        self._open_edit_interface_page(interface_name)
        self._add_edit_ip_interface(name=name,
            ethernet=ethernet,
            ipv4=ipv4,
            ipv6=ipv6,
            hostname=hostname,
            certificate=certificate,
            enable_ftp=enable_ftp,
            ftp_port=ftp_port,
            enable_ssh=enable_ssh,
            ssh_port=ssh_port,
            enable_http=enable_http,
            http_port=http_port,
            enable_https=enable_https,
            https_port=https_port,
            enable_http_redirect=enable_http_redirect,
            enable_api_http=enable_api_http,
            api_http_port=api_http_port,
            enable_api_https=enable_api_https,
            api_https_port=api_https_port,
            enable_spam_http=enable_spam_http,
            spam_http_port=spam_http_port,
            enable_spam_https=enable_spam_https,
            spam_https_port=spam_https_port,
            enable_spam_http_redirect=enable_spam_http_redirect,
            mark_as_default_for_spam=mark_as_default_for_spam,
            url_in_notification=url_in_notification)

    @set_speed(0)
    def ip_interface_delete(self,interface_name, confirm=True):
        """
        Delete the IP Interface.

        *Parameters*:
        - `interface_name`: The name of the interface to delete. Mandatory.

        *Return*:
        None

        *Examples*:
        | Ip Interface Delete | ${data2_name} |
        """
        self._info('Delete interface: %s' % interface_name)
        del_link = \
        self._get_element_delete_link(INTERFACES_TABLE, interface_name)
        self.click_element(del_link, "don't wait")
        if confirm:
            self.click_button(INTERFACE_DELETE_CONFIRM)
        else:
            self.click_button(INTERFACE_DELETE_CANCEL)

    @set_speed(0)
    def ip_interface_get_list(self):
        """
        Get list of configured IP Interfaces.

        *Parameters*:
        None

        *Return*:
        List

        *Examples*:
        | ${interfaces} | Ip Interface Get List |
        | Log List | ${interfaces} |
        | List Should Contain Value | ${interfaces} | ${management_name} |
        """
        self._info('Get list of configured interfaces')
        self._open_page()
        return self._get_element_list(INTERFACES_TABLE)
