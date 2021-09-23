#!/usr/bin/env python

import common.gui.guiexceptions as guiexceptions
from common.gui.guicommon import GuiCommon

import re
import time

NTP_SERVERS_TABLE = 'xpath=//table[@id=\'ntp_servers\']'
ADD_ROW_BUTTON = 'id=ntp_servers_addRow'
DELETE_ROW_BUTTON = 'xpath=//img[@alt=\'Delete...\']'
USE_NTP_RADIOBUTTON = 'id=set_mode_default'
SET_MANUALLY_RADIOBUTTON = 'id=set_mode_manual'
NTP_SERVER_ROW = lambda index: 'id=ntp_servers[%s][addr]' % (index,)
NTP_KEYVALUE_ROW = lambda index: 'id=ntp_servers[%s][keyno]' % (index,)
NTP_KEYPASS_ROW = lambda index: 'id=ntp_servers[%s][keyval]' % (index,)
NTP_AUTHENTICATION = "id=use_auth"
QUERIES_INTERFACE_LIST = 'name=source_ip_interface'
DATE_TEXTBOX = 'id=manual_date'
TIME_TEXTBOX = 'id=manual_time'
UPDATE_NOW_BUTTON = 'name=action:UpdateNow'
FILES_UPDATE_TABLE_CELL = lambda row, column:\
    '//dl[@class="box"][last()]//table[@class="cols"]/tbody/tr[%s]/td[%s]' % (row, column)

