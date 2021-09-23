#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/phoebe1350/gui/services/antispam_def/ims_engine_page.py#1 $ $DateTime: 2020/01/06 01:25:43 $ $Author: saurgup5 $

from common.gui.decorators import set_speed

from base_engine_page import BaseEnginePage


class IMSEnginePage(BaseEnginePage):
    ALWAYS_SCAN_EDIT = ('always_scan_max_size',
                        "//input[@id='adv_msg_size']")
    MAX_SCAN_SIZE_EDIT = ('never_scan_min_size',
                          "//input[@id='max_msg_size']")
    TIMEOUT_EDIT = ('timeout',
                    "//input[@id='timeout']")

    @classmethod
    def get_markers(cls):
        return ('ims',)

    @classmethod
    def get_menu_entry_name(cls):
        return 'IronPort Intelligent Multi-Scan'

    @set_speed(0, 'gui')
    def set(self, new_value):
        self._set_edits(new_value,
                        self.ALWAYS_SCAN_EDIT,
                        self.MAX_SCAN_SIZE_EDIT,
                        self.TIMEOUT_EDIT)

    @set_speed(0, 'gui')
    def get(self):
        details = self._get_values(self.ALWAYS_SCAN_EDIT,
                                   self.MAX_SCAN_SIZE_EDIT,
                                   self.TIMEOUT_EDIT)
        self._cancel_editing()
        TABLE_HEADERS_MAP = {'Rule Type': 1,
                             'Last Update': 2,
                             'Current Version': 3}
        details['Rule Updates'] = self._get_table_details(TABLE_HEADERS_MAP)
        return details
