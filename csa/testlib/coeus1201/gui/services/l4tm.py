#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/gui/services/l4tm.py#1 $

from common.gui.guicommon import GuiCommon
import common.gui.guiexceptions as guiexceptions

class L4tmService(GuiCommon):
    """GUI configurator for 'Security Services -> L4 Traffic Monitor'."""

    def get_keyword_names(self):
        return [
                'l4tm_service_enable',
                'l4tm_service_disable',
                'l4tm_service_is_enabled',
                'l4tm_service_update_now',
                'l4tm_service_edit_global_settings',
                ]

    def _open_page(self):
        """Go to 'Security Services -> L4 Traffic Monitor' configuration page.
        """
        self._navigate_to('Security Services', 'L4 Traffic Monitor')

    def _enable_l4tm(self):
        """Enable L4 Traffic Monitor."""

        enable_proxy_button = "//input[@value='Enable...']"
        accept_license_button = 'action:AcceptLicense'
        self.click_button(enable_proxy_button)
        if self._is_text_present('L4 Traffic Monitor License Agreement'):
            self.click_button(accept_license_button)

    def _click_edit_global_settings_button(self):
        """Click 'Edit Global Settings...' button"""

        edit_settings_button = "//input[@value='Edit Global Settings...']"
        self.click_button(edit_settings_button)

    def _select_traffic_monitor_on(self, port):

        port_radio_button = {'all' : 'ports_all_id',
                             'except' : 'ports_np_id'}
        if port is not None:
            self._click_radio_button(port_radio_button[port.lower()])

    def l4tm_service_is_enabled(self):
        """Checks if L4 Traffic Monitor service is currently enabled.

        Example:
        | ${status}= L4TM Service Is Enabled |
        """
        self._open_page()
        return self._check_feature_status(feature='l4tm')

    def l4tm_service_update_now(self):
        """Clicks 'Update Now' button.

        Example:
        | L4TM Service Update Now |
        """

        update_now_button = "//input[@value=\'Update Now\']"

        self._open_page()
        self.click_button(update_now_button)

    def l4tm_service_disable(self):
        """Disables L4 Traffic Monitor service.

        Example:
        | L4TM Service Disable |
        """

        enable_l4tm_checkbox = 'tm_enabled_id'
        self._open_page()
        if not self._check_feature_status(feature='l4tm'):
            return
        self._click_edit_global_settings_button()
        self.click_element(enable_l4tm_checkbox, "don't wait")
        self._click_submit_button()

    def l4tm_service_enable(self):

        """Enables L4 Traffic Monitor service.

        Example:
        | L4TM Service Enable |
        """

        self._open_page()
        if self._check_feature_status(feature='l4tm'):
            return
        self._enable_l4tm()

    def l4tm_service_edit_global_settings(self, port=None):

        """Edits L4 Traffic Monitor service global settings.

        Parameter:
           - `port` : port to monitor traffic on.  Either 'all' for 'All
                      Ports' or 'except' for 'All Ports Except Web Ports
                      (HTTP/HTTPS)'.

        Examples:
        | L4TM Service Edit Global Settings | port=all |
        | L4TM Service Edit Global Settings | port=except |
        """
        self._open_page()
        if not self._check_feature_status(feature='l4tm'):
            raise exceptions.GuiFeatureDisabledError('L4 Traffic Monitor '
                                   'service is currently disabled')
        self._click_edit_global_settings_button()
        self._select_traffic_monitor_on(port)
        self._click_submit_button()
