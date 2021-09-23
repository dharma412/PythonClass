#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1250/gui/web/reporting/web_reports.py#3 $ $DateTime: 2019/06/07 02:45:52 $ $Author: sarukakk $

import os
from common.gui.reports_base import ReportCheckError
from reports_base_zeus835 import ReportsBaseZeus835
from common.gui import guiexceptions
import time

LOADING_LOCATOR = "//*[contains(@id,'loading')]"
LOADING_TIMEOUT = 60

class WebReporting(ReportsBaseZeus835):
    """
        Keywords for actions and verifications on web reports
        (Overview, Users, Web Sites, URL Categories, Application Visibility,
        Anti-Malware, Client Malware Risk, Web Reputation Filters, L4 Traffic Monitor,
        Reports by User Location, System Capacity, Data Availability, SOCKS Proxy,
        Advanced Malware Protection, Advanced Malware Protection Verdict Updates).
    """

    def get_keyword_names(self):
        return [
                'web_reporting_open',
                'web_reporting_select_time_range',
                'web_reporting_select_items_display',
                'web_reporting_select_chart_option',
                'web_reporting_select_table_columns',
                'web_reporting_filter_table',
                'web_reporting_get_table',
                'web_reporting_check_table',
                'web_reporting_get_cell_value',
                'web_reporting_check_cell_value',
                'web_reporting_save_pdf',
                'web_reporting_section_export',
                'web_reporting_follow_table_link',
                'web_reporting_follow_chart_link',
                'web_reporting_check_chart_presence',
                'web_reporting_move_column',
                'web_reporting_sort_column',
        ]

    def _open_page(self, report_type):
        self._navigate_to('Web', 'Reporting', report_type)

        err_msg = 'The feature key for this feature has expired or is ' + \
                'unavailable'
        if self._is_text_present(err_msg):
            raise guiexceptions.GuiFeaturekeyMissingError(err_msg)

    def _wait_data_loading(self):
        _timer_start = time.time()
        time.sleep(1)
        while (time.time() - _timer_start) < LOADING_TIMEOUT:
            try:
                if not self._is_visible(LOADING_LOCATOR):
                    return
            except:
                return
            time.sleep(1)

        raise guiexceptions.TimeoutError("Loading data was not finished for the report.")

    def web_reporting_open(self, report_type, report_subtype=None):
        """
            Open web report (indicated by `report_type` parameter).

            Parameters:
                - `report_type`: Label of Web report, indicated in 'Web' > 'Reporting' menu.
                - `report_subtype`: Label of sub-report (like it is on 'Reports by User Location'
                web report), indicated on the report page.

            Examples:
            | Web Reporting Open | Users |
        """
        self._open_page(report_type)
        if report_subtype is not None:
            self.click_link("xpath=//div[@class='subtitle']//a[text()='"+report_subtype+"']")

        self._wait_data_loading()

    def web_reporting_select_time_range(self, time_range=None):
        """
            Selects time range for opened web report.

            Parameters:
                - `time_range`: Time range for the report.
                Either predefined time range (day, week, 30 days, 90 days, yesterday, previous month)
                or 'custom:date1:date2', where date1 and date2 should have format
                '01 Jan 2012 01'(%d %b %Y %H).

            Examples:
            | Web Reporting Select Time Range |
            | ... | time_range=day |
        """
        self.error_message = ''

        self._select_time_range(time_range)

        if self.error_message != '':
            raise guiexceptions.GuiValueError(self.error_message)

        self._wait_data_loading()

    def web_reporting_select_items_display(self, section_name, items_display=None):
        """
            Selects number of items to display in a table of a section of currently opened web report.

            Parameters:
                - `section_name`: Label of a section with a table.
                - `items_display`: Number of items to display. Either 10, 20, 100.
                It is applicable only if number of items is > 10.

            Return:
                - List of values in the table.

            Examples:
            | Web Reporting Get |
            | ... | Users |
            | ... | items_display=10 |
        """
        self.error_message = ''

        self._select_items_display(section_name, items_display)

        if self.error_message != '':
            raise guiexceptions.GuiValueError(self.error_message)

        self._wait_data_loading()

    def web_reporting_select_chart_option(self, option, chart_number=1):
        """
            Selects columns to display in a table of a section of currently opened web report.

            Parameters:
                - `option`: Chart option to select.
                - `chart_number`: Chart number to use.
                    First chart is used by default.

            Examples:
            | Web Reporting Select Chart Option |
            | ... | Bandwidth Used |
            | ... | 1 |
        """
        self.error_message = ''

        self._select_chart_option(option, chart_number)

        if self.error_message != '':
            raise guiexceptions.GuiValueError(self.error_message)

        self._wait_data_loading()

    def web_reporting_select_table_columns(self, section_name, columns=None, clear_others=True):
        """
            Selects columns to display in a table of a section of currently opened web report.

            Parameters:
                - `section_name`: Label of a section with a table to get data.
                - `columns`: String of comma-separated list of columns to display.
                You indicate 'all' to select all columns, IDs of columns, labels of columns,
                or parts of lables with wildcards (like `*Completed*`).
                - `clear_others`: ${True} or ${False} to remove other columns or not.
                Other columns are removed if this parameter is skipped.

            Examples:
            | Web Reporting Select Columns |
            | ... | Users |
            | ... | columns=all |
            | Web Reporting Select Columns |
            | ... | Users |
            | ... | columns=*Completed* |
        """
        self.error_message = ''

        self._select_columns(section_name, columns, clear_others)

        if self.error_message != '':
            raise guiexceptions.GuiValueError(self.error_message)

        self._wait_data_loading()

    def web_reporting_filter_table(self, section_name, filter=None):
        """
            Fiters table in a section of currently opened web report page.

            Parameters:
                - `section_name`: Label of a section with a table to get data.
                - `filter`: A value for table filtering.

            Examples:
            | Web Reporting Filter Table |
            | ... | Users |
            | ... | filter=rtester |
        """
        self.error_message = ''

        self._search_row(section_name, filter)

        if self.error_message != '':
            raise guiexceptions.GuiValueError(self.error_message)

        self._wait_data_loading()

    def web_reporting_get_table(self, section_name):
        """
            Get data from a section of currently opened page.

            Parameters:
                - `section_name`: Label of a section with a table to get data.

            Return:
                - List of values in the table.

            Examples:
            | ${data} = | Web Reporting Get |
            | ...       | Users |
            | Log Many  | ${data} |
        """
        self.error_message = ''

        _return_list = self._process_table(section_name)

        if self.error_message != '':
            raise guiexceptions.GuiValueError(self.error_message)

        return _return_list

    def web_reporting_check_table(self, section_name, expected_values, data_in_first_column=True, number_precision=None, time_precision=None):
        """
            Check data from a section of currently opened page.

            Parameters:
                - `section_name`: Label of a section with a table to check data.
                - `expected_values`: String of comma-separated expectations for table rows.
                Expectation for row is comma-separated list of pairs for expectations
                (like "Column1: expected_value11, Column2: expected_value12,
                Column1: expected_value21, Column2: expected_value22").
                Every pair (expectation for table cell) should have column name and expectation, separated by colon.
                Every expectation(for cell value) should be an exact value,
                asterisk ('*' means to skip checking the value),
                or a criterion for the value (like '>0').
                - `data_in_first_column`: ${False} to avoid considering values in first column as row names.
                By default, values in first column are considered as row names and cell values are checked only in expected rows.
                - `number_precision`: Precision to check numbers in cells.
                By default values should be equal exactly.
                - `time_precision`: Precision (in seconds) to check time values in cells.
                By default values should be equal exactly.

            Exception:
                - `ReportCheckError`: exception appears if present value does not satisfy indicated criterion.

            Examples:
            | Web Reporting Check Table |
            | ... | Users |
            | ... | User ID or Client IP:rtester, Total Treansactions:>0 |
        """
        self._debug("Checking table in section: %s" % (section_name,))
        self.error_message = ''

        _return_list = self._process_table(section_name, expected_values, \
            data_in_first_column=data_in_first_column, \
            number_precision=number_precision, time_precision=time_precision)

        if self.error_message != '':
            raise ReportCheckError(self.error_message)

        return _return_list

    def web_reporting_get_cell_value(self, section_name, row, column=None):
        """
            Get value of a cell.

            Parameters:
                - `section_name`: Label of a section with a table to get data.
                - `row`: Row name (indicated in first column) of the cell.
                - `column`: Column header of ther cell. If it is missed, value from first column is returned.

            Return:
                Value in specified cell is returned.

            Examples:
            | ${item_value}= | Web Reporting Get Cell Value |
            | ... | Users |
            | ... | rtester |
            | ... | Transactions Completed |
        """
        self.error_message = ''

        _table_loc = self._find_table(section_name)
        if _table_loc is None:
            raise ReportCheckError("Table was not found in section '%s'" % section_name)
        _found_value = self._get_table_cell_value(_table_loc, row, column)

        if self.error_message != '':
            raise guiexceptions.GuiValueError(self.error_message)

        return _found_value

    def web_reporting_check_cell_value(self, section_name, row, column, criterion):
        """
            Check if value in a cell satisfy indicated criterion.

            Parameters:
                - `section_name`: Label of a section with a table to check data.
                - `row`: Row name (indicated in first column) of a cell to check.
                - `column`: Column of a cell to check.
                - `criterion`: Criterion to check value (like `>0` or `=1`).
                Only numeric values will be checked.

            Exception:
                - `ReportCheckError`: exception appears if present value does not satisfy indicated criterion.

            Examples:
            | Web Reporting Check Cell Value |
            | ... | Users |
            | ... | rtester |
            | ... | Transactions Completed |
            | ... | >0 |
        """
        self.error_message = ''

        if (row is None) or (column is None):
            raise ValueError("'row', 'column' must be indicated.")

        _check_result = self._check_cell_value(section_name, \
                                        row, column, criterion)

        if not _check_result:
            raise ReportCheckError(self.error_message)

    def web_reporting_save_pdf(self):
        """
            Save data of currently opened page to PDF file by
            "Printable (PDF)" link on the page.

            Return:
                Full path to saved file.

            Examples:
            | ${filename}= | Web Reporting Save PDF |
        """
        return self._pdf()

    def web_reporting_section_export(self, section_name=None):
        """
            Export data of a section on currently opened page to CSV file by
            "Export..." link on the page.

            Parameters:
                - `section_name`: Label of a section with a table to check data.

            Return:
                Full path to saved file.

            Examples:
            | ${filename}= | Web Reporting Section Export | Users |
        """
        return self._export(section_name)

    def web_reporting_follow_table_link(self, section_name, row=None, column=None):
        """
            Follow a link in a cell of a section on currently opened page.

            Parameters:
                - `section_name`: Label of a section with a table.
                - `row`: Row name (indicated in first column) of a cell with the link.
                - `column`: Column of a cell with the link.

            Examples:
            | Web Reporting Follow Table Link |
            | ... | Users |
            | ... | row=rtester |
            | ... | column=Transactions Completed |
        """
        self.error_message = ''

        self._follow_link_in_table(section_name, row, column)

        if self.error_message != '':
            raise guiexceptions.GuiValueError(self.error_message)

    def web_reporting_follow_chart_link(self, section_name, link):
        """
            Follow a link in a cell of a section on currently opened page.

            Parameters:
                - `section_name`: Label of a section with a chart.
                - `link`: Title of a link to follow.

            Examples:
            | Web Reporting Follow Chart Link |
            | ... | Top Users: Bandwidth Used |
            | ... | rtester |
        """
        self.error_message = ''

        self._follow_link_in_chart(section_name, link)

        if self.error_message != '':
            raise guiexceptions.GuiValueError(self.error_message)

    def web_reporting_check_chart_presence(self, section_name):
        """
            Check if an image is present for a chart in specified section.

            Parameters:
                - `section_name`: Label of a section with a chart.

            Examples:
            | Web Reporting Check Chart Presence |
            | ... | Top Users: Bandwidth Used |
        """
        self.error_message = ''

        if not self._chart_presence(section_name):
            raise ReportCheckError("Chart was not present in section '%s'" % (section_name))

    def web_reporting_move_column(self, section_name, column_name, target_column):
        """
            Change order of table columns.

            Parameters:
                - `section_name`: Label of a section with a table to get data.
                - `column_name`: Name of a column to move.
                - `target_column`: Name of a column to drop moved column after.

            Exception:
                - `GuiValueError`: exception appears if a column was not found.

            Examples:
            | Web Reporting Move Column |
            | ... | Users |
            | ... | Transactions Completed |
            | ... | Transactions Blocked |
        """
        self.error_message = ''

        _table_loc = self._find_table(section_name)
        self._debug("_table_loc: %s" % (_table_loc,))
        if _table_loc is None:
            raise GuiValueError("Table was not found in section '%s'" % section_name)

        _first_column_loc = "%s//th[normalize-space()='%s']" % (_table_loc, column_name)
        if int(self.get_matching_xpath_count(_first_column_loc)) < 1:
            raise guiexceptions.GuiValueError("Column '%s' was not found in section '%s'." % (column_name, section_name))

        _second_column_loc = "%s//th[normalize-space()='%s']" % (_table_loc, target_column)
        if int(self.get_matching_xpath_count(_second_column_loc)) < 1:
            raise guiexceptions.GuiValueError("Column '%s' was not found in section '%s'." % (target_column, section_name))

        self._drag_and_drop_to_object(_first_column_loc, _second_column_loc)

        if self.error_message != '':
            raise guiexceptions.GuiValueError(self.error_message)

    def web_reporting_sort_column(self, section_name, column_name):
        """
            Change order of table columns.

            Parameters:
                - `section_name`: Label of a section with a table to get data.
                - `column_name`: Name of a column to sort.

            Exception:
                - `GuiValueError`: exception appears if a column was not found.

            Examples:
            | Web Reporting Sort Column |
            | ... | Users |
            | ... | Transactions Completed |
        """
        self.error_message = ''

        _table_loc = self._find_table(section_name)
        self._debug("_table_loc: %s" % (_table_loc,))
        if _table_loc is None:
            raise GuiValueError("Table was not found in section '%s'" % section_name)

        _column_loc = "%s//th[normalize-space()='%s']" % (_table_loc, column_name)
        if int(self.get_matching_xpath_count(_column_loc)) < 1:
            raise guiexceptions.GuiValueError("Column '%s' was not found in section '%s'." % (column_name, section_name))

        self.click_element(_column_loc, "don't wait")

        self._wait_data_loading()

        if self.error_message != '':
            raise guiexceptions.GuiValueError(self.error_message)
