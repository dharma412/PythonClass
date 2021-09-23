#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1250/gui/management/administration/network_access.py#3 $
# $DateTime: 2019/06/07 02:45:52 $
# $Author: sarukakk $

import common.gui.guiexceptions as guiexceptions

from common.gui.guicommon import GuiCommon


GUI_TIMEOUT_TEXTBOX = 'session_timeout'
CONTROL_MODE_LIST = 'access_type'
ACL_LIST_TEXTBOX = 'access_list'
PROXY_LIST_TEXTBOX = 'proxy_list'
HEADER_NAME_TEXTBOX = 'ip_header'

control_mode_map = {
    'any': 'Allow Any Connection',
    'specific': 'Only Allow Specific Connections',
    'proxy': 'Only Allow Specific Connections Through Proxy',
    'specific_proxy': 'Allow Specific Connections Directly or Through Proxy'
    }


class NetworkAccess(GuiCommon):

    """Keywords for Management Appliance -> System Administration -> Network
    Access
    """

    def get_keyword_names(self):
        return ['network_access_edit_settings',
                'network_access_get_gui_timeout',
                'network_access_get_acl_list',
                'network_access_get_proxy_list',
                'network_access_get_ip_header']

    def _open_page(self):
        self._navigate_to('Management', 'System Administration',
            'Network Access')

    def _is_element_disabled(self, locator):
        # disabled element on 'Network Access' page has non-empty style
        # attribute
        try:
            self.get_element_attribute('@'.join((locator, 'style')))
            return True
        except:
            return False

    def _fill_out_field(self, locator, value, name):
        if value is None:
            return

        if self._is_element_disabled(locator):
            raise guiexceptions.GuiFeatureDisabledError(\
                    '%s is disabled' % (name,))

        self.input_text(locator, value)

    def network_access_edit_settings(self, timeout=None, mode=None,
        user_ip=None, proxy_ip=None, header=None):
        """Edit network access settings.

        Parameters:
        - `timeout`: GUI session inactivity timeout in minutes.
        - `mode`: mode of control for access list. One of 'any', 'specific',
           'proxy', 'specific_proxy'.
        - `user_ip`: IP addresses from which users will be allowed to connect
           to the appliance. Comma-separated string of IP addresses.
        - `proxy_ip`: IP addresses of the proxies allowed to connect to the
           appliance. Comma-separated string of IP addresses.
        - `header`: name of the origin IP header that the proxy sends to the
           appliance. String.

        Examples:
        | Network Access Edit Settings | 20 | any |
        | Network Access Edit Settings | 5 | specific | 1.2.3.4, 5.6.7.8 |
        | Network Access Edit Settings | 10 | specific_proxy | 1.2.3.4 |
        | ... | 10.2.3.4, 10.5.6.7 | x-forward |

        Exceptions:
        - `GuiValueError`: in case of invalid `control_mode` value.
        - `GuiFeatureDisabledError`: in case of trying to modify field which is
           disabled. e.g. trying to change `header_name` when `control_mode` is
           'any'.
        """
        self._open_page()

        self._click_edit_settings_button()

        if timeout is not None:
            self.input_text(GUI_TIMEOUT_TEXTBOX, timeout)

        if mode is not None:
            if mode not in control_mode_map:
                raise guiexceptions.GuiValueError(
                    'Wrong %s value for control mode.' % (mode,))
            self.select_from_list(CONTROL_MODE_LIST, control_mode_map[mode])

        for locator, value, field_name in (
            (ACL_LIST_TEXTBOX, user_ip, 'ACL list'),
            (PROXY_LIST_TEXTBOX, proxy_ip, 'Proxy list'),
            (HEADER_NAME_TEXTBOX, header, 'Header name')
            ):
            self._fill_out_field(locator, value, field_name)

        self._click_submit_button(False, True)

    def network_access_get_gui_timeout(self):
        """Get GUI session inactivity timeout.

        Return:
        Session inactivity timeout value.

        Examples:
        | ${inactivity_timeout} = | Network Access Get GUI Timeout |
        """
        self._open_page()

        self._click_edit_settings_button()

        return self.get_value(GUI_TIMEOUT_TEXTBOX)

    def network_access_get_acl_list(self):
        """Get the IP addresses from ACL list.

        Return:
        A list of IP addresses on ACL list.

        Examples:
        | @{acl_list} = | Network Access Get ACL List |
        """
        self._open_page()

        self._click_edit_settings_button()

        acl_list = self.get_value(ACL_LIST_TEXTBOX)

        return self._convert_to_list(acl_list)

    def network_access_get_proxy_list(self):
        """Get the IP addresses from Proxy list.

        Return:
        A list of IP addresses of Proxy list.

        Examples:
        | @{proxy_list} = | Network Access Get Proxy List |
        """
        self._open_page()

        self._click_edit_settings_button()

        proxy_list = self.get_value(PROXY_LIST_TEXTBOX)

        return self._convert_to_list(proxy_list)

    def network_access_get_ip_header(self):
        """Get Origin IP Header value.

        Return:
        Origin IP Header value.

        Examples:
        | ${ip_header} = | Network Access Get Ip Header |
        """
        self._open_page()

        self._click_edit_settings_button()

        return self.get_value(HEADER_NAME_TEXTBOX)