class TimeSettings(GuiCommon):
    """Keywords for Management -> System Administration -> Time Settings"""

    def get_keyword_names(self):
        return [
                'time_settings_edit_settings',
                'time_settings_update_now',
                'time_settings_get_file_status'
                ]

    def _open_page(self):
        self._navigate_to('Management', 'System Administration', 'Time Settings')

    def _select_keeping_method(self, method):
        keeping_locators = {'ntp': USE_NTP_RADIOBUTTON,
                            'manual': SET_MANUALLY_RADIOBUTTON}

        if method not in keeping_locators:
            raise ValueError('Invalid time keeping method - "%s"' % (method,))
        else:
            self._click_radio_button(keeping_locators[method])

    def _select_queries_interface(self, interface):
        int_list = self.get_list_items(QUERIES_INTERFACE_LIST)
        for int_name in int_list:
            if interface in int_name:
                self.select_from_list(QUERIES_INTERFACE_LIST, int_name)
                break
        else:
            raise ValueError('"%s" interface does not exist' % (interface,))

    def _get_ntp_servers_rows_ids(self):
        rows_id = []
        field_patt = re.compile('ntp_servers\[(\d+)\]\[addr\]')

        text_fields = self._get_all_fields()
        for field in text_fields:
            result = field_patt.search(field)
            if result:
                rows_id.append(result.group(1))

        return rows_id

    def _add_table_rows(self, num_of_rows):
        for i in xrange(num_of_rows):
            self.click_button(ADD_ROW_BUTTON, "don't wait")

    def _delete_table_rows(self, num_of_rows):
        for i in xrange(num_of_rows):
            self.click_button(DELETE_ROW_BUTTON, "don't wait")

    def _set_ntp_servers_table(self, num_of_rows):
        current_rows = len(self._get_ntp_servers_rows_ids())
        rows_diff = num_of_rows - current_rows
        if rows_diff > 0:
            self._add_table_rows(rows_diff)
        elif rows_diff < 0:
            self._delete_table_rows(abs(rows_diff))

    def _fill_ntp_servers_table(self, servers,authentication,keynumbers,keyvalues):
        servers = self._convert_to_tuple(servers)
        if len(servers) > 1:
            self._set_ntp_servers_table(len(servers))
        row_indexes = self._get_ntp_servers_rows_ids()

        for index, server in zip(row_indexes, servers):
            self.input_text(NTP_SERVER_ROW(index), server)

        if authentication:
            if not self._is_checked(NTP_AUTHENTICATION):
                self.click_element(NTP_AUTHENTICATION, "Enable NTP authetication")
            keynumbers = self._convert_to_tuple(keynumbers)
            keyvalues = self._convert_to_tuple(keyvalues)
            for index, keynumber, keyvalue in zip(row_indexes, keynumbers, keyvalues):
                self.input_text(NTP_KEYVALUE_ROW(index), keynumber)
                self.input_text(NTP_KEYPASS_ROW(index), keyvalue)


    def _set_system_time(self, local_time):
        time_format = '%m/%d/%Y %H:%M:%S'
        try:
            st = time.strptime(local_time, time_format)
        except ValueError, err_msg:
            raise ValueError('Time format is invalid. Error message - %s' %\
                             (err_msg,))

        datetime_textboxes = (DATE_TEXTBOX, TIME_TEXTBOX)

        for time_directive, textbox_id in zip(time_format.split(' '),
                                              datetime_textboxes):
            time_val = time.strftime(time_directive, st)
            self.input_text(textbox_id, time_val)

    def _click_update_now_button(self):
        self.click_button(UPDATE_NOW_BUTTON)

        self._check_action_result()

    def _get_files_status(self):
        columns = ('type', 'last_update', 'version', 'new_update')
        result_list = []

        num_of_rows = int(self.get_matching_xpath_count(FILES_UPDATE_TABLE_CELL('*', 1)))

        for row in xrange(2, num_of_rows + 2):
            data_dict = {}
            for column, key in enumerate(columns, 1):
                value = self._get_text(FILES_UPDATE_TABLE_CELL(row, column))
                data_dict[key] = value
            result_list.append(data_dict)

        return result_list

    def time_settings_edit_settings(self, keeping_method, delete_ntp_server=None , ntp_servers=None, interface=None, local_time=None,ntp_authentication=None,key_numbers=None,key_passes=None):
        """Edit system time settings.

        Parameters:
            - `keeping_method`: Method of setting system time. Either 'ntp'
                                or 'manual'.
            - `ntp_servers`: a tuple of ntp servers to synchronize the system
                             clock with. Applies only if `keeping_method` is
                             'ntp'.
            - `interface`: interface from which NTP queries should originate.
                           If None default value will be used. Applies only if
                           `keeping_method` is 'ntp'.
            - `local_time`: Date and time in format 'MM/DD/YYYY HH:MM:SS'
                            to set system clock to. If None, default value will
                            be used. Applies only if `keeping_method` is
                            'manual'.
            - 'ntp_authetication: Option to enable NTP authetication for NTP servers
            -  key_numbers : Key numbers for NTP servers
            -  key_passes  : Key passes for NTP servers

        Examples:
        | Time Settings Edit Settings | manual | local_time=13/13/2013 13:13:13 AM |
        | Time Settings Edit Settings | ntp | ntp_servers=time.ironport.com, services.wga |
        | Time Settings Edit Settings | ntp | ntp_servers=time.ironport.com, services.wga |ntp_authentication=True,keynumbers=1 ,2 |keypasses= 1,2|
        | Time Settings Edit Settings | ntp | ntp_servers=time.ironport.com | interface=Management |
        """
        self._open_page()

        self._click_edit_settings_button()

        self._select_keeping_method(keeping_method)

        row_indexes_len = len(self._get_ntp_servers_rows_ids())

        if keeping_method == 'manual' and local_time:
            self._set_system_time(local_time)
        elif keeping_method == 'ntp':
            if ntp_servers:
                self._fill_ntp_servers_table(ntp_servers,ntp_authentication,key_numbers,key_passes)
            if interface:
                self._select_queries_interface(interface)
            if delete_ntp_server:
                if row_indexes_len > 1:
                    self._delete_table_rows(row_indexes_len - 1)

        self._click_submit_button()

    def time_settings_update_now(self):
        """Update time zone file.

        Examples:
        | Time Settings Update Now |
        """
        self._open_page()

        self._click_update_now_button()

    def time_settings_get_file_status(self, timeout=600):
        """Get time zone files status.

        Parameters:
            - `timeout`: Timeout for waiting update status
                (in 'New Update' column of 'Time Zone File Updates' table).
                600 seconds are indicated by default.

        Return:
            A list of dictionaries where each dictionary has the following
            keys:
            - `type`: time zone file type. String.
            - `last_update`: date of the last update. String.
            - `version`: current version of the file. String.
            - `new_update`: version of the available update. String.

        Exceptions:
            - `GuiValueError` appears if an error is present for an update.

        Examples:
        | @{time_zone_status}= | Time Settings Get File Status |
        | Log Many | @{time_zone_status} |
        """
        message=''
        self._open_page()

        result_list=self._get_files_status()

        for index, row in enumerate(result_list):
            update_status = row['new_update']

            step = 60
            time_spent = 0
            while re.compile('Connecting', re.I).search(update_status):
                if time_spent > timeout:
                    break
                time_spent += step
                time.sleep(step)
                result_list=self._get_files_status()
                update_status = (result_list[index])['new_update']

            if re.compile('error', re.I).search(update_status) or\
                re.compile('fail', re.I).search(update_status):
                message += "Update status for '%s' was '%s'.\r\n" % (row['type'], update_status)

        if message != '':
            raise guiexceptions.GuiValueError(message)

        return result_list

