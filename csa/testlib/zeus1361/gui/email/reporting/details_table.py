# $Id: //prod/main/sarf_centos/testlib/zeus1360/gui/email/reporting/details_table.py#1 $ $DateTime: 2020/03/05 19:45:32 $ $Author: sarukakk $

import time

import common.gui.guiexceptions as guiexceptions
from common.util.sarftime import CountDownTimer

import report_table

# Detail tables attributes dictionary.
# Item format is:
# '<table_name_in_gui>': ((<tuple_with_tab_names_to_be_passed_to_navigate_to_method>),
# (<tuple_with_table_coordinates_in_gui_taken_from_"id=ss_0_%d_%d"_parameter>))
TABLE_NAMES = {'User Mail Flow Details': (('Email', 'Reporting', 'Internal Users'),
                                          (2, 0)),
               'Incoming Mail Details': (('Email', 'Reporting', 'Incoming Mail'),
                                          (2, 0)),
               'Outgoing Destinations Detail': (('Email', 'Reporting', 'Outgoing Destinations'),
                                          (1, 0)),
               'Sender Details': (('Email', 'Reporting', 'Outgoing Senders'),
                                          (1, 0)),
               'Virus Types Detail': (('Email', 'Reporting', 'Virus Types'),
                                          (1, 0)),
               'Outgoing TLS Connections Details': (('Email', 'Reporting', 'TLS Connections'),
                                          (5, 0)),
               'Incoming TLS Connections Details': (('Email', 'Reporting', 'TLS Connections'),
                                          (2, 0)),
               'Incoming Content Filter Matches': (('Email', 'Reporting', 'Content Filters'),
                                          (1, 0)),
               'Outgoing Content Filter Matches': (('Email', 'Reporting', 'Content Filters'),
                                          (1, 1)),
               'Threat Details': (('Email', 'Reporting', 'Outbreak Filters'),
                                          (1, 0)),
               'Threat Summary': (('Email', 'Reporting', 'Outbreak Filters'),
                                          (0, 1)),
               'DLP Incident Details': (('Email', 'Reporting', 'DLP Incidents'),
                                          (2, 0)),
               'Summary of External Threat Feeds': (('Email', 'Reporting', 'External Threat Feeds'),
                                          (0, 1)),
               'Summary of External Threat Feed Sources by incoming mail connections': (('Email', 'Reporting', 'External Threat Feeds'),
                                          (2, 1))}

COLUMN_DIV_BY_NAME = lambda coords, column_name: \
                    '%s//div[@id=\'ss_0_%d_%d\']//table[@summary]'\
                    '/thead/tr/th[starts-with(.//text(), \'%s\')]//div'\
                     % (report_table.REPORT_TABLE, coords[0], coords[1], column_name)

RESULT_HEADS = lambda coords: '%s//div[@id=\'ss_0_%d_%d\']//table[@summary]/thead/tr/th'\
                                % (report_table.REPORT_TABLE, coords[0], coords[1])
RESULT_HEADS1 = lambda coords: '%s//div[@id=\'ss_0_%d_%d\']//table[@summary]/thead/tr[2]/th'\
                                % (report_table.REPORT_TABLE, coords[0], coords[1])
HEADER_CELL_BY_IDX = lambda coords, idx: '%s//div[@id=\'ss_0_%d_%d\']//'\
                                        'table[@summary]/thead/tr/th[%d]'\
                                % (report_table.REPORT_TABLE, coords[0], coords[1], idx)
HEADER_CELL_BY_IDX1 = lambda coords, idx: '%s//div[@id=\'ss_0_%d_%d\']//'\
                                        'table[@summary]/thead/tr[2]/th[%d]'\
                                % (report_table.REPORT_TABLE, coords[0], coords[1], idx)
CONTENT_CELL_BY_IDX = lambda coords, col_idx, row_idx: '%s//div[@id=\'ss_0_%d_%d\']'\
                                '//table[@summary]/tbody[2]/tr[%d]/td[%d]'\
                                % (report_table.REPORT_TABLE, coords[0], coords[1], row_idx, col_idx)

CONTENT_CELL_LINK = lambda coords, col_idx, row_idx: '%s//div[@id=\'ss_0_%d_%d\']'\
                                '//table[@summary]/tbody[2]/tr[%d]/td[%d]/div/span/a'\
                                % (report_table.REPORT_TABLE, coords[0], coords[1], row_idx, col_idx)

