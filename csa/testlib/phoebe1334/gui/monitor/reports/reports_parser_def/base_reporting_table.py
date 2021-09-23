#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/phoebe1350/gui/monitor/reports/reports_parser_def/base_reporting_table.py#1 $ $DateTime: 2020/01/06 01:25:43 $ $Author: saurgup5 $

import re
import tempfile

from common.gui.decorators import set_speed
from common.gui.guiexceptions import ConfigError
from common.util.misc import Misc
from sal.clients.crawler import ApplianceCrawler

from data_load_monitor import wait_until_data_loaded, NoDataFound


ITEMS_DISPLAYED_OPTION = 'items_displayed'

normalize = lambda s: re.sub(r'\W', '_', s.lower().strip(':'))


class DataTransformOptions(object):
    def __init__(self, use_normalize, first_column_as_key,
                 result_as_dictionary):
        self._use_normalize = False
        self._first_column_as_key = False
        self._result_as_dictionary = False
        self.result_as_dictionary = result_as_dictionary
        self.first_column_as_key = first_column_as_key
        self.use_normalize = use_normalize

    @property
    def first_column_as_key(self):
        return self._first_column_as_key
    @first_column_as_key.setter
    def first_column_as_key(self, value):
        if value is True:
            self._use_normalize = True
            self._result_as_dictionary = True
        if self._result_as_dictionary is True:
            self._first_column_as_key = True
        else:
            self._first_column_as_key = value

    @property
    def use_normalize(self):
        return self._use_normalize
    @use_normalize.setter
    def use_normalize(self, value):
        if any((self._first_column_as_key, self._result_as_dictionary)):
            self._use_normalize = True
        else:
            self._use_normalize = value

    @property
    def result_as_dictionary(self):
        return self._result_as_dictionary
    @result_as_dictionary.setter
    def result_as_dictionary(self, value):
        if value is True:
            self._first_column_as_key = True
        if self._first_column_as_key is True:
            self._result_as_dictionary = True
        else:
            self._result_as_dictionary = value

    def __unicode__(self):
        return 'result_as_dictionary: {0}\nuse_normalize: {1}\n'\
               'first_column_as_key: {2}'.\
                format(self.result_as_dictionary, self.use_normalize,
                       self.first_column_as_key)
    __str__ = __unicode__


ALL_TABLES_ROOT = ""

