#!/usr/bin/env python -tt

from common.gui.decorators import go_to_page
from common.gui.guicommon import GuiCommon
import common.gui.guiexceptions as guiexceptions
import string

ANALYTICS_CHECKBOX = "//input[@id='check_u_a']"
EDIT_SETTINGS_BUTTON = "//input[@value='Edit Settings']"
CANCEL_BUTTON = "//input[@value='Cancel']"

PAGE_PATH = ('Management', 'System Administration', 'General Settings')


class General_Settings(GuiCommon):
    def get_keyword_names(self):
        return ['edit_general_settings',
                'get_general_analytics_setting_status']

    @go_to_page(PAGE_PATH)
    def edit_general_settings(self, edit_analytics=None):

        """Edit_usage_analytics_settings
        ...  go to management
        ...  go to system administration
        ...  go to General settings
        ...  navigate to edit settings
        ...  check the checkbox according to the user input (enable or disable)
        ...  commit changes
        """
        self.click_button(EDIT_SETTINGS_BUTTON)
        if self._is_element_present(ANALYTICS_CHECKBOX):
            if edit_analytics:
                self.select_checkbox(ANALYTICS_CHECKBOX)
            else:
                self.unselect_checkbox(ANALYTICS_CHECKBOX)
            self._click_submit_button()
            return True

    @go_to_page(PAGE_PATH)
    def get_general_analytics_setting_status(self):

        """get_general_analytics_setting_status
        ...  go to management
        ...  go to system administration
        ...  go to General settings
        ...  navigate to edit settings
        ...  verify the checkbox is enable or disable
        """
        self.click_button(EDIT_SETTINGS_BUTTON)
        if self._is_element_present(ANALYTICS_CHECKBOX):
            if self._is_checked(ANALYTICS_CHECKBOX):
                return True
            else:
                return False
