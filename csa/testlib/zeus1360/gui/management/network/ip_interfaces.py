# $Id: //prod/main/sarf_centos/testlib/zeus1360/gui/management/network/ip_interfaces.py#1 $ $DateTime: 2020/03/05 19:45:32 $ $Author: sarukakk $


import common.gui.guiexceptions as guiexceptions

from common.gui.guicommon import GuiCommon


ADD_INTERFACE_BUTTON = "//input[@value='Add IP Interface...']"
INTERFACES_TABLE_CELL = lambda row, column:\
    "//table[@class='cols']//tr[%s]/td[%s]" % (row, column)
INTERFACES_TABLE = "//*/table[@class='cols']"
INTERFACE_NAME_CELL = lambda row: INTERFACES_TABLE_CELL(row, 1) + '/a'
INTERFACE_DELETE_CELL = lambda row: INTERFACES_TABLE_CELL(row, 4) + '/img'
IF_NAME_TEXTBOX = 'intname'
IF_ETH_PORT_LIST = 'jackname'
IF_ADDRESS_TEXTBOX = 'ip'
IF_NETMASK_TEXTBOX = 'netmask'
IF_HOSTNAME_TEXTBOX = 'hostname'

FTP_CHECKBOX = 'ftpd'
FTP_TEXTBOX = 'ftpdport'
TELNET_CHECKBOX = 'telnetd'
TELNET_TEXTBOX = 'telnetdport'
SSH_CHECKBOX = 'sshd'
SSH_TEXTBOX = 'sshdport'
HTTP_CHECKBOX = 'httpd'
HTTP_TEXTBOX = 'httpdport'
HTTPS_CHECKBOX = 'httpsd'
HTTPS_TEXTBOX = 'httpsdport'
HTTP_REDIRECT_CHECKBOX = 'httpd_redirect'
ISQ_HTTP_CHECKBOX = 'euq_httpd'
ISQ_HTTP_TEXTBOX = 'euq_httpdport'
ISQ_HTTPS_CHECKBOX = 'euq_httpsd'
ISQ_HTTPS_TEXTBOX = 'euq_httpsdport'
ISQ_HTTP_REDIRECT_CHECKBOX = 'euq_httpd_redirect'
ISQ_DEFAULT_IF_CHECKBOX = 'euq_default_interface'
ISQ_LOCALHOST_RADIOBUTTON = 'hostname_url'
ISQ_CUSTOM_HOST_RADIOBUTTON = 'hostname_ip'
ISQ_HOSTNAME_TEXTBOX = 'notification'


