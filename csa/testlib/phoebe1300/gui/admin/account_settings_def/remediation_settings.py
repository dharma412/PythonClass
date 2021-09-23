#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1300/gui/admin/account_settings_def/remediation_settings.py#1 $
# $DateTime: 2019/09/20 06:28:26 $
# $Author: saurgup5 $

from common.gui.inputs_owner import InputsOwner, get_module_inputs_pairs
from common.gui.guiexceptions import GuiValueError

MAXIMUM_ATTEMPTS = ('Maximum number of attempts', "//input[@id='max_retry']")
TIMEOUT_HYBRID = ('Timeout for Hybrid Setup', "//input[@id='timeout_hybrid']")
TIMEOUT_ON_PREM = ('Timeout for On Premise Setup', "//input[@id='timeout_on_prem']")
MAILBOX_REMEDIATION_TABLE = "//table[@class='pairs']"
MAILBOX_REMEDIATION_TABLE_ROWS = "%s//tr[*]" % MAILBOX_REMEDIATION_TABLE
MAILBOX_REMEDIATION_TABLE_ROW_TH = lambda row: "%s//tr[%s]/th" % (MAILBOX_REMEDIATION_TABLE, row)
MAILBOX_REMEDIATION_TABLE_ROW_TD = lambda row: "%s//tr[%s]/td" % (MAILBOX_REMEDIATION_TABLE, row)


class RemediationSettings(InputsOwner):
    def _get_registered_inputs(self):
        return get_module_inputs_pairs(__name__)

    def set(self, new_value):
        self._set_edits(
            new_value,
            MAXIMUM_ATTEMPTS,
            TIMEOUT_HYBRID,
            TIMEOUT_ON_PREM)

    def get(self):
        remediation_settings = {}
        number_of_rows = self.gui.get_matching_xpath_count(
            MAILBOX_REMEDIATION_TABLE_ROWS)

        if not number_of_rows:
            raise GuiValueError("Remediation settings table rows not found")
        else:
            for row_index in xrange(1, int(number_of_rows) + 1):
                setting_name = self.gui.get_text(MAILBOX_REMEDIATION_TABLE_ROW_TH(row_index)).strip()
                setting_value = self.gui.get_text(MAILBOX_REMEDIATION_TABLE_ROW_TD(row_index)).strip()
                remediation_settings[setting_name] = setting_value

        return remediation_settings
