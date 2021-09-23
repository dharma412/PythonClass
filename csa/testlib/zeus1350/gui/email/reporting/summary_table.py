#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/zeus1350/gui/email/reporting/summary_table.py#1 $ $DateTime: 2019/09/18 01:46:35 $ $Author: sarukakk $

import report_table

# Summary tables attributes dictionary.
# Item format is:
# '<table_name_in_gui>': ((<tuple_with_tab_names_to_be_passed_to_navigate_to_method>),
# (<tuple_with_table_coordinates_in_gui_taken_from_"id=ss_0_%d_%d"_parameter>))
TABLE_NAMES = {'Incoming Mail Summary': (('Email', 'Reporting', 'Overview'),
                                         (0, 1)),
               'Outgoing Mail Summary': (('Email', 'Reporting', 'Overview'),
                                         (1, 1)),
               'Message Delivery': (('Email', 'Reporting', 'Overview'),
                                    (2, 0)),
               'Incident Summary': (('Email', 'Reporting', 'DLP Incidents'),
                                    (0, 1)),
               'Incoming TLS Connections Summary': (('Email', 'Reporting', 'TLS Connections'),
                                                    (0, 1)),
               'Incoming TLS Messages Summary': (('Email', 'Reporting', 'TLS Connections'),
                                                 (1, 0)),
               'Outgoing TLS Connections Summary': (('Email', 'Reporting', 'TLS Connections'),
                                                    (3, 1)),
               'Outgoing TLS Messages Summary': (('Email', 'Reporting', 'TLS Connections'),
                                                 (4, 0)),
               'Indicator of Compromise (IOC) Matches': (('Email', 'Reporting', 'External Threat Feeds'),
                                                         (1, 1))}

CONTENT_ROWS = lambda coords: '%s//div[@id=\'ss_0_%d_%d\']//table[@class=\'pairs\']/tbody/tr' % \
                              (report_table.REPORT_TABLE, coords[0], coords[1])
COLUMN_NAMES = lambda coords: '%s//div[@id=\'ss_0_%d_%d\']//table[@class=\'pairs\']/tbody/tr[1]/th' % \
                              (report_table.REPORT_TABLE, coords[0], coords[1])
COLUMN_NAME_BY_INDEX = lambda coords, idx: '%s//div[@id=\'ss_0_%d_%d\']//table[@class=\'pairs\']' \
                                           '/tbody/tr[1]/th[%d]' % \
                                           (report_table.REPORT_TABLE, coords[0], coords[1], idx)

CATEGORY_NAME_BY_INDEX = lambda coords, idx: '%s//div[@id=\'ss_0_%d_%d\']//table[@class=\'pairs\']' \
                                             '/tbody/tr[%d]/th[1]' % \
                                             (report_table.REPORT_TABLE, coords[0], coords[1], idx)
CATEGORY_VALUE_BY_INDEX = lambda coords, category_idx, value_idx: \
    '%s//div[@id=\'ss_0_%d_%d\']//table[@class=\'pairs\']/tbody/tr[%d]/td[%d]' % \
    (report_table.REPORT_TABLE, coords[0], coords[1], category_idx, value_idx)

CATEGORY_NAME_BY_INDEX_CONTENT = lambda coords, idx: '%s//div[@id=\'ss_0_%d_%d\']//table[@class=\'pairs\']' \
                                                     '/tbody/tr[%d]/th[1]/a' % \
                                                     (report_table.REPORT_TABLE, coords[0], coords[1], idx)

CATEGORY_VALUE_BY_INDEX_CONTENT = lambda coords, category_idx, value_idx: \
    '%s//div[@id=\'ss_0_%d_%d\']//table[@class=\'pairs\']/tbody/tr[%d]/td[%d]/a' % \
    (report_table.REPORT_TABLE, coords[0], coords[1], category_idx, value_idx)


class SummaryTableParameters(report_table.CommonReportTableParameters):
    """Summary table parameters are equal to common parameters
    """
    pass


class SummaryTable(report_table.ReportTable):
    """The class have methods to parse tables with class="pairs" attribute
    """

    def _get_table_parameters(self, kwargs={}):
        return SummaryTableParameters(self._wui, **kwargs)

    def _get_data(self,
                  table_name,
                  table_parameters=None,
                  should_navigate_to_table=True):
        table_path, table_coords = self._extract_table_attributes(table_name)
        if should_navigate_to_table:
            self._navigate_to_table(table_path, table_parameters)

        content_rows = CONTENT_ROWS(table_coords)
        self._wait_for_table_load(content_rows)

        cells_count_in_col = int(self._wui.get_matching_xpath_count(content_rows))
        cells_count_in_row = int(self._wui.get_matching_xpath_count(COLUMN_NAMES(table_coords)))

        result_dict = {}
        for row_idx in range(2, cells_count_in_col + 1):
            for col_idx in range(1, cells_count_in_row + 1):
                if col_idx == 1:
                    cell_locator = CATEGORY_NAME_BY_INDEX(table_coords,
                                                          row_idx)
                else:
                    cell_locator = CATEGORY_VALUE_BY_INDEX(table_coords,
                                                           row_idx,
                                                           col_idx - 1)
                try:
                    cell_value = self._wui.get_text(cell_locator)
                except Exception:
                    # Ignoring empty rows
                    break

                col_name = self._wui.get_text(COLUMN_NAME_BY_INDEX(table_coords,
                                                                   col_idx))
                if col_name in result_dict.keys():
                    result_dict[col_name].append(cell_value)
                else:
                    result_dict[col_name] = [cell_value, ]
        return result_dict

    def _get_report_get_content_link(self,
                                     table_name,
                                     table_parameters=None,
                                     should_navigate_to_table=True):
        table_path, table_coords = self._extract_table_attributes(table_name)
        if should_navigate_to_table:
            self._navigate_to_table(table_path, table_parameters)

        content_rows = CONTENT_ROWS(table_coords)
        self._wait_for_table_load(content_rows)

        cells_count_in_col = int(self._wui.get_matching_xpath_count(content_rows))
        cells_count_in_row = int(self._wui.get_matching_xpath_count(COLUMN_NAMES(table_coords)))

        result_dict = {}
        for row_idx in range(2, cells_count_in_col + 1):
            for col_idx in range(1, cells_count_in_row + 1):
                if col_idx == 1:
                    cell_locator = CATEGORY_NAME_BY_INDEX_CONTENT(table_coords,
                                                                  row_idx)
                else:
                    cell_locator = CATEGORY_VALUE_BY_INDEX_CONTENT(table_coords,
                                                                   row_idx,
                                                                   col_idx - 1)
                try:
                    cell_value = cell_locator
                except Exception:
                    # Ignoring empty rows
                    break

                col_name = self._wui.get_text(COLUMN_NAME_BY_INDEX(table_coords,
                                                                   col_idx))
                if col_name in result_dict.keys():
                    result_dict[col_name].append(cell_value)
                else:
                    result_dict[col_name] = [cell_value, ]
        return result_dict

    def _get_table_attributes_dict(self):
        return TABLE_NAMES
