#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/gui/admin/fips_mode.py#1 $ $DateTime: 2019/08/14 09:58:47 $ $Author: uvelayut $

from common.gui.guicommon import GuiCommon
import common.gui.guiexceptions as guiexceptions

class FipsMode(GuiCommon):
    """Keywords for System Administration -> Fips Mode
    """

    def get_keyword_names(self):
        return [
                'fips_mode_edit',
               ]

    def _open_page(self):
        """
        Navigate to fips mode configuration page.
        """
        self._navigate_to('System Administration', 'FIPS Mode')

    def _enable_fips_mode(self, state):
        fipsmode_loc = 'id=enable_fips'
        if state.lower() == 'enable':
            self.select_checkbox(fipsmode_loc)
        elif state.lower() == 'disable':
            self.unselect_checkbox(fipsmode_loc)
        else:
            raise guiexceptions.ConfigError('Value should be either'\
                                            'enable or disable.')

    def fips_mode_edit(self, fipsmode=None):
        """Edit fips mode settings.

        Parameters:
        - `fipsmode`: enable fips mode
                    Either 'Enable' or 'Disable'.
                    If None, value will be left unchanged

        Examples:
        | Fips Mode Edit | fipsmode=enable |
        | Fips Mode Edit | fipsmode=disable |
        """
        self._info('Editing fips mode settings.')
        self._open_page()
        self._click_edit_settings_button()
        if fipsmode is not None:
            self._enable_fips_mode(fipsmode)
        self._click_submit_button(wait=False, accept_confirm_dialog=True)


