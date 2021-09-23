#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1350/gui/help/packet_capture.py#1 $ $DateTime: 2020/01/06 01:25:43 $ $Author: saurgup5 $

from common.gui.guicommon import GuiCommon
from common.gui.guiexceptions import SeleniumClientException, GuiValueError
from sal.exceptions import ConfigError
from sal.containers.cfgholder import CfgHolder
from common.util.sarftime import CountDownTimer
import re
import time

START_CAPTURE_BUTTON = "//input[@value='Start Capture']"
STOP_CAPTURE_BUTTON = "//input[@value='Stop Capture']"
DELETE_BUTTON = "//input[@value='Delete Selected Files']"
DOWNLOAD_BUTTON = "//input[@value='Download File']"
CAPTURE_STATUS = "//*[@id='capture-status']"
CAPTURED_FILES_OPT = "//*[@id='capture_filename_id']/option"
CAPTURED_FILES = "//*[@id='capture_filename_id']"
CAPTURED_FILE = lambda x: "//*[@id='capture_filename_id']/option[%s]" % x
ACTION_RESULTS = "//*[@id='action-results']"
ACTION_RESULTS_TITLE = "//*[@id='action-results-title']"
ACTION_RESULTS_MESSAGE = "//*[@id='action-results-message']"
EDIT_SETTINGS_BUTTON = "//input[@value='Edit Settings...']"
PACKET_CAPTURE_SETTINGS_TABLE = "//*[@id='form']/dl[2]/dd/table/tbody"

# Edit Settings page
FILESIZE_TEXTBOX = "//*[@id='capture_filesize']"
TIMELIMIT_TEXTBOX = "//*[@id='capture_timelimit']"
PORTS_TEXTBOX = "//*[@id='ports']"
CLIENT_IP_TEXTBOX = "//*[@id='source_ip']"
SERVER_IP_TEXTBOX = "//*[@id='destination_ip']"
CUSTOM_FILTER_TEXTBOX = "//*[@id='custom_filter']"
FILE_SIZE_LIMIT_RADIOBUTTON = "//*[@id='d_filesize_id']"
TIME_LIMIT_RADIOBUTTON = "//*[@id='d_timelimit_id']"
RUN_INDEFINITELY_RADIOBUTTON = "//*[@id='d_indef_id']"
USE_ALL_IFACES_RADIOBUTTON = "//*[@id='use_all_ifaces']"
USE_SELECTED_IFACES_RADIOBUTTON = "//*[@id='use_selected_ifaces']"
NO_FILTERS_RADIOBUTTON = "//*[@id='no_filters_id']"
PREDEFINED_FILTERS_RADIOBUTTON = "//*[@id='predefined_id']"
CUSTOM_FILTER_RADIOBUTTON = "//*[@id='custom_id']"
INTERFACE_ID = lambda x: "//*[@id='%s']" % x
INTERFACES_NUM = "//*[@id='form']/dl/dd/table/tbody/*[contains(.,'Interfaces')]//input[@type='checkbox']"
INTERFACE_NAME = lambda idx: "//*[@id='use_selected_ifaces']/following::tr[%s]" % idx

