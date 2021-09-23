#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1380/gui/management/administration/feature_key_settings.py#1 $ $DateTime: 2020/05/25 00:19:30 $ $Author: sarukakk $

FKEY_SETTINGS_LOC = 'xpath=//input[@name=\'action:EditSettings\']'
AUTOCHECK_LOC = 'id=autocheck'
AUTOACT_LOC = 'id=autoapply'


from common.gui.guicommon import GuiCommon


class FeatureKeySettings(GuiCommon):
    """ Keywords for Management -> System Administration -> Feature Key Setting
    """

    def get_keyword_names(self):
        return [
                'feature_key_settings_edit'
                ]

    def _open_page(self):
        self._navigate_to('Management', 'System Administration',
                               'Feature Key Settings')

    def _click_edit_fkey_settings(self):
        self.click_button(FKEY_SETTINGS_LOC)
        self._info('Clicked "Edit Feature Key Settings..." button.')

    def _enable_autocheck(self, enable):
        if enable:
            self.select_checkbox(AUTOCHECK_LOC)
            self._info('Enabled automatic check for new feature keys.')
        else:
            self.unselect_checkbox(AUTOCHECK_LOC)
            self._info('Disabled automatic check for new feature keys.')

    def _enable_autoactivation(self, enable):
        if enable:
            self.select_checkbox(AUTOACT_LOC)
            self._info('Enabled automatic apply of downloaded keys.')
        else:
            self.unselect_checkbox(AUTOACT_LOC)
            self._info('Disabled automatic apply of downloaded keys.')

    def feature_key_settings_edit(self, autocheck=None, autoactivate=None):
        """Edit feature key settings.

        Parameters:
            - `autocheck`: enable automatic check for new feature keys. If
                           None, value will be left unchanged.
            - `autoactivate`: enable automatic activation of downloaded feature
                              keys. If None, value will be left unchanged.

        Examples:
        | Feature Key Settings Edit | ${true} | ${true} |
        | Feature Key Settings Edit | autocheck=${true} |  |
        | Feature Key Settings Edit | autoactivate=${true} |  |
       """

        self._info('Editing feature key settings.')

        self._open_page()

        self._click_edit_fkey_settings()

        if autocheck is not None:
            self._enable_autocheck(autocheck)

        if autoactivate is not None:
            self._enable_autoactivation(autoactivate)

        self._click_submit_button()

        self._info('Configured feature key settings.')

