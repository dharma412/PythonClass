#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1362/gui/help/packet_capture.py#1 $
# $DateTime: 2020/06/10 22:29:20 $
# $Author: sarukakk $

import re

from common.gui.guicommon import GuiCommon
from sal.exceptions import ConfigError


START_CAPTURE_BUTTON = 'action:StartCapture'
STOP_CAPTURE_BUTTON = 'action:StopCapture'
RESULT_FILENAME_TEXT = 'action-results-message'
CAPTURE_STATUS_TEXT = 'capture-status'
DELETE_CAPTURE_FILES_BUTTON = 'delete_button'
CAPTURE_FILENAMES_LIST = 'capture_filename_id'
FILE_SIZE_LIMIT_TEXTBOX = 'capture_filesize'
SIZE_LIMIT_DURATION_RADIOBUTTON = 'd_filesize_id'
TIME_DURATION_RADIOBUTTON = 'd_timelimit_id'
TIME_DURATION_TEXTBOX = 'capture_timelimit'
INDEFINITE_DURATION_RADIOBUTTON = 'd_indef_id'
ALL_INTERFACES_RADIOBUTTON = 'use_all_ifaces'
SELECTED_INTERFACES_RADIOBUTTON = 'use_selected_ifaces'
INTERFACE_CHECKBOX = lambda row:\
    "//tr[%s]/td/input[@name='interfaces[]']" % (row,)
INTERFACE_CHECKBOX_NAME = lambda name:\
    "//input[@id='%s' and @name='interfaces[]']" % (name,)
NO_FILTER_RADIOBUTTON = 'no_filters_id'
PREDEFINED_FILTER_RADIOBUTTON = 'predefined_id'
PREDEFINED_FILTER_PORT_TEXTBOX = 'ports'
PREDEFINED_FILTER_CLIENT_TEXTBOX = 'source_ip'
PREDEFINED_FILTER_SERVER_TEXTBOX = 'destination_ip'
CUSTOM_FILTER_RADIOBUTTON = 'custom_id'
CUSTOM_FILTER_TEXTBOX = 'custom_filter'


