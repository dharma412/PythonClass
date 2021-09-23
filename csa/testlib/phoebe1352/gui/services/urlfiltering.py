#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1350/gui/services/urlfiltering.py#1 $
# $DateTime: 2020/01/06 01:25:43 $
# $Author: saurgup5 $
from common.gui.decorators import set_speed
from common.gui.guicommon import GuiCommon

ENABLE_BUTTON =  "//input[@value='Enable...']"
ENABLE_CHECKBOX = "//input[@id='enabled']"
SETTINGS_BUTTON = "//input[@value='Edit Global Settings...']"
SERVICE_DISABLED_FLAG = '//dl[@class="box"]//div[@class="text-info"]'
SETTINGS_TABLE = "//table[@class='pairs s50-50']"
URLWHITELIST_COMBO = "//select[@id='url_whitelist']"
URL_CLICKTRACKING_CHECKBOX = "//input[@id='url_clicktrack']"

class urlFilteringService(GuiCommon):
    """Keywords are used to disable/enable
     URL Filtering and to edit its settings
    """

    def get_keyword_names(self):
        return ['url_Filtering_enable',
                'url_Filtering_disable',
                'url_Filtering_is_enabled',
                'url_Filtering_edit_settings',
                'url_Filtering_get_details']

    def _open_page(self):
        self._navigate_to('Security Services', "URL Filtering")

    @set_speed(0)
    def url_Filtering_enable(self, url_whitelist=None, url_click_tracking=None):
        """Enable URL Filtering Service

        Parameters:
         - url_whitelist: Assign URL Whitelists here
         - url_click_tracking: Enable URL Click Tracking
         *Example*:
         | Url Filtering Enable | url_whitelist=urllist4 | url_click_tracking=${True} |
        """
        self._info('Enabling URL Filtering Service')
        self._open_page()
        if self.url_Filtering_is_enabled():
            self._info('URL Filtering is already enabled')
            self.click_button(SETTINGS_BUTTON)
            if url_whitelist is not None:
                self.select_from_list(URLWHITELIST_COMBO,url_whitelist)

            if url_click_tracking is True:
                self.select_checkbox(URL_CLICKTRACKING_CHECKBOX)
            else:
                self.unselect_checkbox(URL_CLICKTRACKING_CHECKBOX)
        else:
            self.click_button(ENABLE_BUTTON)
            self._select_checkbox(ENABLE_CHECKBOX)

            if url_whitelist is not None:
                self.select_from_list(URLWHITELIST_COMBO,url_whitelist)

            if url_click_tracking is True:
                self.select_checkbox(URL_CLICKTRACKING_CHECKBOX)

        self._click_submit_button()

    @set_speed(0)
    def url_Filtering_disable(self):
        """Disable URL Filtering Service
        *Example*:
        | Url Filtering Disable |
        """
        self._info('Disabling URL Filtering Service')
        self._open_page()
        if not self.url_Filtering_is_enabled():
            self._info('URL Filtering is already disabled')
            return
        self.click_button(SETTINGS_BUTTON)
        self._unselect_checkbox(ENABLE_CHECKBOX)
        self._click_submit_button()

    @set_speed(0)
    def url_Filtering_is_enabled(self):
        """Check whether URL Filtering is enabled
        Return:
            Boolean True or False
        *Example*:
        | Url Filtering Is Enabled |
        """
        self._info('Checking if URL Filtering is enabled')
        self._open_page()
        return not self._is_element_present(SERVICE_DISABLED_FLAG)

    @set_speed(0)
    def url_Filtering_edit_settings(self, url_whitelist=None, url_click_tracking=None):
        """Edit URL Filtering Service settings

        Parameters:
         - url_whitelist: Assign URL Whitelists here
         - url_click_tracking: Enable URL Click Tracking
        *Example*:
        | url_Filtering_Edit Settings | url_whitelist=urllist2 | url_click_tracking=${False} |
        """
        self._info("Editing URL Filtering settings")
        self._open_page()
        self.click_button(SETTINGS_BUTTON)
        self._edit_settings(url_whitelist, url_click_tracking)

    def _edit_settings(self, url_whitelist=None, url_click_tracking=None):
        if url_whitelist is not None:
            self.select_from_list(URLWHITELIST_COMBO,url_whitelist)
        if url_click_tracking is not None:
            if url_click_tracking:
                self.select_checkbox(URL_CLICKTRACKING_CHECKBOX)
            else:
                self.unselect_checkbox(URL_CLICKTRACKING_CHECKBOX)
        self._click_submit_button()

    @set_speed(0)
    def url_Filtering_get_details(self):
        """Collect information related to URL Filtering

        *Return:*
        Dictionary which keys are:

        | URL Category and Reputation Filters | <Url Filtering status text (Enabled/Disabled)> |
        | Cisco Web Security Services connection status | <Connected or not > |
        | URL Whitelist | <url whitelist selected> |
        | URL Click Tracking | <Enabled/Disabled> |

        *Examples:*
        | ${details}= | URL Filtering Get Details |
        | ${settings}= | Get From Dictionary | ${details} | Settings |
        | Log | ${settings} |
        """
        self._open_page()
        if not self.url_Filtering_is_enabled():
            self._info('URL Filtering is already disabled')
            return
        status_info = {}
        status_info['Settings'] = self._get_settings()
        return status_info

    def _get_settings(self):
        settings = {}
        for row in xrange(1, 5):
            key = self.get_text("%s/tbody/tr[%d]/th" % \
                                (SETTINGS_TABLE, row)).strip()
            value = self.get_text("%s/tbody/tr[%d]/td" % \
                                (SETTINGS_TABLE, row)).strip()
            settings[key] = value
        return settings
