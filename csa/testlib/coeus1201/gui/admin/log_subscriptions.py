#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/gui/admin/log_subscriptions.py#1 $
# $DateTime: 2019/08/14 09:58:47 $
# $Author: uvelayut $

import itertools
import re

from common.gui.guicommon import GuiCommon
from common.gui import guiexceptions

LOGS_TABLE = 'xpath=//table[@class=\'cols\']'
LOG_ROW = LOGS_TABLE + '//tr'
LOG_NAME_CELL = lambda index: '%s[%s]/td[1]' % (LOG_ROW, index)
ADD_LOG_SUBSCRIPTION_BUTTON = 'AddListener'
LOG_TYPE_LIST = 'name=type'
LOG_TYPE_OPTION = lambda log_type: 'label=%s' % (log_type,)
LOG_NAME_TEXTBOX = 'name=new_id'
LOG_FILENAME_TEXTBOX = 'name=filename'
LOG_FILESIZE_TEXTBOX = 'name=filesize'
LOG_COMPRESSION_CHECKBOX = 'name=log_compression'
LOG_EXCLUSIONS_TEXTBOX = 'name=filter_status_codes'
CUSTOM_FIELDS_TEXTBOX = 'name=custom_fields'
W3C_CUSTOM_FIELDS_TEXTBOX = 'name=custom_field'
W3C_PREDEFINED_FIELDS_LISTBOX = 'id=w3c_field[]'
W3C_SELECTED_FIELDS_LISTBOX = 'id=selected_field[]'
W3C_FIELD_OPTION = lambda field: 'label=%s' % (field,)
ADD_FIELDS_BUTTON = 'xpath=//input[@value=\'Add >>\']'
REMOVE_W3C_FIELD_BUTTON = 'xpath=//input[@value=\'Remove\']'

ROLLOVER_LOG_CHECKBOX = lambda log_name: 'id=%s' % (log_name,)
ROLLOVER_ALL_CHECKBOX = 'id=roll'
ROLLOVER_NOW_BUTTON = '_rollover'

EDIT_LOG_LINK = lambda index: '%s[%s]/td[1]/a' % (LOG_ROW, index)
DELETE_LOG_LINK = lambda index: '%s[%s]/td[7]/img' % (LOG_ROW, index)

FTP_POLL_RADIOBUTTON = 'xpath=//input[@value="file"]'
FTP_PUSH_RADIOBUTTON = 'xpath=//input[@value="ftp_push"]'
SCP_PUSH_RADIOBUTTON = 'xpath=//input[@value="scp_push"]'
SYSLOG_PUSH_RADIOBUTTON = 'xpath=//input[@value="syslog_push"]'

ROLLOVER_TIME_LISTBOX = "id=rollover_by_time"
ROLLOVER_DAILY_TEXTBOX = "id=rollover_daily_time"
ROLLOVER_WEEKLY_TEXTBOX = "id=rollover_weekly_time"
ROLLOVER_DAY_ITEM = lambda item: 'id=roll_day%s' % (item,)
ROLLOVER_CUSTOM_TEXTBOX = "id=rollover_custom_time"

MAX_FTP_FILES_TEXTBOX = 'id=max_num_files'

FTP_HOST_TEXTBOX = 'id=ftp_host'
FTP_DIRECTORY_TEXTBOX = 'id=ftp_directory'
FTP_USERNAME_TEXTBOX = 'id=ftp_username'
FTP_PASSWORD_TEXTBOX = 'id=ftp_password'

SCP_SSH1_RADIOBUTTON = 'id=scp_protocol1'
SCP_SSH2_RADIOBUTTON = 'id=scp_protocol2'
SCP_HOST_TEXTBOX = 'id=scp_host'
SCP_PORT_TEXTBOX = 'id=scp_port'
SCP_DIRECTORY_TEXTBOX = 'id=scp_directory'
SCP_USERNAME_TEXTBOX = 'id=scp_username'
SCP_KEYCHECKING_CHECKBOX = 'id=scp_key'
SCP_AUTO_KEY_RADIOBUTTON = 'id=key_method_radio1'
SCP_MANUAL_KEY_RADIOBUTTON = 'id=key_method_radio2'
SCP_HOST_KEY_TEXTBOX = 'id=key_value'

SYSLOG_HOST_TEXTBOX = 'id=syslog_hostname'
SYSLOG_MSG_SIZE_TEXTBOX = 'id=syslog_msg_size'
SYSLOG_UDP_RADIOBUTTON = 'id=syslog_protocol1'
SYSLOG_TCP_RADIOBUTTON = 'id=syslog_protocol2'
SYSLOG_FACILITY_LIST = 'name=syslog_facility'
SYSLOG_FACILITY_ITEM = lambda item: 'label=%s' % (item,)

