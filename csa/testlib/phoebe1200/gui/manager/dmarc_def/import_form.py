#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/phoebe1200/gui/manager/dmarc_def/import_form.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $

from common.gui.decorators import set_speed
from common.gui.guicommon import Wait
from common.gui.inputs_owner import InputsOwner, get_module_inputs_pairs

FILE_TO_IMPORT_LIST = ('File to Import',
                       "//select[@id='impfile']")
CONFIRM_DLG = "//div[@id='confirmation_dialog_c' and " \
              "contains(@style, 'visibility: visible')]"
IMPORT_BTN = "{0}//button[normalize-space()='Import']".format(CONFIRM_DLG)
SUBMIT_BTN = "//input[@value='Submit' and @type='submit']"


class ImportForm(InputsOwner):
    def _get_registered_inputs(self):
        return get_module_inputs_pairs(__name__)

    def set(self, new_value):
        self._set_combos(new_value,
                         FILE_TO_IMPORT_LIST)

    def perform_import(self):
        previous_timeout = self.gui.set_selenium_timeout(5)
        try:
            try:
                self.gui.click_button(SUBMIT_BTN)
            except Exception:
                self.gui.click_button(IMPORT_BTN)
        finally:
            self.gui.set_selenium_timeout(previous_timeout)
        self.gui._check_action_result()