HEADER_CELL_BY_IDX_TEXT = lambda coords, idx, text: '%s//div[@id=\'ss_0_%d_%d\']//'\
                                'table[@summary]/thead/tr/th[%d][starts-with(.//text(), \'%s\')]'\
                                        % (report_table.REPORT_TABLE, coords[0], coords[1], idx, text)

TABLE_CONTENT_ROWS = lambda coords: '%s//div[@id=\'ss_0_%d_%d\']//'\
                            'table[@summary]/tbody[2]/tr' % \
                            (report_table.REPORT_TABLE, coords[0], coords[1])

COLUMNS_LINK = lambda coords: '%s//td[@id=\'ss_0_%d_%d-links\']/span[contains(@onclick,'\
                    '\'showTableOptionsDlg\')]' % \
                    (report_table.REPORT_TABLE, coords[0], coords[1])
COLUMNS_DLG = '//div[@id=\'yui_table_options_dlg_c\']'
COLUMNS_CHECKBOX_BY_NAME = lambda cb_name: '%s//tr[.//text()=\'%s\']//input[@type=\'checkbox\']' % \
                            (COLUMNS_DLG, cb_name)
COLUMNS_CHECKBOX_BY_IDX = lambda idx: '%s//tr[%d]//input[@type=\'checkbox\']' % \
                            (COLUMNS_DLG, idx)
COLUMN_CHECKBOXES = '%s//input[@type=\'checkbox\']' % (COLUMNS_DLG,)
COLUMNS_DLG_DONE_BUTTON = '%s//button[@type=\'button\' and text()=\'Done\']' % \
                        (COLUMNS_DLG,)



class DetailsTableParameters(report_table.CommonReportTableParameters):
    """Detail table parameters are equal to common parameters
    """
    pass