class IPInterfaces(GuiCommon):

    """Keywords for Management Appliance -> Network -> IP Interfaces"""

    def get_keyword_names(self):
        return ['ip_interfaces_add',
                'ip_interfaces_edit',
                'ip_interfaces_delete',
                'ip_interface_get_list',
                ]

    def _open_page(self):
        self._navigate_to('Management', 'Network', 'IP Interfaces')

    def _get_interfaces_names(self):
        if_names = []

        num_of_rows =\
        int(self.get_matching_xpath_count(INTERFACE_NAME_CELL('*')))

        for row in range(2, num_of_rows + 2):
            if_names.append(self.get_text(INTERFACE_NAME_CELL(row)))

        return if_names

    def _fill_interface_info(self, name, address, host, netmask, eth_port):
        if not (self._is_visible(IF_NAME_TEXTBOX) or name is None):
            raise guiexceptions.ConfigError(
                'Name of the interface can not be changed')

        for locator, value in ((IF_NAME_TEXTBOX, name),
                               (IF_ADDRESS_TEXTBOX, address),
                               (IF_HOSTNAME_TEXTBOX, host),
                               (IF_NETMASK_TEXTBOX, netmask)):
            if value is not None:
                self.input_text(locator, value)

        if eth_port is not None:
            self.select_from_list(IF_ETH_PORT_LIST, eth_port)

    def _select_services(self, ftp, telnet, ssh, http, https, http_redirect,
        isq_http, isq_https, isq_http_redirect, isq_default):

        for checkbox, textbox, value in (
                (FTP_CHECKBOX, FTP_TEXTBOX, ftp),
                (TELNET_CHECKBOX, TELNET_TEXTBOX, telnet),
                (SSH_CHECKBOX, SSH_TEXTBOX, ssh),
                (HTTP_CHECKBOX, HTTP_TEXTBOX, http),
                (HTTPS_CHECKBOX, HTTPS_TEXTBOX, https),
                (HTTP_REDIRECT_CHECKBOX, None, http_redirect),
                (ISQ_HTTP_CHECKBOX, ISQ_HTTP_TEXTBOX, isq_http),
                (ISQ_HTTPS_CHECKBOX, ISQ_HTTPS_TEXTBOX, isq_https),
                (ISQ_HTTP_REDIRECT_CHECKBOX, None, isq_http_redirect)):

            if value is None:
                continue

            if not value:
                self._unselect_checkbox(checkbox)
            else:
                self._select_checkbox(checkbox)
                if isinstance(value, basestring):
                    self.input_text(textbox, value)

        if isq_default is not None:
            if isq_default:
                self._select_checkbox(ISQ_DEFAULT_IF_CHECKBOX)
                if isinstance(isq_default, basestring):
                    self._click_radio_button(ISQ_CUSTOM_HOST_RADIOBUTTON)
                    self.input_text(ISQ_HOSTNAME_TEXTBOX, isq_default)
                else:
                    self._click_radio_button(ISQ_LOCALHOST_RADIOBUTTON)
            else:
                self._unselect_checkbox(ISQ_DEFAULT_IF_CHECKBOX)

    def _get_interface_row_index(self, name):
        names = self._get_interfaces_names()
        if name not in names:
            raise ValueError('`%s` interface is not present on the page' %\
                (name,))

        return names.index(name) + 2

    def _click_edit_interface_link(self, name):
        row_index  = self._get_interface_row_index(name)
        self.click_element(INTERFACE_NAME_CELL(row_index))

    def _click_delete_interface_link(self, name):
        row_index  = self._get_interface_row_index(name)
        delete_loc = INTERFACE_DELETE_CELL(row_index)

        if not self._is_element_present(delete_loc):
            raise guiexceptions.ConfigError(
                '`%s` interface can not be removed' % (name,))

        self.click_element(delete_loc, 'dont wait')
        self._click_continue_button()

    def ip_interfaces_add(self, name, ip_address, hostname, netmask=None,
        eth_port=None, ftp_service=None, telnet_service=None, ssh_service=None,
        http_service=None, https_service=None, redirect_http=None,
        isq_http_service=None, isq_https_service=None, redirect_isq_http=None,
        isq_default=None):
        """Add new interface.

        Parameters:
        - `name`: nickname of the interface.
        - `ip_address`: IP address of the interface
        - `hostname`: hostname that is related to the interface.
        - `netmask`: network's mask.
        - `eth_port`: ethernet port of the interface.
        - `ftp_service`: FTP service configuration. ${False} to disable,
           ${True} to enable or specify a number to enable FTP on custom port.
        - `telnet_service`: telnet service configuration. ${False} to disable,
           ${True} to enable or specify a number to enable Telnet on custom
           port.
        - `ssh_service`: SSH service configuration. ${False} to disable,
           ${True} to enable or specify a number to enable Telnet on custom
           port.
        - `http_service`: HTTP service configuration. ${False} to disable,
           ${True} to enable or specify a number to enable HTTP on custom
           port.
        - `https_service`: HTTPS service configuration. ${False} to disable,
           ${True} to enable or specify a number to enable HTTPS on custom
           port.
        - `redirect_http`: redirect HTTP requests to HTTPS. Boolean.
        - `isq_http_service`: ISQ HTTP service configuration. ${False} to
           disable, ${True} to enable or specify a number to enable ISQ HTTP
           on custom port.
        - `isq_https_service`: ISQ HTTPS service configuration. ${False} to
           disable, ${True} to enable or specify a number to enable ISQ HTTPS
           on custom port.
        - `redirect_isq_http`: redirect ISQ HTTP requests to HTTPS. Boolean.
        - `isq_default`: configure as default interface for ISQ. ${True} to
           use as default interface for ISQ and use hostname as URL displayed
           in notifications, any other URL string to enable and use this string
           as URL, ${False} to no use as default interface.

        Examples:
        | IP Interfaces Add | new_intf | 1.2.3.4 | somedut.qa |
        | IP Interfaces Add | my_intf | 1.2.3.4 | mydut.qa | 255.255.255.0 |
        | ... | Data 1 | ${True} | 26 | ${True} | ${False} | ${True} |
        | ... | ${True} | 82 | 83 | ${False} | http//mydut.qa/ |
        """
        self._open_page()

        self.click_button(ADD_INTERFACE_BUTTON)

        self._fill_interface_info(name, ip_address, hostname, netmask,
            eth_port)

        self._select_services(ftp_service, telnet_service, ssh_service,
            http_service, https_service, redirect_http, isq_http_service,
            isq_https_service, redirect_isq_http, isq_default)

        self._click_submit_button()

    def ip_interfaces_edit(self, name, new_name=None, ip_address=None,
        hostname=None, netmask=None, eth_port=None, ftp_service=None,
        telnet_service=None, ssh_service=None, http_service=None,
        https_service=None, redirect_http=None, isq_http_service=None,
        isq_https_service=None, redirect_isq_http=None, isq_default=None):
        """Edit configured interface.

        Parameters:
        - `name`: name of the interface to edit.
        - `newname`: new name for the interface.
        - `ip_address`: IP address of the interface
        - `hostname`: hostname that is related to the interface.
        - `netmask`: network's mask.
        - `eth_port`: ethernet port of the interface.
        - `ftp_service`: FTP service configuration. ${False} to disable,
           ${True} to enable or specify a number to enable FTP on custom port.
        - `telnet_service`: telnet service configuration. ${False} to disable,
           ${True} to enable or specify a number to enable Telnet on custom
           port.
        - `ssh_service`: SSH service configuration. ${False} to disable,
           ${True} to enable or specify a number to enable Telnet on custom
           port.
        - `http_service`: HTTP service configuration. ${False} to disable,
           ${True} to enable or specify a number to enable HTTP on custom
           port.
        - `https_service`: HTTPS service configuration. ${False} to disable,
           ${True} to enable or specify a number to enable HTTPS on custom
           port.
        - `redirect_http`: redirect HTTP requests to HTTPS. Boolean.
        - `isq_http_service`: ISQ HTTP service configuration. ${False} to
           disable, ${True} to enable or specify a number to enable ISQ HTTP
           on custom port.
        - `isq_https_service`: ISQ HTTPS service configuration. ${False} to
           disable, ${True} to enable or specify a number to enable ISQ HTTPS
           on custom port.
        - `redirect_isq_http`: redirect ISQ HTTP requests to HTTPS. Boolean.
        - `isq_default`: configure as default interface for ISQ. ${True} to
           use as default interface for ISQ and use hostname as URL displayed
           in notifications, any other URL string to enable and use this string
           as URL, ${False} to no use as default interface.

        Exceptions:
        - `ValueError`: in case interface was not found on the page.
        - `ConfigError`: when trying to change the name of the interface that
           can not be edited. e.g. Management.

        Examples:
        | IP Interfaces Edit | my_intf | isq_default=${True} |
        | IP Interfaces Edit | my_intf | eth_port=Data 2 |
        | ... | http_service=${False} |
        | IP Interfaces Edit | my_intf | new_name | 1.2.3.4 | mydut.qa |
        | ... | 255.255.255.0 | Data 1 | ${True} | 26 | ${True} | ${False} |
        | ... | ${True} | ${True} | 82 | 83 | ${False} | http//mydut.qa/ |
        """
        self._open_page()

        self._click_edit_interface_link(name)

        self._fill_interface_info(new_name, ip_address, hostname, netmask,
            eth_port)

        self._select_services(ftp_service, telnet_service, ssh_service,
            http_service, https_service, redirect_http, isq_http_service,
            isq_https_service, redirect_isq_http, isq_default)

        self._click_submit_button()

    def ip_interfaces_delete(self, name):
        """Delete IP interface.

        Parameters:
        - `name`: name of the IP interface to delete.

        Exceptions:
        - `ValueError`: in case interface was not found on the page.
        - `ConfigError`: when trying to remove interface that can not be
           removed. e.g. Management

        Examples:
        | IP Interfaces Delete | my_interface |
        """
        self._open_page()

        self._click_delete_interface_link(name)

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

