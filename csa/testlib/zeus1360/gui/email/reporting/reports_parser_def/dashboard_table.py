#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/zeus1360/gui/email/reporting/reports_parser_def/dashboard_table.py#1 $ $DateTime: 2020/03/05 19:45:32 $ $Author: sarukakk $

from common.gui.decorators import set_speed
from common.gui.guiexceptions import ConfigError
from common.util.ordered_dict import OrderedDict
from sal.containers.cfgholder import CfgHolder

from base_reporting_table import BaseReportingTable, normalize
from data_load_monitor import wait_until_data_loaded, NoDataFound

CURRENT_INFORMATION_PREFIX = 'Current Information for'


class DashboardTable(BaseReportingTable):
    """The class represents dashboard tables on email reporting pages
    """

    ALL_ROWS = lambda self, table_name: \
                "{0}/tbody[not(contains(@style, 'display: none'))]"\
                "/tr[td and not(contains(@class, 'spacer'))]".\
                                   format(self._get_table_root(table_name))
    CELL_BY_COL_ROW = \
        lambda self, col_idx, row_idx, table_name, use_any_cell = False: \
       "{0}[{1}]/*[string-length() > 0][{2}]".\
       format(self.ALL_ROWS(table_name), row_idx, col_idx) if use_any_cell else \
       "{0}[{1}]/td[string-length() > 0][{2}]".\
       format(self.ALL_ROWS(table_name), row_idx, col_idx)
    TITLED_CELL_BY_COL_ROW = \
        lambda self, col_idx, row_idx, table_name, use_any_cell = False: \
         "{0}//*[@title]".format(self.CELL_BY_COL_ROW(col_idx, row_idx,
                                            table_name, use_any_cell))
    TITLE_ATTR_BY_COL_ROW = \
        lambda self, col_idx, row_idx, table_name, use_any_cell = False: \
         "{0}@title".format(self.TITLED_CELL_BY_COL_ROW(col_idx, row_idx,
                                            table_name, use_any_cell))
    HEADER_COLS = lambda self, table_name: "{0}//thead/tr/th".format(
                                        self._get_table_root(table_name))
    COL_HEADER_BY_IDX = lambda self, idx, table_name: "{0}[{1}]".\
                                    format(self.HEADER_COLS(table_name), idx)
    COLS_IN_ROW = lambda self, row_idx, table_name: \
                                    "{0}[{1}]/td[string-length() > 0]".\
                                    format(self.ALL_ROWS(table_name), row_idx)
    HEADERS_IN_ROW = lambda self, row_idx, table_name: \
                                    "{0}[{1}]/th[string-length() > 0]".\
                                    format(self.ALL_ROWS(table_name), row_idx)
    ITEMS_IN_ROW = lambda self, row_idx, table_name: \
                                    "{0}[{1}]/*[string-length() > 0]".\
                                    format(self.ALL_ROWS(table_name), row_idx)
    LINK_BY_COL_ROW_IDX = lambda self, col_idx, row_idx, table_name: \
        "{0}//a".format(self.CELL_BY_COL_ROW(col_idx, row_idx, table_name))
    ALL_TABLE_HEADERS_IN_CONTAINER = lambda self: \
            "{0}//tr[contains(@class, 'section-row-header')]"\
            "/td[contains(@class, 'dashboard-header')]".\
            format(self._get_xpath_root())
    TABLE_HEADER_IN_CONTAINER_BY_IDX = lambda self, idx: "{0}[{1}]"\
            "//span[contains(@class, 'display_name')]".\
            format(self.ALL_TABLE_HEADERS_IN_CONTAINER(), idx)

    @classmethod
    def get_special_name_prefixes(cls):
        return [CURRENT_INFORMATION_PREFIX]

    @classmethod
    def get_available_table_names(cls):
        return ['System Overview', 'System Status']

    def _get_xpath_root(self):
        return "{0}//dt[.//span[normalize-space(.)='{1}']]/following-sibling"\
               "::dd//table[contains(@class, 'dashboard')]".\
               format(super(DashboardTable, self)._get_xpath_root(), self._name)

    def _get_container_tables_mapping(self):
        tables_count_in_container = int(self.gui.get_matching_xpath_count(
                            self.ALL_TABLE_HEADERS_IN_CONTAINER()))
        result = {}
        for table_idx in xrange(1, 1 + tables_count_in_container):
            current_table_name = self.gui.get_text(
                            self.TABLE_HEADER_IN_CONTAINER_BY_IDX(table_idx)).strip()
            result[current_table_name] = table_idx
        return result

    def _get_table_root(self, table_name):
        mapping = self._get_container_tables_mapping()
        dest_table_info = filter(lambda x: x[0].startswith(table_name),
                                 mapping.iteritems())
        if dest_table_info:
            _, table_idx = dest_table_info[0]
            return "xpath=({0}/following::"\
             "table[(contains(@class,'dashboard-innertable') or @summary) and .//th])"\
             "[{1}]".format(self.ALL_TABLE_HEADERS_IN_CONTAINER(), table_idx)
        else:
            raise ValueError('The table "{0}" could not be found on current page'.\
                             format(table_name))

    def _get_col_idx_by_name(self, col_name, table_name):
        headers = self._get_headers(table_name)
        if col_name in headers:
            return headers.index(col_name) + 1
        else:
            raise NoDataFound('The table "{0}" does not contain column '\
                              'named "{1}"'.format(table_name, col_name))

    def _get_headers(self, table_name):
        headers_count = int(self.gui.get_matching_xpath_count(
                                                self.HEADER_COLS(table_name)))
        headers = []
        for header_idx in xrange(1, 1 + headers_count):
            header_value = self.gui.get_text(
                                self.COL_HEADER_BY_IDX(header_idx,
                                                       table_name)).strip()
            headers.append(header_value)
        return headers

    def _get_row_idx_by_cell_value(self, col_idx, cell_value, table_name):
        rows_count = int(self.gui.get_matching_xpath_count(
                                                   self.ALL_ROWS(table_name)))
        for row_idx in xrange(1, 1 + rows_count):
            current_cell_value = self.gui.get_text(self.CELL_BY_COL_ROW(
                                        col_idx, row_idx, table_name)).strip()
            if current_cell_value == cell_value:
                return row_idx
        raise NoDataFound('The table "{0}" does not contain value "{1}" '\
                          'in column #"{2}"'.format(table_name, cell_value,
                                                    col_idx))

    @set_speed(0, 'gui')
    def click_cell(self, row_coords, dest_col_name):
        table_name, key_cell_value = tuple(map(lambda x: x.strip(),
                                            row_coords.split(',')))
        table_root = self._get_table_root(table_name)
        dest_row_idx = self._get_row_idx_by_cell_value(1, key_cell_value,
                                                       table_name)
        dest_col_idx = self._get_col_idx_by_name(dest_col_name, table_name)
        dest_cell_locator = self.CELL_BY_COL_ROW(dest_col_idx, dest_row_idx,
                                                 table_name)
        if not self.gui._is_element_present(dest_cell_locator):
            raise NoDataFound('Table cell by given "{0}" row and "{1}" column '\
                             'does not exist'.format(row_coords, dest_col_name))
        dest_link_locator = self.LINK_BY_COL_ROW_IDX(dest_col_idx,
                                                     dest_row_idx,
                                                     table_name)
        element_text = self.gui.get_text(dest_cell_locator).strip()
        if self.gui._is_element_present(dest_link_locator):
            self.gui.click_element(dest_link_locator)
            return (element_text, True)
        else:
            return (element_text, False)

    @set_speed(0, 'gui')
    def get_data(self, is_full_text_mode):
        def get_cell_value(col_idx, row_idx, table_name, use_any_cell=False):
            """Returns cell_value depending on is_full_text_mode flag"""
            cell_value = None
            if is_full_text_mode and self.gui._is_element_present(
                        self.TITLED_CELL_BY_COL_ROW(col_idx, row_idx,
                                            table_name, use_any_cell)):
                cell_value = self.gui.get_element_attribute(
                   self.TITLE_ATTR_BY_COL_ROW(col_idx, row_idx,
                                    table_name, use_any_cell)).strip()
            if cell_value is None:
                cell_value = self.gui.get_text(
                   self.CELL_BY_COL_ROW(col_idx, row_idx,
                                   table_name, use_any_cell)).strip()
            return cell_value

        mapping = self._get_container_tables_mapping()
        if not mapping:
            return []
        else:
            table_names = mapping.keys()
        result_data = []
        for table_name in table_names:
            rows_count = int(self.gui.get_matching_xpath_count(
                                                 self.ALL_ROWS(table_name)))
            current_headers = []
            for row_idx in xrange(1, 1 + rows_count):
                items_count_in_row = int(self.gui.get_matching_xpath_count(
                                    self.ITEMS_IN_ROW(row_idx, table_name)))
                cols_count_in_row = int(self.gui.get_matching_xpath_count(
                                    self.COLS_IN_ROW(row_idx, table_name)))
                headers_count_in_row = int(self.gui.get_matching_xpath_count(
                                    self.HEADERS_IN_ROW(row_idx, table_name)))
                row_info = OrderedDict()
                if items_count_in_row == headers_count_in_row:
                    current_headers = []
                    for col_idx in xrange(1, 1 + items_count_in_row):
                        current_headers.append(get_cell_value(col_idx,
                                                    row_idx, table_name, True))
                elif headers_count_in_row > 0 and cols_count_in_row == 0:
                    pass
                elif headers_count_in_row == cols_count_in_row == 1:
                    header = self.gui.get_text(self.HEADERS_IN_ROW(row_idx,
                                                        table_name)).strip()
                    row_info[header] = get_cell_value(1, row_idx, table_name)
                elif items_count_in_row == len(current_headers) and current_headers:
                    for col_idx in xrange(1, 1 + items_count_in_row):
                        cell_value = get_cell_value(col_idx, row_idx,
                                                    table_name, True)
                        row_info[current_headers[col_idx - 1]] = cell_value
                if row_info:
                    result_data.append(row_info)
        return result_data

    def transform_data(self, initial_data, transform_opts):
        def parse_table_row(row_idx):
            one_row_data = CfgHolder()
            headers = initial_data[row_idx].keys()
            category_name = normalize(initial_data[row_idx][headers[0]]) \
                            if transform_opts.use_normalize \
                            else initial_data[row_idx][headers[0]]
            if transform_opts.first_column_as_key:
                if len(initial_data[row_idx]) == 1:
                    one_row_data[category_name] = \
                                            initial_data[row_idx][category_name]
                else:
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

        if transform_opts.result_as_dictionary:
            result = CfgHolder()
            for row_idx in xrange(len(initial_data)):
                result.update(parse_table_row(row_idx))
        else:
            result = []
            for row_idx in xrange(len(initial_data)):
                result.append(parse_table_row(row_idx))
        return result

    def export_as(self, dest_path=None):
        raise ConfigError('The table "{0}" has no export feature'.\
                          format(self._name))
