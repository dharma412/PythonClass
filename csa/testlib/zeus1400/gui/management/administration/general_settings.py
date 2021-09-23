#!/usr/bin/env python -tt

from common.gui.decorators import go_to_page
from common.gui.guicommon import GuiCommon
import common.gui.guiexceptions as guiexceptions
import string

ANALYTICS_CHECKBOX = "//input[@id='check_u_a']"
SECUREX_CHECKBOX = "//input[@id='secure_x' and @type='checkbox']"
GENERAL_SETTINGS_PREFRENCES = "//*[@class='pairs']"
GENERAL_SETTINGS_PREFRENCES_TH = "/tbody/tr[%s]/th"
GENERAL_SETTINGS_PREFRENCES_TD = "/tbody/tr[%s]/td"
EDIT_SETTINGS_BUTTON = "//input[@value='Edit Settings']"
CANCEL_BUTTON = "//input[@value='Cancel']"

PAGE_PATH = ('Management','System Administration','General Settings')

class General_Settings(GuiCommon):
    def get_keyword_names(self):
        return ['edit_general_settings',
                'get_general_analytics_setting_status',
                'edit_securex_settings',
                'get_securex_edit_setting_status',
                'get_general_settings_preferences']

    def _edit_securex_settings(self,state):
        if self._is_element_present(SECUREX_CHECKBOX):
           self._set_checkbox(state, SECUREX_CHECKBOX)

    def _edit_analytics_settings(self,state):
         if self._is_element_present(ANALYTICS_CHECKBOX):
            self._set_checkbox(state, ANALYTICS_CHECKBOX)


    @go_to_page(PAGE_PATH)
    def edit_general_settings(self,edit_analytics=None ,edit_securex= True):

        """Edit_usage_analytics_settings
        ...  go to management
        ...  go to system administration
        ...  go to General settings
        ...  navigate to edit settings
        ...  check the checkbox according to the user input (enable or disable)
        ...  commit changes
        """
        self.click_button(EDIT_SETTINGS_BUTTON)

        if edit_analytics:
            self._edit_analytics_settings(True)
        else:
            self._edit_analytics_settings(False)

        if edit_securex:
           self._edit_securex_settings(True)
        else:
           self._edit_securex_settings(False)

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

    @go_to_page(PAGE_PATH)
    def edit_securex_settings(self,enable= True):
        """
         *Example*

         |Enable - Edit Securex Settings  True |
         |Disable- Edit Securex Settings  False or None |

        """
        self.click_button(EDIT_SETTINGS_BUTTON)
        if enable:
           self._edit_securex_settings(True)
        else:
           self._edit_securex_settings(False)

        self._click_submit_button()


    @go_to_page(PAGE_PATH)
    def get_securex_edit_setting_status(self):
        """ Get Securex Setting Status
         *Examples:*
         | ${status}= Get Securex Edit Setting Status |
        """
        self.click_button(EDIT_SETTINGS_BUTTON)
        if self._is_element_present(SECUREX_CHECKBOX):
           if self._is_checked(SECUREX_CHECKBOX):
              return True
           else:
              return False

    @go_to_page(PAGE_PATH)
    def get_general_settings_preferences(self):
       """
         To get the General Preferences
         :return: settings dictionary
       """
       settings = {}
       for index in range(1,4):
           key = ''.join([GENERAL_SETTINGS_PREFRENCES, GENERAL_SETTINGS_PREFRENCES_TH % index])
           print key
           value = ''.join([GENERAL_SETTINGS_PREFRENCES, GENERAL_SETTINGS_PREFRENCES_TD % index])
           print value
           settings[self.get_text(key)] = self.get_text(value)

       return settings
