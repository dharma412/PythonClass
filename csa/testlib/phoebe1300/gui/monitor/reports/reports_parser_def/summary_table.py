#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/phoebe1300/gui/monitor/reports/reports_parser_def/summary_table.py#1 $
# $DateTime: 2019/06/27 23:26:24 $
# $Author: aminath $

from common.gui.decorators import set_speed
from common.util.ordered_dict import OrderedDict
from sal.containers.cfgholder import CfgHolder

from base_reporting_table import BaseReportingTable, normalize
from data_load_monitor import wait_until_data_loaded, NoDataFound


class SummaryTable(BaseReportingTable):
    """The class have methods to parse tables having class="pairs" attribute
    """
    ALL_ROWS = lambda self: \
        "{0}/tbody[not(contains(@style, 'display: none'))]" \
        "/tr[not(contains(@class, 'spacer'))]". \
            format(self._get_xpath_root())

    @classmethod
    def get_available_table_names(cls):
        return ['Incoming Mail Summary', 'Outgoing Mail Summary',
                'Incident Summary', 'Incoming TLS Connections Summary',
                'Incoming TLS Messages Summary', 'Message Delivery',
                'Outgoing TLS Connections Summary',
                'Outgoing TLS Messages Summary', 'Counters', 'Gauges',
                'Rates (Events per Hour)', 'Incoming Content Filter Matches',
                'Outgoing Content Filter Matches',
                'Incoming Mail from this Sender Domain',
                'Summary of Incoming files handled by AMP',
                'Incoming files handled by AMP',
                'Summary of Outgoing files handled by AMP',
                'Outgoing files handled by AMP',
                'Summary of Incoming Malicious files by Category',
                'Summary of Outgoing Malicious files by Category',
                'Indicator of Compromise (IOC) Matches',
                'Summary of Indicator of Compromise (IOC) Matches within Source',
                'Summary of Incoming Messages handled by SDR',
                'SDR Threat Category',
                'Summary of Messages by SDR Threat Category', ]
        # TODO: subclass Gauges since it contains 2 subtables

    def _get_xpath_root(self):
        return "{0}//dt[.//span[normalize-space()='{1}']]/following-sibling::" \
               "dd//table[contains(@class, 'pairs')][1]". \
            format(super(SummaryTable, self)._get_xpath_root(),
                   self._name)

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
        result_data = []
        current_headers = []
        for row_idx in xrange(1, 1 + rows_count):
            items_count_in_row = int(self.gui.get_matching_xpath_count(
                self.ITEMS_IN_ROW(row_idx)))
            cols_count_in_row = int(self.gui.get_matching_xpath_count(
                self.COLS_IN_ROW(row_idx)))
            headers_count_in_row = int(self.gui.get_matching_xpath_count(
                self.HEADERS_IN_ROW(row_idx)))
            row_info = OrderedDict()
            if items_count_in_row == headers_count_in_row:
                current_headers = []
                for col_idx in xrange(1, 1 + items_count_in_row):
                    current_headers.append(get_cell_value(col_idx,
                                                          row_idx, True))
            elif headers_count_in_row > 0 and cols_count_in_row == 0:
                pass
            elif headers_count_in_row == cols_count_in_row == 1:
                header = self.gui.get_text(self.HEADERS_IN_ROW(row_idx)).strip()
                row_info[header] = get_cell_value(1, row_idx)
            elif items_count_in_row == len(current_headers) and current_headers:
                for col_idx in xrange(1, 1 + items_count_in_row):
                    cell_value = get_cell_value(col_idx, row_idx, True)
                    row_info[current_headers[col_idx - 1]] = cell_value
            if row_info:
                result_data.append(row_info)
        return result_data

    @set_speed(0, 'gui')
    def click_cell(self, row_name):
        row_idx = self._get_row_idx_by_cell_value(1, row_name, True)
        items_count = int(self.gui.get_matching_xpath_count(
            self.ITEMS_IN_ROW(row_idx)))
        cell_value = None
        for col_idx in xrange(1, 1 + items_count):
            cell_locator = self.CELL_BY_COL_ROW(col_idx, row_idx, True)
            cell_value = self.gui.get_text(cell_locator).strip()
            link_locator = self.LINK_BY_COL_ROW_IDX(col_idx, row_idx, True)
            if self.gui._is_element_present(link_locator):
                self.gui.click_element(link_locator)
                return (cell_value, True)
        return (cell_value, False)

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

    @set_speed(0, 'gui')
    def open_item(self, item_name):
        self.gui.click_element("{0}//a[normalize-space()='{1}']".format(
            self._get_xpath_root(), item_name))
        wait_until_data_loaded(self.gui)
