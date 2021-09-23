#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/gui/services/ftp_proxy.py#1 $

import common.gui.guiexceptions as guiexceptions
from common.gui.guicommon import GuiCommon

ENABLE_FTP_CHECKBOX = 'ftp_enabled'
SETTINGS_VALUE = lambda  row:\
                    '//table[@class=\'pairs\']/tbody/tr[%s]/td[1]' % str(row)

SETTINGS_NAME = lambda  row:\
                    '//table[@class=\'pairs\']/tbody/tr[%s]/th[1]' % str(row)

class FtpProxy(GuiCommon):
    """FTP Proxy Settings page interaction class."""

    def get_keyword_names(self):
        return ['ftp_proxy_enable',
                'ftp_proxy_disable',
                'ftp_proxy_edit_settings',
                'ftp_proxy_get_settings',]

    def _open_page(self):
        """Open 'FTP Proxy Management page' """
        self._navigate_to('Security Services', 'FTP Proxy')

    def ftp_proxy_enable(self,
                         port=None,
                         caching=None,
                         server_spoofing=None,
                         auth_format=None,
                         passive_port_range=None,
                         active_port_range=None,
                         welcome_banner=None,
                         control_timeout_client= None,
                         control_timeout_server= None,
                         data_timeout_client=None,
                         data_timeout_server=None):
        """Enables FTP Proxy Settings.

        Parameters:
        - `port`: proxy listening port number.
        - `caching`: set 'True' to enable, 'False' to disable.
        - `server_spoofing`: set 'True' to enable, 'False' to disable.
        - `auth_format`: authentication format.
                        Either 'Check Point' or 'Raptor'.
        - `passive_port_range`: passive mode data port range such
                            as 11000-11009.
        - `active_port_range`: active mode data port range such as 11000-11009.
        - `welcome_banner`: provide custom welcome banner. Otherwise it uses
                        FTP Server message as welcome banner.
        - `control_timeout_client`: set client side control connection
                                         timeouts in seconds.
        - `control_timeout_server`: set server side control connection
                                         timeouts in seconds.
        - `data_timeout_client` : set client side data connection timeouts
                                      in seconds.
        - `data_timeout_server`: set server side data connection timeouts
                                      in seconds.

        Example:
        | Ftp Proxy Enable |
        | Ftp Proxy Enable | port=12 | caching=${False} | server_spoofing=${True} | auth_format=Raptor | passive_port_range=100-100 | active_port_range=100-100 |
        | Ftp Proxy Enable | port=8021 | welcome_banner=Hi | control_timeout_client=100 | control_timeout_server=101 | data_timeout_client=10 | data_timeout_server=11 |
        """

        enable_ftp_button = "xpath=//input[@value='Enable and Edit Settings...']"
        self._open_page()
        if self._check_feature_status(feature='ftp_proxy'):
            return
        self.click_button(enable_ftp_button)
        self.click_element(ENABLE_FTP_CHECKBOX, "don't wait")
        self._set_proxy_listening_port(port)
        self._manipulate_caching(caching)
        self._manipulate_server_side_ip_spoofing(server_spoofing)
        self._select_authentication_format(auth_format)
        self._set_passive_mode_port_range(passive_port_range)
        self._set_active_mode_port_range(active_port_range)
        self._set_welcome_banner(welcome_banner)
        self._set_control_connection_timeout_client(control_timeout_client)
        self._set_control_connection_timeout_server(control_timeout_server)
        self._set_data_connection_timeout_client(data_timeout_client)
        self._set_data_connection_timeout_server(data_timeout_server)
        self._click_submit_button()

    def ftp_proxy_disable(self):
        """Disables Ftp proxy.

        Example:
        | Ftp Proxy Disable |
        """
        self._open_page()
        if not self._check_feature_status(feature='ftp_proxy'):
            return
        self._click_edit_settings_button()
        self.unselect_checkbox(ENABLE_FTP_CHECKBOX)
        self._click_submit_button()

    def ftp_proxy_get_settings(self):
        """Get ftp proxy settings.

        Parameters:
            None.

        Return:
            Dictionary, keys of which represent settings name.

        Example:
        | ${settings} | Ftp Proxy Get Settings |
        """

        self._open_page()
        entries = {}
        num_of_entries = int(self.get_matching_xpath_count(\
                SETTINGS_NAME('*')))
        for row in xrange(1, num_of_entries):
            if not(self._is_element_present(SETTINGS_VALUE(row))):
                continue
            entries[self.get_text(SETTINGS_NAME(row))] = \
                   self.get_text(SETTINGS_VALUE(row))
        return entries


    def _set_proxy_listening_port(self, port=None):

        listening_port_field = 'listening_port'
        if port:
            self.input_text(listening_port_field, port)

    def _manipulate_caching(self, caching=None):

        caching_checkbox = 'cache_enabled'
        if caching is not None:
            if caching:
                self.select_checkbox(caching_checkbox)
            else:
                self.unselect_checkbox(caching_checkbox)

    def _manipulate_server_side_ip_spoofing(self, server_spoofing=None):

        spoofing_checkbox = 'spoofing_enabled'
        if server_spoofing is not None:
            if server_spoofing:
                self.select_checkbox(spoofing_checkbox)
            else:
                self.unselect_checkbox(spoofing_checkbox)

    def _select_authentication_format(self, auth_format=None):

        auth_format_select = 'auth_format'
        if auth_format:
            auth_format_option = "label=%s" % (auth_format,)
            self.select_from_list(auth_format_select,
                                   auth_format_option)

    def _set_passive_mode_port_range(self, passive_port_range=None):

        passive_port_range_field = 'passive_mode_port_range'
        if passive_port_range:
            self.input_text(passive_port_range_field,
                                   passive_port_range)

    def _set_active_mode_port_range(self, active_port_range=None):

        active_port_range_field = 'active_mode_port_range'
        if active_port_range:
            self.input_text(active_port_range_field,
                                   active_port_range)

    def _set_welcome_banner(self, welcome_banner=None):

        banner_radio_button = {'server' : 'welcome_banner_server',
                               'custom' : 'welcome_banner_custom'}
        welcome_banner_txt = 'welcome_banner_custom_text'
        if not welcome_banner:
            self._click_radio_button(banner_radio_button['server'])
        else:
            self._click_radio_button(banner_radio_button['custom'])
            self.input_text(welcome_banner_txt, welcome_banner)

    def _set_control_connection_timeout_client(self,
                                               control_timeout_client=None):

        control_timeout_client_field = 'reserve_timeout_client'
        if control_timeout_client:
            self.input_text(control_timeout_client_field,
                                   control_timeout_client)

    def _set_control_connection_timeout_server(self,
                                               control_timeout_server=None):

        control_timeout_server_field = 'reserve_timeout_server'
        if control_timeout_server:
            self.input_text(control_timeout_server_field,
                                   control_timeout_server)

    def _set_data_connection_timeout_client(self, data_timeout_client=None):

        data_timeout_client_field = 'persistent_timeout_client'
        if data_timeout_client:
            self.input_text(data_timeout_client_field,
                                   data_timeout_client)

    def _set_data_connection_timeout_server(self, data_timeout_server=None):

        data_timeout_server_field = 'persistent_timeout_server'
        if data_timeout_server:
            self.input_text(data_timeout_server_field,
                                   data_timeout_server)

    def ftp_proxy_edit_settings(self,
                  port=None,
                  caching=None,
                  server_spoofing=None,
                  auth_format=None,
                  passive_port_range=None,
                  active_port_range=None,
                  welcome_banner=None,
                  control_timeout_client= None,
                  control_timeout_server= None,
                  data_timeout_client=None,
                  data_timeout_server=None):
        """Sets FTP Proxy Settings.

        Parameters:
        - `port`: proxy listening port number.
        - `caching`: set 'True' to enable, 'False' to disable.
        - `server_spoofing`: set 'True' to enable, 'False' to disable.
        - `auth_format`: authentication format.
                        Either 'Check Point' or 'Raptor'.
        - `passive_port_range`: passive mode data port range such
                            as 11000-11009.
        - `active_port_range`: active mode data port range such as 11000-11009.
        - `welcome_banner`: provide custom welcome banner. Otherwise it uses
                        FTP Server message as welcome banner.
        - `control_timeout_client`: set client side control connection
                                         timeouts in seconds.
        - `control_timeout_server`: set server side control connection
                                         timeouts in seconds.
        - `data_timeout_client` : set client side data connection timeouts
                                      in seconds.
        - `data_timeout_server`: set server side data connection timeouts
                                      in seconds.

        Example:
        | Ftp Proxy Edit Settings | port=12 | caching=${False} | server_spoofing=${True} | auth_format=Raptor | passive_port_range=100-100 | active_port_range=100-100 |
        | Ftp Proxy Edit Settings | port=8021 | welcome_banner=Hi | control_timeout_client=100 | control_timeout_server=101 | data_timeout_client=10 | data_timeout_server=11 |
        """

        self._open_page()
        if not self._check_feature_status(feature='ftp_proxy'):
            raise guiexceptions.GuiFeatureDisabledError\
                ('Cannot edit FTP proxy settings as disabled')
        self._click_edit_settings_button()
        self._set_proxy_listening_port(port)
        self._manipulate_caching(caching)
        self._manipulate_server_side_ip_spoofing(server_spoofing)
        self._select_authentication_format(auth_format)
        self._set_passive_mode_port_range(passive_port_range)
        self._set_active_mode_port_range(active_port_range)
        self._set_welcome_banner(welcome_banner)
        self._set_control_connection_timeout_client(control_timeout_client)
        self._set_control_connection_timeout_server(control_timeout_server)
        self._set_data_connection_timeout_client(data_timeout_client)
        self._set_data_connection_timeout_server(data_timeout_server)
        self._click_submit_button()
