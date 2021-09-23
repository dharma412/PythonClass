#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/zeus1360/gui/email/reporting/reports_parser_def/details_table.py#1 $ $DateTime: 2020/03/05 19:45:32 $ $Author: sarukakk $

import time

from common.gui.decorators import set_speed
from common.gui.guicommon import Wait
from common.gui.guiexceptions import ConfigError
from sal.containers.cfgholder import CfgHolder

from base_reporting_table import BaseReportingTable, normalize
from data_load_monitor import wait_until_data_loaded, NoDataFound


COLUMNS_OPTION = 'columns'

COLUMNS_OPTIONS_DIALOG = "//div[@id='yui_table_options_dlg_c' and "\
                         "contains(@style, 'visibility: visible')]"
COLUMN_NAMES_CHECKBOXES = "{0}//input[@name='table_options_columns[]']".\
            format(COLUMNS_OPTIONS_DIALOG)
COLUMN_CHECKBOX_BY_IDX = lambda idx: \
                "xpath=({0}//input[@name='table_options_columns[]'])"\
                "[{1}]".format(COLUMNS_OPTIONS_DIALOG, idx)
COLUMN_CHECKBOX_BY_NAME = lambda col_name: "{0}//label[normalize-space()='{1}']"\
                "/preceding::input[@name='table_options_columns[]'][1]".format(
                                                COLUMNS_OPTIONS_DIALOG, col_name)
OPTIONS_DIALOG_DONE_BUTTON = "{0}//button[normalize-space()='Done']".\
                                                format(COLUMNS_OPTIONS_DIALOG)

SEARCH_FOR_PREFIX = 'Search Results for'


