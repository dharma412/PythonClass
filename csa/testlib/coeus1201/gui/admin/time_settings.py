#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/gui/admin/time_settings.py#1 $


import re
import time

from common.gui.guicommon import GuiCommon


NTP_SERVERS_TABLE = 'xpath=//table[@id=\'ntp_servers\']'
ADD_ROW_BUTTON = 'id=ntp_servers_domtable_AddRow'
DELETE_ROW_BUTTON = 'xpath=//img[@alt=\'Delete...\']'
USE_NTP_RADIOBUTTON = 'id=set_mode_default'
SET_MANUALLY_RADIOBUTTON = 'id=set_mode_manual'
ROUTING_TABLE_LIST = 'name=routing_table'
NTP_SERVER_ROW = lambda index: 'id=ntp_servers[%s][host]' % (index,)
NTP_KEY_ROW = lambda index: 'id=ntp_servers[%s][keyno]' % (index,)
NTP_VALUE_ROW = lambda index: 'id=ntp_servers[%s][keyvalue]' % (index,)
MONTH_TEXTBOX = 'id=mm'
DAY_TEXTBOX = 'id=dd'
YEAR_TEXTBOX = 'id=yyyy'
HOUR_TEXTBOX = 'id=hh'
MINUTES_TEXTBOX = 'id=mi'
SECONDS_TEXTBOX = 'id=ss'
DAY_PERIOD_TEXTBOX = 'id=ap'
ENABLE_NTP_AUTH= "xpath=//input[@type='checkbox' and @id='ntp_serversauth_enabled']"

class TimeSettings(GuiCommon):

    def _open_page(self):
        self._navigate_to('System Administration', 'Time Settings')

    def get_keyword_names(self):
        return [
                'time_settings_edit_settings',
                'disable_ntp_server_authentication'
               ]

    def _select_keeping_method(self, method):
        keeping_locators = {'ntp': USE_NTP_RADIOBUTTON,
			    'ntpauth': USE_NTP_RADIOBUTTON,
                            'manual': SET_MANUALLY_RADIOBUTTON}

        if method not in keeping_locators:
            raise guiexceptions.ConfigError('Invalid time keeping method - "%s"' % (method,))
        else:
            self._click_radio_button(keeping_locators[method])

    def _select_routing_table(self, interface):
        if not self._is_visible(ROUTING_TABLE_LIST):
            raise ValueError('To select interface for routing at least '\
                              'two interfaces must be configured')

        interfaces = self.get_list_items(ROUTING_TABLE_LIST)
        if interface in interfaces:
            self.select_from_list(ROUTING_TABLE_LIST, interface)
        else:
            raise guiexceptions.GuiValueError('"%s" interface does not exist' % (interface,))

    def _get_ntp_servers_rows_ids(self):
        rows_id = []
        field_patt = re.compile('ntp_servers\[(\d+)\]\[host\]')
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
            self.click_element(DELETE_ROW_BUTTON, "don't wait")

    def _set_ntp_servers_table(self, num_of_rows):
        current_rows = len(self._get_ntp_servers_rows_ids())
        rows_diff = num_of_rows - current_rows
        if rows_diff > 0:
            self._add_table_rows(rows_diff)
        elif rows_diff < 0:
            self._delete_table_rows(abs(rows_diff))

    def _fill_ntp_servers_table(self, servers):
        servers = self._convert_to_tuple(servers)
        self._set_ntp_servers_table(len(servers))
        row_indexes = self._get_ntp_servers_rows_ids()

        for index, server in zip(row_indexes, servers):
            self.input_text(NTP_SERVER_ROW(index), server)

    def _fill_ntp_server_key_value_table(self, servers, key, value):
        servers = self._convert_to_tuple(servers)
        self._set_ntp_servers_table(len(servers))
        row_indexes = self._get_ntp_servers_rows_ids()

        for index, server in zip(row_indexes, servers):
            self.input_text(NTP_SERVER_ROW(index), server)
            self.input_text(NTP_KEY_ROW(index), key)
            self.input_text(NTP_VALUE_ROW(index), value) 

    def _set_system_time(self, local_time):
        try:
            st = time.strptime(local_time, '%m/%d/%Y %I:%M:%S %p')
        except ValueError, err_msg:
            raise ValueError('Time format is invalid. Error message - %s' %\
                             (err_msg,))

        datetime_textboxes = (MONTH_TEXTBOX, DAY_TEXTBOX, YEAR_TEXTBOX,
                              HOUR_TEXTBOX, MINUTES_TEXTBOX, SECONDS_TEXTBOX)

        for time_directive, textbox_id in zip(('%m', '%d', '%Y', '%I', '%M', '%S'),
                                              datetime_textboxes):
            time_val = time.strftime(time_directive, st)
            self.input_text(textbox_id, time_val)

        ap = time.strftime('%p', st)
        self.select_from_list(DAY_PERIOD_TEXTBOX, ap)

    def disable_ntp_server_authentication(self):
        self._open_page()
        self._click_edit_settings_button()
        self._unselect_checkbox(ENABLE_NTP_AUTH)
        self._fill_ntp_servers_table("time.ironport.com")
        self._click_submit_button()

    def time_settings_edit_settings(self,
                                    keeping_method, ntp_servers=None,
                                    interface=None, local_time=None, enable_ntp=None,
                                    key=None, value=None):
        """Edit system time settings.

        Parameters:
          - `keeping_method`: Method of setting system time. Either 'ntp'
                              or 'manual'.
          - `ntp_servers`: string with comma separated values of ntp servers to synchronize
                           the system clock with. Applicable to 'ntp' only.
          - `interface`: interface from which NTP queries should originate.
                         Either 'Management' or 'Data'. Applicable to 'ntp' only.
          - `local_time`: Date and time in format 'MM/DD/YYYY HH:MM:SS AM|PM'
                          to set system clock. Applicable to 'ntp' only.

        Examples:
        | Time Settings Edit Settings | manual | local_time=13/13/2013 13:13:13 AM |
        | Time Settings Edit Settings | ntp | ntp_servers=time.ironport.com, services.wga |
        | Time Settings Edit Settings | ntp | ntp_servers=time.ironport.com | interface=Management |

        """
        self._open_page()
        self._click_edit_settings_button()
        self._select_keeping_method(keeping_method)
        if keeping_method == 'manual' and local_time:
            self._set_system_time(local_time)
        elif keeping_method == 'ntp':
            if ntp_servers:
                self._fill_ntp_servers_table(ntp_servers)
            if interface:
                self._select_routing_table(interface)
        elif keeping_method == 'ntpauth':
            if enable_ntp:
                self._select_checkbox(ENABLE_NTP_AUTH)
                self._fill_ntp_server_key_value_table(ntp_servers,key,value)
        self._click_submit_button()
