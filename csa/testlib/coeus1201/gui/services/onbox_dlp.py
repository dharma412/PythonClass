#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/gui/services/onbox_dlp.py#1 $
# $DateTime: 2019/08/14 09:58:47 $
# $Author: uvelayut $

from common.gui.guicommon import GuiCommon


class DataSecurityFilters(GuiCommon):
    """Keywords for interaction with 'Security Services -> Data Transfer Filters'
    page."""

    # method required by RF
    # return a list with all public methods
    def get_keyword_names(self):
        return ['onbox_dlp_enable',
                'onbox_dlp_disable',
                'onbox_dlp_get_status',
                ]

    def onbox_dlp_get_status(self):
        """Get Onbox Get Settings.

        Parameters:
            None.

        Return:
            ${True} is service is enabled and ${False} if not.

        Example:
        | ${result} | Onbox DLP Get Status |
        """
        value_locator = "//table[@class='pairs']/tbody/tr[1]/td[1]"
        self._open_datasecurity_filters_page()
        if self.get_text(value_locator) == "Enabled":
            return True
        else:
            return False

    def onbox_dlp_disable(self):
        """Disable Ironport Data Security Filters.

        Example:
        | Onbox Dlp Disable |
        """

        enable_filters_checkbox = 'xpath=id("dlp_toggle")'
        self._open_datasecurity_filters_page()
        # check if already disabled
        if not self._check_feature_status(feature='data_transfer_filters'):
            return

        self._click_edit_settings_button()
        self.unselect_checkbox(enable_filters_checkbox)
        self._click_submit_button()

    def onbox_dlp_enable(self):
        """Enable Ironport Data Security Filters Settings.

        Example:
        | Onbox Dlp Enable |
        """

        self._open_datasecurity_filters_page()
        # check if already enabled
        if self._check_feature_status(feature='data_transfer_filters'):
            return
        self._enable_filters()

    def _open_datasecurity_filters_page(self):
        """Open 'Cisco Ironport Data Security Filters' page."""

        self._navigate_to('Security Services', 'Data Transfer Filters')

    def _enable_filters(self):
        """Enable Cisco Ironport Data Security Filters."""

        enable_filters_button = "xpath=//input[@value='Enable...']"
        self.click_button(enable_filters_button)
