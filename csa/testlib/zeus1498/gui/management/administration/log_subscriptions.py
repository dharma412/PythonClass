#!/usr/bin/env python

import itertools
import re

from common.gui.guicommon import GuiCommon
import common.gui.guiexceptions as guiexceptions

LOGS_TABLE = 'xpath=//table[@class="cols"]'
LOG_ROW = LOGS_TABLE + '/tbody/tr'
LOG_NAME_CELL = lambda index: '%s[%s]/td[1]' % (LOG_ROW, index)
ADD_LOG_SUBSCRIPTION_BUTTON = 'name=AddListener'
LOG_TYPE_LIST = 'name=type'
LOG_TYPE_OPTION = lambda log_type: 'label=%s' % (log_type,)
LOG_NAME_TEXTBOX = 'name=new_id'
LOG_FILENAME_TEXTBOX = 'name=filename'
LOG_FILESIZE_TEXTBOX = 'name=filesize'
INCLUDE_PASSWORDS_RADIOBUTTON = 'id=show_password_yes'
EXCLUDE_PASSWORDS_RADIOBUTTON = 'id=show_password_no'
LIST_LABEL = lambda item: 'label=%s' % (item,)

ROLLOVER_LOG_CHECKBOX = lambda log_name: 'id=%s' % (log_name,)
ROLLOVER_ALL_CHECKBOX = 'id=roll'
ROLLOVER_NOW_BUTTON = 'name=_rollover'

EDIT_LOG_LINK = lambda index: '%s[%s]/td[1]/a' % (LOG_ROW, index)
DELETE_LOG_LINK = lambda index: '%s[%s]/td[7]/img' % (LOG_ROW, index)

RATE_LIMIT = 'name=rl_status'
LOGGED_EVENTS_TEXTBOX='name=rl_event_limit'
TIME_LIMIT_TEXTBOX='name=rl_time_limit'

FTP_POLL_RADIOBUTTON = 'id=method_radio1'
FTP_PUSH_RADIOBUTTON = 'id=method_radio2'
SCP_PUSH_RADIOBUTTON = 'id=method_radio3'
SYSLOG_PUSH_RADIOBUTTON = 'id=method_radio4'

ROLLOVER_TIME_LISTBOX = "id=rollover_by_time"
ROLLOVER_DAILY_TEXTBOX = "id=rollover_daily_time"
ROLLOVER_WEEKLY_TEXTBOX = "id=rollover_weekly_time"
ROLLOVER_DAY_ITEM = lambda item: 'id=roll_day%s' % (item,)
ROLLOVER_CUSTOM_TEXTBOX = "id=rollover_custom_time"

MAX_FTP_FILES_TEXTBOX = 'id=max_num_files'

FTP_INTERVAL_TEXTBOX = 'id=ftp_max_time'
FTP_HOST_TEXTBOX = 'id=ftp_host'
FTP_DIRECTORY_TEXTBOX = 'id=ftp_directory'
FTP_USERNAME_TEXTBOX = 'id=ftp_username'
FTP_PASSWORD_TEXTBOX = 'id=ftp_password'

SCP_INTERVAL_TEXTBOX = 'id=scp_max_time'
SCP_HOST_TEXTBOX = 'id=scp_host'
SCP_PORT_TEXTBOX = 'id=scp_port'
SCP_DIRECTORY_TEXTBOX = 'id=scp_directory'
SCP_USERNAME_TEXTBOX = 'id=scp_username'
SCP_KEYCHECKING_CHECKBOX = 'id=scp_key'
SCP_AUTO_KEY_RADIOBUTTON = 'id=key_method_radio1'
SCP_MANUAL_KEY_RADIOBUTTON = 'id=key_method_radio2'
SCP_HOST_KEY_TEXTBOX = 'id=key_value'

SYSLOG_HOST_TEXTBOX = 'id=syslog_hostname'
SYSLOG_UDP_RADIOBUTTON = 'id=syslog_protocol1'
SYSLOG_TCP_RADIOBUTTON = 'id=syslog_protocol2'
SYSLOG_FACILITY_LIST = 'name=syslog_facility'
SYSLOG_FACILITY_ITEM = lambda item: 'label=%s' % (item,)