class DetailsTable(BaseReportingTable):
    """The class represents footer details tables on email reporting pages
    """
    HEADER_COLS = lambda self: "{0}//thead/tr[last()]/th".format(
                                                           self._get_xpath_root())
    SHOW_COLUMNS_LINK = lambda self: \
            "{0}/following::span[contains(@onclick, 'showTableOptionsDlg')]".\
            format(self._get_xpath_root())

    @classmethod
    def get_available_table_names(cls):
        return ['User Mail Flow Details', 'Incoming Mail Details',
                'Outgoing Destinations Detail', 'Sender Details',
                'Virus Types Detail', 'Outgoing TLS Connections Details',
                'Incoming TLS Connections Details',
                'Incoming Content Filter Matches', 'Threat Summary',
                'Outgoing Content Filter Matches', 'Threat Details',
                'DLP Incident Details', 'Ordered IP Addresses', 'MX Records',
                'SMTP Routes for this host', 'IP Address', 'Domain',
                'Network Owner', 'Internal User', 'Destination Domain',
                'Internal Sender Domain', 'Internal Sender IP Address',
                'Outgoing Domain Delivery Status', 'Incoming TLS Domain',
                'Outgoing TLS Domain', 'Outgoing Destinations Status',
                'Past Year Virus Outbreaks', 'Incoming Malicious Threat Files', 'Completed Analysis Requests']
        # TODO: Subclass tables containing special headers (rowspan/colspan)

    @classmethod
    def get_special_name_prefixes(cls):
        return [SEARCH_FOR_PREFIX]

    def _get_xpath_root(self):
        return "{0}//dt[.//span[normalize-space(.)='{1}']]/following-sibling"\
               "::dd//table[@summary]".\
                format(super(DetailsTable, self)._get_xpath_root(), self._name)

    def get_available_options_names(self):
        return super(DetailsTable, self).get_available_options_names() + \
                    [COLUMNS_OPTION]

    def _set_visible_columns(self, columns_to_show):
        if not self.gui._is_element_present(self.SHOW_COLUMNS_LINK()):
            raise ConfigError('The table "{0}" does not have option to show/'\
                              'hide columns'.format(self._name))
        self.gui.click_element(self.SHOW_COLUMNS_LINK(), 'don\'t wait')
        Wait(until=self.gui._is_element_present,
             msg='Columns selection dialog has not been shown within 5 '\
                 'seconds timeout',
             timeout=5).wait(COLUMNS_OPTIONS_DIALOG)
        checkboxes_count = int(self.gui.get_matching_xpath_count(
                                                    COLUMN_NAMES_CHECKBOXES))
        if columns_to_show.lower() == 'all':
            for cb_idx in xrange(1, 1 + checkboxes_count):
                self.gui._select_checkbox(COLUMN_CHECKBOX_BY_IDX(cb_idx))
        else:
            # clear existing selection first
            for cb_idx in xrange(1, 1 + checkboxes_count):
                self.gui._unselect_checkbox(COLUMN_CHECKBOX_BY_IDX(cb_idx))
            column_names = map(lambda x: x.strip(), columns_to_show.split(','))
            for column_name in column_names:
                self.gui._select_checkbox(COLUMN_CHECKBOX_BY_NAME(column_name))
        self.gui.click_button(OPTIONS_DIALOG_DONE_BUTTON, 'don\'t wait')
        time.sleep(0.5)

    @set_speed(0, 'gui')
    def click_cell(self, row_coords, dest_col_name):
        key_col_name, key_cell_value = tuple(map(lambda x: x.strip(),
                                            row_coords.split(',')))
        key_col_idx = self._get_col_idx_by_name(key_col_name)
        dest_row_idx = self._get_row_idx_by_cell_value(key_col_idx,
                                                       key_cell_value)
        dest_col_idx = self._get_col_idx_by_name(dest_col_name)
        dest_cell_locator = self.CELL_BY_COL_ROW(dest_col_idx,
                                                       dest_row_idx)
        if not self.gui._is_element_present(dest_cell_locator):
            raise NoDataFound('Table cell by given "{0}" row and "{1}" column '\
                             'does not exist'.format(row_coords, dest_col_name))
        dest_link_locator = self.LINK_BY_COL_ROW_IDX(dest_col_idx,
                                                     dest_row_idx)
        element_text = self.gui.get_text(dest_cell_locator).strip()
        if self.gui._is_element_present(dest_link_locator):
            self.gui.click_element(dest_link_locator)
            return (element_text, True)
        else:
            return (element_text, False)

    @set_speed(0, 'gui')
    def get_data(self, is_full_text_mode):
        def get_cell_value(col_idx, row_idx, use_any_cell=False):
            """Returns cell_value depending on is_full_text_mode flag"""
            cell_value = None
            if is_full_text_mode and self.gui._is_element_present(
                        self.TITLED_CELL_BY_COL_ROW(col_idx, row_idx,
                                                    use_any_cell)):
                cell_value = self.gui.get_element_attribute(
                   self.TITLE_ATTR_BY_COL_ROW(col_idx, row_idx,
                                              use_any_cell)).strip()
            if cell_value is None:
                cell_value = self.gui.get_text(
                   self.CELL_BY_COL_ROW(col_idx, row_idx,
                                        use_any_cell)).strip()
            return cell_value

        rows_count = int(self.gui.get_matching_xpath_count(self.ALL_ROWS()))
        headers = self._get_headers()
        result_data = []
        for row_idx in xrange(1, 1 + rows_count):
            cols_count_in_row = int(self.gui.get_matching_xpath_count(
                                        self.COLS_IN_ROW(row_idx)))
            row_info = {}
            if cols_count_in_row == len(headers):
                for col_idx in xrange(1, 1 + cols_count_in_row):
                    row_info[headers[col_idx - 1]] = get_cell_value(col_idx,
                                                                    row_idx)
            if row_info:
                result_data.append(row_info)
        return result_data

    def transform_data(self, initial_data, transform_opts):
        def parse_table_row(row_idx):
            one_row_data = CfgHolder()
            category_name = normalize(initial_data[row_idx][headers[0]]) if \
                transform_opts.use_normalize else initial_data[row_idx][headers[0]]
            if transform_opts.first_column_as_key:
                one_row_data[category_name] = CfgHolder()
                for header in headers[1:]:
                    key = normalize(header) if transform_opts.use_normalize \
                                                    else header
                    one_row_data[category_name][key] = \
                                              initial_data[row_idx][header]
            else:
                for header in headers:
                    key = normalize(header) if transform_opts.use_normalize \
                                                    else header
                    one_row_data[key] = initial_data[row_idx][header]
            return one_row_data

        headers = self._get_headers()
        if transform_opts.result_as_dictionary:
            result = CfgHolder()
            for row_idx in xrange(len(initial_data)):
                result.update(parse_table_row(row_idx))
        else:
            result = []
            for row_idx in xrange(len(initial_data)):
                result.append(parse_table_row(row_idx))
        return result

    @set_speed(0, 'gui')
    def set_options(self, options):
        super(DetailsTable, self).set_options(options)
        if COLUMNS_OPTION in options:
            self._set_visible_columns(options[COLUMNS_OPTION])

    @set_speed(0, 'gui')
    def open_item(self, item_name):
        self.gui.click_element("{0}//a[normalize-space()='{1}']".format(
                                    self._get_xpath_root(), item_name))
        wait_until_data_loaded(self.gui)