class DetailsTable(report_table.ReportTable):
    """The class represents footer details tables on email reporting pages
    """

    def _get_column_index(self,
                          table_name,
                          column_name,
                          table_parameters=None,
                          should_navigate_to_table=True):
        table_path, table_coords = self._extract_table_attributes(table_name)
        if should_navigate_to_table:
            self._navigate_to_table(table_path, table_parameters)

        content_rows = TABLE_CONTENT_ROWS(table_coords)
        self._wait_for_table_load(content_rows)

        heads_locator = RESULT_HEADS(table_coords)
        cells_count = int(self._wui.get_matching_xpath_count(heads_locator))
        for index in range(1, cells_count + 1):
            if self._wui._is_element_present(HEADER_CELL_BY_IDX_TEXT(table_coords,
                                                                     index,
                                                                     column_name)):
                return index
        raise ValueError('You should provide correct column name to get index from')

    def _drag_column(self,
                     table_name,
                     source_column_name,
                     target_column_name,
                     table_parameters=None,
                     should_navigate_to_table=True):
        table_path, table_coords = self._extract_table_attributes(table_name)
        if should_navigate_to_table:
            self._navigate_to_table(table_path, table_parameters)

        source_column_div = COLUMN_DIV_BY_NAME(table_coords,
                                               source_column_name)
        target_column_div = COLUMN_DIV_BY_NAME(table_coords,
                                               target_column_name)

        self._wait_for_table_load(source_column_div)
        if not self._wui._is_element_present(source_column_div):
            raise ValueError('You should provide correct source column name')
        if not self._wui._is_element_present(target_column_div):
            raise ValueError('You should provide correct target column name')

        self._wui._drag_and_drop_to_object(source_column_div,
                                           target_column_div)

    def _sort_column(self,
                     table_name,
                     column_name,
                     table_parameters=None,
                     should_navigate_to_table=True):
        table_path, table_coords = self._extract_table_attributes(table_name)
        if should_navigate_to_table:
            self._navigate_to_table(table_path, table_parameters)

        column_div = COLUMN_DIV_BY_NAME(table_coords,
                                        column_name)
        self._wait_for_table_load(column_div)

        if not self._wui._is_element_present(column_div):
            raise ValueError('You should provide correct column name to sort it')

        self._wui._click_radio_button(column_div)

        content_rows = TABLE_CONTENT_ROWS(table_coords)
        self._wait_for_table_load(content_rows)

    def _show_columns(self,
                      table_name,
                      columns='all',
                      table_parameters=None,
                      should_navigate_to_table=True):
        table_path, table_coords = self._extract_table_attributes(table_name)

        content_rows = TABLE_CONTENT_ROWS(table_coords)
        if should_navigate_to_table:
            self._navigate_to_table(table_path, table_parameters)
        self._wait_for_table_load(content_rows)

        self._wui.click_button(COLUMNS_LINK(table_coords), 'don\'t wait')
        timer = CountDownTimer(5).start()
        while timer.is_active():
            if self._wui._is_element_present(COLUMNS_DLG):
                break
            time.sleep(1.0)

        col_count = int(self._wui.get_matching_xpath_count(COLUMN_CHECKBOXES))
        map(lambda x: self._wui._unselect_checkbox(COLUMNS_CHECKBOX_BY_IDX(x)),
            range(1, col_count + 1))

        if isinstance(columns, basestring) and columns.lower() == 'all':
            map(lambda x: self._wui._select_checkbox(COLUMNS_CHECKBOX_BY_IDX(x)),
                range(1, col_count + 1))
        elif isinstance(columns, list) or isinstance(columns, tuple):
            map(lambda x: self._wui._select_checkbox(COLUMNS_CHECKBOX_BY_NAME(x)),
                columns)
        else:
            raise ValueError('Incorrect value of "columns" parameter (%s) is passed'\
                             % (columns,))

        self._wui.click_button(COLUMNS_DLG_DONE_BUTTON, 'don\'t wait')
        self._wait_for_table_load(content_rows)

    def _get_data(self,
                  table_name,
                  table_parameters=None,
                  should_navigate_to_table=True):
        table_path, table_coords = self._extract_table_attributes(table_name)

        content_rows = TABLE_CONTENT_ROWS(table_coords)
        if should_navigate_to_table:
            self._navigate_to_table(table_path, table_parameters)
        self._wait_for_table_load(content_rows)

        return self._extract_rows_columns(table_coords, content_rows, table_name)

    def _get_report_get_content_link(self,
                  table_name,
                  table_parameters=None,
                  should_navigate_to_table=True):
        table_path, table_coords = self._extract_table_attributes(table_name)

        content_rows = TABLE_CONTENT_ROWS(table_coords)
        if should_navigate_to_table:
            self._navigate_to_table(table_path, table_parameters)
        self._wait_for_table_load(content_rows)

        return self._extract_rows_columns_link(table_coords, content_rows, table_name)

    def _extract_rows_columns(self, table_coords, content_rows, table_name):
        cells_count_in_row = int(self._wui.get_matching_xpath_count(RESULT_HEADS(table_coords)))
        cells_count_in_col = int(self._wui.get_matching_xpath_count(content_rows))

        result_dict = {}
        if (table_name == "Outgoing Destinations Detail"):
            print "Outgoing Destinations Detail"
            cells_count_in_row = int(self._wui.get_matching_xpath_count(RESULT_HEADS1(table_coords)))
        for row_idx in range(1, cells_count_in_row + 1):
            if (table_name == "Outgoing Destinations Detail"):
                 col_name = self._wui.get_text(HEADER_CELL_BY_IDX1(table_coords,
                                                                  row_idx))
            else:
                 col_name = self._wui.get_text(HEADER_CELL_BY_IDX(table_coords,
                                                                  row_idx))
            cell_values = []
            for col_idx in range(1, cells_count_in_col + 1):
                cell_values.append(self._wui.get_text(CONTENT_CELL_BY_IDX(table_coords,
                                                                               row_idx,
                                                                               col_idx)))
            result_dict[col_name] = cell_values
        return result_dict

    def _extract_rows_columns_link(self, table_coords, content_rows, table_name):
        cells_count_in_row = int(self._wui.get_matching_xpath_count(RESULT_HEADS(table_coords)))
        cells_count_in_col = int(self._wui.get_matching_xpath_count(content_rows))

        result_dict = {}
        for row_idx in range(1, cells_count_in_row + 1):
            col_name = self._wui.get_text(HEADER_CELL_BY_IDX(table_coords,
                                                                  row_idx))
            cell_values = []
            for col_idx in range(1, cells_count_in_col + 1):
                cell_values.append(CONTENT_CELL_LINK(table_coords,
                                                             row_idx,
                                                             col_idx))
            result_dict[col_name] = cell_values
        return result_dict

    def _get_table_parameters(self, kwargs={}):
        return DetailsTableParameters(self._wui, **kwargs)

    def _get_table_attributes_dict(self):
        return TABLE_NAMES
