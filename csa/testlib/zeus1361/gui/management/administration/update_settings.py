#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1360/gui/management/administration/update_settings.py#1 $ $DateTime: 2020/03/05 19:45:32 $ $Author: sarukakk $

import re

from common.gui.guicommon import GuiCommon


EDIT_SETTINGS_BUTTON = 'xpath=//input[@value="Edit Update Settings..."]'
INTERFACES_LIST = 'name=interface'
AUTO_UPDATE_LOC = 'id=enable_auto'
UPDATE_INTERVAL_LOC = 'id=update_interval'
LIST_LABEL = lambda label: 'label=%s' % (label,)

# Locators for 'Image Server'
IP_IMAGE_SERVER_RADIOBUTTON = 'id=server_type_ironport'
LOCAL_IMAGE_SERVER_RADIOBUTTON = 'id=server_type_local'
IMAGE_SERVER_URL_TEXTBOX = 'id=base_url'
IMAGE_SERVER_PORT_TEXTBOX = 'id=port'
IMAGE_SERVER_USER_TEXTBOX = 'id=username'
IMAGE_SERVER_PASSWD_TEXTBOXES = ('id=password', 'id=retype_password')
ASYNCOS_UPDATE_URL_TEXTBOX = 'id=upd_download_server'

# Locators for 'List Server'
IP_LIST_SERVER_RADIOBUTTON = 'id=upd_fetch_type_dynamic'
LOCAL_LIST_SERVER_RADIOBUTTON = 'id=upd_fetch_type_static'
LIST_SERVER_URL_TEXTBOX = 'id=upd_static_url'
LIST_SERVER_USER_TEXTBOX = 'id=upd_username'
LIST_SERVER_PASSWD_TEXTBOXES = ('id=upd_password', 'id=upd_retype_password')
LIST_SERVER_PORT_TEXTBOX = 'id=upd_port'

# Locators for 'HTTP proxy server'
HTTP_PROXY_URL = 'id=proxy_server'
HTTP_PROXY_PORT = 'id=proxy_port'
HTTP_PROXY_USER = 'id=proxy_username'
HTTP_PROXY_PASSWD = ('id=proxy_password', 'id=proxy_retype_password')

# Locators for 'HTTPS proxy server'
HTTPS_PROXY_URL = 'id=https_proxy_server'
HTTPS_PROXY_PORT = 'id=https_proxy_port'
HTTPS_PROXY_USER = 'id=https_proxy_username'
HTTPS_PROXY_PASSWD = ('id=https_proxy_password', 'id=https_proxy_retype_password')

class ServiceParams():
    """Service parameters.

    :Attributes:
        - `url`: full url to update list.
        - `port`: port.
        - `username`: username to use to connect to update server. If None,
                      assume that server does not require authentication.
        - `password`: password for `username`.
        - `asyncos_url`: url to use for upgrades for AsyncOS.
    """
    def __init__(self, url, port, username, password, asyncos_url):
        self.url = url
        self.port = port
        self.username = username
        self.password = password
        self.asyncos_url = asyncos_url


    def __str__(self):
        s = 'Full URL: %s\n' % self.url
        s += 'Port: %s\n' % self.port
        s += 'Username: %s\n' % self.username
        s += 'Password: %s\n' % self.password
        s += 'AsyncOS URL: %s\n' % self.asyncos_url

        return s


