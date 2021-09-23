#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/phoebe1210/gui/manager/access_table_def/externalthreatfeeds_settings.py#1 $
# $DateTime: 2019/05/29 03:16:07 $
# $Author: saurgup5 $

import re
from common.gui.decorators import set_speed
from common.gui import guiexceptions
from common.gui.inputs_owner import InputsOwner, get_module_inputs_pairs
from common.gui.guiexceptions import ConfigError, GuiPageNotFoundError

ADD_ROW_BUTTON = "//input[@id='etf_selection_domtable_AddRow']"
ETF_SOURCE = lambda index: \
    "//select[@id='etf_selection[%s][etf_source]']" % index
REGEX_ETF_SELECTION = 'etf_selection'
ETF_TBODY_ROW = lambda field: '//tbody[@id=\"%s_rowContainer\"]/tr' % (field,)
ETF_DEL = lambda etf, index, td: 'xpath=//tr[@id="%s_row%s"]/td[%d]/img[1]' % (etf, index, td,)
ETF_TABLE_FIELD = lambda etf, index, field: '%s[%d][%s]' % (etf, index, field,)
GET_FIELD_REGEX = lambda etf: '%s\[(\d+)\]\[etf_source\]' % (etf,)
GET_SELECT_VALUE = lambda index: 'xpath=//*[@id="etf_selection[%d][etf_source]"]' % (index,)


class ExternalThreatFeedsSettings(InputsOwner):

    @set_speed(0, 'gui')
    def add_etf_sources(self, sources=None):
        """Add Threat Feed sources.

        - `sources`: List of external threat feed sources to be added.
        """
        regex_etf = 'etf_selection'
        num_entry = int(
            self.gui.get_matching_xpath_count(ETF_TBODY_ROW(regex_etf)))
        if sources is not None:
            index = 0
            for source_name in sources:
                if index > 0:
                    self.gui.click_button(ADD_ROW_BUTTON, "don't wait")
                source_names = self.gui.get_list_items(ETF_SOURCE(index))
                if source_name in source_names:
                    self.gui.select_from_list(ETF_SOURCE(index), source_name)
                else:
                    raise ValueError('There is no etf source with name %s' % source_name)
                index += 1

    @set_speed(0, 'gui')
    def delete_etf_sources(self, sources=None):
        """Delete Threat feed sources.
        - `sources`: List of external threat feed sources to be deleted.
        """
        if sources is not None:
            self.perform_delete_operation \
                (regex_etf=REGEX_ETF_SELECTION, source=sources)

    @set_speed(0, 'gui')
    def perform_delete_all_operation(self, regex_etf=None, table_column=2):
        num_entry = int(
            self.gui.get_matching_xpath_count(ETF_TBODY_ROW(regex_etf)))
        for i in range(num_entry):
            self.gui.click_button \
                (ETF_DEL(regex_etf, i, table_column), "don't wait")
        return num_entry

    @set_speed(0, 'gui')
    def delete_all_etf_sources(self):
        """Delete All Threat Feed sources from sender group

        """

        num_entry = self.perform_delete_all_operation \
            (regex_etf=REGEX_ETF_SELECTION)
        return num_entry

    @set_speed(0, 'gui')
    def perform_delete_operation(self,
                                 regex_etf=None,
                                 table_column=2,
                                 source=None):
        source = self.gui._convert_to_tuple(eval(source))
        num_entry = int(
            self.gui.get_matching_xpath_count(ETF_TBODY_ROW(regex_etf)))
        for i in range(num_entry):
            text_value = self.gui._get_selected_label(GET_SELECT_VALUE(i))
            if text_value in source:
                self.gui.click_button \
                    (ETF_DEL(regex_etf, i, table_column), "don't wait")

    @set_speed(0, 'gui')
    def edit_etf_sources(self, sources=None):
        """Edit Threat Feed sources.

        - `sources`: List of external threat feed sources to be added.
        """
        regex_etf = 'etf_selection'
        num_entry = int(
            self.gui.get_matching_xpath_count(ETF_TBODY_ROW(regex_etf)))
        if sources is not None:
            index = num_entry
            for source_name in sources:
                if index > 0:
                    self.gui.click_button(ADD_ROW_BUTTON, "don't wait")
                source_names = self.gui.get_list_items(ETF_SOURCE(index))
                if source_name in source_names:
                    self.gui.select_from_list(ETF_SOURCE(index), source_name)
                else:
                    raise ValueError('There is no etf source with name %s' % source_name)
                index += 1