class PacketCapture(GuiCommon):
    def get_keyword_names(self):
        return ['packet_capture_start',
                'packet_capture_stop',
                'packet_capture_get_status',
                'packet_capture_get_files',
                'packet_capture_delete_files',
                'packet_capture_edit_settings',
                'packet_capture_get_settings',
                'packet_capture_download_files',]

    def _open_page(self):
        self._navigate_to('Help and Support', 'Packet Capture')

    def _get_capture_status(self):
        tmr = CountDownTimer(30).start()
        while tmr.is_active():
            if self._is_element_present(CAPTURE_STATUS):
                return self.get_text(CAPTURE_STATUS)
            time.sleep(1)
        else:
            raise SeleniumClientException\
            ('Failed to get capture status. \
            No locator "%s" present' % CAPTURE_STATUS)

    def _get_results(self):
        try:
            res, msg = self._check_action_result()
            result = '%s: %s' % (res, msg)
        except GuiValueError as err:
            result = err
        return result

    def _get_action_results(self):
        tmr = CountDownTimer(30).start()
        while tmr.is_active():
            if self._is_element_present(ACTION_RESULTS):
                res = self._get_results()
                self._info(res)
                return res
            time.sleep(1)
        else:
            raise SeleniumClientException\
            ('Failed to get action results. \
            No locator "%s" present' % ACTION_RESULTS)

    def _get_filename(self):
        file_text = self.get_text(ACTION_RESULTS_MESSAGE)
        result = re.search('File "(.*?)" was created', file_text)
        return result.group(1) if result else file_text

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

    def _get_list_of_captured_files(self):
        # get_list_items returns [''] if no items in the list
        # so need extra check
        _lst = [el for el in self.get_list_items(CAPTURED_FILES) if el]
        if not _lst:
            return {}
        _files = [f.split()[0] for f in _lst]
        _sizes = [s.split()[1].replace('(','').replace(')','') for s in _lst]
        return dict(zip(_files, _sizes))

    def _unselect_all_interfaces(self):
        lst_ifaces = []
        for i in xrange\
            (1, int(self.get_matching_xpath_count(INTERFACES_NUM))+1):
            interface_check_box = \
            '%s//input[@name="interfaces[]"]' % INTERFACE_NAME(i)
            if self._is_element_present(interface_check_box):
                self._unselect_checkbox(interface_check_box)
            lst_ifaces.append(self.get_text(INTERFACE_NAME(i)))
        return lst_ifaces

    def _select_captured_files(self, filenames):
        captured_files = self._get_list_of_captured_files()
        if not captured_files:
            raise ValueError('No captured files present')
        _all = 'all'
        _top = 'top'
        _filename_option = lambda f: '%s' % f
        if isinstance(filenames, basestring):
            if filenames.lower() == _all:
                return self.select_from_list(CAPTURED_FILES, *[])
            elif filenames.lower() == _top:
                return self.select_from_list\
                    (CAPTURED_FILES, self.get_text(CAPTURED_FILE(1)))
        if isinstance(filenames, dict):
            filenames = filenames.keys()
        else:
            filenames = self._convert_to_tuple(filenames)
        wrong_files = [f for f in filenames if f not in captured_files.keys()]
        if wrong_files:
            raise ValueError\
            ('There are no such files: %s' % ', '.join(wrong_files))
        else:
            opts = [_filename_option(f) for f in filenames]
            self.select_from_list(CAPTURED_FILES,  *opts)

    def _get_current_settings(self, use_normalize=False):
        settings = CfgHolder()
        rows = int(self.get_matching_xpath_count\
            ('%s/tr' % PACKET_CAPTURE_SETTINGS_TABLE))
        rowno = 1
        text = lambda row:self.get_text\
            ('%s/tr[%s]' % (PACKET_CAPTURE_SETTINGS_TABLE, row))
        try:
            while rowno <= rows:
                key,value = text(rowno).split(':')
                settings.__setattr__\
                (self._normalize(key, use_normalize=use_normalize), value)
                rowno += 1
        except SeleniumClientException, ex:
            self._warn(ex)
        return settings

    def _select_duration(self, duration):
        if duration is None:
            return
        duration_type = duration.lower()
        if duration_type == 'indefinite':
            self._click_radio_button(RUN_INDEFINITELY_RADIOBUTTON)
        elif duration_type == 'size limit':
            self._click_radio_button(FILE_SIZE_LIMIT_RADIOBUTTON)
        else:
            self._click_radio_button(TIME_LIMIT_RADIOBUTTON)
            self.input_text(TIMELIMIT_TEXTBOX, duration)

    def _select_interfaces(self, interfaces):
        if interfaces is None:
            return
        if isinstance(interfaces, basestring):
            if interfaces.lower() == 'all':
                self._click_radio_button(USE_ALL_IFACES_RADIOBUTTON)
                return
        interfaces = self._convert_to_tuple(interfaces)
        lst_ifaces = self._unselect_all_interfaces()
        self._click_radio_button(USE_SELECTED_IFACES_RADIOBUTTON)
        for interface in interfaces:
            if interface not in lst_ifaces:
                raise ValueError\
                ('No such interface:  %s. \
                Available interfaces: %s' % (interface, ', '.join(lst_ifaces)))
            self._click_radio_button(INTERFACE_ID(interface))

    def _convert_to_tuple_from_semicolon_separated_string(self, user_input):
        if isinstance(user_input, (str, unicode)):
            user_input = tuple(filter(None,
                (item.strip() for item in user_input.split(';'))))
        if isinstance(user_input, list):
            user_input = tuple(user_input)
        return user_input

    def _select_filters(self, filters):
        if filters is None:
            return
        if filters == False:
            self._click_radio_button(NO_FILTERS_RADIOBUTTON)
            return
        allowed_filter_types = ('custom', 'client_ip', 'server_ip', 'ports',)
        if isinstance(filters, basestring):
            filters = \
            self._convert_to_tuple_from_semicolon_separated_string(filters)
        elif isinstance(filters, dict):
            filters = self._convert_to_tuple_from_semicolon_separated_string\
                (';'.join(['%s:%s' % (k, v) for k,v in filters.iteritems()]))
        for f in filters:
            capture_filter = f.split(':',1)
            if len(capture_filter) == 2:
                filter_type = capture_filter[0].lower()
                if filter_type not in allowed_filter_types:
                    raise ValueError\
                    ('Filter type must be one of the following: %s' % \
                     ','.join(allowed_filter_types))
                filter_itself = capture_filter[1]
                if filter_type == 'custom':
                    self._click_radio_button(CUSTOM_FILTER_RADIOBUTTON)
                    self.input_text(CUSTOM_FILTER_TEXTBOX, filter_itself)
                    break
                else:
                    self._click_radio_button(PREDEFINED_FILTERS_RADIOBUTTON)
                if filter_type == 'ports':
                    self.input_text(PORTS_TEXTBOX, filter_itself)
                if filter_type == 'client_ip':
                    self.input_text(CLIENT_IP_TEXTBOX, filter_itself)
                if filter_type == 'server_ip':
                    self.input_text(SERVER_IP_TEXTBOX, filter_itself)

    def packet_capture_get_files(self):
        """Get available capture files.

        *Return*:
        Dictionary of packet capture files, like {filename:size}

        Examples:
        | ${files} = | Packet Capture Get Files |
        | Log Dictionary | ${files} |
        """
        self._info('Get list of captured files')
        self._open_page()
        return self._get_list_of_captured_files()

    def packet_capture_get_status(self, as_dictionary=False):
        """Get current packet capture status.

        *Parameters*:
        - `as_dictionary`: Return result as dictionary. Boolean.

        Return:
        Current packet capture status. String or Dictionary.

        Examples:
        | ${status} = | Packet Capture Get Status |
        """
        self._info('Get status of packet capture')
        self._open_page()
        status = self._get_capture_status()
        if as_dictionary:
            try:
                _lst = status.split('\n')
                _keys = [k.split(':')[0] for k in _lst if k]
                _values = ''.join([v.split(':')[1:] for v in _lst if v])
                return dict(zip(_keys, _values))
            except Exception:
                pass
        return status

    def packet_capture_start(self):
        """Start a packet capture.

        *Examples*:
        | Packet Capture Start |

        *Exceptions*:
        - `ConfigError`: in case packet capture has been started already.
        """
        self._info('Start Packet Capture')
        self._open_page()
        self._click_start_capture_button()
        return self._get_action_results()

    def packet_capture_stop(self):
        """Stop packet capture.

        *Examples*:
        | Packet Capture Stop |
        | ${cap_file} = | Packet Capture Stop |

        *Return*:
        Name of the file file.

        *Exceptions*:
        - `ConfigError`: in case packet capture has not been started.
        """
        self._info('Stop Packet Capture')
        self._open_page()
        self._click_stop_capture_button()
        return self._get_filename()

    def packet_capture_download_files(self, filenames=None):
        """Download captured files.

        *Parameters*:
        - `filenames`: Can be - String of comma-separated values; List of filenames;
        Dictionary {file:size}.
        Use _top_ - to download last created file.

        *Return*:
        Action result. String.

        *Examples*:
        | ${files}= | Packet Capture Get Files |
        | Packet Capture Download Files | filenames=${files} |

        | Packet Capture Download Files | filenames=X1000-001143ECD34D-1LHGP61-20120917-185233.cap |

        | Packet Capture Download Files | filenames=top |

        *Exceptions*:
        - `ValueError`: if wrong file given.
        """
        self._info('Download captured files')
        self._open_page()
        self._select_captured_files(filenames)
        self._debug('Click "Download File" button')
        self.click_button(DOWNLOAD_BUTTON, "don't wait")
        return self._get_action_results()

    def packet_capture_delete_files(self, filenames=None):
        """Delete captured files.

        *Parameters*:
        - `filenames`: Can be - String of comma-separated values; List of filenames;
        Dictionary {file:size}.
        Use _all_ - to delete all files, _top_ - to delete last created file.

        *Return*:
        Action result. String.

        *Examples*:
        In this example _filenames_ accept dictionary returned by `Packet Capture Get Files` keyword.
        | ${files}= | Packet Capture Get Files |
        | Packet Capture Delete Files | filenames=${files} |

        To delete several files
        | Packet Capture Delete Files | filenames=X1000-001143ECD34D-1LHGP61-20120917-185233.cap, X1000-001143ECD34D-1LHGP61-20120917-185305.cap |

        To delete all files
        | Packet Capture Delete Files | filenames=all |

        To delete last created file
        | Packet Capture Delete Files | filenames=top |

        *Exceptions*:
        - `ValueError`: if wrong file given.
        """
        self._info('Delete captured files')
        self._open_page()
        self._select_captured_files(filenames)
        self._debug('Click "Delete Selected Files" button')
        self.click_button(DELETE_BUTTON)
        return self._get_action_results()

    def packet_capture_get_settings(self, use_normalize=False):
        """
        Get current packet capture settings.

        *Parameters*:
        `use_normalize`: use normalize for dictionary keys. Boolean.

        *Examples*:
        | ${res}= | Packet Capture Get Settings |
        | Log Dictionary | ${res} |

        *Return*:
        CfgHolder (dictionary).
        """
        self._info('Get current capture settings')
        self._open_page()
        return self._get_current_settings(use_normalize=use_normalize)

    def packet_capture_edit_settings(self,
                                     size_limit=None,
                                     duration=None,
                                     interfaces=None,
                                     filters=None):
        """
        Edit packet capture settings.

        *Parameters*:
        - `size_limit`: the maximum file size for all packet capture files in
           megabytes.
        - `duration`: how long to run the packet capture. Can be one of
          'indefinite' or 'size_limit' to run packet capture indefinitely or
           until file size limit is reached. Or enter the time in seconds(s),
           minutes (m), or hours (h) to run capture for.
        - `interfaces`: a string of comma-separated values of interfaces names
           to run capture on. 'all' to run capture on all interfaces.
        - `filters`: ${False} to not use filters.
        String or Dictionary.
        String format is: filter_type1: values; filter_type2: values; ...
        Filter types should be separated with semicolon (;).
        Allowed filter types: _ports_, _client_ip_, _server_ip_, _custom_.
        Dictionary: keys are the same as allowed filter types.

        *Examples*:
        | Packet Capture Edit Settings |
        | ... | size_limit=100 |
        | ... | duration=size-limit |
        | ... | interfaces=a001.d1.${DUT}, Management |
        | ... | filters=custom:host ${CLIENT_IP} && port 443 |

        | ${x}= | Create Dictionary |
        | ... | ports  22, 23, 21 |
        | ... | server_ip  1.1.1.1 |
        | Packet Capture Edit Settings |
        | ... | filters=${x} |

        | Packet Capture Edit Settings |
        | ... | size_limit=200 |
        | ... | duration=indefinite |
        | ... | interfaces=all |
        | ... | filters=ports:25, 80, 443; client_ip=${CLIENT_IP} |

        *Return*:
        Action result. String.

        *Exceptions*:
        - `ValueError`: in case of invalid interface name or filter type.
        """
        # edit main capture settings
        self._info('Edit Packet Capture settings')
        self._open_page()
        self.click_button(EDIT_SETTINGS_BUTTON)
        self._input_text_if_not_none(FILESIZE_TEXTBOX, size_limit)
        self._select_duration(duration)
        self._select_interfaces(interfaces)
        self._select_filters(filters)
        self._click_submit_button()
        return self._get_action_results()
