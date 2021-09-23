#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/gui/admin/feature_key_settings.py#1 $

from common.gui.guicommon import GuiCommon
import common.gui.guiexceptions as guiexceptions

class FeatureKeySettings(GuiCommon):
    """Feature Key Settings page interaction class.

    This class designed to interact with GUI elements of
    'System Administration' -> 'Feature Key Settings' page.
    """

    def get_keyword_names(self):
        return ['feature_key_settings_edit',]

    def _open_page(self):
        self._navigate_to('System Administration', 'Feature Key Settings')

    def _click_edit_fkey_settings(self):
        fkey_settings_loc =\
                    "xpath=//input[@value='Edit Feature Key Settings...']"
        self.click_button(fkey_settings_loc)

    def _enable_autocheck(self, state):
        autocheck_loc = 'id=autocheck'
        if state.lower() == 'enable':
            self.select_checkbox(autocheck_loc)
        elif state.lower() == 'disable':
            self.unselect_checkbox(autocheck_loc)
        else:
            raise guiexceptions.ConfigError('Value should be either'\
                                            'enable or disable.')

    def _enable_autoactivation(self, state):
        autoact_loc = 'id=autoapply'
        if state.lower() == 'enable':
            self.select_checkbox(autoact_loc)
        elif state.lower() == 'disable':
            self.unselect_checkbox(autoact_loc)
        else:
            raise guiexceptions.ConfigError('Value should be either'\
                                            'enable or disable.')

    def feature_key_settings_edit(self, autocheck=None, autoactivate=None):
        """Edit feature key settings.

        Parameters:
        - `autocheck`: enable automatic check for new feature keys.
                    Either 'Enable' or 'Disable'.
                    If None, value will be left unchanged.
        - `autoactivate`: enable automatic activation of downloaded feature
                        keys. If None, value will be left unchanged.
                        Either 'Enable' or 'Disable'.

        Example:
        | Feature Key Settings Edit | autocheck=enable |
        | Feature Key Settings Edit | autocheck=enable | autoactivate=enable |
        | Feature Key Settings Edit | autoactivate=disable |
        """

        self._open_page()

        self._click_edit_fkey_settings()

        if autocheck is not None:
            self._enable_autocheck(autocheck)

        if autoactivate is not None:
            self._enable_autoactivation(autoactivate)

        self._click_submit_button(wait=False, skip_wait_for_title=True)