class LogSubscriptions(GuiCommon):
    """Keywords for interaction with "System Administration > Log Subscriptions"
    GUI page.

    *Adding and Editing Log Subscription*

    Adding of a new Log Subscription can be done in two steps:
     - Add Log Subscription with default Log Retrieval Method
     - Set desired Retrieval Method

    Example:
    Add a new gui_logs subscription with "SCP Push" as retrieval method:
    | Log Subscriptions Add | GUI Logs | My GUI Log |
    | Log Subscriptions Set Retrieval Method to SCP Push | My GUI Log | myhost.wga | /logs/ | testuser |

    Editing of a Log Subscription is split into two keywords:

     - `Log Subscriptions Edit (Access Log | W3C Log)` to edit all settings
        except Log Retrieval Method
     - `Log Subscriptions Set Retrieval Method to (Manually Download |
        FTP Push | SCP Push | Syslog Push)` to edit Log Retieval Method

    *Rollover by Time*

    'Rollover by Time' setting consists of more then one HTML elements but it
    is going to be passed in one keyword's argument: `retrieval_interval`.
    Format of this argument is the next:

     - `None` - 'None' will be selected in 'Rollover by Time' drop-down list.

     Note: 'None' is a string in this case and should be specified as
     | rollover_interval=None

     Specifying 'None' as a string and specifying real None value (either by
     skipping `rollover_interval` parameter or using ${None}) is very different
     and in latter case 'Rollover by Time' setting will be left unchanged.

     - `HH:MM` - 'Daily Rollover' will be selected in the drop-down list and
       a value of this parameter will be put in 'Time of day" text box.

     - `<Week day list> HH:MM` - 'Weekly Rollover' will be selected in the
       drop-down list, the time will be put in "Time of Day" text box and
       all days of the week specified in <Week day list> will be checked, days
       that does not present in the list will be unchecked.
       <Week day list> is a comma separated list of days of the week. Day can be
       specified using full name or just first 3 letter: Monday and Mon is
       equivalent. Day is case insensitive.

       Example:
       | rollover_interval=Mon, Tue, Fri 10:00
       | rollover_interval=Monday, Tuesday, Wednesday, Thursday 12:00

     - `<custom time interval>` - 'Custom Time Interval' will be selected in the
       drop-down list and a value of this parameter will be put in 'Rollover
       every' text box.
       Examples: 120s, 5m 30s, 4h, 2d

    If `retrieval_interval` argument is skip in keyword then no changes will be
    made in 'Rollover by Time' setting.

    *Log Types Constants*

    When a new Log Subscription is added an exact value of Log Type should be
    passed as an first argument to `Log Subscriptions Add` keyword.
    To avoid typing Log Types manually and to make test cases impregnable to
    changes in Log Type constants can be and highly appreciated to be used
    instead of hard-coded Log Types strings.

    To be able to use constants user should add 'constants.py' file to the test
    case. This can be done via adding following line at the top of the test
    case under \*** Settings \*** section:
        Variables       constants.py

    Example of constant's usage:
    | ${log_type.acllog}
    | ${log_type.gui}

    Full list of log_type constants:
    | acllog | 'Access Control Engine Logs' |
    | aclog | 'Access Logs' |
    | musd_log | 'AnyConnect Secure Mobility Daemon Logs' |
    | authlog | 'Authentication Framework Logs' |
    | avclog | 'AVC Engine Framework Logs' |
    | avc_log | 'AVC Engine Logs' |
    | cli | 'CLI Audit Logs' |
    | configlog | 'Configuration Logs' |
    | connlog | 'Connection Management Logs' |
    | dsdataloss_log | 'Data Security Logs' |
    | dslog | 'Data Security Module Logs' |
    | dcalog | 'DCA Engine Framework Logs' |
    | dca_log | 'DCA Engine Logs' |
    | proxyerrlog | 'Default Proxy Logs' |
    | diskmgrlog | 'Disk Manager Logs' |
    | external_auth_logs | 'External Authentication Logs' |
    | feedback_log | 'Feedback Logs' |
    | ftplog | 'FTP proxy Logs' |
    | ftpd_text | 'FTP Server Logs' |
    | gui | 'GUI Logs' |
    | haystackd | 'Haystack Logs' |
    | httpslog | 'HTTPS Logs' |
    | licenselog | 'License Module Logs' |
    | logframeworklog | 'Logging Framework Logs' |
    | logderrlog | 'Logging Logs' |
    | mcafeeframeworklog | 'McAfee Integration Framework Logs' |
    | mcafee_log | 'McAfee Logs' |
    | memmgrlog | 'Memory Manager Logs' |
    | misclog | 'Miscellaneous Proxy Modules Logs' |
    | sntpd | 'NTP Logs' |
    | pacd_log | 'PAC File Hosting Daemon Logs' |
    | tmon_bypass | 'Proxy Bypass Logs' |
    | reportd | 'Reporting Logs' |
    | reportqueryd | 'Reporting Query Logs' |
    | saas_auth_log | 'SaaS Auth Logs' |
    | shd | 'SHD Logs' |
    | snmp_logs | 'SNMP Logs' |
    | snmplog | 'SNMP Module Logs' |
    | sophosframeworklog | 'Sophos Integration Framework Logs' |
    | sophos_log | 'Sophos Logs' |
    | status_log | 'Status Logs' |
    | system | 'System Logs' |
    | tmon_err | 'Traffic Monitor Error Logs' |
    | tmon_misc | 'Traffic Monitor Logs' |
    | uds_log | 'UDS Logs' |
    | updater_logs | 'Updater Logs' |
    | w3c_log | 'W3C Logs' |
    | wbnp_log | 'WBNP Logs' |
    | wbrsframeworklog | 'WBRS Integration Framework Logs' |
    | wccplog | 'WCCP Module Logs' |
    | webcatframeworklog | 'Webcat Integration Framework Logs' |
    | webrootframeworklog | 'Webroot Integration Framework Logs' |
    | webrootlog | 'Webroot Logs' |
    | welcomeack_log | 'Welcome Page Acknowledgement Logs' |

    """

    # method required by RF
    # return a list with all public methods
    def get_keyword_names(self):
        return [
            'log_subscriptions_add',
            'log_subscriptions_add_access_log',
            'log_subscriptions_add_w3c_log',
            'log_subscriptions_edit',
            'log_subscriptions_edit_access_log',
            'log_subscriptions_edit_w3c_log',
            'log_subscriptions_delete',
            'log_subscriptions_rollover',
            'log_subscriptions_set_retrieval_method_to_manually_download',
            'log_subscriptions_set_retrieval_method_to_ftp_push',
            'log_subscriptions_set_retrieval_method_to_scp_push',
            'log_subscriptions_set_retrieval_method_to_syslog_push',
                ]

    def _open_page(self):
        self._navigate_to('System Administration', 'Log Subscriptions')

    def _get_log_row_index(self, log_name):
        num_of_logs = int(self.get_matching_xpath_count(LOG_ROW[6:]))
        for index in xrange(2, num_of_logs+1):
            if log_name == self.get_text(LOG_NAME_CELL(index)):
                return index
        else:
            raise ValueError('"%s" log does not exist' % (log_name))

    def _click_edit_log_link(self, log_name):
        log_index = self._get_log_row_index(log_name)
        self.click_link(EDIT_LOG_LINK(log_index))
        self._info('Click "Edit" for "%s" log.' % (log_name,))
        self._wait_until_text_is_present('Edit Log Subscription')

    def _click_delete_log_link(self, log_name):
        log_index = self._get_log_row_index(log_name)
        self.click_element(DELETE_LOG_LINK(log_index), "don't wait")
        self._info('Clicked "Delete" for "%s" log.' % (log_name,))

    def _click_add_log_subscriptions_button(self):
        self.click_button(ADD_LOG_SUBSCRIPTION_BUTTON)
        self._info('Adding new log...')

    def _select_log_type(self, log_type):
        if log_type is not None:
            log_label = LOG_TYPE_OPTION(log_type)
            if log_type not in self.get_list_items(LOG_TYPE_LIST):
                raise ValueError('"%s" log type is invalid.' % (log_type,))

            self.select_from_list(LOG_TYPE_LIST, log_label)
            self.wait_until_page_loaded()
            self._info('Selected "%s" log type to create.' % (log_type,))

    def _set_log_name(self, log_name):
        if log_name is not None:
            self.input_text(LOG_NAME_TEXTBOX, log_name)
            self._info('Set name for new log to: "%s".' % (log_name,))

    def _set_rollover_interval(self, interval=None):
        time_pattern = r"(\d\d:\d\d)"
        week_days = [
            'monday',
            'tuesday',
            'wednesday',
            'thursday',
            'friday',
            'saturday',
            'sunday']

        if interval is not None:
            if interval.lower() == 'none':
                # None is selected for 'Rollover by Time'
                self.select_from_list(ROLLOVER_TIME_LISTBOX, 'None')
            elif re.search(time_pattern, interval.strip()):
                # Daily or Weekly Rollover
                if re.match(time_pattern, interval.strip()):
                    # Daily Rollover
                    self.select_from_list(ROLLOVER_TIME_LISTBOX,
                            'Daily Rollover')
                    self.input_text(ROLLOVER_DAILY_TEXTBOX, interval.strip())
                else:
                    # Weekly Rollover
                    self.select_from_list(ROLLOVER_TIME_LISTBOX,
                            'Weekly Rollover')
                    match = re.match(r"(.*)" + time_pattern, interval)
                    days = self._convert_to_tuple(match.group(1))
                    time = match.group(2)
                    # select only desired week days
                    for i in range(len(week_days)):
                        is_desired_day = False
                        for day in days:
                            if day.strip().lower()[:3] == week_days[i][:3]:
                                is_desired_day = True
                                break
                        if is_desired_day:
                            self.select_checkbox(ROLLOVER_DAY_ITEM(i))
                        else:
                            self.unselect_checkbox(ROLLOVER_DAY_ITEM(i))
                    # set time
                    self.input_text(ROLLOVER_WEEKLY_TEXTBOX, time)
            else:
                # Custom Rollover Time
                self.select_from_list(ROLLOVER_TIME_LISTBOX,
                        'Custom Time Interval')
                self.input_text(ROLLOVER_CUSTOM_TEXTBOX, interval.strip())

    def _set_log_filename(self, filename):
        if filename is not None:
            self.input_text(LOG_FILENAME_TEXTBOX, filename)
            self._info('Set log filename to "%s".' % (filename,))

    def _set_max_logfile_size(self, filesize):
        if filesize is not None:
            self.input_text(LOG_FILESIZE_TEXTBOX, filesize)
            self._info('Set log maximum file size to "%s".' % (filesize,))

    def _set_log_compression(self, log_compression):
        if log_compression is not None:
            if log_compression:
                self.select_checkbox(LOG_COMPRESSION_CHECKBOX)
                self._info('Enabled "Log Compression".')
            else:
                self.unselect_checkbox(LOG_COMPRESSION_CHECKBOX)
                self._info('Disabled "Log Compression".')

    def _is_log_level_supported(self, log_level_id):
        if self._is_element_present(log_level_id):
            return True

        return False

    def _select_log_level(self, log_level):
        log_levels_map = {
            'Critical': 'id=level_radio1',
            'Warning': 'id=level_radio2',
            'Info': 'id=level_radio3',
            'Debug': 'id=level_radio4',
            'Trace': 'id=level_radio5'}

        if log_level is not None:
            if log_level not in log_levels_map:
                raise ValueError('Invalid log level - "%s".' % (log_level,))

            if not self._is_log_level_supported(log_levels_map[log_level]):
                raise ConfigError('"%s" log level is not supported' % (log_level,))

            self._click_radio_button(log_levels_map[log_level])
            self._info('Selected "%s" log level.' % (log_level,))

    def _select_log_style(self, log_style):
        log_styles_map = {
            'Squid': 'id=style_radio2',
            'Apache': 'id=style_radio1',
            'Details': 'id=style_radio3'}

        if log_style is not None:
            if log_style in log_styles_map:
                self._click_radio_button(log_styles_map[log_style])
                self._info('Selected "%s" log style.' % (log_style,))
            else:
                raise ValueError('Unknown log style - "%s".' % (log_style,))

    def _set_custom_fields(self, custom_fields):
        if custom_fields is not None:
            fields = ''.join(custom_fields)
            self.input_text(CUSTOM_FIELDS_TEXTBOX, fields)
            self._info('Set custom fields to "%s".' % (fields,))

    def _set_log_exclusions(self, log_exclusions):
        if log_exclusions is not None:
            log_exclusions = self._convert_to_tuple(log_exclusions)
            http_codes = ','.join(log_exclusions)
            self.input_text(LOG_EXCLUSIONS_TEXTBOX, http_codes)
            self._info('Set log exclusions to "%s".' % (http_codes,))

    def _clear_w3c_fields(self, remove_predefined=True):
        predefined_fields = \
            self.get_list_items(W3C_PREDEFINED_FIELDS_LISTBOX)
        current_fields = \
            self.get_list_items(W3C_SELECTED_FIELDS_LISTBOX)

        filter_func = lambda field: field in predefined_fields
        if remove_predefined:
            fields_to_del = itertools.ifilter(filter_func, current_fields)
        else:
            fields_to_del = itertools.ifilterfalse(filter_func, current_fields)

        list_items_to_del = []
        for field in fields_to_del:
            list_items_to_del.append(W3C_FIELD_OPTION(field))
        self.select_from_list(W3C_SELECTED_FIELDS_LISTBOX, *list_items_to_del)
        self.click_button(REMOVE_W3C_FIELD_BUTTON, "don't wait")

    def _add_w3c_log_fields(self, w3c_log_fields):
        if w3c_log_fields is not None:
            w3c_log_fields = self._convert_to_tuple(w3c_log_fields)
            self._clear_w3c_fields()
            w3c_log_field_options_list = map(W3C_FIELD_OPTION, w3c_log_fields)
            self.select_from_list(W3C_PREDEFINED_FIELDS_LISTBOX,
                                             *w3c_log_field_options_list)
            self.click_button(ADD_FIELDS_BUTTON, "don't wait")
            self._info('Added "%s" w3c log fields.' % (w3c_log_fields,))

    def _set_w3c_log_custom_fields(self, custom_fields):
        if custom_fields is not None:
            custom_fields = self._convert_to_tuple(custom_fields)
            self._clear_w3c_fields(False)
            fields = '\n'.join(custom_fields)
            self.input_text(W3C_CUSTOM_FIELDS_TEXTBOX, fields)
            self.click_button(ADD_FIELDS_BUTTON, "don't wait")
            self._info('Added "%s" custom fields.' % (custom_fields,))

    def _click_rollover_button(self):
        self.click_button(ROLLOVER_NOW_BUTTON)
        self._info('Clicked "Rollover now" button.')
        self._check_action_result()

    def _check_all_logs_to_rollover(self):
        self.click_button(ROLLOVER_ALL_CHECKBOX, "don't wait")
        self._info('Selected "All" logs to rollover.')

    def _check_log_to_rollover(self, log_name):
        log_locator = ROLLOVER_LOG_CHECKBOX(log_name)
        if self._is_element_present(log_locator):
            self.select_checkbox(log_locator)
            self._info('Selected "%s" log to rollover.' % (log_name,))
        else:
            raise ValueError('"%s" log does not exist.' % (log_name,))

    def _is_retrieval_supported(self, retrieval_button):
        if self._is_element_present(retrieval_button):
            return True
        return False

    def _setup_ftp_poll_retrieval(self, max_num_files):
        self._info('Configuring FTP poll log retrieval.')
        self._click_radio_button(FTP_POLL_RADIOBUTTON)

        if max_num_files is not None:
            self._set_max_files_to_store(max_num_files)

    def _set_max_files_to_store(self, max_files):
        self.input_text(MAX_FTP_FILES_TEXTBOX, max_files)
        self._info('Set maximum number of files to store to "%s".' %\
                         (max_files,))

    def _setup_ftp_push_retrieval(self, hostname, directory, username,
            password):
        self._info('Configuring FTP push retrieval.')
        self._click_radio_button(FTP_PUSH_RADIOBUTTON)

        self._fill_ftp_push_hostname(hostname)

        self._fill_ftp_push_directory(directory)

        self._fill_ftp_push_username(username)

        self._fill_ftp_push_password(password)

    def _fill_ftp_push_hostname(self, host):
        self.input_text(FTP_HOST_TEXTBOX, host)
        self._info('Set hostname to push log to to "%s".' % (host,))

    def _fill_ftp_push_directory(self, directory):
        self.input_text(FTP_DIRECTORY_TEXTBOX, directory)
        self._info('Set directory to "%s".' % (directory,))

    def _fill_ftp_push_username(self, user):
        self.input_text(FTP_USERNAME_TEXTBOX, user)
        self._info('Set username to "%s".' % (user,))

    def _fill_ftp_push_password(self, password):
        self.input_text(FTP_PASSWORD_TEXTBOX, password)
        self._info('Set password to "%s".' % (password,))

    def _setup_scp_push_retrieval(self, hostname, directory, username,
            port=None, enable_key_checking=None, key=None):
        self._info('Configuring SCP push retrieval.')
        self._click_radio_button(SCP_PUSH_RADIOBUTTON)
        self._fill_scp_push_hostname(hostname)
        self._fill_scp_push_port(port)
        self._fill_scp_push_directory(directory)
        self._fill_scp_push_username(username)

        if enable_key_checking is not None:
            self._set_scp_push_key_checking(enable_key_checking)
            if enable_key_checking:
                self._set_scp_push_key(key)
            else:
                self._info("Enable_key_checking is not True, but " + str(enable_key_checking))

    def _fill_scp_push_hostname(self, host):
        self.input_text(SCP_HOST_TEXTBOX, host)
        self._info('Set hostname to "%s".' % (host,))

    def _fill_scp_push_port(self, port):
        if port is not None:
            self.input_text(SCP_PORT_TEXTBOX, port)
            self._info('Set port to "%s".' % (port,))

    def _fill_scp_push_directory(self, directory):
        self.input_text(SCP_DIRECTORY_TEXTBOX, directory)
        self._info('Set directory to "%s".' % (directory,))

    def _fill_scp_push_username(self, user):
        self.input_text(SCP_USERNAME_TEXTBOX, user)
        self._info('Using "%s" username for scp.' % (user,))

    def _set_scp_push_key_checking(self, enable):
        if enable:
            if not self._is_checked(SCP_KEYCHECKING_CHECKBOX):
                self.click_button(SCP_KEYCHECKING_CHECKBOX, "don't wait")
                self._info('Enabled host key checking.')
        else:
            self.unselect_checkbox(SCP_KEYCHECKING_CHECKBOX)
            self._info('Disabled host key checking.')

    def _set_scp_push_key(self, key):
        if key is None:
            self._click_radio_button(SCP_AUTO_KEY_RADIOBUTTON)
            self._info('Selected auto scan for host key.')
        else:
            self.click_button(SCP_MANUAL_KEY_RADIOBUTTON, "don't wait")
            self.input_text(SCP_HOST_KEY_TEXTBOX, key)
            self._info('Set host key to "%s".' % (key,))

    def _setup_syslog_push_retrieval(self, hostname, protocol=None,
            msg_size=1024, facility=None):
        self._info('Configuring Syslog push retrieval.')
        if not self._is_retrieval_supported(SYSLOG_PUSH_RADIOBUTTON):
            raise ConfigError('syslog push retrieval is not supported')
        self._click_radio_button(SYSLOG_PUSH_RADIOBUTTON)

        self._fill_syslog_hostname(hostname)

        if protocol is not None:
            self._select_syslog_protocol(protocol.lower())

        self._fill_syslog_msg_size(msg_size)

        if facility is not None:
            self._select_syslog_facility(facility)

    def _fill_syslog_hostname(self, host):
        self.input_text(SYSLOG_HOST_TEXTBOX, host)
        self._info('Set syslog to be pushed to "%s".' % (host,))

    def _select_syslog_protocol(self, protocol):
        if protocol == 'udp':
            self._click_radio_button(SYSLOG_UDP_RADIOBUTTON)
        elif protocol == 'tcp':
            self._click_radio_button(SYSLOG_TCP_RADIOBUTTON)
        else:
            raise ValueError('Invalid "%s" protocol for syslog push' %\
                             (protocol,))
        self._info('Selected "%s" protocol.' % (protocol,))

    def _fill_syslog_msg_size(self, msg_size):
        self.input_text(SYSLOG_MSG_SIZE_TEXTBOX, msg_size)
        self._info('Set syslog maximum message size to "%s".' % (msg_size,))

    def _select_syslog_facility(self, facility):
        facilities = self.get_list_items(SYSLOG_FACILITY_LIST)
        if facility in facilities:
            self.select_from_list(SYSLOG_FACILITY_LIST,
                                   SYSLOG_FACILITY_ITEM(facility))
            self._info('Selected "%s" syslog facility.' % (facility,))
        else:
            raise ValueError('"%s" facility is not available.' % (facility,))

    def _fill_log_subscription_page(self,
        log_type,
        log_name,
        filename,
        log_size,
        log_compression,
        rollover_interval=None,
        log_level=None,
        log_style=None,
        custom_fields=None,
        log_exclusions=None,
        w3c_log_fields=None,
        w3c_custom_fields=None):

        self._select_log_type(log_type)

        self._set_log_name(log_name)

        self._set_log_filename(filename)

        self._set_max_logfile_size(log_size)

        self._set_rollover_interval(rollover_interval)

        self._set_log_compression(log_compression)

        self._select_log_level(log_level)

        self._select_log_style(log_style)

        self._set_custom_fields(custom_fields)

        self._set_log_exclusions(log_exclusions)

        self._add_w3c_log_fields(w3c_log_fields)

        self._set_w3c_log_custom_fields(w3c_custom_fields)

        self._click_submit_button()

    def log_subscriptions_add(self,
        log_type,
        log_name,
        filename=None,
        log_size=None,
        rollover_interval=None,
        log_compression=False,
        log_level=None):
        """Add new log subscription.

        Using this keyword a new Log Subscription can be added with default
        retrieval method: Manually download logs.

        Retrieval method of an existent log subscription can be changed using
        one of keywords:
            - `Log Subscriptions Set Retrieval Method To FTP Push`
            - `Log Subscriptions Set Retrieval Method To SCP Push`
            - `Log Subscriptions Set Retrieval Method To Syslog Push`
            - `Log Subscriptions Set Retrieval Method To Manually Download`

        Parameters:
            - `log_type`: type of log to associate with the subscription. See
              `introduction` for details about available log types constants.
            - `log_name`: name for the log subscription.
            - `filename`: name for the log file. If None, default value will be used.
            - `log_size`: maximum file size in bytes the log file can be.
            - `rollover_interval`: log rollover interval or time. See
              `introduction` for details about format of this string.
            - `log_compression`: compress log file after it has been rolled over. Default to False.
            - `log_level`: log level to use. If None, default value will be used.

        Examples:
        | Log Subscriptions Add | ${log_type.gui} | My GUI Log | filename=my_gui | log_size=5M |
        | | rollover_interval=Mon, Fri 10:00 | log_compression=${True} | log_level=Trace |
        | Log Subscriptions Add | Status Logs | My Status Log | filename=my_status | log_size=6M |
        | | rollover_interval=7d | log_compression=${False} | log_level=Debug |
        """

        self._info('Adding "%s" log type.' % (log_type,))

        self._open_page()

        self._click_add_log_subscriptions_button()

        self._fill_log_subscription_page(
            log_type,
            log_name,
            filename,
            log_size,
            log_compression,
            log_level=log_level,
            rollover_interval=rollover_interval)

    def log_subscriptions_add_access_log(self,
        log_name,
        log_style=None,
        custom_fields=None,
        filename=None,
        log_size=None,
        rollover_interval=None,
        log_compression=False,
        log_exclusions=None):
        """Add new Access Logs subscription.

        Using this keyword a new Access Log Subscription can be added with default
        retrieval method: Manually download logs.

        Retrieval method of an existent log subscription can be changed using
        one of keywords:
            - `Log Subscriptions Set Retrieval Method To FTP Push`
            - `Log Subscriptions Set Retrieval Method To SCP Push`
            - `Log Subscriptions Set Retrieval Method To Syslog Push`
            - `Log Subscriptions Set Retrieval Method To Manually Download`

        Parameters:
            - `log_name`: name for the log subscription.
            - `log_style`: format of the log information. Available values:
              'Squid', 'Apache', 'Details'. If None, default value will be used.
            - `custom_fields`: a comma separated list of custom fields to include in log
                               entries.
            - `filename`: name for the log file. If None, default value will be
                          used.
            - `log_size`: maximum file size in bytes the log file can be.
            - `rollover_interval`: log rollover interval or time. See
              `introduction` for details about format of this string.
            - `log_compression`: compress log file after it has been rolled
                                 over. Default to False.
            - `log_exclusions`: a comma separated list of HTTP status codes to filter out.

        Examples:
        | Log Subscriptions Add Access Log | My Access Log | log_style=Apache | rollover_interval=None |
        | Log Subscriptions Add Access Log | My Access Log | log_style=Details | custom_fields=%C, %M, %V | log_exclusions=404 |
        | | filename=my_aclog | log_size=5M | rollover_interval=10:00 | log_compression=${True} |
        """

        self._info('Adding Access Log.')

        self._open_page()

        self._click_add_log_subscriptions_button()

        self._fill_log_subscription_page('Access Logs',
            log_name,
            filename,
            log_size,
            log_compression,
            log_style=log_style,
            custom_fields=custom_fields,
            log_exclusions=log_exclusions,
            rollover_interval=rollover_interval)

        self._info('Added "%s" Access Log subscription.' % (log_name,))

    def log_subscriptions_add_w3c_log(self,
            log_name,
            w3c_log_fields=None,
            custom_fields=None,
            filename=None,
            log_size=None,
            rollover_interval=None,
            log_compression=False,
            log_exclusions=None):
        """Add new W3C Logs subscription.

        Using this keyword a new W3C Log Subscription can be added with default
        retrieval method: Manually download logs.

        Retrieval method of an existent log subscription can be changed using
        one of keywords:
            - `Log Subscriptions Set Retrieval Method To FTP Push`
            - `Log Subscriptions Set Retrieval Method To SCP Push`
            - `Log Subscriptions Set Retrieval Method To Syslog Push`
            - `Log Subscriptions Set Retrieval Method To Manually Download`

        Parameters:
            - `log_name`: name for the log subscription.
            - `w3c_log_fields`: a  of predefined W3C log fields to
                include. If None, default value will be used.
            - `custom_fields`: a comma separated list of custom fields to
                include in log entries.
            - `filename`: name for the log file. If None, default value will be
                used.
            - `log_size`: maximum file size in bytes the log file can be.
            - `rollover_interval`: log rollover interval or time. See
              `introduction` for details about format of this string.
            - `log_compression`: compress log file after it has been rolled
                                 over. Default to False.
            - `log_exclusions`: a comma separated list of HTTP status codes to
                filter out.

        Examples:
        | Log Subscriptions Add W3C Log | My W3C Log | w3c_log_fields=cs-username, cs-method, cs-url | custom_fields=cs(User-Agent), cs(Referer) |
        | Log Subscriptions Add W3C Log | My W3C Log | w3c_log_fields=cs-username, cs-method, cs-url | log_exclusions=404 | filename=my_w3clog |
        | | log_size=5M | rollover_interval=10:00 | log_compression=${True} |
        """

        self._info('Adding W3C log.')

        self._open_page()

        self._click_add_log_subscriptions_button()

        self._fill_log_subscription_page('W3C Logs',
            log_name,
            filename,
            log_size,
            log_compression,
            log_exclusions=log_exclusions,
            w3c_log_fields=w3c_log_fields,
            w3c_custom_fields=custom_fields,
            rollover_interval=rollover_interval)

        self._info('Added "%s" W3C Log subscription.' % (log_name,))

    def log_subscriptions_edit(self,
            log_name,
            new_log_name=None,
            filename=None,
            log_size=None,
            rollover_interval=None,
            log_compression=None,
            log_level=None):
        """Edit log subscription.

        Using this keyword all settings except 'Retrieval Method' can be edited

        Retrieval method of an existent log subscription can be changed using
        one of keywords:
            - `Log Subscriptions Set Retrieval Method To FTP Push`
            - `Log Subscriptions Set Retrieval Method To SCP Push`
            - `Log Subscriptions Set Retrieval Method To Syslog Push`
            - `Log Subscriptions Set Retrieval Method To Manually Download`

        Parameters:
            - `log_name`: name of the log to edit.
            - `new_log_name`: new name for the log subscription. If None, value
                              will be left unchanged.
            - `filename`: name for the log file. If None, value will be left
                          unchanged.
            - `log_size`: maximum file size in bytes the log file can be. If
                          None, value will be left unchaged.
            - `rollover_interval`: log rollover interval or time. See
              `introduction` for details about format of this string.
            - `log_compression`: compress log file after it has been rolled
                                 over. If None, value will be left unchanged.
            - `log_level`: log level to use. If None, value will be left
                           unchanged.

        Examples:
        | Log Subscriptions Edit | gui_logs | new_log_name=new_gui_logs | log_level=Trace |
        | Log Subscriptions Edit | cli_logs | new_log_name=my_cli_logs | filename=my_cli | log_size=12M |
        | | rollover_interval=Wednesday 13:00 | log_compression=${False} | log_level=Debug |
        """

        self._info('Editing "%s" log subscription.' % (log_name,))

        self._open_page()

        self._click_edit_log_link(log_name)

        self._fill_log_subscription_page(None,
            new_log_name,
            filename,
            log_size,
            log_compression,
            log_level=log_level,
            rollover_interval=rollover_interval)

    def log_subscriptions_edit_access_log(self,
        log_name,
        new_log_name=None,
        log_style=None,
        custom_fields=None,
        filename=None,
        log_size=None,
        rollover_interval=None,
        log_compression=False,
        log_exclusions=None):
        """Edit Access Logs subscription.

        Using this keyword all settings except 'Retrieval Method' can be edited

        Retrieval method of an existent log subscription can be changed using
        one of keywords:
            - `Log Subscriptions Set Retrieval Method To FTP Push`
            - `Log Subscriptions Set Retrieval Method To SCP Push`
            - `Log Subscriptions Set Retrieval Method To Syslog Push`
            - `Log Subscriptions Set Retrieval Method To Manually Download`

        Parameters:
            - `log_name`: name of the log to edit.
            - `new_log_name`: new name for the log subscription. If None, value
                              will be left unchanged.
            - `log_style`: format of the log information. Available values:
              'Squid', 'Apache', 'Details'. If None, default value will be used.
            - `custom_fields`: a comma separated list of custom fields to include in log
                               entries.
            - `filename`: name for the log file. If None, value will be left
                          unchanged.
            - `log_size`: maximum file size in bytes the log file can be. If
                          None, value will be left unchaged.
            - `rollover_interval`: log rollover interval or time. See
              `introduction` for details about format of this string.
            - `log_compression`: compress log file after it has been rolled
                                 over. If None, value will be left unchanged.
            - `log_exclusions`: a comma separated list of HTTP status codes to filter out.

        Examples:
        | Log Subscriptions Edit Access Log | accesslogs | log_style=Squid | log_size=15G |
        | Log Subscriptions Edit Access Log | accesslogs | new_log_name=my_aclog | log_style=Details | custom_fields=%C, %M, %V |
        | | log_exclusions=404 | filename=my_aclog | log_size=5M | rollover_interval=10:00 | log_compression=${True} |
        """

        self._info('Editing "%s" Access Log subscription.' % (log_name,))

        self._open_page()

        self._click_edit_log_link(log_name)

        self._fill_log_subscription_page(None,
            new_log_name,
            filename,
            log_size,
            log_compression,
            log_style=log_style,
            custom_fields=custom_fields,
            log_exclusions=log_exclusions,
            rollover_interval=rollover_interval)

    def log_subscriptions_edit_w3c_log(self,
        log_name,
        new_log_name=None,
        w3c_log_fields=None,
        custom_fields=None,
        filename=None,
        log_size=None,
        rollover_interval=None,
        log_compression=False,
        log_exclusions=None):
        """Edit W3C Logs subscription.

        Using this keyword all settings except 'Retrieval Method' can be edited

        Retrieval method of an existent log subscription can be changed using
        one of keywords:
            - `Log Subscriptions Set Retrieval Method To FTP Push`
            - `Log Subscriptions Set Retrieval Method To SCP Push`
            - `Log Subscriptions Set Retrieval Method To Syslog Push`
            - `Log Subscriptions Set Retrieval Method To Manually Download`

        Parameters:
            - `log_name`: name of the log to edit.
            - `new_log_name`: new name for the log subscription. If None, value
                              will be left unchanged.
            - `w3c_log_fields`: a comma separated list of predefined W3C log fields to
                include. If None, default value will be used.
            - `custom_fields`: a comma separated list of custom fields to
                include in log entries.
            - `filename`: name for the log file. If None, default value will be
                used.
            - `log_size`: maximum file size in bytes the log file can be.
            - `rollover_interval`: log rollover interval or time. See
              `introduction` for details about format of this string.
            - `log_compression`: compress log file after it has been rolled
                                 over. Default to False.
            - `log_exclusions`: a comma separated list of HTTP status codes to
                filter out.

        Examples:
        | Log Subscriptions Edit W3C Log | My W3C Log | w3c_log_fields=cs-username, cs-method, cs-url | custom_fields=cs(User-Agent), cs(Referer) |
        | Log Subscriptions Edit W3C Log | My W3C Log | new_log_name=Updated W3C Log | w3c_log_fields=cs-username, cs-method, cs-url | log_exclusions=404, 405 |
        | | filename=my_w3clog | log_size=5M | rollover_interval=10:00 | log_compression=${True} |
        """

        self._info('Editing W3C log.')

        self._open_page()

        self._click_edit_log_link(log_name)

        self._fill_log_subscription_page(None,
        new_log_name,
        filename,
        log_size,
        log_compression,
        log_exclusions=log_exclusions,
        w3c_log_fields=w3c_log_fields,
        w3c_custom_fields=custom_fields,
        rollover_interval=rollover_interval)

        self._info('Edited "%s" W3C Log subscription.' % (log_name,))

    def log_subscriptions_delete(self, log_name):
        """Delete log subscription.

        Parameters:
            - `log_name`: name of the log subscription to delete.

        Examples:
        | Log Subscriptions Delete | gui_logs |
        """
        self._info('Removing "%s" log.' % (log_name,))

        self._open_page()

        self._click_delete_log_link(log_name)
        self._click_continue_button(text="Delete")

    def log_subscriptions_rollover(self, log_names):
        """Rollover log subscription.

        Parameters:
            - `log_names`: a comma separated list of names of log subscriptions to rollover.
                           If 'All', all currently configured log subscriptions
                           will be rolled over.

        Examples:
        | Log Subscriptions Rollover | All |
        | Log Subscriptions Rollover | gui_logs, cli_logs |
        """
        self._info('Rolling over logs.')

        self._open_page()

        if isinstance(log_names, basestring) and log_names == 'All':
            self._check_all_logs_to_rollover()
        else:
            log_names = self._convert_to_tuple(log_names)
            for log_name in log_names:
                self._check_log_to_rollover(log_name)

        self._click_rollover_button()

    def log_subscriptions_set_retrieval_method_to_manually_download(self,
            log_name,
            max_num_files=None,
            filename=None):
        """Change retrieval method of the log subscription to FTP Poll.

        Parameters:
            - `log_name`: name of the log to edit.
            - `max_num_files`: maximum number of files. If None then default
              value will be used and value will be updated
            - `filename`: name for the log file. If None, value will be left
              unchanged. This value is required when former Retrieval Method was
              Syslog Push.

        Examples:
        | Log Subscriptions Set Retrieval Method to Manually Download | gui_logs | 20 |
        | Log Subscriptions Set Retrieval Method to Manually Download | cli_logs | max_num_files=15 | filename=my_cli |
        """

        self._open_page()

        self._click_edit_log_link(log_name)

        self._setup_ftp_poll_retrieval(max_num_files)

        self._set_log_filename(filename)

        self._click_submit_button()

    def log_subscriptions_set_retrieval_method_to_ftp_push(self,
            log_name,
            hostname,
            directory,
            username,
            password,
            filename=None):
        """Change retrieval method of the log subscription to FTP Push.

        Parameters:
            - `log_name`: name of the log to edit.
            - `hostname`: hostname of the FTP server
            - `directory`: directory on the FTP server where logs will be pushed
            - `username`: user name to the FTP server
            - `password`: password to the FTP server
            - `filename`: name for the log file. If None, value will be left
              unchanged. This value is required when former Retrieval Method was
              Syslog Push.

        Examples:
        | Log Subscriptions Set Retrieval Method to FTP Push | gui_logs | myftp.wga | /logs/ | testuser |
        | | ironport |
        | Log Subscriptions Set Retrieval Method to FTP Push | cli_logs | myftp.wga | /logs/ | testuser |
        | | ironport | filename=cli |
        """

        self._open_page()

        self._click_edit_log_link(log_name)

        self._setup_ftp_push_retrieval(hostname, directory, username, password)

        self._set_log_filename(filename)

        self._click_submit_button()

    def log_subscriptions_set_retrieval_method_to_scp_push(self,
            log_name,
            hostname,
            directory,
            username,
            protocol=None,
            port=None,
            enable_key_checking=None,
            key=None,
            filename=None):
        """Change retrieval method of the log subscription to SCP Push.

        Parameters:
            - `log_name`: name of the log to edit.
            - `hostname`: hostname of the SSH server
            - `directory`: directory on the SSH server where logs will be pushed
            - `username`: user name to the SSH server
            - `protocol`: that field is depricated and is left for backward
            compatibility with legacy tests; assigning that parameter does not
            take any effect
            - `port`: port on SSH server that SSH daemon is listening to. If
              None, default 22 port will be used.
            - `enable_key_checking`: boolean value (${True} or ${False})
              specifies whether enable or disable Host Key Checking. If None,
              False will be used by default.
            - `key`: string with a key which will be put into 'Enter Manually'
              text box. If None, 'Automatically Scan' will be used by default.
            - `filename`: name for the log file. If None, value will be left
              unchanged. This value is required when former Retrieval Method was
              Syslog Push.

        Examples:
        | Log Subscriptions Set Retrieval Method to SCP Push | gui_logs | myhost.wga | /logs/ | testuser |
        | Log Subscriptions Set Retrieval Method to SCP Push | cli_logs | myhost.wga | / | testuser |
        | | enable_key_cheking=${True} | key="ssh-rsa <long key data string>" | filename=cli |
        """

        self._open_page()

        self._click_edit_log_link(log_name)

        self._setup_scp_push_retrieval(hostname, directory, username,
                port, enable_key_checking, key)

        self._set_log_filename(filename)

        self._click_submit_button()

    def log_subscriptions_set_retrieval_method_to_syslog_push(self,
            log_name,
            hostname,
            protocol=None,
            msg_size=1024,
            facility=None):
        """Change retrieval method of the log subscription to Syslog Push.

        Parameters:
            - `log_name`: name of the log to edit.
            - `hostname`: hostname of the Syslog server
            - `protocol`: protocol to be used either 'UDP' or 'TCP'. If
              None, default UDP will be used.
            - `msg_size`: Maximum message size for syslog push
            - `facility`: name of facility to be used. If None, default value
              will be used.

        Examples:
        | Log Subscriptions Set Retrieval Method to Syslog Push | gui_logs | mysysloghost.wga |
        | Log Subscriptions Set Retrieval Method to Syslog Push | cli_logs | mysysloghost.wga | protocol=TCP | facility=console |
        """

        self._open_page()

        self._click_edit_log_link(log_name)

        self._setup_syslog_push_retrieval(hostname, protocol, msg_size, facility)

        self._click_submit_button()
