#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1350/gui/services/update_settings.py#1 $
# $DateTime: 2020/01/06 01:25:43 $
# $Author: saurgup5 $

import re
from common.gui.decorators import set_speed
from common.gui.guicommon import GuiCommon
from common.gui import guiexceptions

AUTO_UPDATE_CHKBOX = 'enable_auto_upd'

class UpdateSettings(GuiCommon):
    """Keywords for interaction with "Security Services > Service Updates"
       GUI page."""

    # method required by RF
    # return a list with all public methods
    def get_keyword_names(self):
        return [
                'update_settings_edit',
                'update_settings_edit_list_servers',
                'update_settings_edit_images_servers',
                'update_settings_edit_proxy_server',
                ]

    def _open_page(self):
        """Open 'Service Updates' """

        self._navigate_to('Security Services','Service Updates')

    def _click_edit_update_settings(self):
        """Edit Update Settings."""

        edit_settings_button = "xpath=//input[@value='Edit Update Settings...']"
        self.click_button(edit_settings_button)
        self._info('Clicked \'Edit Update Settings...\' button')

    def _select_update_servers_list(self, list_server=None, user=None,
            passwd=None, repasswd=None):

        list_radio_button = {'ironport': 'upd_fetch_type_dynamic',
                             'local': 'upd_fetch_type_static'}

        if list_server is not None:
            if list_server.lower() == 'cisco':
                self._click_radio_button(list_radio_button['ironport'])
                self._info('Selected \'IronPort Update Servers\'')
            else:
                # server url and port given
                self._click_radio_button(list_radio_button['local'])
                self._info('Selected \'Local Update Servers(list)\'')
                self._fill_server_info('list', list_server, user, passwd,
                        repasswd)

    def _select_update_servers_images(self, image_server=None, user=None,
            passwd=None, repasswd=None):

        image_radio_button = {'same': 'server_type_ironport',
                              'local': 'server_type_local'}

        if image_server is not None:
            if image_server.lower() == 'same':
                self._click_radio_button(image_radio_button['same'])
                self._info('Selected \'Same as defined in Update Servers\'')
            else:
                # server url and port given
                self._click_radio_button(image_radio_button['local'])
                self._info('Selected \'Local Update Servers(image)\'')
                self._fill_server_info('img', image_server, user, passwd,
                        repasswd)

    def _manipulate_automatic_updates_checkbox(self, enable_auto_update=None):

        if enable_auto_update is not None:
            if enable_auto_update:
                self.select_checkbox(AUTO_UPDATE_CHKBOX)
                self._info('Enabled automatic updates')
            else:
                self.unselect_checkbox(AUTO_UPDATE_CHKBOX)
                self._info('Disabled automatic updates')

    def _set_update_interval(self, interval=None):

        interval_field = 'upd_fetch_interval'
        if interval is not None:
            if self._is_checked(AUTO_UPDATE_CHKBOX):
                self.input_text(interval_field, interval)
                self._info('Setting interval to %s' % interval)
            else:
                raise guiexceptions.GuiFeatureDisabledError\
                       ('Cannot set update interval, as disabled')

    def _fill_server_info(self, name=None, server=None, user=None, passwd=None,
            repasswd=None):

        server_locators = {
            'url': ('upd_static_url', 'base_url', 'proxy_server', 'https_proxy_server',),
            'port': ('upd_port', 'port', 'proxy_port', 'https_proxy_port',),
            'user': ('upd_username', 'username', 'proxy_username', 'https_proxy_username',),
            'passwd': ('upd_password', 'password', 'proxy_password', 'https_proxy_password',),
            'repasswd': ('upd_retype_password', 'retype_password',\
                                          'proxy_retype_password', 'https_proxy_retype_password',)}
        server_index = {'list': 0, 'img': 1, 'proxy': 2, 'https_proxy': 3}

        if server is not None:
            # retrieve url and port
            server_pattern = r"(.*):(\d+)$"
            server_match = re.match(server_pattern, server.strip())
            if server_match:
                url = server_match.group(1)
                port = server_match.group(2)
            else:
                url = server
                port = None

            # set retype password
            if repasswd is None:
                repasswd = passwd

            self._info('Setting "%s" server info.' % (name,))
            server_id = server_index[name]
            self.input_text(server_locators['url'][server_id], url)
            if port is not None:
                self.input_text(server_locators['port'][server_id], port)
            if user is not None:
                self.input_text("//input[@id='%s']" % server_locators['user'][server_id], user)
            if passwd is not None:
                self.input_text("//input[@id='%s']" % server_locators['passwd'][server_id], passwd)
                self.input_text("//input[@id='%s']" % server_locators['repasswd'][server_id], repasswd)

    @set_speed(0)
    def update_settings_edit(self,
                      enable_auto_update=None,
                      interval=None,
                      list_server=None,
                      image_server=None):
        """Edit Update settings.

        Using this keyword you can edit Automatic Updates and Routing Table
        settings and edit basic parameters such as URL and
        port of Update Servers.

        Whole parameters of Update Servers (list), Update Servers (images) and
        Proxy Server settings can be edited using following keywords:
            - `Update Settings Edit List Servers`
            - `Update Settings Edit Images Servers`
            - `Update Settings Edit Proxy Server`

        Parameters:
         - `enable_auto_update`: ${True} to enable automatic updates,
                                 ${False} to disable
         - `interval`: Update Interval for automatic updates applicable
            if 'enable_auto_update' is enabled (Use a trailing 'm' for minutes,
            'h' for hours or 'd' for days)
         - `list_server`: Update Servers (list). Value can be either 'Cisco' if
           'Cisco IronPort Update Servers' should be used or 'url:port' string
            if local update servers should be used.
            If post is skip then default one will be used.
         - `image_server`: Update Servers (images). Value can be either 'Same'
            if 'Same as defined in Update Servers (list)' should be used or
            'url:port' string if local update servers should be used
            If post is skip then default one will be used.

        Examples:
        | Update Settings Edit | enable_auto_update=${True} | interval=15m | list_server=Cisco | image_server=Same |
        | Update Settings Edit | enable_auto_update=${False} | list_server=http://updates.example.com/my_updates.xml:80 | image_server=http://downloads.ironport.com/ |
        """
        self._info('Editing Update Settings...')
        self._open_page()
        self._click_edit_update_settings()
        self._manipulate_automatic_updates_checkbox(enable_auto_update)
        self._set_update_interval(interval)
        self._select_update_servers_list(list_server)
        self._select_update_servers_images(image_server)
        self._click_submit_button()

    @set_speed(0)
    def update_settings_edit_list_servers(self,
                      list_server=None,
                      username=None,
                      password=None,
                      repassword=None):
        """Edit Update Servers (list).

        Parameters:
         - `list_server`: Update Servers (list). Value can be either 'Cisco' if
           'Cisco IronPort Update Servers' should be used or 'url:port' string
            if local update servers should be used.
            If post is skip then default one will be used.
         - `username`: user name. If None value will be left unchanged.
         - `password`: user's password
         - `repassword`: password that will be typed in 'Retype Password' field.
         If None the value of `password` parameter will be used.

        Examples:
        | Update Settings Edit List Servers | list_server=Cisco |
        | Update Settings Edit List Servers | list_server=http://updates.example.com/my_updates.xml:80 | username=testuser | password=userpass |
        """
        self._info('Editting Upgrade & Update Settings...')
        self._open_page()
        self._click_edit_update_settings()
        self._select_update_servers_list(list_server, username, password,
                repassword)
        self._click_submit_button()

    @set_speed(0)
    def update_settings_edit_images_servers(self,
                      image_server=None,
                      username=None,
                      password=None,
                      repassword=None):
        """Edit Update settings.

        Parameters:
         - `image_server`: Update image Servers
                          * 'same': Same as defined in Update Servers (list)
                          * 'host:port' string for Local Update Servers
                            (location of update image files)

         - `username`: user name. If None value will be left unchanged.
         - `password`: user's password
         - `repassword`: password that will be typed in 'Retype Password' field.
         If None the value of `password` parameter will be used.

        Examples:
        | Update Settings Edit Images Servers | image_server=Same |
        | Update Settings Edit Images Servers | image_server=http://downloads.example.com:80 | username=testuser | password=userpass |
        """
        self._info('Editting Update Settings...')
        self._open_page()
        self._click_edit_update_settings()
        self._select_update_servers_images(image_server, username, password,
                repassword)
        self._click_submit_button()

    @set_speed(0)
    def update_settings_edit_proxy_server(self,
                      proxy_type=None,
                      proxy_server=None,
                      username=None,
                      password=None,
                      repassword=None):
        """Edit Update settings.

        Parameters:
         - `proxy_server`:  'host:port' string for Proxy Server
         - `username`: user name. If None value will be left unchanged.
         - `password`: user's password
         - `repassword`: password that will be typed in 'Retype Password' field.
         If None the value of `password` parameter will be used.

        Examples:
        | Update Settings Edit Proxy Server | proxy_server=http://proxy.example.com:80 | username=testuser | password=userpass |
        """
        self._info('Editing Update Settings...')
        self._open_page()
        self._click_edit_update_settings()
        if proxy_type.lower() == 'http':
            self._fill_server_info('proxy', proxy_server, username, password, repassword)
        if proxy_type.lower() == "https":
            self._fill_server_info('https_proxy', proxy_server, username, password, repassword)
        self._click_submit_button()