class BaseReportingTable(object):
    """Base abstract class designed to interact with email reporting tables on
    Reporting pages.
    """
    ALL_ROWS = lambda self: \
                "{0}/tbody[not(contains(@style, 'display: none'))]"\
                "/tr[td]".format(self._get_xpath_root())
    CELL_BY_COL_ROW = lambda self, col_idx, row_idx, use_any_cell = False: \
       "{0}[{1}]/*[not(string-length()=0)][{2}]".\
       format(self.ALL_ROWS(), row_idx, col_idx) \
       if use_any_cell \
       else "{0}[{1}]/td[not(string-length()=0)][{2}]".\
       format(self.ALL_ROWS(), row_idx, col_idx)
    TITLED_CELL_BY_COL_ROW = \
          lambda self, col_idx, row_idx, use_any_cell = False: \
         "{0}//*[@title]".format(self.CELL_BY_COL_ROW(col_idx, row_idx,
                                                      use_any_cell))
    TITLE_ATTR_BY_COL_ROW = \
         lambda self, col_idx, row_idx, use_any_cell = False: \
         "{0}@title".format(self.TITLED_CELL_BY_COL_ROW(col_idx, row_idx,
                                                        use_any_cell))
    HEADER_COLS = lambda self: "{0}//tr/th".format(self._get_xpath_root())
    COL_HEADER_BY_IDX = lambda self, idx: "{0}[{1}]".\
                                        format(self.HEADER_COLS(), idx)
    COLS_IN_ROW = lambda self, row_idx: "{0}[{1}]/td[not(string-length()=0)]".\
                                        format(self.ALL_ROWS(), row_idx)
    HEADERS_IN_ROW = lambda self, row_idx: "{0}[{1}]/th[not(string-length()=0)]".\
                                        format(self.ALL_ROWS(), row_idx)
    ITEMS_IN_ROW = lambda self, row_idx: "{0}[{1}]/*[not(string-length()=0)]".\
                                        format(self.ALL_ROWS(), row_idx)
    LINK_BY_COL_ROW_IDX = lambda self, col_idx, row_idx, use_any_cell = False: \
        "{0}//a".format(self.CELL_BY_COL_ROW(col_idx, row_idx, use_any_cell))
    EXPORT_LINK = lambda self: "{0}/ancestor::div[starts-with(@id, 'ss_')]"\
        "//span[normalize-space()='Export...' and "\
        "starts-with(@onclick, 'SectionExport(')]".format(self._get_xpath_root())
    EXPORT_LINK_DEST_URL = lambda self: "{0}@onclick".format(self.EXPORT_LINK())
    ITEMS_COUNT_COMBO = lambda self: "{0}/ancestor::div[starts-with(@id, 'ss_')]"\
                                     "//select[starts-with(@name, 'rows_ss_')]".\
                                     format(self._get_xpath_root())

    def __init__(self, gui_common, name):
        self.gui = gui_common
        if not (name in self.get_available_table_names() or \
           any(map(lambda x: name.startswith(x), self.get_special_name_prefixes()))):
                raise ValueError('There is no such table "{0}" in class "{1}"'.\
                                 format(name, self.__class__.__name__))
        self._name = name

    @property
    def name(self):
        return self._name

    @classmethod
    def get_available_table_names(cls):
        return []

    @classmethod
    def get_special_name_prefixes(cls):
        return []

    def _get_xpath_root(self):
        return ALL_TABLES_ROOT

    def _get_row_idx_by_cell_value(self, col_idx, cell_value, use_any_cell=False):
        rows_count = int(self.gui.get_matching_xpath_count(
                                                    self.ALL_ROWS()))
        for row_idx in xrange(1, 1 + rows_count):
            current_cell_value = self.gui.get_text('xpath=%s' % self.CELL_BY_COL_ROW(
                                        col_idx, row_idx, use_any_cell)).strip()
            if current_cell_value.startswith(cell_value):
                return row_idx
        raise NoDataFound('The table "{0}" does not contain value "{1}" '\
                          'in column #"{2}"'.format(self._name, cell_value,
                                                    col_idx))

    def _get_col_idx_by_name(self, col_name):
        headers = self._get_headers()
        if col_name in headers:
            return headers.index(col_name) + 1
        else:
            raise NoDataFound('The table "{0}" does not contain column '\
                              'named "{1}"'.format(self._name, col_name))

    def _get_headers(self):
        headers_count = int(self.gui.get_matching_xpath_count(
                                                self.HEADER_COLS()))
        headers = []
        for header_idx in xrange(1, 1 + headers_count):
            header_value = self.gui.get_text(
                                self.COL_HEADER_BY_IDX(header_idx)).strip()
            headers.append(header_value)
        print '>>> headers', headers
        return headers

    def get_available_options_names(self):
        """Override this method in subclasses
        and implement option(s) setting in set_options
        method if necessary."""
        return [ITEMS_DISPLAYED_OPTION]

    def _set_displayed_items(self, items_count):
        if not self.gui._is_element_present(self.ITEMS_COUNT_COMBO()):
            raise ConfigError('The table "{0}" does not contain option to set '\
                              'items count'.format(self._name))
        available_items = self.gui.get_list_items(self.ITEMS_COUNT_COMBO())
        for item in available_items:
            if items_count.lower() == item.lower():
                self.gui.select_from_list(self.ITEMS_COUNT_COMBO(), item)
                wait_until_data_loaded(self.gui)
                return
        raise ValueError('There are no "{0}" option. Available options are:\n{1}'.\
                         format(items_count, available_items))

    def set_options(self, options):
        available_options = set(self.get_available_options_names())
        given_options = set(options.keys())
        if not given_options.issubset(available_options):
            raise ValueError('There are no such option(s):\n{0}\n'\
                'available for the table "{1}". Available options:\n{2}"'.\
                format(list(given_options - available_options),
                       self._name, list(available_options)))
        if ITEMS_DISPLAYED_OPTION in options:
            self._set_displayed_items(options[ITEMS_DISPLAYED_OPTION])

    @set_speed(0, 'gui')
    def export_as(self, dest_path=None):
        if dest_path is None:
            dest_path = tempfile.mkstemp('.csv')[1]
        if not self.gui._is_element_present(self.EXPORT_LINK()):
            raise ConfigError('The table "{0}" does not contain export option')
        link = self.gui.get_element_attribute(self.EXPORT_LINK_DEST_URL())
        link = re.search(r'SectionExport\(\'([^\']+)', link).groups()[0]
        print '>>> export link: {0}'.format(link)
        password = Misc(None, None).get_admin_password(self.gui.dut)
        downloader = ApplianceCrawler(self.gui.dut, 'admin', password)
        file_in_memory = downloader.download(link)
        try:
            with open(dest_path, 'wb') as dest_file:
                dest_file.write(file_in_memory.read())
        finally:
            file_in_memory.close()
        return dest_path


if __name__ == '__main__':
    opts = DataTransformOptions(use_normalize=False, first_column_as_key=True,
                                result_as_dictionary=False)
    print opts