class UpdateSettings(GuiCommon):
    """keywords for Management -> System Administration -> Update Settings"""

    def get_keyword_names(self):
        return [
                'update_settings_edit_settings',
                'update_settings_set_service_params'
                ]

    def _open_page(self):
        self._navigate_to('Management', 'System Administration',
                               'Update Settings')

    def _click_edit_update_settings(self):
        self.click_button(EDIT_SETTINGS_BUTTON)
        self._info('Clicked "Edit Update Settings..." button')

    def _fill_server_credentials(self, username, username_loc,
                                       password, passwd_loc):
        if username is not None:
            self._fill_username_textbox(username, username_loc)
            self._fill_password_textboxes(password, passwd_loc)

    def _fill_username_textbox(self, username, locator):
        self.input_text(locator, username)
        self._info('Set username to "%s".' % (username,))

    def _fill_password_textboxes(self, passwd, locators):
        if passwd is not None:
            for locator in locators:
                self.input_text(locator, passwd)
            self._info('Set password to "%s".' % (passwd,))

    def _fill_port_textbox(self, port, locator):
        if port is not None:
            self.input_text(locator, port)
            self._info('Set port to "%s".'% (port,))

    def _fill_base_url_textbox(self, url, locator):
        if url is not None:
            self.input_text(locator, url)
            self._info('Set base URL to "%s".' % (url,))

    def _fill_asyncos_url_textbox(self, url, port):
        if url is not None:
            # check whether URL already contains port number
            if re.match('.*?:\d+', url) or url == '':
                update_url = url
            else:
                update_url = ':'.join((url, str(port)))
            self.input_text(ASYNCOS_UPDATE_URL_TEXTBOX, update_url)
            self._info('Set AsyncOS update URL to "%s".' % (update_url,))

    def _fill_image_server_info(self, image_server):
        if image_server is None:
            return

        if isinstance(image_server, basestring) and image_server == 'ironport':
            self._click_radio_button(IP_IMAGE_SERVER_RADIOBUTTON)
            self._info('Selected IronPort image update server.')
        elif isinstance(image_server, ServiceParams):
            self._click_radio_button(LOCAL_IMAGE_SERVER_RADIOBUTTON)
            self._info('Selected local image update server.')
            self._fill_base_url_textbox(image_server.url, IMAGE_SERVER_URL_TEXTBOX)

            self._fill_server_credentials(image_server.username,
                                          IMAGE_SERVER_USER_TEXTBOX,
                                          image_server.password,
                                          IMAGE_SERVER_PASSWD_TEXTBOXES)
            self._fill_port_textbox(image_server.port, IMAGE_SERVER_PORT_TEXTBOX)
            self._fill_asyncos_url_textbox(image_server.asyncos_url,
                                           image_server.port)
        else:
            raise ValueError('Image server must be either string "ironport" '\
                             'or an instance of UpdateImageService class')

    def _fill_list_server_info(self, list_server):
        if list_server is None:
            return

        if isinstance(list_server, basestring) and list_server == 'ironport':
            self._click_radio_button(IP_LIST_SERVER_RADIOBUTTON)
            self._info('Selected IronPort list server.')
        elif isinstance(list_server, ServiceParams):
            self._click_radio_button(LOCAL_LIST_SERVER_RADIOBUTTON)
            self._info('Selected to use local list server.')
            self._fill_base_url_textbox(list_server.url, LIST_SERVER_URL_TEXTBOX)
            self._fill_server_credentials(list_server.username,
                                          LIST_SERVER_USER_TEXTBOX,
                                          list_server.password,
                                          LIST_SERVER_PASSWD_TEXTBOXES)
            self._fill_port_textbox(list_server.port, LIST_SERVER_PORT_TEXTBOX)
        else:
            raise ValueError('List server must be either string "ironport" '\
                             'or an instance of UpdateListService class')

    def _select_auto_update(self, auto_update):
        if auto_update is None:
            return

        if auto_update != self._is_checked(AUTO_UPDATE_LOC):
            self.click_element(AUTO_UPDATE_LOC, "don't wait")
            if auto_update:
                self._info('Selected "Automatic Update".')
            else:
                self._info('Deselected "Automatic Update".')

    def _fill_update_interval(self, update_interval):
        if update_interval is None:
            return

        if self._is_checked(AUTO_UPDATE_LOC):
            self.input_text(UPDATE_INTERVAL_LOC, update_interval)
            self._info('Set Update Interval to "%s".' % update_interval)
        else:
            self._info('Update Interval was not changed because Automatic Update is not selected.')


    def _select_update_interface(self, interface):
        if interface is None:
            return

        interfaces = self.get_list_items(INTERFACES_LIST)
        for int_name in interfaces:
            if interface in int_name:
                self.select_from_list(INTERFACES_LIST, LIST_LABEL(int_name))
                self._info('Selected "%s" interface.' % (int_name,))
                break
        else:
            raise ValueError('"%s" interface does not exist' % (interface,))

    def _fill_http_proxy_info(self, proxy):
        if proxy is not None:
            self._info('Filling HTTP proxy information.')
            self._fill_proxy_name_textbox(proxy.url, HTTP_PROXY_URL,
                                          'http://')
            self._fill_server_credentials(proxy.username,
                                          HTTP_PROXY_USER,
                                          proxy.password,
                                          HTTP_PROXY_PASSWD)
            self._fill_port_textbox(proxy.port, HTTP_PROXY_PORT)

    def _fill_https_proxy_info(self, proxy):
        if proxy is not None:
            self._info('Filling HTTPS proxy information.')
            self._fill_proxy_name_textbox(proxy.url, HTTPS_PROXY_URL,
                                          'https://')
            self._fill_server_credentials(proxy.username,
                                          HTTPS_PROXY_USER,
                                          proxy.password,
                                          HTTPS_PROXY_PASSWD)
            self._fill_port_textbox(proxy.port, HTTPS_PROXY_PORT)

    def _fill_proxy_name_textbox(self, hostname, locator, prefix):
        if hostname is not None:
            proxy_name = hostname if hostname.startswith(prefix) or hostname=='' \
                                  else prefix + hostname
            self.input_text(locator, proxy_name)
            self._info('Set proxy name to "%s".' % (proxy_name,))



    def update_settings_edit_settings(self, image_server=None, list_server=None,
                      auto_update=None, update_interval=None, interface=None, http_proxy=None, https_proxy=None):
        """Edit Update Settings.

        Parameters:
            - `image_server`: server used to obtain update images. Either
                              string 'ironport' to use IronPort update servers
                              or ServiceParams instance to use custom
                              update server.
            - `list_server`: server used to obtain a list of available updates.
                             Either string 'ironport' to use IronPort update
                             server or ServiceParams instance to use custom
                             update server.
            - `auto_update`: True/False to enable disable Automatic updates for
                             Time zone rules
            - `update_interval`: update interval for Automatic Update. Use a
                                 trailing 's' for seconds, 'm' for minutes or
                                 'h' for hours. It is ignored if Automatic Update
                                 is disabled.
            - `interface`: name of the network interface to accept IronPort
                           AsyncOS upgrades.
            - `http_proxy`: HTTP proxy server to use for upgrades. An instance
                            of ServiceParams object.
            - `https_proxy`: HTTPS proxy server to use for upgrades. An
                             instance of ServiceParams object.

        Examples:
        | ${image_server}= | Update Settings Set Service Params |
        | ... | url=http://ironport.com |
        | ... | port=80 |
        | ... | username=admin |
        | ... | password=ironport |
        | ... | asyncos_url=ironport.com:80 |
        | ${list_server}= | Update Settings Set Service Params |
        | ... | url=http://ironport.com |
        | ... | port=80 |
        | ... | username=admin |
        | ... | password=ironport |
        | ${http_proxy_server}= | Update Settings Set Service Params |
        | ... | url=ironport.com |
        | ... | port=80 |
        | ... | username=admin |
        | ... | password=ironport |
        | ${https_proxy_server}= | Update Settings Set Service Params |
        | ... | url=ironport.com |
        | ... | port=443 |
        | ... | username=admin |
        | ... | password=ironport |
        | Update Settings Edit Settings |
        | ... | image_server=${image_server} |
        | ... | list_server=${list_server} |
        | ... | auto_update=${True} |
        | ... | update_interval=5m |
        | ... | interface=Management |
        | ... | http_proxy=${http_proxy_server} |
        | ... | https_proxy=${https_proxy_server} |

       Exceptions:
            - `ValueError`: in case of invalid value for any of the input
                            parameters.
            - `ConfigError`: in case of any malformed configuration for
                             `image_server`, `list_server`, `http(s)_proxy`.
        """
        self._info('Editing Update Settings...')

        self._open_page()

        self._click_edit_update_settings()

        self._fill_image_server_info(image_server)

        self._fill_list_server_info(list_server)

        self._select_auto_update(auto_update)

        self._fill_update_interval(update_interval)

        self._select_update_interface(interface)

        self._fill_http_proxy_info(http_proxy)

        self._fill_https_proxy_info(https_proxy)

        self._click_submit_button()

        self._info('Edited update settings.')


    def update_settings_set_service_params(self, url=None, port=None, username=None, password=None, asyncos_url=None):
        """Define a service parameters.

        Parameters:
            - `url`: service URL.
            - `port`: port.
            - `username`: username.
            - `password`: password.
            - `asyncosurl`: URL for Async OS updates.

        Return:
        Value of SeviceParams class

        Examples:
        | @{image_server} | Update Settings Set Service Params |
        | ... | url=http://downloads.ironport.com |
        | ... | port=80 |
        | ... | username=admin |
        | ... | password=ironport |
        | ... | asyncos_url= downloads.ironport.com |
        """
        return ServiceParams( url, port, username, password, asyncos_url)


