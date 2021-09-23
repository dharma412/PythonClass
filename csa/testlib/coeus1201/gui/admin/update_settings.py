#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/gui/admin/update_settings.py#1 $
# $DateTime: 2019/08/14 09:58:47 $
# $Author: uvelayut $

import re
from common.gui.guicommon import GuiCommon
from common.gui import guiexceptions

AUTO_UPDATE_CHKBOX = 'enable_auto'

class UpdateSettings(GuiCommon):
    """Keywords for interaction with "System Administration > Upgrade and Update
    Settings" GUI page."""

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
        """Open 'Upgrade and Update Settings' """

        self._navigate_to('System Administration',\
                               'Upgrade and Update Settings')

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

    def _set_update_interval(self, interval=None, interval_other=None):

        interval_field = 'xpath=//input [@id="wbrs_update_interval"]'
        interval_other_field = 'xpath=//input [@id="update_interval"]'
        if interval is not None:
            self.input_text(interval_field, interval)
            self._info('Setting interval to %s' % interval)
        if interval_other is not None:
            self.input_text(interval_other_field, interval_other)
            self._info('Setting interval other to %s' % interval_other)

    def _set_upgrade_notification(self, display_notification=None):

        notification_checkbox = 'upgrade_notification'
        if display_notification is not None:
            if display_notification:
                self.select_checkbox(notification_checkbox)
            else:
                self.unselect_checkbox(notification_checkbox)

    def _select_routing_table(self, routing=None):

        routing_select = 'routing_table'
        routing_option = {'data': 'label=Data',
                          'management': 'label=Management'}

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

    def _fill_server_info(self, name=None, server=None, user=None, passwd=None,
            repasswd=None):

        server_locators = {
         'url': ('upd_static_url', 'upd_download_server', 'proxy_server',),
         'port': ('upd_port', 'port', 'proxy_port',),
         'user': ('upd_username', 'username', 'proxy_username',),
         'passwd': ('upd_password', 'password', 'proxy_password',),
         'repasswd': ('upd_retype_password', 'retype_password',\
                                       'proxy_retype_password',)}

        server_index = {'list': 0, 'img': 1, 'proxy': 2}

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
                self.input_text(server_locators['user'][server_id], user)
            if passwd is not None:
                self.input_text(server_locators['passwd'][server_id], passwd)
                self.input_text(server_locators['repasswd'][server_id],
                        repasswd)

    def update_settings_edit(self,
                      enable_auto_update=None,
                      interval=None,
                      interval_other=None,
                      display_notification=None,
                      routing=None,
                      list_server=None,
                      image_server=None):
        """Edit Upgrade and Update settings.

        Using this keyword you can edit Automatic Updates, Upgrade Notifications
        and Routing Table settings and edit basic parameters such as URL and
        port of Update Servers.

        Whole parameters of Update Servers (list), Update Servers (images) and
        Proxy Server settings can be edited using following keywords:
            - `Update Settings Edit List Servers`
            - `Update Settings Edit Images Servers`
            - `Update Settings Edit Proxy Server`

        Parameters:
         - `enable_auto_update`: ${True} to enable automatic updates,
                                 ${False} to disable
            that parameter is depricated in Rainier. For backward compatibility
            assigning 0 intervals to disable updates
         - `interval`: Update Interval for Web Reputation and Categorization
            Use a trailing 'm' for minutes, 'h' for hours or 'd' for days
         - `interval_other`: Update Interval for other services
            Use a trailing 'm' for minutes, 'h' for hours or 'd' for days
         - `display_notification`: ${True} to display notification of available
           AsyncOS Upgrades, ${False} to disable notification.
         - `routing`: Routing Table either 'Management' or 'Data'
         - `list_server`: Update Servers (list). Value can be either 'Cisco' if
           'Cisco IronPort Update Servers' should be used or 'url:port' string
            if local update servers should be used.
            If post is skip then default one will be used.
         - `image_server`: Update Servers (images). Value can be either 'Same'
            if 'Same as defined in Update Servers (list)' should be used or
            'url:port' string if local update servers should be used
            If post is skip then default one will be used.

        Examples:
        | Update Settings Edit | enable_auto_update=${True} | interval=15m | routing=Management | list_server=Cisco | image_server=Same | display_notification=${False} |
        | Update Settings Edit | enable_auto_update=${False} | list_server=http://updates.example.com/my_updates.xml:80 | image_server=http://downloads.ironport.com/ |
        """
        self._info('Editting Upgrade & Update Settings...')
        self._open_page()
        self._click_edit_update_settings()
        if enable_auto_update is not None:
            if not enable_auto_update:
                interval = 0
                interval_other = 0
                self._info('Setting both interval and interval_other to 0')
        self._set_update_interval(interval, interval_other)
        self._set_upgrade_notification(display_notification)
        self._select_routing_table(routing)
        self._select_update_servers_list(list_server)
        self._select_update_servers_images(image_server)
        self._click_submit_button()

    def update_settings_edit_list_servers(self,
                      list_server=None,
                      username=None,
                      password=None,
                      repassword=None):
        """Edit Upgrade and Update Servers (list).

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

    def update_settings_edit_images_servers(self,
                      image_server=None,
                      username=None,
                      password=None,
                      repassword=None):
        """Edit Upgrade and Update settings.

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
        self._info('Editting Upgrade & Update Settings...')
        self._open_page()
        self._click_edit_update_settings()
        self._select_update_servers_images(image_server, username, password,
                repassword)
        self._click_submit_button()

    def update_settings_edit_proxy_server(self,
                      proxy_server=None,
                      username=None,
                      password=None,
                      repassword=None):
        """Edit Upgrade and Update settings.

        Parameters:
         - `proxy_server`:  'host:port' string for Proxy Server
         - `username`: user name. If None value will be left unchanged.
         - `password`: user's password
         - `repassword`: password that will be typed in 'Retype Password' field.
         If None the value of `password` parameter will be used.

        Examples:
        | Update Settings Edit Proxy Server | proxy_server=http://proxy.example.com:80 | username=testuser | password=userpass |
        """
        self._info('Editting Upgrade & Update Settings...')
        self._open_page()
        self._click_edit_update_settings()
        self._fill_server_info('proxy', proxy_server, username, password,
                repassword)
        self._click_submit_button()
