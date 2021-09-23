#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/phoebe1100/gui/admin/feature_key_settings.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $

import functools

from common.gui.decorators import go_to_page
from common.gui.guicommon import GuiCommon
import common.gui.guiexceptions as guiexceptions

EDIT_BUTTON = "//input[@value='Edit Feature Key Settings...']"
AUTO_DOWNLOAD_CHECKBOX = "//input[@id='autocheck']"
AUTO_ACTIVATE_CHECKBOX = "//input[@id='autoapply']"
CANCEL_BUTTON = "//input[@value='Cancel']"
SUBMIT_BUTTON = "//input[@value='Submit']"

PAGE_PATH = ('System Administration', 'Feature Key Settings')


class FeatureKeySettings(GuiCommon):
    """Keywords for interaction with System Administration ->
    Feature Key Settings page
    """

    SETTINGS_EDIT_FORM = {
        'auto_download': AUTO_DOWNLOAD_CHECKBOX,
        'auto_activate': AUTO_ACTIVATE_CHECKBOX}

    def get_keyword_names(self):
        return ['feature_key_settings_edit',
                'feature_key_settings_get_details']

    @go_to_page(PAGE_PATH)
    def feature_key_settings_edit(self, **kwargs):
        """Edit Feature Key Settings

        *Parameters:*
        - `auto_download`: whether to check for fkeys and
        download them automatically. Either ${True} or ${False}
        - `auto_activate`: whether to activate feature keys
        automatically. Either ${True} or ${False}

        *Exceptions*:
        - `ValueError`: if any of passed arguments is not correct

        *Examples:*
        | Feature Key Settings Edit | auto_download=${False} |
        | ... | auto_activate=${False} |
        """
        self.click_button(EDIT_BUTTON)

        for name, value in kwargs.iteritems():
            if name not in self.SETTINGS_EDIT_FORM.keys():
                raise ValueError('Unknown setting name "%s" is ' \
                                 'passed' % (name,))
            self._select_unselect_checkbox(self.SETTINGS_EDIT_FORM[name],
                                           value)
        self.click_button(SUBMIT_BUTTON)

    @go_to_page(PAGE_PATH)
    def feature_key_settings_get_details(self):
        """Get current Feature Key Settings

        *Return:*
        Dictionary, whose items are
        | `auto_download` | whether "Check for fkeys and
        download them automatically" feature is enabled.
        Either ${True} or ${False} |
        | `auto_activate` | whether "Activate feature keys
        automatically" feature is enabled.
        Either ${True} or ${False} |

        *Examples:*
        | ${fk_settings}= | Feature Key Settings Get Details |
        | ${auto_download}= | Get From Dictionary | ${fk_settings} | auto_download |
        | Should Be True | ${auto_download} |
        """
        self.click_button(EDIT_BUTTON)

        details = {}
        for name, locator in self.SETTINGS_EDIT_FORM.iteritems():
            details[name] = self._is_checked(locator)
        self.click_button(CANCEL_BUTTON)
        return details