EDIT_SETTINGS_BUTTON = 'name=EditGlobals'
METRICS_FREQUENCY_TEXTBOX = 'name=system_measurements_frequency'
LOG_MID_CHECKBOX = 'id=log_message_id'
LOG_SUBJECT_CHECKBOX = 'id=log_orig_subj'
LOG_RESPONSE_CHECKBOX = 'id=log_remote_response'
CUSTOM_HEADERS_TEXTBOX = 'name=customer_headers'
SCHEDULED_PERIODS_LIST = 'rollover_by_time'
SCHEDULED_ROLLOVER_TIME_TEXTBOX = 'rollover_weekly_time'
SCHEDULED_ROLLOVER_INTERVAL_TEXTBOX = 'rollover_custom_time'
SCHEDULED_DAY_CHECKBOX = lambda index: 'roll_day%s' % (index,)

CONFIGURED_LOG_SUBSCRIPTION = lambda table, row, col:\
            '//table[@class=\'cols\'][%d]/tbody/tr[%s]/td[%d]' %\
            (table,str(row), col)
FREQUENCY = '//table[@class=\'pairs\']/tbody/tr[1]/td'
LOGGIN_OPTIONS = lambda row:\
            '//table[@class=\'pairs transparent\']/tbody/tr[%d]/td' % (row)

