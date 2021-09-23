#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1362/gui/management/services/centralized_web_reporting.py#1 $ $DateTime: 2020/06/10 22:29:20 $ $Author: sarukakk $


import common.gui.guiexceptions as guiexceptions
from common.gui.guicommon import GuiCommon


ENABLE_BUTTON = 'xpath=//input[@value=\'Enable...\']'
ENABLE_REPORTING_CHECKBOX = 'id=enabled'
ANONYMIZE_USERS_CHECKBOX = 'id=anonymizing_enabled'


class CentralizedWebReporting(GuiCommon):

    """Keywords for Management Appliance -> Centralized Services -> Centralized
    Web Reporting
    """

    def get_keyword_names(self):
        return ['centralized_web_reporting_enable',
                'centralized_web_reporting_edit_settings',
                'centralized_web_reporting_disable',
                ]

    def _open_page(self):
        # Using direct link as there are two items named 'Centralized
        # Reporting' in 'Centralized Services' menu.
        self.go_to(
            '/services/centralized_configuration/centralized_web_reporting')

        if not self._is_feature_key_available():
            raise guiexceptions.GuiFeturekeyMissingError(
                'Feature Key Unavailable')

    def _click_enable_web_reporting_button(self):
        self.click_button(ENABLE_BUTTON)

    def _is_reporting_disabled(self):
        return self._is_text_present('The Centralized Reporting service '\
                                     'is currently disabled.')

    def _uncheck_reporting_checkbox(self):
        self.unselect_checkbox(ENABLE_REPORTING_CHECKBOX)

    def _check_anonymize_users_checkbox(self, check):
        if check:
            self.select_checkbox(ANONYMIZE_USERS_CHECKBOX)
        else:
            self.unselect_checkbox(ANONYMIZE_USERS_CHECKBOX)

    def _is_feature_key_available(self):
        return not self._is_text_present('Feature Key Unavailable')

    def centralized_web_reporting_enable(self):
        """Enable Centralized Web Reporting.

        Examples:
        | Centralized Web Reporting Enable |

        Exceptions:
        - `GuiFeaturekeyMissingError`: in case feature key has expired or
           is unavailable.
        """

        self._open_page()

        if not self._is_reporting_disabled():
            return

        self._click_enable_web_reporting_button()

        self._accept_license()

    def centralized_web_reporting_edit_settings(self, anonymize_users=None):
        """Edit Centralized Web Reporting settings.

        Parameters:
        - `anonymize_users`: anonymize usernames in reports. Boolean.

        Examples:
        | Centralized Web Reporting Edit Settings | anonymize_users=${True} |
        | Centralized Web Reporting Edit Settings | anonymize_users=${False} |

        Exceptions:
        - `GuiFeatureDisabledError`: in case Centralized Web reporting is
           not enabled.
        - `GuiFeaturekeyMissingError`: in case feature key has expired or
           is unavailable.
        """

        self._open_page()

        if self._is_reporting_disabled():
            raise guiexceptions.GuiFeatureDisabledError(
                'Centralized Web Reporting must be enabled first.')

        self._click_edit_settings_button()

        if anonymize_users is not None:
            self._check_anonymize_users_checkbox(anonymize_users)

        self._click_submit_button()

    def centralized_web_reporting_disable(self):
        """Disable Centralized Web Reporting.

        Examples:
        | Centralized Web Reporting Disable |

        Exceptions:
        - `GuiFeaturekeyMissingError`: in case feature key has expired or
           is unavailable.
        """

        self._open_page()

        if self._is_reporting_disabled():
            return

        self._click_edit_settings_button()

        self._uncheck_reporting_checkbox()

        self._click_submit_button()


