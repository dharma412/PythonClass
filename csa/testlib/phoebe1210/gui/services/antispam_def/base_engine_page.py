#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/phoebe1210/gui/services/antispam_def/base_engine_page.py#1 $ $DateTime: 2019/05/07 03:16:10 $ $Author: bimmanue $

from common.gui.decorators import set_speed
from common.gui.inputs_owner import InputsOwner, get_object_inputs_pairs
from common.gui.guicommon import Wait
from common.gui.guiexceptions import GuiControlNotFoundError

UPDATENOW_BUTTON = "//input[@name='action:UpdateNow']"
UPDATE_RESULTS = "//div[@id='status']"
UPDATE_RUNNING_MARK = 'Getting update status'
CANCEL_BUTTON = "//input[@name='action:EditCancel' or @name='CancelSettings']"

INFO_TABLE = "//table[@class='cols']"
INFO_TABLE_ROWS = "%s//tr[count(td) > 1 or count(th) > 1]" % (INFO_TABLE,)


class BaseEnginePage(InputsOwner):
    def _get_registered_inputs(self):
        return get_object_inputs_pairs(self)

    @classmethod
    def get_menu_entry_name(cls):
        raise NotImplementedError('Should be implemented in subclasses')

    @classmethod
    def get_markers(cls):
        raise NotImplementedError('Should be implemented in subclasses')

    def _cancel_editing(self):
        self.gui.click_button(CANCEL_BUTTON)

    def _get_table_details(self, table_headers_map):
        INFO_TABLE_CELL = lambda header, row: "%s//tr[%d]/td[%d]" % \
                                              (INFO_TABLE, row, table_headers_map[header])
        table_details = []
        info_rows_count = int(self.gui.get_matching_xpath_count(INFO_TABLE_ROWS)) - 1
        for row_num in xrange(2, 2 + info_rows_count):
            one_row_dict = {}
            for col_name in table_headers_map.iterkeys():
                one_row_dict[col_name] = self.gui.get_text(INFO_TABLE_CELL(col_name,
                                                                           row_num)).strip()
            table_details.append(one_row_dict)
        return table_details

    @set_speed(0, 'gui')
    def update_now(self):
        if self.gui._is_element_present(UPDATENOW_BUTTON):
            self.gui.click_button(UPDATENOW_BUTTON)
            Wait(until=self.gui._is_text_present,
                 msg='Update result has not been shown within 30 seconds timeout',
                 timeout=30). \
                wait(UPDATE_RUNNING_MARK)
            return self.gui.get_text(UPDATE_RESULTS).strip()
        else:
            raise GuiControlNotFoundError('"%s" feature' \
                                          ' cannot be updated manually' % (self.get_menu_entry_name(),))
