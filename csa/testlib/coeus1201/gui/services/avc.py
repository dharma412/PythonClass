#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/gui/services/avc.py#2 $

import common.gui.guiexceptions as guiexceptions
from common.gui.guicommon import GuiCommon

ACCEPT_LICENSE_BUTTON = 'action:AcceptLicense'

class AVC(GuiCommon):
    """Acceptable Use Control Settings page interaction class."""

    def get_keyword_names(self):
        return ['avc_enable',
                'avc_disable',
                'avc_update_now',
                'avc_get_settings',
                'avc_edit_global_settings']

    def _open_page(self):
        """Open 'Acceptable Use Controls' page """

        self._navigate_to('Security Services', 'Acceptable Use Controls')
        # Feature key: IPURL SurfControl
        if self._is_text_present\
               ('The feature key for this feature is expired or unavailable.'):
            raise guiexceptions.GuiFeaturekeyMissingError\
             ('Feature \'Acceptable Use Controls\' unavailable as missing feature key')

    def _enable_control(self):
        """Enable Acceptable Use Controls"""

        enable_control_button = "xpath=//input[@value='Enable...']"
        self.click_button(enable_control_button)
        if self._is_text_present\
               ('Acceptable Use Controls License Agreement'):
            self.click_button(ACCEPT_LICENSE_BUTTON)

    def _click_edit_global_settings_button(self):
        """Click 'Edit Global Settings...' button"""

        edit_settings_button = "xpath=//input[@value='Edit Global Settings...']"
        self.click_button(edit_settings_button)

    def _select_default_action(self, action):

        action_radio_button = {'block': 'action_block',
                               'monitor': 'action_scan'}
        if action is not None:
            self._click_edit_global_settings_button()
            if action.lower() == 'block':
                self._click_radio_button(action_radio_button['block'])
            else: # assuming user will give valid input
                self._click_radio_button(action_radio_button['monitor'])
            self._click_submit_button(wait=False, accept_EULA=True)

    def _select_acceptable_use_control(self,
                                       controls,
                                       dynamic,
                                       application,
                                       multi_cat):

        # As of 8.0.5, "Cisco URL Filters" is deprecated. Therefore
        # controls argument is no longer in use.
        # controls_radio_button = {'ironport': 'engine_webcat',
        #                          'cisco': 'engine_firestone'}
        dynamic_checkbox = 'dynamic_categorization'
        application_checkbox = 'avc_enabled'
        multi_cat_checkbox = 'multi_cat_enabled'
        self._click_edit_global_settings_button()

        # Deprecated Feature key: Cisco IronPort Web Usage Controls
        # if self._is_text_present\
        #                           ('The feature key for this feature '\
        #                                   'is expired or unavailable.'):
        #     raise guiexceptions.GuiFeaturekeyMissingError\
        #       ('Cannot use control as Feature key is missing for '\
        #                    '\'Cisco IronPort Web Usage Controls\'')

        if dynamic is not None:
            if dynamic:
                self.select_checkbox(dynamic_checkbox)
            else:
                self.unselect_checkbox(dynamic_checkbox)
        if application is not None:
            if application:
                self.select_checkbox(application_checkbox)
            else:
                self.unselect_checkbox(application_checkbox)
        if multi_cat is not None:
            if multi_cat:
                self.select_checkbox(multi_cat_checkbox)
            else:
                self.unselect_checkbox(multi_cat_checkbox)
        self._click_submit_button(wait=False, accept_confirm_dialog=True,
                                  accept_EULA=True)

    def avc_update_now(self):
        """Click 'Update Now' button to update
           'Acceptable Use Controls Engine Updates'

        Example:
        | AVC Update Now |

        """
        update_now_button = "xpath=//input[@value='Update Now']"
        self._open_page()
        # check if Acceptable Use Control already disabled or not
        if not self._check_feature_status(feature='acceptable_use_control'):
            raise guiexceptions.GuiFeatureDisabledError\
              ('Cannot update \'Acceptable Use Controls Engine\'')
        self.click_button(update_now_button)
        # Validate errors on the page
        self._check_action_result()

    def avc_get_settings(self):
        """Gets settings

        Example:
        | ${result} | AVC Get Settings |

        """
        ENTRY_ENTITIES = lambda row,col:\
            '//table[@class=\'pairs\']/tbody/tr[%s]%s' % (str(row),col)
        entries = {}

        self._open_page()
        num_of_entries = int(self.get_matching_xpath_count(ENTRY_ENTITIES('*',''))) + 1
        if num_of_entries > 1:
            for row in xrange(1, num_of_entries):
                if (self._is_element_present(ENTRY_ENTITIES(row, '/td[1]')) and
                        self._is_element_present(ENTRY_ENTITIES(row, '/th[1]'))):
                    name = self.get_text(ENTRY_ENTITIES(row, '/th[1]'))
                    value = self.get_text(ENTRY_ENTITIES(row, '/td[1]'))
                    entries[name] = value
        return entries

    def avc_disable(self):
        """Disable Acceptable Use Controls.

        Example:
        | AVC Disable |

        """
        enable_control_checkbox = 'enabled'
        self._open_page()
        # check if Acceptable Use Control already disabled or not
        if not self._check_feature_status(feature='acceptable_use_control'):
            return
        self._click_edit_global_settings_button()
        self.unselect_checkbox(enable_control_checkbox)
        self._click_submit_button()

    def avc_enable(self):
        """Enable Acceptable Use Controls Settings.

        Example:
        | AVC Enable |

        """
        self._open_page()
        # check if already enabled
        if self._check_feature_status(feature='acceptable_use_control'):
            return
        self._enable_control()
        self._click_submit_button(wait=False, accept_EULA=True)

    def avc_edit_global_settings(self,
                             action=None,
                             controls=None,
                             dynamic=None,
                             application=None,
                             multi_cat=None):

        """Edit Acceptable Use Controls Global Settings.

        Parameters:
           - `action`: Default Action for unreachable service to 'Monitor' or 'Block'
           - `controls`: Acceptable Use Controls Service,  `ironport` to select 'IronPort URL Filters' & `cisco` to select 'Cisco IronPort Web Usage Controls'
           - `dynamic`: True to enable 'Dynamic Content Analysis Engine', False to disable & Default to None
           - `application`: True to enable 'Applications Visibility and Control', False to disable. 'application' applicable only if control service is 'cisco'.

        Example:
        | AVC Edit Global Settings | action=block | controls=cisco | dynamic=${True} | application=${True} |
        | AVC Edit Global Settings | action=monitor | controls=cisco | dynamic=${False} | application=${True} |

        """
        self._open_page()
        # check if Acceptable Use Control already disabled or not
        if not self._check_feature_status(feature='acceptable_use_control'):
            raise guiexceptions.GuiFeatureDisabledError\
               ('Cannot edit \'Acceptable Use Controls\' as disabled')
        self._select_acceptable_use_control(controls, dynamic, application, multi_cat)
        self._select_default_action(action)