class LogSubscriptions(GuiCommon):
    """Keywords for interaction with "System Administration > Log Subscriptions" GUI page.

    *Adding and Editing Log Subscription*

    Adding of a new Log Subscription can be done in two steps:
     - Add Log Subscription with default Log Retrieval Method
     - Set desired Retrieval Method

    Example:
    Add a new auth_logs subscription with "SCP Push" as retrieval method:
    | Log Subscriptions Add | Authentication Logs | My Auth Log |
    | Log Subscriptions Set Retrieval Method to SCP Push | My Auth Log | myhost.sma | /logs/ | testuser |

    Editing of a Log Subscription is split into two keywords:

     - `Log Subscriptions Edit` to edit all settings except Log Retrieval Method
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
       all days of the week specified in <Week day list> will be checked,
       days that does not present in the list will be unchecked.
       <Week day list> is a comma separated list of days of the week.
       Day can be specified using full name or just first 3 letter: Monday and
       Mon is equivalent. Day is case insensitive.

       Example:
       | rollover_interval=Mon, Tue, Fri 11:00|
       | rollover_interval=Monday, Tuesday, Wednesday, Thursday 02:00

     - `<custom time interval>` - 'Custom Time Interval' will be selected in the
       drop-down list and a value of this parameter will be put in 'Rollover
       every' text box.
       Examples: 120s, 5m 30s, 4h, 2d

    If `retrieval_interval` argument is skip in keyword then no changes will be
    made in 'Rollover by Time' setting.

    *Edit Log Subscriptions Global Settings*
    Editing of a Global Settings for Log Subscription can be done following:
        - Log Subscriptions Edit Settings

    Example:
    | Log Subscriptions Edit Settings | metrics_timeout=timeout |
    | | log_mid_header=off | log_subject=on | log_response=off |

    * Log Types Constants *
    When a new Log Subscription is added an exact value of Log Type should be
    passed as an first argument to `Log Subscriptions Add` keyword.
    To avoid typing Log Types manually and to make test cases impregnable to
    changes in Log Type constants can be and highly appreciated to be used
    instead of hard-coded Log Types strings.

    To be able to use constants user should add 'constants.py' file to the test
    case. This can be done via adding following line at the top of the test
    case under \*** Settings \*** section:
            Variables      sma/constants.py

    Example of constant's usage:
    | ${log_types.AUTH}
    | ${log_type.BACKUP}

    Full list of log_type constants:
    | AUTH | 'Authentication Logs' |
    | BACKUP | 'Backup Logs' |
    | CLI_AUDIT | 'CLI Audit Logs' |
    | CONF_HISTORY | 'Configuration History Logs' |
    | FTP_SERVER | 'FTP Server Logs' |
    | HTTP | 'HTTP Logs' |
    | HAYSTACK | 'Haystack Logs' |
    | MAIL | 'IronPort Text Mail Logs' |
    | LDAP_DEBUG | 'LDAP Debug Logs' |
    | NTP | 'NTP logs' |
    | REPORTING | 'Reporting Logs' |
    | REPORTING_QUERY | 'Reporting Query Logs' |
    | SMA | 'SMA Logs' |
    | SNMP | 'SNMP Logs' |
    | SLBL | 'Safe/Block Lists Logs' |
    | EUQ_GUI | 'Spam Quarantine GUI Logs' |
    | EUQ | 'Spam Quarantine Logs' |
    | STATUS | 'Status Logs' |
    | SYSTEM | 'System Logs' |
    | TRACKING | 'Tracking Logs' |
    | UPDATER | 'Updater Logs' |
    """

    # method required by RF
    # return a list with all public methods
    def get_keyword_names(self):
        return [
                'log_subscriptions_add_log',
                'log_subscriptions_edit_log',
                'log_subscriptions_delete',
                'log_subscriptions_get_logs',
                'log_subscriptions_rollover',
                'log_subscriptions_get_global_settings',
                'log_subscriptions_edit_settings',
                'log_subscriptions_set_retrieval_method_to_manually_download',
                'log_subscriptions_set_retrieval_method_to_ftp_push',
                'log_subscriptions_set_retrieval_method_to_scp_push',
                'log_subscriptions_set_retrieval_method_to_syslog_push',
             ]

    def _open_page(self):
        self._navigate_to('Management', 'System Administration',
                               'Log Subscriptions')

    def _get_log_row_index(self, log_name):
        num_of_logs = int(self.get_matching_xpath_count(LOG_ROW[6:]))
        for index in xrange(2, num_of_logs+1):
            if log_name == self.get_text(LOG_NAME_CELL(index)):
                return index
        else:
            raise ValueError('"%s" log does not exist' % (log_name))

    def _click_edit_log_link(self, log_name):
        log_index = self._get_log_row_index(log_name)
        self.click_element(EDIT_LOG_LINK(log_index))
        self._info('Click "Edit" for "%s" log.' % (log_name,))

    def _click_delete_log_link(self, log_name):
        log_index = self._get_log_row_index(log_name)
        self.click_image(DELETE_LOG_LINK(log_index))
        self._info('Clicked "Delete" for "%s" log.' % (log_name,))

    def _click_add_log_subscriptions_button(self):
        self.click_button(ADD_LOG_SUBSCRIPTION_BUTTON)
        self._info('Adding new log...')

    def _select_log_type(self, log_type):
        if log_type is not None:
            log_label = LOG_TYPE_OPTION(log_type)
            if log_type not in self.get_list_items(LOG_TYPE_LIST):
                raise ValueError('"%s" log type is invalid.' % (log_type,))

            self.select_from_list(LOG_TYPE_LIST, log_type)
            self.wait_until_page_loaded()
            self._info('Selected "%s" log type to create.' % (log_type,))

    def _set_log_name(self, log_name):
        if log_name is not None:
            self.input_text(LOG_NAME_TEXTBOX, log_name)
            self._info('Set name for new log to: "%s".' % (log_name,))

    def _set_log_filename(self, filename):
        if filename is not None:
            self.input_text(LOG_FILENAME_TEXTBOX, filename)
            self._info('Set log filename to "%s".' % (filename,))

    def _set_max_logfile_size(self, filesize):
        if filesize is not None:
            if not self._is_element_present(LOG_FILESIZE_TEXTBOX):
                raise guiexceptions.ConfigError('Configuration of max log size is '\
                                  'not supported')

            self.input_text(LOG_FILESIZE_TEXTBOX, filesize)
            self._info('Set log maximum file size to "%s".' % (filesize,))

    def _set_rate_limit(self, logged_events,time_limit):
        if logged_events is not None or time_limit is not None :
            if not self._is_checked(RATE_LIMIT):
                self.click_element(RATE_LIMIT, "don't wait")
            if logged_events:
                self.input_text(LOGGED_EVENTS_TEXTBOX, logged_events)
                self._info('Set logged events to "%s".' % (logged_events,))
            if time_limit:
                self.input_text(TIME_LIMIT_TEXTBOX, time_limit)
                self._info('Set time range to "%s".' % (time_limit,))

    def _is_log_level_supported(self, log_level_id):
        if self._is_element_present(log_level_id):
            return True

        return False

    def _select_log_level(self, log_level):
        log_levels_map = {'Critical': 'id=level_radio1',
                          'Warning': 'id=level_radio2',
                          'Info': 'id=level_radio3',
                          'Debug': 'id=level_radio4',
                          'Trace': 'id=level_radio5'}

        if log_level is not None:
            if log_level not in log_levels_map:
                raise ValueError('Invalid log level - "%s".' % (log_level,))

            if not self._is_log_level_supported(log_levels_map[log_level]):
                raise guiexceptions.ConfigError('"%s" log level is not supported' % (log_level,))

            self._click_radio_button(log_levels_map[log_level])
            self._info('Selected "%s" log level.' % (log_level,))

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
        self._info('Set maximum number of files to store to "%s".' % (max_files,))
        self.input_text(MAX_FTP_FILES_TEXTBOX, max_files)

    def _setup_ftp_push_retrieval(self, hostname, directory, username, password):
        self._info('Configuring FTP push retrieval.')
        self._click_radio_button(FTP_PUSH_RADIOBUTTON)

        self._fill_ftp_push_hostname(hostname)

        self._fill_ftp_push_directory(directory)

        self._fill_ftp_push_username(username)

        self._fill_ftp_push_password(password)

    def _fill_ftp_push_retr_interval(self, interval):
        self.input_text(FTP_INTERVAL_TEXTBOX, interval)

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

    def _fill_scp_push_retr_interval(self, interval):
        self.input_text(SCP_INTERVAL_TEXTBOX, interval)

    def _fill_scp_push_hostname(self, host):
        self.input_text(SCP_HOST_TEXTBOX, host)

    def _fill_scp_push_port(self, port):
        if port is not None:
            self.input_text(SCP_PORT_TEXTBOX, port)
            self._info('Set port to "%s".' % (port,))

    def _fill_scp_push_directory(self, directory):
        self.input_text(SCP_DIRECTORY_TEXTBOX, directory)
        self._info('Using "%s" directory for scp.' % (directory,))

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
                                                     facility=None):
        self._info('Configuring Syslog push retrieval.')
        if not self._is_retrieval_supported(SYSLOG_PUSH_RADIOBUTTON):
            raise guiexceptions.ConfigError('syslog push retrieval is not supported')
        self._click_radio_button(SYSLOG_PUSH_RADIOBUTTON)

        self._fill_syslog_hostname(hostname)

        if protocol is not None:
            self._select_syslog_protocol(protocol.lower())

        if facility:
            self._select_syslog_facility(facility)

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

    def _select_syslog_facility(self, facility):
        facilities = self.get_list_items(SYSLOG_FACILITY_LIST)
        if facility in facilities:
            self.select_from_list(SYSLOG_FACILITY_LIST,
                                   SYSLOG_FACILITY_ITEM(facility))
            self._info('Selected "%s" syslog facility.' % (facility,))
        else:
            raise ValueError('"%s" facility is not available.' % (facility,))

    def _select_include_passwords(self, include_pwd):
        if include_pwd is not None:
            if not self._is_element_present(INCLUDE_PASSWORDS_RADIOBUTTON):
                raise guiexceptions.ConfigError('Passwords inclusion is not supported')

            if include_pwd:
                self._click_radio_button(INCLUDE_PASSWORDS_RADIOBUTTON)
                self._info('Enabled password inclusion')
            else:
                self._click_radio_button(EXCLUDE_PASSWORDS_RADIOBUTTON)
                self._info('Disabled password inclusion')

    def _click_edit_settings_button(self):
        self.click_button(EDIT_SETTINGS_BUTTON)
        self._info('Clicked "Edit Settings button')

    def _fill_metrics_frequency(self, timeout):
        if timeout is not None:
            self.input_text(METRICS_FREQUENCY_TEXTBOX, timeout)
            self._info('Selected "%s" metrics frequency.' % (timeout,))

    def _check_mid_logging(self, enable):
        if enable is not None:
            if enable:
                self.select_checkbox(LOG_MID_CHECKBOX)
                self._info('Enabled mid logging')
            else:
                self.unselect_checkbox(LOG_MID_CHECKBOX)
                self._info('Disabled mid logging')

    def _check_subject_logging(self, enable):
        if enable is not None:
            if enable:
                self.select_checkbox(LOG_SUBJECT_CHECKBOX)
                self._info('Enabled subject logging')
            else:
                self.unselect_checkbox(LOG_SUBJECT_CHECKBOX)
                self._info('Disabled mid logging')

    def _check_response_logging(self, enable):
        if enable is not None:
            if enable:
                self.select_checkbox(LOG_RESPONSE_CHECKBOX)
                self._info('Enabled response logging')
            else:
                self.unselect_checkbox(LOG_RESPONSE_CHECKBOX)
                self._info('Disabled mid logging')

    def _fill_custom_headers(self, headers):
        if headers is not None:
            headers_text = headers.replace(';','\n')
            self.input_text(CUSTOM_HEADERS_TEXTBOX, headers_text)
            self._info('Added custom headers "%s"' % (headers,))

    def _set_rollover_interval(self, interval=None):
        time_pattern = r"((?:\d\d|\*):(?:\d\d|\*))"
        week_days = ['monday',
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
                            day = day.strip().lower()
                            if day not in week_days:
                                raise guiexceptions.ConfigError('There are no such day of the week')
                            if day.strip().lower() == week_days[i]:
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

    def _fill_log_subscription_page(self, log_type, log_name, filename,
                     log_size, rollover_interval, log_level, include_pwd,logged_events,time_limit):

        self._select_log_type(log_type)

        self._set_log_name(log_name)

        self._set_log_filename(filename)

        self._set_max_logfile_size(log_size)

        self._set_rate_limit(logged_events,time_limit)

        self._set_rollover_interval(rollover_interval)

        self._select_log_level(log_level)

        self._select_include_passwords(include_pwd)

        self._click_submit_button()

    def log_subscriptions_add_log(self, log_type, log_name, filename=None,
                    log_size=None, rollover_interval=None,log_level=None,
                    include_pwd=None,logged_events=None,time_limit=None):
        """Add new log subscription.

        Parameters:
            - `log_type`: type of log to associate with the subscription. It is
              suggested to use log_types constant.
            - `log_name`: name for the log subscription.
            - `filename`: name for the log file. If None, default value will be
              used.
            - `log_size`: maximum file size in bytes the log file can be.
            - `rollover_interval`: time interval to roll over log. If None,
              default value will be used.
            - `log_level`: log level to use. If None, default value will be
              used.
            - `include_pwd`: include passwords in Log. Applies only to
              'Configuration History Logs'.

        Examples:
        | Log Subscriptions Add Log | ${sma_log_types.BACKUP} | testLog |
        | | filename=test_log |  log_size=5M | log_level=Debug |
        | Log Subscriptions Add Log | ${sma_log_types.CONF_HISTORY} |
        | | test_logs | include_pwd=yes |

        Exception:
            - `ConfigError`: in case if day of the week in rollover_interval is
              invalid.
        """

        self._open_page()

        self._click_add_log_subscriptions_button()

        self._fill_log_subscription_page(log_type, log_name, filename,
                    log_size, rollover_interval, log_level, include_pwd,logged_events,time_limit)

    def log_subscriptions_edit_log(self, log_name, new_log_name=None,
                filename=None, log_size=None, rollover_interval=None,
                log_level=None, include_pwd=None,logged_events=None,time_limit=None):
        """Edit log subscription.

        Parameters:
            - `log_name`: name of the log to edit.
            - `new_log_name`: new name for the log subscription. If None, value
              will be left unchanged.
            - `filename`: name for the log file. If None, value will be left
              unchanged.
            - `log_size`: maximum file size in bytes the log file can be. If
              None, value will be left unchaged.
            - `rollover_interval`: time interval to roll over log. If None,
              default value will be used.
            - `log_level`: log level to use. If None, value will be left
              unchanged.
            - `include_pwd`: include passwords in Log. Applies only to
              'Configuration History Logs'.
        Examples:
        | Log Subscriptions Edit Log | test_log | new_log_name=new_test_log
        | | filename=log_file | log_size=6M | log_level=Debug |
        | Log Subscriptions Edit Log | new_test_log | rollover_interval=10:15 |

        Exception:
            - `ConfigError`: in case if day of the week in rollover_interval is
              invalid.
        """

        self._open_page()

        self._click_edit_log_link(log_name)

        self._fill_log_subscription_page(None, new_log_name, filename,
                    log_size, rollover_interval, log_level, include_pwd,logged_events,time_limit)

    def log_subscriptions_delete(self, log_name):
        """Delete log subscription.

        Parameters:
            - `log_name`: name of the log subscription to delete.
        Examples:
        | Log Subscriptions Delete | backup_logs |
        """

        self._open_page()

        self._click_delete_log_link(log_name)

        self._click_continue_button()

    def log_subscriptions_rollover(self, log_names):
        """Rollover log subscription.

        Parameters:
            - `log_names`: names of the log subscriptions to rollover.
              If 'All', all currently configured log subscriptions will be
              rolled over.
        Examples:
        | Log Subscriptions Rollover | cli_logs, backup_logs |
        | Log Subscriptions Rollover | All |
        """

        self._open_page()

        if log_names == 'All':
            self._check_all_logs_to_rollover()
        else:
            log_names = self._convert_to_tuple(log_names)
            for log_name in log_names:
                self._check_log_to_rollover(log_name)

        self._click_rollover_button()

    def log_subscriptions_edit_settings(self, metrics_timeout=None,
            log_mid_header=None, log_subject=None, log_response=None,
            headers=None):
        """Edit log subscriptions global settings.

        Parameters:
            - `metrics_timeout`: the amount of time, in seconds, that the
              system waits between recording metrics. If None value will be
              left unchanged.
            - `log_mid_header`: record the Message ID headers. Boolean. If
              None value will be left unchanged.
            - `log_subject`: record the subject header of the original message.
              Boolean. If None value will be left unchanged.
            - `log_response`: record the remote response status code. Boolean.
              If None value will be left unchanged.
            - `headers`: a strings of headers that should be logged
              for each message. If None value will be left unchanged.

        Examples:
        | Log Subscriptions Edit Settings | metrics_timeout=timeout |
        | | log_mid_header=off | log_subject=on | log_response=off |
        """

        self._open_page()

        self._click_edit_settings_button()

        self._fill_metrics_frequency(metrics_timeout)

        self._check_mid_logging(log_mid_header)

        self._check_subject_logging(log_subject)

        self._check_response_logging(log_response)

        self._fill_custom_headers(headers)

        self._click_submit_button()

    def log_subscriptions_set_retrieval_method_to_manually_download(self,
                    log_name, max_num_files=None, filename=None):
        """Change retrieval method of the log subctription to FTP Poll.

        Parameters:
            - `log_name`: name of the log to edit.
            - `max_num_files`: maximum number of files. If None then default
              value will be used and value will be updated
            - `filename`: name for the log file. If None, value will be left
              unchanged. This value is required when former Retrieval Method was
              Syslog Push.

        Examples:
            | Log Subscriptions Set Retrieval Method to Manually Download | backup_logs | 20 |
            | Log Subscriptions Set Retrieval Method to Manually Download | cli_logs | max_num_files=15 | filename=my_cli |
        """

        self._open_page()

        self._click_edit_log_link(log_name)

        self._setup_ftp_poll_retrieval(max_num_files)

        self._set_log_filename(filename)

        self._click_submit_button()

    def log_subscriptions_set_retrieval_method_to_ftp_push(self, log_name,
                     hostname, directory, username, password, filename=None):
        """Change retrieval method of the log subctription to FTP Push.

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
        | Log Subscriptions Set Retrieval Method to FTP Push | backup_logs | myftp.sma | /logs/ | testuser | ironport |
        | Log Subscriptions Set Retrieval Method to FTP Push | cli_logs | myftp.sma | /logs/ | testuser | ironport | filename=cli |
        """

        self._open_page()

        self._click_edit_log_link(log_name)

        self._setup_ftp_push_retrieval(hostname, directory, username, password)

        self._set_log_filename(filename)

        self._click_submit_button()

    def log_subscriptions_set_retrieval_method_to_scp_push(self, log_name,
                    hostname, directory, username, port=None,
                    enable_key_checking=None, key=None, filename=None):
        """Change retrieval method of the log subctription to SCP Push.

        Parameters:
            - `log_name`: name of the log to edit.
            - `hostname`: hostname of the SSH server
            - `directory`: directory on the SSH server where logs
              will be pushed
            - `username`: user name to the SSH server
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
            | Log Subscriptions Set Retrieval Method to SCP Push | backup_logs | myhost.sma | /logs/ | testuser |
            | Log Subscriptions Set Retrieval Method to SCP Push | cli_logs | myhost.sma | / | testuser |
            | | enable_key_cheking=${True} | key="ssh-rsa <long key data string>" | filename=cli |
        """

        self._open_page()

        self._click_edit_log_link(log_name)

        self._setup_scp_push_retrieval(hostname, directory, username,
                    port, enable_key_checking, key)

        self._set_log_filename(filename)

        self._click_submit_button()

    def log_subscriptions_set_retrieval_method_to_syslog_push(self, log_name,
                        hostname, protocol=None, facility=None):
        """Change retrieval method of the log subctription to Syslog Push.

        Parameters:
            - `log_name`: name of the log to edit.
            - `hostname`: hostname of the Syslog server
            - `protocol`: protocol to be used either 'UDP' or 'TCP'. If
              None, default UDP will be used.
            - `facility`: name of facility to be used. If None, default value will be used.

        Examples:
        | Log Subscriptions Set Retrieval Method to Syslog Push | baclup_logs | mysysloghost.sma |
        | Log Subscriptions Set Retrieval Method to Syslog Push | cli_logs | mysysloghost.sma | protocol=TCP | facility=console |
        """

        self._open_page()

        self._click_edit_log_link(log_name)

        self._setup_syslog_push_retrieval(hostname, protocol, facility)

        self._click_submit_button()

    def log_subscriptions_get_logs(self):
        """ Gets existing log subscriptions

        Parameters:
            None

        Return:
            - dictionary of existing log subscriptions

        Exception:
            None

        Examples:
            | @{logs} | Log Subscriptions Get Logs |
        """
        self._info('log_subscriptions_get_logs')
        self._open_page()

        entries = {}
        num_of_entries = int(self.get_matching_xpath_count(CONFIGURED_LOG_SUBSCRIPTION(1, '*', 1)))

        for row in xrange(2, num_of_entries):
            name = self.get_text(CONFIGURED_LOG_SUBSCRIPTION(1, row, 1))
            type = self.get_text(CONFIGURED_LOG_SUBSCRIPTION(1, row, 2))
            file = self.get_text(CONFIGURED_LOG_SUBSCRIPTION(1, row, 3))
            interval = self.get_text(CONFIGURED_LOG_SUBSCRIPTION(1, row, 4))
            entries[name] = [type, file, interval]

        return entries

    def log_subscriptions_get_global_settings(self):
        """ Gets log subscriptions global settings

        Parameters:
            None

        Return:
            - existing log subscriptions global settings

        Exception:
            None

        Examples:
            | @{settings} | Log Subscriptions Get Glogal Settings |
        """
        self._info('log_subscriptions_get_global_settings')
        self._open_page()

        entries = {}
        entries['frequency'] = self.get_text(FREQUENCY)
        entries['message_id'] = self.get_text(LOGGIN_OPTIONS(1))
        entries['subject'] = self.get_text(LOGGIN_OPTIONS(2))
        entries['responce'] = self.get_text(LOGGIN_OPTIONS(3))
        entries['headers'] = self.get_text(LOGGIN_OPTIONS(4))

        return entries