class PacketCapture(GuiCommon):

    """Keywords for Help And Support -> Packet Capture"""

    def get_keyword_names(self):
        # TODO: Add 'packet_capture_download_file' keyword for downloading
        # pac file. Browser's download dialog can't be handled as for now.

        return [
            'packet_capture_start',
            'packet_capture_stop',
            'packet_capture_get_status',
            'packet_capture_get_files',
            'packet_capture_delete_files',
            'packet_capture_edit_settings',
            'packet_capture_get_info',
            ]

    def _open_page(self):
        self._navigate_to('Help and Support', 'Packet Capture')

    def _click_start_capture_button(self):
        if self._is_element_present(START_CAPTURE_BUTTON):
            self.click_button(START_CAPTURE_BUTTON)
        else:
            raise ConfigError('Packet capture has been started already')

    def _click_stop_capture_button(self):
        if self._is_element_present(STOP_CAPTURE_BUTTON):
            self.click_button(STOP_CAPTURE_BUTTON)
        else:
            raise ConfigError('Packet capture has not been started')

    def _get_status(self):
        return self.get_text(CAPTURE_STATUS_TEXT)

    def _select_files_to_delete(self, filenames):
        available_files = self.get_list_items(CAPTURE_FILENAMES_LIST)
        filenames = self._convert_to_tuple(filenames)

        for filename in filenames:
            filename = self._get_full_file_name(filename)
            if filename in available_files:
                self.select_from_list(CAPTURE_FILENAMES_LIST, filename)
            else:
                raise ValueError('`%s` filename was not found' % (filename,))

    def _get_full_file_name(self, filename):
        available_files = self.get_list_items(CAPTURE_FILENAMES_LIST)
        for file in available_files:
            if filename in file:
                return file
        return filename

    def _get_filename(self):
        file_text = self.get_text(RESULT_FILENAME_TEXT)
        result = re.search('File "(.*?)" was created', file_text)
        return result.group(1) if result else file_text

    def _fill_file_size_limit(self, limit):
        if limit is not None:
            self.input_text(FILE_SIZE_LIMIT_TEXTBOX, limit)

    def _select_duration(self, duration):
        if duration is None:
            return

        duration_type = duration.lower()

        if duration_type == 'indefinite':
            self._click_radio_button(INDEFINITE_DURATION_RADIOBUTTON)
        elif duration_type == 'size-limit':
            self._click_radio_button(SIZE_LIMIT_DURATION_RADIOBUTTON)
        else:
            self._click_radio_button(TIME_DURATION_RADIOBUTTON)
            self.input_text(TIME_DURATION_TEXTBOX, duration)

    def _unselect_all_interfaces(self):
        num_of_interfaces = int(self.get_matching_xpath_count(
            INTERFACE_CHECKBOX('*')))

        for i in range(num_of_interfaces):
            self.unselect_checkbox(INTERFACE_CHECKBOX(i + 2))

    def _select_interfaces(self, interfaces):
        if interfaces is None:
            return

        self._unselect_all_interfaces()

        if interfaces.lower() == 'all':
            self._click_radio_button(ALL_INTERFACES_RADIOBUTTON)
        else:
            self._click_radio_button(SELECTED_INTERFACES_RADIOBUTTON)
            for name in self._convert_to_tuple(interfaces):
                interface_loc = INTERFACE_CHECKBOX_NAME(name)

                if not self._is_element_present(interface_loc):
                    raise ValueError('`%s` interface was not found' % (name,))

                self.select_checkbox(interface_loc)

    def _select_filters(self, filter_settings):
        if filter_settings is None:
            return

        if filter_settings == False:
            self._click_radio_button(NO_FILTER_RADIOBUTTON)
        elif filter_settings.count(':') == 2:
            self._click_radio_button(PREDEFINED_FILTER_RADIOBUTTON)
            for value, locator in zip(filter_settings.split(':'),
                    (PREDEFINED_FILTER_PORT_TEXTBOX,
                    PREDEFINED_FILTER_CLIENT_TEXTBOX,
                    PREDEFINED_FILTER_SERVER_TEXTBOX)):
                if value is not None:
                    self.input_text(locator, value)
        else:
            self._click_radio_button(CUSTOM_FILTER_RADIOBUTTON)
            self.input_text(CUSTOM_FILTER_TEXTBOX, filter_settings)

    def _get_list_items(self):
        list_items = self.get_list_items(CAPTURE_FILENAMES_LIST)
        list_items_without_size = []

        for item in list_items:
            item_without_size = re.search(r"(.*) (.*)", item).group(1)
            list_items_without_size.append(item_without_size)

        return list_items_without_size

    def packet_capture_start(self):
        """Start a packet capture.

        Examples:
        | Packet Capture Start |

        Exceptions:
        - `ConfigError`: in case packet capture has been started already.
        """
        self._open_page()

        self._click_start_capture_button()

    def packet_capture_stop(self):
        """Stop packet capture.

        Return:
        Name of the file where packet capture activity was saved.

        Examples:
        | Packet Capture Stop |
        | ${cap_file} = | Packet Capture Stop |

        Exceptions:
        - `ConfigError`: in case packet capture has not been started.
        """
        self._open_page()

        self._click_stop_capture_button()

        return self._get_filename()

    def packet_capture_get_status(self):
        """Get current packet capture status.

        Return:
        Current packet capture status.

        Examples:
        | ${status} = | Packet Capture Get Status |
        """
        self._open_page()

        return self._get_status()

    def packet_capture_get_files(self):
        """Get available capture files.

        Return:
        List of packet capture filenames.

        Examples:
        | ${files} = | Packet Capture Get Files |
        """
        self._open_page()

        return self._get_list_items()

    def packet_capture_delete_files(self, filenames):
        """Delete packet capture files.

        Parameters:
        - `filenames`: a string of comma-separated values of capture filenames
           to delete.

        Examples:
        | Packet Capture Delete Files | M600-00114336AC38.cap |
        | Packet Capture Delete Files |
        | ... | M600-00114336AC38.cap,M600-00114336AC40.cap |

        Exceptions:
        - `ValueError`: in case no filename was found.
        """
        self._open_page()

        self._select_files_to_delete(filenames)

        self.click_button(DELETE_CAPTURE_FILES_BUTTON)

    def packet_capture_edit_settings(self, size_limit=None, duration=None,
        interfaces=None, filter_settings=None):
        """Edit packet capture settings.

        Parameters:
        - `size_limit`: the maximum file size for all packet capture files in
           megabytes.
        - `duration`: how long to run the packet capture. Can be one of
          'indefinite' or 'size_limit' to run packet capture indefinitely or
           until file size limit is reached. Or enter the time in seconds(s),
           minutes (m), or hours (h) to run capture for.
        - `interfaces`: a string of comma-separated values of interfaces names
           to run capture on. 'all' to run capture on all interfaces.
        - `filter_settings`: ${False} to not use filters. String in
          'ports:client_ip:server_ip' format to use predefined filter, any
           other string to use custom filter.

        Examples:
        | Packet Capture Edit Settings | 100 | indefinite | all |
        | ... | host 1.2.3.4 && port 8 |
        | Packet Capture Edit Settings | 200 | 5h | Management,Data |
        | ... | 10,20,30:1.2.3.4:5.6.7.8 |
        | Packet Capture Edit Settings | duration=size_limit |
        | ... | filter_settings=${False} |

        Exceptions:
        - `ValueError`: in case of invalid interface name.
        """
        self._open_page()

        self._click_edit_settings_button()

        self._fill_file_size_limit(size_limit)

        self._select_duration(duration)

        self._select_interfaces(interfaces)

        self._select_filters(filter_settings)

    def packet_capture_get_info(self):
        """
        Returns: Dictionary of packet-capturing-information with the following
        keys:
        - `state` - current state of packet capturing
        - `captured_files` - list of captured files
        - `size_limit` - Capture File Size Limit
        - `duration` - Capture Duration
        - `interfaces` - Interfaces Selected
        - `filters` - Filters Selected

        Examples:
        | ${packet_capture_info}= | Packet Capture Get Info |
        | Should Be True | ${packet_capture_info}['state'])=='No packet capture in progress' |
        | Should Be True | len(${packet_capture_info}['captured_files']) > 3  |
        | Should Be True | ${packet_capture_info}['duration'] == 'Run Capture Indefinitely ' |
        """
        STATUS = "xpath=//div [@id='capture-status']"
        GET_VALUE = lambda value: \
            self._get_text("//th[contains(text() , '%s')]/../td" % value)
        FILE = lambda num: \
            "xpath=//select [@id='capture_filename_id']/option[%d]" % num

        self._open_page()

        result={}
        result['state'] = self._get_text(STATUS)

        files = []

        row = 1
        while self._is_element_present(FILE(row)):
            files.append(self.get_value(FILE(row)))
            row += 1

        result['captured_files'] = files
        result['size_limit'] = GET_VALUE('Capture File Size Limit')
        result['duration']   = GET_VALUE('Capture Duration')
        result['interfaces'] = GET_VALUE('Interfaces Selected')
        result['filters']    = GET_VALUE('Filters Selected')
        return result
