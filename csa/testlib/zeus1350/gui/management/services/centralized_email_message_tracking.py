#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1350/gui/management/services/centralized_email_message_tracking.py#1 $ $DateTime: 2019/09/18 01:46:35 $ $Author: sarukakk $


import common.gui.guiexceptions as guiexceptions
from common.gui.guicommon import GuiCommon

ENABLE_BUTTON = "//input[@value='Enable...']"
ENABLE_TRACKING_CHECKBOX = 'id=enable'


class CentralizedEmailMessageTracking(GuiCommon):
    """Keywords for Management Appliance -> Centralized Services -> Centralized
    Message Tracking
    """

    def get_keyword_names(self):
        return ['centralized_email_message_tracking_enable',
                'centralized_email_message_tracking_disable',
                ]

    def _open_page(self):
        self._navigate_to('Management', 'Centralized Services',
                          'Centralized Message Tracking')

        if not self._is_feature_key_available():
            raise guiexception.GuiFeaturerkeyMissingError(
                'Feature Key Unavailbale')

    def _click_enable_tracking_button(self):
        self.click_button(ENABLE_BUTTON)

    def _is_tracking_disabled(self):
        return self._is_text_present('The Centralized Message Tracking ' \
                                     'service is currently disabled.')

    def _uncheck_tracking_checkbox(self):
        self.unselect_checkbox(ENABLE_TRACKING_CHECKBOX)

    def _is_feature_key_available(self):
        return not self._is_text_present('Feature Key Unavailable')

    def centralized_email_message_tracking_enable(self):
        """Enable Centralized Message Tracking.

        Examples:
        | Centralized Email Message Tracking Enable |

        Exceptions:
        - `GuiFeaturekeyMissingError`: in case feature key is expired or
           missing.
        """

        self._open_page()

        if not self._is_tracking_disabled():
            return

        self._click_enable_tracking_button()

        self._accept_license()

    def centralized_email_message_tracking_disable(self):
        """Disable Centralized Message Tracking.

        Examples:
        | Centralized Email Message Tracking Disable |

        Exceptions:
        - `GuiFeaturekeyMissingError`: in case feature key is expired or
           missing.
        """

        self._open_page()

        if self._is_tracking_disabled():
            return

        self._click_edit_settings_button()

        self._uncheck_tracking_checkbox()

        self._click_submit_button()
