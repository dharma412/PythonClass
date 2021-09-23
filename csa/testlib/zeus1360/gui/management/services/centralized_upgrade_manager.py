#!/usr/bin/env python
# $Id:
#$ $DateTime:
#$ $Author:

import common.gui.guiexceptions as guiexceptions
from common.gui.guicommon import GuiCommon


ENABLE_BUTTON = "//input[@value='Enable...']"
ENABLE_ICCM_CHECKBOX = 'id=enable'


class CentralizedWebConfigurationManager(GuiCommon):

    """Keywords for Management Appliance -> Centralized Services -> Centralized
    Upgrade Manager
    """

    def get_keyword_names(self):
        return ['centralized_upgrade_manager_enable',
                'centralized_upgrade_manager_disable',
                ]

    def _open_page(self):
        self._navigate_to('Management', 'Centralized Services',
                               'Centralized Upgrade Manager')

        if not self._is_feature_key_available():
            raise guiexceptions.GuiFeaturekeyMissingError(
                'Feature Key Unavailable')

    def _click_enable_iccm_button(self):
        self.click_button(ENABLE_BUTTON)

    def _is_iccm_disabled(self):
        return self._is_text_present('The Centralized upgrade '\
                                     'is disabled.')

    def _uncheck_iccm_checkbox(self):
        self.unselect_checkbox(ENABLE_ICCM_CHECKBOX)

    def _is_feature_key_available(self):
        return not self._is_text_present('Feature Key Unavailable')

    def centralized_upgrade_manager_enable(self):
        """Enable Centralized Upgrade Manager.

        Examples:
        | Centralized Upgrade Manager Enable |

        Exceptions:
        - `GuiFeaturekeyMissingError`: in case feature key is expired or
           missing.
        """

        self._open_page()

        if not self._is_iccm_disabled():
            return

        self._click_enable_iccm_button()

        self._accept_license()

    def centralized_upgrade_manager_disable(self):
        """Disable Centralized Upgrade Manager.

        Examples:
        | Centralized Upgrade Manager Disable |

        Exceptions:
        - `GuiFeaturekeyMissingError`: in case feature key is expired or
           missing.
        """

        self._open_page()

        if self._is_iccm_disabled():
            return

        self._click_edit_settings_button()

        self._uncheck_iccm_checkbox()

        self._click_submit_button()
