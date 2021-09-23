#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1362/gui/email/tracking/message_tracking_data_availability.py#1 $ $DateTime: 2020/06/10 22:29:20 $ $Author: sarukakk $

import time
import sal.time

import common.gui.guiexceptions as guiexceptions
from common.gui.guicommon import GuiCommon

class MessageTrackingDataAvailability(GuiCommon):
    """Message Tracking Data Availability page interaction class.

    This class designed to interact with GUI elements of Email -> Message
    Tracking -> Message Tracking Data Availability page. Use keywords,
    listed below, to manipulate with Message Tracking Data Availability page.
    """

    # method required by RF
    # return a list with all public methods
    def get_keyword_names(self):
        return ['message_tracking_data_availability_get_tracking_data_range',
                'message_tracking_data_availability_get_missing_data_intervals'
               ]

    def _open_page(self):
        self._navigate_to('Email', 'Message Tracking',
                          'Message Tracking Data Availability')

    def _check_data_availability(self, table_data_name):
        MISSING_DATA_ERROR = "xpath=//div[@id='sma_tracking_availability" + \
                             "_missing_data_intervals-errors']"
        DATA_RANGE_ERROR = "xpath=//div[@id='sma_tracking_availability" + \
                           "_tracking_data_range-errors']"
        no_data_msg = 'No data was found'
        data_exist = False

        if table_data_name == 'data_range':
            if self._is_visible(DATA_RANGE_ERROR):
                self._info(no_data_msg)
            else:
                data_exist = True
        elif table_data_name == 'data_missing':
            if self._is_visible(MISSING_DATA_ERROR):
                self._info(no_data_msg)
            else:
                data_exist = True
        return data_exist

    def _wait_for_data_loading(self):
        DATA_RANGE_TABLE_CELL_DATA = lambda row, column: \
            "//tr[%s][contains(@id, 'yui-rec')]/td[%s]" % (row, column)

        result = []
        # waiting for table to be generated
        timer = sal.time.CountDownTimer(timeout=10).start()
        while timer.is_active():
            if self._is_element_present(DATA_RANGE_TABLE_CELL_DATA(1, 2)):
                break
            else:
                time.sleep(1)
        else:
            return result

        # Data may be still loading in some rows.
        timer = sal.time.CountDownTimer(10).start()
        while timer.is_active():
            if not self._is_text_present('Loading'):
                break
            time.sleep(2)

    def _select_item_from_list(self, item):
        LIST_LABEL = lambda label : 'label=%s' % (label,)

        options = self.get_list_items("xpath=//select[@id='filter_s_1']")

        for option in options:
            if item in option:
                self.select_from_list("xpath=//select[@id='filter_s_1']",
                                      LIST_LABEL(option))
                # wait for a page load to happen or timeout expires.
                self.wait_until_page_loaded(5000)
                break
        else:
            raise guiexceptions.ConfigError('No %s option was found.' % (item,))

    def _select_number_of_items(self, number_of_items):
        if not self._is_element_present("xpath=//select[@id='rows_s_1']"):
            return
        number_of_items_types = ['10', '20', '50', '100']
        if number_of_items not in number_of_items_types:
            raise guiexceptions.ConfigError(
                "Invalid displayed items '%s'." % number_of_items)
        self.select_from_list('id=rows_s_1', 'value=%s' % number_of_items)

    def _get_data_range_results(self):
        DATA_INFO_CELL = lambda row, title_column: DATA_TABLE % \
            (row, title_column)
        DATA_TABLE = "//div[@id='table_cols_sma_tracking_availability" + \
                     "_tracking_data_range_div']/table/tbody[2]/tr[%s]/td[%s]"

        result = []
        start_row = 1
        self._wait_for_data_loading()
        if self._check_data_availability('data_range'):
            num_of_rows = int(self.get_matching_xpath_count(
                DATA_INFO_CELL('*', 1)))
            columns_order = ('status', 'ip', 'description', 'data_range_from',
                             'data_range_to')
            for row in xrange(start_row, num_of_rows + start_row - 1):
                data_info = {}
                for column, column_name in enumerate(columns_order, 1):
                    data_info[column_name] = self.get_text(
                        DATA_INFO_CELL(row, column))
                result.append(str(TrackingDataRangeInfo(**data_info)))

        return result

    def _get_missing_data_intervals_results(self):
        DATA_INFO_CELL = lambda row, title_column: DATA_TABLE % \
            (row, title_column)
        DATA_TABLE = "//div[@id='table_cols_sma_tracking_availability_" + \
                     "missing_data_intervals_div']/table/tbody[2]/tr[%s]/td[%s]"

        result = []
        start_row = 1
        self._wait_for_data_loading()
        if self._check_data_availability('data_missing'):
            num_of_rows = int(self.get_matching_xpath_count(
                DATA_INFO_CELL('*', 1)))
            columns_order = ('ip', 'description', 'data_range_from',
                             'data_range_to')
            for row in xrange(start_row, num_of_rows + start_row):
                data_info = {}
                for column, column_name in enumerate(columns_order, 1):
                    data_info[column_name] = self.get_text(
                        DATA_INFO_CELL(row, column))
                result.append(str(TrackingDataRangeInfo(**data_info)))

        return result

    def message_tracking_data_availability_get_tracking_data_range(self):
        """Get tracking data range.

        Return:
            A list of TrackingDataRangeInfo objects.
            Each object has the following attributes:
            - `status`: current status of receiving message tracking data.
            - `ip`: appliance ip address.
            - `description`: appliance name.
            - `data_range_from`: day, month, year and time, appliance started
            receive message tracking data.
            - `data_range_to`: day, month, year and time, appliance stopped
            receive message tracking data.

        Example:
        | ${results} = | Message Tracking Data Availability Get Tracking Data Range |
        """
        self._open_page()

        return self._get_data_range_results()

    def message_tracking_data_availability_get_missing_data_intervals(self,
                                                                      appl_name_filter=None,
                                                                      number_of_items='100'):
        """Get missing data intervals.

        A missing-data interval is a period of time during which the SMA
        appliance received no message tracking data from ESA appliances.

        Parameters:
          - `appl_name_filter`: filter by email appliance. String of email
          appliance name to enable filtering.
          - `number_of_items`: number of items to display on page, can be one of
          _10_, _20_, _50_ or _100_. Default is_100_.

        Return:
            A list of TrackingDataRangeInfo objects.
            Each object has the following attributes:
            - `ip`: appliance ip address.
            - `description`: appliance name.
            - `data_range_from`: day, month, year and time, appliance started
            receive no message tracking data
            - `data_range_to`: day, month, year and time, appliance stopped
            receive no message tracking data

        Example:
        | ${results} = | Message Tracking Data Availability Get Missing Data Intervals |

        | ${results} = | Message Tracking Data Availability Get Missing Data Intervals |
        | ... | appl_name_filter=esa01 |
        | ... | number_of_items=10 |
        """
        self._open_page()

        if appl_name_filter:
            self._select_item_from_list(appl_name_filter)

        self._select_number_of_items(number_of_items)

        return self._get_missing_data_intervals_results()

class TrackingDataRangeInfo(object):
    """Container class holding information about tracking data ranges.

    Attributes:
        - `status`: current status of receiving message tracking data.
        - `ip`: appliance ip address.
        - `description`: appliance name.
        - `data_range_from`: day, month, year and time, appliance started
        receive (no) message tracking data.
        - `data_range_to`: day, month, year and time, appliance stopped
        receive (no) message tracking data.
    """
    def __init__(self, ip, description, data_range_from, data_range_to,
                 status=None):
        self.status = status
        self.ip = ip
        self.description = description
        self.data_range_from = data_range_from
        self.data_range_to = data_range_to

    def __str__(self):
        info_str = 'Ip: %s; Description: %s; Data Range From: %s; ' \
                   'Data Range To: %s;' % (self.ip, self.description,
                                          self.data_range_from,
                                          self.data_range_to)

        if self.status is not None:
            info_str += ' Status: %s;' % (self.status,)

        return info_str
