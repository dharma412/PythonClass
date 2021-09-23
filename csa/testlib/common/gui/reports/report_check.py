#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/common/gui/reports/report_check.py#1 $
# $DateTime: 2019/03/22 01:36:06 $
# $Author: aminath $

import re
import time

from common.gui.guicommon import GuiCommon
from common.gui.wait_for_download import WaitForDownload
import common.gui.guiexceptions as guiexceptions


class ReportCheck(GuiCommon):
    """Base class for gathering information from reports and verifying it.
    """

    error_message = ''

    TABLE_COLUMNS_LINK_SELECTOR = "//a[contains(@href, 'showTableOptions')]"
    SECTION_EXPORT_LINK_SELECTOR = "//a[contains(@href, 'showTableOptions')]"

    def _get_reports_info(self, report_class, report_type='email'):
        REPORT_INFO_CELL = lambda row, title_column: REPORTS_TABLE % \
                                                     (row, title_column)
        REPORTS_TABLE = "//table[@class='cols']/tbody/tr[%s]/td[%s]"

        reports = []
        start_row = 2
        if self._check_reports_availability():
            num_of_rows = int(self.get_matching_xpath_count(
                REPORT_INFO_CELL('*', 1)))

            if report_type == 'email':
                columns_order = report_class._email_columns_order
            else:
                columns_order = report_class._web_columns_order

            for row in xrange(start_row, num_of_rows + start_row):
                report_info = {}
                for column, column_name in enumerate(columns_order, 1):
                    report_info[column_name] = self.get_text(
                        REPORT_INFO_CELL(row, column))
                reports.append(str(report_class(**report_info)))

        return reports

    def _make_section_loc(self, section_path, exact=True):
        self._debug("Prepearing section locatoor for section: %s" % (section_path,))
        if exact:
            text_selection = "(normalize-space(text())="
        else:
            text_selection = "contains(text(),"
        section_path_list = section_path.split(" > ")
        section_loc = ""
        section_loc += "//dl[contains(@class,'header') or contains(@class,'box')]"
        section_loc += "/dt/descendant-or-self::*[%s'%s')]" % (text_selection, section_path_list[0])
        section_loc += "/ancestor-or-self::dt/"
        if len(section_path_list) == 1:
            section_loc += "/following-sibling::dd"
            return [section_loc]

        # search subsection in 'dashboard' tables
        section_loc1 = section_loc
        section_loc1 += "/following-sibling::dd"
        section_loc1 += "//table[@class='dashboard']//*[%s'%s')]" % (text_selection, section_path_list[1])
        section_loc1 += "/ancestor::table[@class='dashboard']/following-sibling::table"

        # search subsection in the same parent row
        section_loc2 = section_loc
        section_loc2 += "/ancestor::tr[1]"
        section_loc2 += "//dl[contains(@class,'header') or contains(@class,'box')]"
        section_loc2 += "/dt/descendant-or-self::*[%s'%s')]" % (text_selection, section_path_list[1])
        section_loc2 += "/ancestor-or-self::dt/following-sibling::dd"

        # search subsection in next rows
        section_loc3 = section_loc
        section_loc3 += "/ancestor::tr[1]/following-sibling::tr"
        section_loc3 += "//dl[contains(@class,'header') or contains(@class,'box')]"
        section_loc3 += "/dt/descendant-or-self::*[%s'%s')]" % (text_selection, section_path_list[1])
        section_loc3 += "/ancestor-or-self::dt[1]/following-sibling::dd"
        section_loc3 = "(%s)[1]" % section_loc3
        return [section_loc1, section_loc2, section_loc3]

    def _set_element_id(self, locator):
        """ Assign id to the element and return xpath to search by id."""
        if int(self.get_matching_xpath_count(locator + "/self::*[@id]")) > 0:
            _id = self.get_element_attribute("xpath=" + locator + "@id")
        else:
            _id = time.time()
            self.assign_id_to_element("xpath=" + locator, _id)
        return "//*[@id='%s']" % _id

    def _find_section_area(self, section_path, timeout=60):
        """ Find table by indicating section name and parent headers as path. """
        self._debug("Searching section: %s" % (section_path,))
        sections = section_path.split(" > ")
        section_locs = self._make_section_loc(section_path, True) + \
                       self._make_section_loc(section_path, False)

        section_loc = None
        _timer_start = time.time()
        while ((time.time() - _timer_start) < timeout) \
                and (section_loc is None):
            for section_loc_i in section_locs:
                section_count = int(self.get_matching_xpath_count(section_loc_i))
                self._debug("Search by locator: %s gave %s items" % (section_loc_i, section_count))
                if section_count > 0:
                    section_loc = "(%s)[1]" % (section_loc_i,)
                    return self._set_element_id(section_loc)
            time.sleep(3)

        return section_loc

    def _find_table(self, section_path, section_loc=None, timeout=60):
        """ Find table by indicating section name and parent headers as path. """
        if section_loc is None:
            table_loc = self._find_section_area(section_path)
        else:
            table_loc = section_loc
        if table_loc is None:
            return None
        tables_count = 0
        _timer_start = time.time()
        while (time.time() - _timer_start) < timeout:
            _table_loc = table_loc + "//thead/parent::table"
            tables_count = int(self.get_matching_xpath_count(_table_loc))
            if tables_count == 0:
                _table_loc = table_loc + "//tr[contains(@class, 'header')]/parent::table"
                tables_count = int(self.get_matching_xpath_count(_table_loc))
            if tables_count == 0:
                _table_loc = table_loc + "//tr[contains(@class, 'header')]/parent::tbody/parent::table"
                tables_count = int(self.get_matching_xpath_count(_table_loc))
            if tables_count == 0:
                _table_loc = table_loc + "/table"
                tables_count = int(self.get_matching_xpath_count(_table_loc))
            if tables_count == 0:
                time.sleep(1)
            else:
                break
        if tables_count > 0:
            return _table_loc
        else:
            return None

    def _get_table_head_loc(self, table_loc):
        """ Return list of headesr in a table, specified by table locator. """
        # trying to find table with thead
        table_head = table_loc + "/thead"
        table_head_count = int(self.get_matching_xpath_count(table_head))
        table_head_rows_count = 0
        if table_head_count > 0:
            table_head_rows_count = int(self.get_matching_xpath_count(table_head + "/tr"))
        else:
            # trying to find table with headers in rows
            table_head_rows_count = int(self.get_matching_xpath_count(table_loc + "//tr[contains(@class, 'header')]"))
            table_head = table_loc + "//tr[contains(@class, 'header')]/parent::*"

        return [table_head, table_head_rows_count]

    def _get_table_headers(self, table_loc):
        """ Return list of headesr in a table, specified by table locator. """
        head_data = []
        rowspan_numbers = []

        table_head, table_head_rows_count = self._get_table_head_loc(table_loc)

        # get table headers (first row)
        _header_th_count = int(self.get_matching_xpath_count(table_head + "/tr[1]/th"))
        self._debug("_header_th_count: %s" % _header_th_count)
        for _th in range(1, 1 + _header_th_count):
            # prepare getting value
            _th_loc = table_head + "/tr[1]/th[" + str(_th) + "]"
            self._debug("_th_loc: %s" % _th_loc)
            # check visibility
            _visible = self._is_visible("xpath=" + _th_loc)
            # get column span
            _th_colspan = 1
            if int(self.get_matching_xpath_count(_th_loc + "/self::*[@colspan]")) > 0:
                _th_colspan = int(self.get_element_attribute("xpath=" + _th_loc + "@colspan"))
            # get row span
            _th_rowspan = 1
            if int(self.get_matching_xpath_count(_th_loc + "/self::*[@rowspan]")) > 0:
                _th_rowspan = int(self.get_element_attribute("xpath=" + _th_loc + "@rowspan"))
            # get value
            if _visible:
                _th_value = self.get_text("xpath=" + _th_loc)
            else:
                _th_value = None
            for _data_index in range(_th_colspan):
                rowspan_numbers.append(_th_rowspan)
                head_data.append(_th_value)

        # loop through other rows to have unique headers in the list
        for th_tr in range(2, 1 + table_head_rows_count):
            _header_th_count = int(self.get_matching_xpath_count(table_head + "/tr[" + str(th_tr) + "]/th"))
            self._debug("_header_th_count: %s" % _header_th_count)
            _cell_index = 0
            # loop through header TH elements
            for _th in range(1, 1 + _header_th_count):
                # skip first cells missed by row spanning
                while rowspan_numbers[_cell_index] > 1:
                    rowspan_numbers[_cell_index] -= 1
                    _cell_index += 1
                    self._debug("_cell_index: %s" % _cell_index)
                # prepare getting value
                _th_loc = table_head + "/tr[" + str(th_tr) + "]/th[" + str(_th) + "]"
                self._debug("_th_loc: %s" % _th_loc)
                # check visibility
                _visible = self._is_visible("xpath=" + _th_loc)
                # get column span
                _th_colspan = 1
                if int(self.get_matching_xpath_count(_th_loc + "/self::*[@colspan]")) > 0:
                    _th_colspan = int(self.get_element_attribute("xpath=" + _th_loc + "@colspan"))
                # get row span
                _th_rowspan = 1
                if int(self.get_matching_xpath_count(_th_loc + "/self::*[@rowspan]")) > 0:
                    _th_rowspan = int(self.get_element_attribute("xpath=" + _th_loc + "@rowspan"))
                # get value
                _th_value = self.get_text("xpath=" + _th_loc)
                for _data_index in range(_cell_index, _cell_index + _th_colspan):
                    rowspan_numbers[_data_index] = _th_rowspan
                    if _visible:
                        head_data[_data_index] += " " + _th_value
                    else:
                        head_data[_data_index] = None
                _cell_index += _th_colspan

        return head_data

    def _get_table_header_index(self, table_loc, header):
        """ Return index of cells for specified header. """
        table_head, table_head_rows_count = self._get_table_head_loc(table_loc)
        if table_head_rows_count == 1:
            _header_loc = table_head + "/tr[1]/th/descendant-or-self::*[normalize-space(text())='" + header + "']"
            _header_count = int(self.get_matching_xpath_count(_header_loc))
            if _header_count < 1:
                return None
            return int(
                self.get_matching_xpath_count(_header_loc + "/ancestor-or-self::th[1]/preceding-sibling::th")) + 1
        else:
            head_list = self._get_table_headers(table_loc)
            try:
                return head_list.index(header) + 1
            except:
                return None

    def _get_table_rows_loc(self, table_loc):
        """ Return locator for table rows. """
        table_body = table_loc + "/tbody[not(contains(@style,'display: none'))]"
        if int(self.get_matching_xpath_count(table_body)) > 0:
            table_rows = table_body + "/tr[not(contains(@class, 'header'))]"
        else:
            table_rows = table_loc + "//tr[contains(@class, 'header')]/parent::*/tr[not(contains(@class, 'header'))]"

        return table_rows

    def _get_table_values(self, tables_loc):
        """ Return list of values in a table or tables, specified by table locator. """
        _prev_speed = self.set_selenium_speed(0)

        tables_list = []
        tables_count = int(self.get_matching_xpath_count(tables_loc))
        for table_num in range(1, 1 + tables_count):
            table_list = []
            table_loc = "(" + tables_loc + ")[" + str(table_num) + "]"

            _new_id = time.time()
            self.assign_id_to_element("xpath=" + table_loc, _new_id)
            table_loc = "//*[@id='%s']" % _new_id

            head_list = self._get_table_headers(table_loc)
            cleared_head_list = list(head_list)
            for i in range(cleared_head_list.count(None)):
                cleared_head_list.remove(None)

            table_list.append(cleared_head_list)

            # getting table body for getting data
            table_rows = self._get_table_rows_loc(table_loc)

            # going through rows
            tr_count = int(self.get_matching_xpath_count(table_rows))
            for tr_num in range(1, 1 + tr_count):
                row_loc = "(" + table_rows + ")[" + str(tr_num) + "]"
                if not self._is_visible("xpath=" + row_loc + "/*[1]"):
                    continue
                row_list = []
                td_count = int(self.get_matching_xpath_count(row_loc + "/*"))
                for td_num in range(1, 1 + td_count):
                    td_loc = row_loc + "/*[" + str(td_num) + "]"
                    # skip invisible
                    if head_list[td_num - 1] is None:
                        continue
                    td_value = self.get_text("xpath=" + td_loc)
                    row_list.append(td_value)
                table_list.append(row_list)
            tables_list.append(table_list)

        self.set_selenium_speed(_prev_speed)

        # parsing case of one table found
        if len(tables_list) == 1:
            return tables_list[0]
        else:
            return tables_list

    def _get_table_row_index(self, table_loc, row_name):
        """ Return index of cells for specified header. """
        # getting table body for getting data
        table_rows = self._get_table_rows_loc(table_loc)

        _row_loc = table_rows + "/*[1]/descendant-or-self::*[normalize-space(text())='" + row_name + "']"
        tr_count = int(self.get_matching_xpath_count(_row_loc))
        if tr_count < 1:
            return None
        return int(self.get_matching_xpath_count(
            _row_loc + "/ancestor-or-self::tr[1]/preceding-sibling::tr[not(contains(@class, 'header'))]")) + 1

    def _get_table_cell_loc(self, table_loc, row_name, header=None):
        table_rows = self._get_table_rows_loc(table_loc)
        _row = self._get_table_row_index(table_loc, row_name)
        if header is None:
            _col = 1
        else:
            _col = self._get_table_header_index(table_loc, header)
        self._debug("_row: %s" % _row)
        # self._debug("Row: %s" % self.get_text("xpath=" +("("+table_rows+")["+str(_row)+"]/*[1]")))
        self._debug("_col: %s" % _col)
        # self._debug("Column: %s" % (self._get_table_headers(table_loc))[_col-1])
        return "(" + table_rows + ")[" + str(_row) + "]/*[" + str(_col) + "]"

    def _get_table_cell_value(self, table_loc, row_name, header=None):
        _cell_loc = self._get_table_cell_loc(table_loc, row_name, header)
        return self.get_text("xpath=" + _cell_loc)

    def _convert_tuple_to_table(self, user_input):
        """ Convert tuple with strings of comma-separated pairs ('key:value') to
        multidimentional list. """
        _first_column_name = None
        _headers = []
        _table = []
        _row = []
        for _user_string in user_input:
            _user_string = _user_string.replace("\,", "&#044;")
            _user_string = _user_string.replace("\:", "&#058;")
            _array = _user_string.split(',')
            for _pair in _array:
                _pos = _pair.find(':')
                if _pos < 0:
                    _name = ''
                    _value = _pair.strip()
                    if _value == '':
                        continue
                elif _pos == 0:
                    _name = ''
                    _value = _pair[1:].strip()
                else:
                    _name = _pair[0:_pos].strip()
                    _value = _pair[_pos + 1:].strip()

                _name = _name.replace("&#044;", ",")
                _name = _name.replace("&#058;", ":")
                _value = _value.replace("&#044;", ",")
                _value = _value.replace("&#058;", ":")

                if _first_column_name is None:
                    _first_column_name = _name
                elif _name == _first_column_name:
                    _table.append(list(_row))
                    _row = map(lambda x: '', range(len(_headers)))
                if _name not in _headers:
                    _headers.append(_name)
                    _row.append(_value)
                else:
                    _row[_headers.index(_name)] = _value
        _table.append(list(_row))
        _table.insert(0, _headers)
        self._debug(_table)
        return _table

    def _convert_str_to_time(self, str_time):
        time_value_time = None
        try:
            time_value_time = time.strptime(str_time, "%Y-%m-%d %H:%M:%S")
        except:
            pass
        if time_value_time is None:
            try:
                time_value_time = time.strptime(str_time, "%Y %m %d %H")
            except:
                pass
        if time_value_time is None:
            try:
                time_value_time = time.strptime(str_time, "%Y %m %d %H %M")
            except:
                pass
        if time_value_time is None:
            try:
                time_value_time = time.strptime(str_time, "%d %b %Y %H:%M")
            except:
                pass
        if time_value_time is None:
            try:
                time_value_time = time.strptime(str_time, "%d %b %Y %H:%M  (GMT)")
            except:
                pass
        if time_value_time is not None:
            time_value_time = time.mktime(time_value_time)
        self._debug("time_value_time")
        self._debug(str_time)
        self._debug(time_value_time)

        return time_value_time

    def _compare_times(self, time1, time2, time_precision=None):
        """Compares two strings with datetime and return True if equal.
        """
        time1_value_time = self._convert_str_to_time(time1)
        time2_value_time = self._convert_str_to_time(time2)
        if time1_value_time is not None and time2_value_time is not None:
            self._debug("time difference")
            self._debug(time1_value_time - time2_value_time)
            if time_precision is not None:
                return abs(time1_value_time - time2_value_time) < time_precision
            else:
                return time1_value_time == time2_value_time
        else:
            return False

    def _compare_numbers(self, num1, num2, number_precision=None):
        self._debug("num1=%s" % num1)
        self._debug("num2=%s" % num2)
        num1_value_num = None
        try:
            num1_value_num = float(num1)
        except:
            pass
        if num1_value_num is None:
            m = re.search("[^\-\d\.]{0,2}(\-?\d+\.?\d*)[^\-\d\.]{0,2}", str(num1))
            if m is not None:
                num1_value_num = (m.groups())[0]
                self._debug("num1_value_num=%s" % num1_value_num)
                try:
                    num1_value_num = float(num1_value_num)
                except:
                    pass
        self._debug("num1_value_num=%s" % num1_value_num)
        num2_value_num = None
        try:
            num2_value_num = float(num2)
        except:
            pass
        if num2_value_num is None:
            m = re.search("[^\-\d\.]{0,2}(\-?\d+\.?\d*)[^\-\d\.]{0,2}", str(num2))
            if m is not None:
                num2_value_num = (m.groups())[0]
                self._debug("num2_value_num=%s" % num2_value_num)
                try:
                    num2_value_num = float(num2_value_num)
                except:
                    pass
        self._debug("num2_value_num=%s" % num2_value_num)
        if (num1_value_num is None) and (num2_value_num is not None) and len(num1) > 0:
            _first_char = str(num1)[0]
            if _first_char == '=' or _first_char == '>' or _first_char == '<':
                try:
                    return eval(str(num2_value_num) + str(num1))
                except:
                    return False
        if (num1_value_num is not None) and (num2_value_num is not None):
            self._debug("number difference")
            self._debug(num1_value_num - num2_value_num)
            if number_precision is not None:
                return abs(num1_value_num - num2_value_num) < number_precision
            else:
                return num1_value_num == num2_value_num

        return False

    def _simple_match(self, input_string, find_string):
        _find_string = re.sub(r'([\.\^\$\+\{\}\[\]\\\|\(\)])', r'\\\1', find_string)
        _find_string = re.sub(r'(\*)', r'.*', _find_string)
        _find_string = re.sub(r'(\\\\\.\*?)', r'\*', _find_string)
        _find_string = re.sub(r'(\?)', r'.{1}', _find_string)
        _find_string = re.sub(r'(\\\\\.\{1\})', r'\?', _find_string)
        _find_string = '^' + _find_string + '$'
        return not (re.match(_find_string, input_string) is None)

    def _compare_tables(self, exp_table, fnd_table, section_name=None,
                        number_precision=None, time_precision=None, data_in_first_column=True):
        """Compares two-dimentional arrays (expected table and found table) and
        returns message for reporting errors.
        """
        self._debug("Compare tables: section_name")
        self._debug(section_name)
        self._debug("Compare tables: exp_table")
        self._debug(exp_table)
        self._debug("Compare tables: fnd_table")
        self._debug(fnd_table)

        _error_message = ''
        if section_name != None:
            section_name = " in '%s' section" % section_name
        else:
            section_name = ''

        # Checking column headers from first rows.
        # 'new_exp_head' and 'new_fnd_head' contain matched headers.
        new_exp_head = []
        new_fnd_head = {}
        for exp_head in exp_table[0]:
            if (fnd_table[0].count(exp_head)) == 0:
                _error_message += "\r\n'%s' column was not found%s." % (exp_head, section_name)
                self._debug(_error_message)
            else:
                new_exp_head.append([exp_head, exp_table[0].index(exp_head)])
                new_fnd_head[exp_head] = fnd_table[0].index(exp_head)

        for fnd_head in fnd_table[0]:
            if (exp_table[0].count(fnd_head)) == 0:
                _error_message += "\r\n'%s' column was not expected%s." % (fnd_head, section_name)
                self._debug(_error_message)

        if data_in_first_column is False:
            new_exp_row = []
            new_fnd_row = {}
            for i in range(1, len(exp_table)):
                new_exp_row.append([i, i])
                new_fnd_row[i] = i
        else:
            # Creating list of row identifiers by taking values from first column.
            exp_items = []
            for i in range(1, len(exp_table)):
                exp_items.append(exp_table[i][0])

            fnd_items = []
            for i in range(1, len(fnd_table)):
                fnd_items.append(fnd_table[i][0])

            # Checking rows by values in first column.
            # 'new_exp_row' and 'new_fnd_row' contain matched rows.
            new_exp_row = []
            new_fnd_row = {}
            for exp_item in exp_items:
                if (fnd_items.count(exp_item)) == 0:
                    _error_message += "\r\n'%s' row was not found%s." % (exp_item, section_name)
                    self._debug(_error_message)
                else:
                    new_exp_row.append([exp_item, exp_items.index(exp_item) + 1])
                    new_fnd_row[exp_item] = fnd_items.index(exp_item) + 1

            for fnd_item in fnd_items:
                if (exp_items.count(fnd_item)) == 0:
                    _error_message += "\r\n'%s' row was not expected%s." % (fnd_item, section_name)
                    self._debug(_error_message)

        # Checking values in mached rows and columns
        for row_name, row_num in new_exp_row:
            for col_name, col_num in new_exp_head:
                exp_value = exp_table[row_num][col_num]
                fnd_value = fnd_table[new_fnd_row[row_name]][new_fnd_head[col_name]]
                if self._simple_match(fnd_value, exp_value):
                    self._info("'%s' column of '%s' row contains value '%s'%s." % (
                    col_name, row_name, fnd_value, section_name))
                elif (exp_value != fnd_value):
                    exp_value = str(exp_value).strip()
                    fnd_value = str(fnd_value).strip()
                    if self._compare_numbers(exp_value, fnd_value, number_precision):
                        pass
                    elif self._compare_times(exp_value, fnd_value, time_precision):
                        pass
                    else:
                        _error_message += "\r\n'%s' was present instead of expected '%s' for '%s' column '%s' row%s." % (
                        fnd_value, exp_value, col_name, row_name, section_name)
                        self._debug(_error_message)

        self._debug(_error_message)
        return _error_message

    def _process_table(self, section_name, expected_values=None,
                       data_in_first_column=None, number_precision=None, time_precision=None):
        """ Process getting or checking a table, specified by section full name (with names of parent headers). """
        _sct_loc = self._find_section_area(section_name)
        self._debug("Section locator:")
        self._debug(_sct_loc)
        if _sct_loc is None:
            self.error_message += "Section '%s' was not found." % (section_name)
            return None
        if not self._is_visible("xpath=" + _sct_loc):
            self.error_message += "Section '%s' was not found." % (section_name)
            return None
        _tbl_loc = self._find_table(section_name, _sct_loc)
        self._debug("Table locator:")
        self._debug(_tbl_loc)
        if _tbl_loc is None or not self._is_visible("xpath=" + _tbl_loc):
            section_value = self.get_text("xpath=" + _sct_loc)
            style_loc = _sct_loc + "//style"
            for style_counter in range(1, 1 + int(self.get_matching_xpath_count(style_loc))):
                style_value = self.get_text(style_loc + "[" + str(style_counter) + "]")
                section_value = section_value.replace(style_value, "")
            section_value = section_value.strip(' \r\n')
            self._debug(section_value)
            if expected_values is None:
                return section_value
            else:
                if isinstance(expected_values, (list, tuple)):
                    expected_values = expected_values[0]
                if section_value.strip() != str(expected_values).strip():
                    self.error_message += "'%s' was present instead of '%s' in section '%s'." % (
                    section_value, str(expected_values), section_name)
                    return None
                else:
                    return section_value

        _actual_table = self._get_table_values(_tbl_loc)

        self._debug("Expected table:")
        self._debug(expected_values)
        self._debug("Actual_table:")
        self._debug(_actual_table)

        if expected_values is None:
            return _actual_table

        if isinstance(expected_values, (str, unicode)):
            expected_values = tuple([expected_values])

        if len(expected_values) > 0:
            _expected_table = self._convert_tuple_to_table(expected_values)
            self._debug("Expected table:")
            self._debug(_expected_table)
            self._debug("Actual_table:")
            self._debug(_actual_table)
            self.error_message += self._compare_tables(_expected_table,
                                                       _actual_table, section_name, number_precision=number_precision,
                                                       time_precision=time_precision,
                                                       data_in_first_column=data_in_first_column)

        return _actual_table

    def _select_chart_option(self, option, chart_number, timeout=60):
        chart_number = int(chart_number)

        self._debug("----- Select chart option (%s) for chart %s -----\r\n" % (option, chart_number))

        _options_link_loc = "//a[contains(@onclick, 'ChartOptions')]"

        # waiting for 'Columns...' link
        _timer_start = time.time()
        while (time.time() - _timer_start) < timeout:
            if int(self.get_matching_xpath_count(_options_link_loc)) > 0:
                break
            else:
                time.sleep(1)

        option_list = option.split(":")
        if len(option_list) > 1:
            _section_loc = self._find_section_area(option_list[0])
            if _section_loc is None:
                raise guiexceptions.GuiValueError("'%s' section was not found." % \
                                                  (option_list[0],))
            _options_link_loc = _section_loc + _options_link_loc
            option = option_list[1].strip()

        if int(self.get_matching_xpath_count(_options_link_loc)) < 1:
            raise guiexceptions.GuiValueError("'Chart Options' link was not found.")

        self.click_element("xpath=(%s)[%s]" % (_options_link_loc, chart_number), "don't wait")

        # check if dialog is open
        _options_dlg_loc = "//div[@id='chart_option_dlg']"
        if not self._is_visible(_options_dlg_loc):
            raise guiexceptions.GuiValueError("Chart Options dialog was not found.")

        _option_loc = "%s//*[normalize-space(text())='%s']" % (_options_dlg_loc, option)
        if int(self.get_matching_xpath_count(_option_loc)) == 0:
            _option_loc = "%s//*[contains(text(), '%s')]" % (_options_dlg_loc, option)
        if int(self.get_matching_xpath_count(_option_loc)) == 0:
            raise guiexceptions.GuiValueError("Option '%s' was not found in chart %s" % (option, chart_number))

        self.click_element(_option_loc, "don't wait")

        self.click_button("xpath=//button[text()='Save']", "don't wait")
        self._debug("\r\n----- (Select chart options) -----")

    def _select_columns(self, section_name, columns, clear_others=False, timeout=60):
        if columns is None:
            return False

        _done_button = "xpath=//button[text()='Done']"

        self._debug("----- Select columns (%s) in section '%s' -----\r\n" % (str(columns), str(section_name)))

        _section_loc = self._find_section_area(section_name)
        self._debug("_section_loc: %s" % _section_loc)
        if _section_loc is None:
            raise guiexceptions.GuiValueError("'%s' section was not found." % \
                                              (section_name,))
        _columns_link_loc = _section_loc + self.TABLE_COLUMNS_LINK_SELECTOR
        self._debug("_columns_link_loc: %s" % _columns_link_loc)

        # waiting for 'Columns...' link
        _timer_start = time.time()
        while (time.time() - _timer_start) < timeout:
            if int(self.get_matching_xpath_count(_columns_link_loc)) > 0:
                break
            else:
                time.sleep(1)

        if int(self.get_matching_xpath_count(_columns_link_loc)) < 1:
            raise guiexceptions.GuiValueError("'Columns' link was not found for section '%s'." % \
                                              (section_name,))

        self._debug("Clicking _columns_link_loc")
        self.click_element(_columns_link_loc, "don't wait")

        # check if dialog is open
        _columns_dlg_loc = "//div[@id='yui_table_options_dlg']"
        try:
            self.element_should_be_visible(_columns_dlg_loc)
        except:
            raise guiexceptions.GuiValueError("Table columns dialog was not found.")

        self._debug("Dialog is open.")

        # get list of columns
        columns_list = map(lambda x: x.strip(), columns.split(','))
        columns_not_found = list(columns_list)
        self._debug("Columns: " + str(columns_list))

        _columns_tbody_loc = _columns_dlg_loc + "//table[1]/tbody"

        _prev_speed = self.set_selenium_speed(0)
        self._debug("Selenium speed was: %s" % _prev_speed)

        _select_all_columns = None
        if "all" in columns_list:
            _select_all_columns = True
            self._debug("Selecting all columns.")
        elif columns == '':
            _select_all_columns = False
            self._debug("Removing all columns.")

        if _select_all_columns is not None:
            _columns_loc = _columns_tbody_loc + "//input[@name='table_options_columns[]' and @type='checkbox']"
            _columns_count = int(self.get_matching_xpath_count(_columns_loc))
            self._debug("_columns_count: %s" % _columns_count)
            for _col in range(1, 1 + _columns_count):
                _input_loc = "xpath=(" + _columns_loc + ")[" + str(_col) + "]"
                _column_state = self._is_checked(_input_loc)
                if _column_state != _select_all_columns:
                    self.click_element(_input_loc, "don't wait")
        else:
            # going through rows on the dialog
            _columns_rows_loc = _columns_tbody_loc + "/tr"
            _columns_rows_count = int(self.get_matching_xpath_count(_columns_rows_loc))
            columns_not_found = list(columns_list)
            for _row in range(1, 1 + _columns_rows_count):
                self._debug("_row: %s" % _row)
                _input_loc = _columns_rows_loc + "[" + str(
                    _row) + "]//input[@name='table_options_columns[]' and @type='checkbox']"
                _column_state = self._is_checked(_input_loc)
                self._debug("_column_state: %s" % _column_state)

                # suppose checkbox label was specified
                _column_label = self.get_text(_columns_rows_loc + "[" + str(_row) + "]//label[@for]")
                self._debug("_column_label: %s" % _column_label)
                _column_found = False
                for _column in columns_list:
                    self._debug("_column: %s" % _column)
                    self._debug("_simple_match: %s" % self._simple_match(_column_label, _column))
                    if self._simple_match(_column_label, _column):
                        if not _column_state:
                            self.click_element("xpath=" + _input_loc, "don't wait")
                        try:
                            columns_not_found.remove(_column)
                        except:
                            pass
                        self._debug("columns_not_found: %s" % columns_not_found)
                        _column_found = True
                        break
                if _column_found:
                    continue

                # suppose checkbox id was specified
                _column_id = self.get_element_attribute(_input_loc + "@id")
                self._debug("_column_id: %s" % _column_id)
                if _column_id in columns_list:
                    if not _column_state:
                        self.click_element("xpath=" + _input_loc, "don't wait")
                    try:
                        columns_not_found.remove(_column_id)
                    except:
                        pass
                    self._debug("columns_not_found: %s" % columns_not_found)
                    continue

                # clear checkbox if the column is not needed
                if clear_others and _column_state:
                    self.click_element("xpath=" + _input_loc, "don't wait")

            self._debug("columns_not_found: %s" % columns_not_found)
            if len(columns_not_found) > 0:
                _absent_columns = ''
                for _column in columns_not_found:
                    _absent_columns += "'%s', " % (_column,)
                self.error_message += "Columns %s were not found on page '%s'.\r\n\t" \
                                      % (_absent_columns, self.get_location())

        self.set_selenium_speed(_prev_speed)

        self._debug("Clicking 'Done' button.")
        self.click_button(_done_button, "don't wait")
        self._debug("\r\n----- (Select columns) -----")

    def _search_row(self, section_name, row_name=None, timeout=60):
        if row_name is None:
            return False

        self._debug("Searching row '%s' in section '%s'" % (str(row_name), str(section_name)))

        _section_loc = self._find_section_area(section_name)
        self._debug("_section_loc: %s" % _section_loc)
        if _section_loc is None:
            self.error_message += "Section '%s' was not found on page '%s'.\r\n" \
                                  % (section_name, self.get_location())
            return False
        _search_field_loc = _section_loc + "//input[contains(@id, 'search_field')]"

        if int(self.get_matching_xpath_count(_search_field_loc)) < 1:
            raise guiexceptions.GuiValueError(
                "'Search' field was not found for section '%s'.\nLocator: '%s'" % \
                (section_name, _search_field_loc))

        self.input_text(_search_field_loc, row_name)

        _search_button_loc = _section_loc + "//input[contains(@id, 'search-button')]"
        self.click_element(_search_button_loc, "don't wait")

        _tbl_loc = self._find_table(section_name)
        _timer_start = time.time()
        while (time.time() - _timer_start) < timeout:
            if _tbl_loc is None:
                time.sleep(1)
                _tbl_loc = self._find_table(section_name)
            else:
                break
        if _tbl_loc is None:
            self.error_message += "Row '%s' was not found on page '%s'.\r\n" \
                                  % (row_name, self.get_location())
            return False

    def _select_items_display(self, section_name, items_display=None, timeout=60):
        if items_display is None:
            return False

        self._debug(
            "Selecting '%s' number of items to display in '%s' section." % (str(items_display), str(section_name)))

        _section_loc = self._find_section_area(section_name)
        _display_sel_loc = _section_loc + "//*[contains(@id, 'display-rows')]//select"

        # waiting for the field
        _timer_start = time.time()
        while (time.time() - _timer_start) < timeout:
            if int(self.get_matching_xpath_count(_display_sel_loc)) > 0:
                break
            else:
                time.sleep(1)

        self.select_from_list(_display_sel_loc, str(items_display))

        # waiting for enabling the field
        _timer_start = time.time()
        while (time.time() - _timer_start) < timeout:
            if int(self.get_matching_xpath_count(_display_sel_loc + "/self::*[not(@disabled='disabled')]")) > 0:
                break
            else:
                time.sleep(1)

        if not int(self.get_matching_xpath_count(_display_sel_loc + "/self::*[not(@disabled='disabled')]")) > 0:
            self.error_message += "Enabled 'Items Displayed' was not found.\r\n"

    def _open_details(self, section_name, row_name):
        self._search_row(section_name, row_name)
        _table_loc = self._find_table(section_name)
        _return_list = self._process_table(section_name)
        if _return_list is None:
            return None
        _row = False
        for i in range(len(_return_list)):
            if _return_list[i][0].strip() == row_name:
                _row = i
                break
        if not _row:
            raise guiexceptions.GuiValueError("'%s' row was not found in section '%s'." % \
                                              (row_name, section_name,))
        self.click_link(
            "xpath=((" + _table_loc + "/tbody[not(contains(@style,'display: none'))]/tr)[" + str(_row) + "]/td)[1]//a")

    def _follow_link_in_table(self, section_name, row_name, col_name=None):
        _table_loc = self._find_table(section_name)
        _cell_loc = self._get_table_cell_loc(_table_loc, row_name, col_name)
        _link_loc = _cell_loc + "//a"
        _link_count = int(self.get_matching_xpath_count(_link_loc))
        if _link_count < 1:
            raise guiexceptions.GuiValueError("Link was not found for '%s' row '%s' column in section '%s'." % \
                                              (row_name, col_name, section_name,))
        else:
            self.click_link("xpath=" + _link_loc)

    def _follow_link_in_chart(self, section_name, link_name):
        _sct_loc = self._find_section_area(section_name)
        self._debug("Section locator:")
        self._debug(_sct_loc)
        if _sct_loc is None:
            self.error_message += "Section '%s' was not found." % (section_name)
            return None

        _link_loc = "%s//a[normalize-space(text())='%s']" % (_sct_loc, link_name)
        if int(self.get_matching_xpath_count(_link_loc)) == 0:
            _link_loc = "%s//a[contains(text(), '%s')]" % (_sct_loc, link_name)
        if int(self.get_matching_xpath_count(_link_loc)) == 0:
            raise guiexceptions.GuiValueError("Link '%s' was not found in section %s" % (link_name, section_name))

        self.click_link("xpath=" + _link_loc)

    def _chart_presence(self, section_name):
        _sct_loc = self._find_section_area(section_name)
        self._debug("Section locator:")
        self._debug(_sct_loc)
        if _sct_loc is None:
            self.error_message += "Section '%s' was not found." % (section_name)
            return False

        _chart_loc = "%s//img" % (_sct_loc)
        if int(self.get_matching_xpath_count(_chart_loc)) == 0:
            return False

        return self._is_visible("xpath=" + _chart_loc)

    def _export(self, section_name, timeout=60):
        self._debug("Exporting section '%s'" % str(section_name))

        _section_loc = self._find_section_area(section_name)
        if _section_loc is None:
            raise ValueError("Section '%s' was not found." % section_name)
        _export_link_loc = _section_loc + self.SECTION_EXPORT_LINK_SELECTOR

        # waiting for 'Export' link
        for i in range(timeout):
            if int(self.get_matching_xpath_count(_export_link_loc)) > 0:
                break
            else:
                time.sleep(1)

        if int(self.get_matching_xpath_count(_export_link_loc)) < 1:
            raise guiexceptions.GuiValueError("'Export' link was not found for section '%s'." % \
                                              (section_name,))

        _title = self.get_text("xpath=//*[@id='report_title']/h1").strip()

        _start_time = time.strftime("%Y-%m-%d %H:%M:%S")
        self.click_element("xpath=" + _export_link_loc, "don't wait")

        sections = section_name.split(" > ")

        filename = WaitForDownload(self.dut).wait_for_download(_title + " " + (sections[-1]).strip(),
                                                               start_time=_start_time, timeout=120)
        self._info("CSV file was saved as %s" % filename)
        return filename

    def _pdf(self):
        self._debug("Saving section '%s' in PDF format.")

        _pdf_link_loc = "//a[contains(@href, 'javascript:printReport()')]"

        if int(self.get_matching_xpath_count(_pdf_link_loc)) < 1:
            raise guiexceptions.GuiValueError("'PDF' link was not found.")

        _title = self.get_text("xpath=//*[@id='report_title']/h1").strip()

        _start_time = time.strftime("%Y-%m-%d %H:%M:%S")
        self.click_element("xpath=" + _pdf_link_loc, "don't wait")

        filename = WaitForDownload(self.dut).wait_for_download(_title,
                                                               start_time=_start_time, timeout=120)
        self._info("PDF file was saved as %s" % filename)
        return filename

    def _get_value(self, section_name, _return_list, row, column):
        _row = 0
        for _row_num in range(1, len(_return_list)):
            if str(_return_list[_row_num][0]).strip() == row.strip():
                _row = _row_num
                break
        if _row < 1:
            try:
                _row = int(row)
            except:
                pass
        if _row < 1 or _row >= len(_return_list):
            self.error_message += "Row '%s' was not found in '%s' table." % (row, section_name)
            return None

        _col = 0
        for _col_num in range(1, len(_return_list[0])):
            if str(_return_list[0][_col_num]).strip().find(column.strip()) > -1:
                _col = _col_num
                break
        if _col < 1:
            self.error_message += "Column '%s' was not found in '%s' table." % (column, section_name)
            return None

        _found_value = str(_return_list[_row][_col])
        return _found_value

    def _check_value(self, section_name, _return_list, row, column, criterion):
        self._debug("section_name: %s" % section_name)
        self._debug("_return_list: %s" % _return_list)
        self._debug("row: %s" % row)
        self._debug("column: %s" % column)
        self._debug("criterion: %s" % criterion)

        _found_value = self._get_value(section_name, _return_list, row, column)
        self._debug("_found_value: %s" % _found_value)

        if str(criterion)[0] != '<' and str(criterion)[0] != '>' and str(criterion)[0:2] != '==':
            if str(criterion)[0] != '=':
                criterion = "='%s'" % criterion
            else:
                criterion = "=='%s'" % criterion
            _found_value = "'%s'" % _found_value
            self._debug("criterion: %s" % criterion)
            self._debug("_found_value: %s" % _found_value)

        if _found_value is not None:
            try:
                if eval(_found_value + criterion):
                    return True
            except:
                pass
            # compare as numbers
            _found_value = re.search("([\-\d\.]+)", _found_value).groups()[0]
            try:
                if eval(_found_value + criterion):
                    return True
            except:
                pass

        self.error_message += "'%s' column for '%s' row in '%s' table had value %s, which does not satisfy %s criterion." % (
        column, row, section_name, _found_value, criterion)
        return False

    def _check_cell_value(self, section_name, row, column, criterion):
        self._debug("section_name: %s" % section_name)
        self._debug("row: %s" % row)
        self._debug("column: %s" % column)
        self._debug("criterion: %s" % criterion)

        _tbl_loc = self._find_table(section_name)
        if _tbl_loc is None:
            self.error_message += "Table was not found in section '%s'." % (section_name,)
            return False
        _found_value = self._get_table_cell_value(_tbl_loc, row, column)
        self._debug("_found_value: %s" % _found_value)

        if str(criterion)[0] != '<' and str(criterion)[0] != '>' and str(criterion)[0:2] != '==':
            if str(criterion)[0] == '=':
                criterion = "='%s'" % criterion
            else:
                criterion = "=='%s'" % criterion
            _found_value = "'%s'" % _found_value
            self._debug("criterion: %s" % criterion)
            self._debug("_found_value: %s" % _found_value)

        if _found_value is not None:
            try:
                if eval(_found_value + criterion):
                    return True
            except:
                pass
            # compare as numbers
            if _found_value is not None:
                _found_value = re.search("([\-\d\.]+)", _found_value).groups()[0]
                try:
                    if eval(_found_value + criterion):
                        return True
                except:
                    pass

        self.error_message += "'%s' column for '%s' row in '%s' table had value %s, which does not satisfy %s criterion." % (
        column, row, section_name, _found_value, criterion)
        return False
