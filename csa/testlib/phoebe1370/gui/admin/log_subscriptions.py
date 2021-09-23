#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/phoebe1350/gui/admin/log_subscriptions.py#1 $ $DateTime: 2020/01/06 01:25:43 $ $Author: saurgup5 $

import functools
import traceback

from common.gui.decorators import go_to_page
from common.gui.guicommon import GuiCommon
import common.gui.guiexceptions as guiexceptions

from log_subscriptions_def.subscription_settings import SubscriptionSettings
from log_subscriptions_def.subscriptions_global_settings import \
                                                 SubscriptionsGlobalSettings
from log_subscriptions_def.subscription_files import SubscriptionFiles


ADD_SUBSCRIPTION_BUTTON = "//input[@name='AddListener']"
SUBSCRIPTION_TABLE = "//table[@class='cols']"
LOG_ROWS = "%s/tbody/tr" % (SUBSCRIPTION_TABLE,)
# index starts from 1
LOG_NAME_CELL = lambda index: "%s[%d]/td[1]" % (LOG_ROWS, index)
SUBSCRIPTION_EDIT_LINK = lambda name: "%s//a[normalize-space()='%s']" % \
                        (SUBSCRIPTION_TABLE, name)
SUBSCRIPTION_FILES_LINK = lambda name: "%s//td[normalize-space()='%s']"\
                        "/following-sibling::td[2]/a" % \
                        (SUBSCRIPTION_TABLE, name)
SUBSCRIPTION_ROLLOVER_CHECKBOX = lambda name: "%s//td[normalize-space()='%s']"\
                        "/following-sibling::td[5]/input" % \
                        (SUBSCRIPTION_TABLE, name)
SUBSCRIPTION_ROLLOVER_ALL_CHECKBOX = "//input[@name='rollover_all']"
SUBSCRIPTION_DELETE_LINK = lambda name: "%s//td[normalize-space()='%s']"\
                        "/following-sibling::td[6]/img" % \
                        (SUBSCRIPTION_TABLE, name)
ROLLOVER_NOW_BUTTON = "//input[@name='_rollover']"
EDIT_GLOBAL_SETTINGS_BUTTON = "//input[@name='EditGlobals']"
# Log Files entry
DELETE_BUTTON = "//input[@value='Delete']"
BACK_BUTTON = "//input[@value='< Back']"


PAGE_PATH = ('System Administration', 'Log Subscriptions')


def go_to_log_files(func):
    """Decorator is used for LogSubscriptions class methods
    for navigating to subscription files entry.
    The first decorated method parameter should be the
    log subscription name

    *Exceptions:*
    - `ValueError`: if log subscription named `log_name` is
    not found or it contains no log files (for example when
    its retrieval method is set to Syslog Push)
    """
    @functools.wraps(func)
    def decorator(self, log_name, *args, **kwargs):
        if self._is_element_present(SUBSCRIPTION_FILES_LINK(log_name)):
            self.click_link(SUBSCRIPTION_FILES_LINK(log_name))
        else:
            raise ValueError('Log subscription named "%s" is not found or '\
                             'it contains no log files' % \
                             (log_name,))

        return func(self, log_name, *args, **kwargs)
    return decorator


class LogSubscriptions(GuiCommon):
    """Keywords for GUI interaction with ESA page
    System Administration -> Log Subscriptions
    """

    def get_keyword_names(self):
        return ['log_subscriptions_add',
                'log_subscriptions_edit',
                'log_subscriptions_delete',
                'log_subscriptions_get_all',
                'log_subscriptions_rollover',
                'log_subscriptions_download_file',
                'log_subscriptions_get_files_details',
                'log_subscriptions_delete_log_files',
                'log_subscriptions_edit_settings']

    def _get_subscription_settings_controller(self):
        if not hasattr(self, '_subscription_settings_controller'):
            self._subscription_settings_controller = SubscriptionSettings(self)
        return self._subscription_settings_controller

    def _get_global_settings_controller(self):
        if not hasattr(self, '_global_settings_controller'):
            self._global_settings_controller = SubscriptionsGlobalSettings(self)
        return self._global_settings_controller

    def _get_subscription_files_controller(self):
        if not hasattr(self, '_subscription_files_controller'):
            self._subscription_files_controller = SubscriptionFiles(self)
        return self._subscription_files_controller

    @go_to_page(PAGE_PATH)
    def log_subscriptions_add(self, log_type, log_name, settings):
        """Add new log subscription

        *Parameters:*
        - `log_type`: type of log to associate with the subscription.
        There are next log types available:
        | Anti-Spam Archive |
        | Anti-Spam Logs |
        | Anti-Virus Archive |
        | Anti-Virus Logs |
        | Authentication Logs |
        | Bounce Logs |
        | CLI Audit Logs |
        | Configuration History Logs |
        | Delivery Logs |
        | Domain Debug Logs |
        | Encryption Logs |
        | FTP Server Logs |
        | HTTP Logs |
        | Injection Debug Logs |
        | IronPort Text Mail Logs |
        | LDAP Debug Logs |
        | NTP logs |
        | Reporting Logs |
        | Reporting Query Logs |
        | Reputation Engine Logs |
        | SMTP Conversation Logs |
        | SNMP Logs |
        | Safe/Block Lists Logs |
        | Scanning Logs |
        | Spam Quarantine GUI Logs |
        | Spam Quarantine Logs |
        | Status Logs |
        | System Logs |
        | Tracking Logs |
        | Updater Logs |
        | qmail Format Mail Logs |
        - `log_name`: name for the new log subscription.
        - `settings`: dictionary containing new subscription settings.
        Its actually, its items set depends on chosen log type. All possible
        items are:
        | `File Name` | log file name |
        | `Rollover by File Size` | maximum log file size. You can add a
        trailing K or M to indicate size units |
        | `Rollover by Time` | time period for log rollover. Either "None",
        "Daily Rollover", "Weekly Rollover" or "Custom Time Interval" |
        | `Custom Rollover Interval` | custom log files rollover interval,
        for example 120s, 5m 30s, 4h, 2d. mndatory if `Rollover by Time` is
        set to "Custom Time Interval" |
        | `Log Level` | minimum log level of messages to be stored in log,
        either "Critical" or "Warning" or "Information" or "Debug" or
        "Trace" |
        | `Retrieval Method` | log files retrieval method, either
        "Manually Download Logs" or "FTP Push to Remote Server"
        or "SCP Push to Remote Server" or "Syslog Push" |
        | `Maximum Files` | maximum number of files retained on the appliance.
        Available only if `Retrieval Method` is set to "Manually Download Logs" |
        | `FTP Host` | FTP host name. Mandatory if `Retrieval Method` is set to
        "FTP Push to Remote Server" |
        | `FTP Directory` | FTP directory name. Mandatory if `Retrieval Method` is
        set to "FTP Push to Remote Server" |
        | `FTP Username` | FTP user name. Mandatory if `Retrieval Method` is
        set to "FTP Push to Remote Server" |
        | `FTP Password` | FTP password. Available if `Retrieval Method` is
        set to "FTP Push to Remote Server" |
        Available if `Retrieval Method` is set to "SCP Push to Remote Server" |
        | `SCP Host` | SCP host name. Mandatory if `Retrieval Method` is set to
        "SCP Push to Remote Server" |
        | `SCP Port` | SCP port number. Available if `Retrieval Method` is set to
        "SCP Push to Remote Server" |
        | `SCP Directory` | SCP directory name. Mandatory if `Retrieval Method` is
        set to "SCP Push to Remote Server" |
        | `SCP Username` | SCP user name. Mandatory if `Retrieval Method` is
        set to "SCP Push to Remote Server" |
        | `Enable Host Key Checking` | whether to enable host key checking for SCP.
        Either ${True} or ${False} |
        | `Host Key Checking` | host key checking settings. Either "Automatically
        Scan" or key fingerprint string. Available only if `Enable Host Key Checking`
        is set to ${True} |
        | `Hostname` | name of the host used for syslog push. Mandatory if
        `Retrieval Method` is set to "Syslog Push" |
        | `Syslog Push Protocol` | Syslog Push protocol. Either "UDP" or "TCP".
        Available if `Retrieval Method` to "Syslog Push" |
        | `Facility` | syslog push facility. Either "auth", "authpriv", "console",
        "daemon", "ftp", "local0", "local1", "local2", "local3", "local4",
        "local5", "local6", "local7", "mail", "ntp", "security", "user" |

        *Exceptions:*
        - `ValueError`: if any of given values is not correct

        *Examples:*
        | ${settings}= | Create Dictionary |
        | ... | File Name | antispam_archive.mbox |
        | ... | Rollover by File Size | 15M |
        | ... | Rollover by Time | Custom Time Interval |
        | ... | Custom Rollover Interval | 2d |
        | ... | Retrieval Method | Manually Download Logs |
        | ... | Maximum Files | 15 |
        | Log Subscriptions Add | Anti-Spam Archive | my_anti_spam |
        | ... | ${settings} |
        """
        self.click_button(ADD_SUBSCRIPTION_BUTTON)

        controller = self._get_subscription_settings_controller()
        settings.update({'Log Type': log_type,
                         'Log Name': log_name})
        controller.set(settings)
        self._click_submit_button()

    @go_to_page(PAGE_PATH)
    def log_subscriptions_edit(self, log_name, settings={}):
        """Edit log subscription

        *Parameters:*
        - `log_name`: name for the existing log subscription.
        - `settings`: dictionary containing new subscription settings.
        Its actually, its items set depends on chosen log type. All possible
        items are:
        | `Log Name` | new log subcription name |
        | `File Name` | log file name |
        | `Rollover by File Size` | maximum log file size. You can add a
        trailing K or M to indicate size units |
        | `Rollover by Time` | time period for log rollover. Either "None",
        "Daily Rollover", "Weekly Rollover" or "Custom Time Interval" |
        | `Custom Rollover Interval` | custom log files rollover interval,
        for example 120s, 5m 30s, 4h, 2d. mndatory if `Rollover by Time` is
        set to "Custom Time Interval" |
        | `Log Level` | minimum log level of messages to be stored in log,
        either "Critical" or "Warning" or "Information" or "Debug" or
        "Trace" |
        | `Retrieval Method` | log files retrieval method, either
        "Manually Download Logs" or "FTP Push to Remote Server"
        or "SCP Push to Remote Server" or "Syslog Push" |
        | `Maximum Files` | maximum number of files retained on the appliance.
        Available only if `Retrieval Method` is set to "Manually Download Logs" |
        | `FTP Host` | FTP host name. Mandatory if `Retrieval Method` is set to
        "FTP Push to Remote Server" |
        | `FTP Directory` | FTP directory name. Mandatory if `Retrieval Method` is
        set to "FTP Push to Remote Server" |
        | `FTP Username` | FTP user name. Mandatory if `Retrieval Method` is
        set to "FTP Push to Remote Server" |
        | `FTP Password` | FTP password. Available if `Retrieval Method` is
        set to "FTP Push to Remote Server" |
        Available if `Retrieval Method` is set to "SCP Push to Remote Server" |
        | `SCP Host` | SCP host name. Mandatory if `Retrieval Method` is set to
        "SCP Push to Remote Server" |
        | `SCP Port` | SCP port number. Available if `Retrieval Method` is set to
        "SCP Push to Remote Server" |
        | `SCP Directory` | SCP directory name. Mandatory if `Retrieval Method` is
        set to "SCP Push to Remote Server" |
        | `SCP Username` | SCP user name. Mandatory if `Retrieval Method` is
        set to "SCP Push to Remote Server" |
        | `Enable Host Key Checking` | whether to enable host key checking for SCP.
        Either ${True} or ${False} |
        | `Host Key Checking` | host key checking settings. Either "Automatically
        Scan" or key fingerprint string. Available only if `Enable Host Key Checking`
        is set to ${True} |
        | `Hostname` | name of the host used for syslog push. Mandatory if
        `Retrieval Method` is set to "Syslog Push" |
        | `Syslog Push Protocol` | Syslog Push protocol. Either "UDP" or "TCP".
        Available if `Retrieval Method` to "Syslog Push" |
        | `Facility` | syslog push facility. Either "auth", "authpriv", "console",
        "daemon", "ftp", "local0", "local1", "local2", "local3", "local4",
        "local5", "local6", "local7", "mail", "ntp", "security", "user" |

        *Exceptions:*
        - `ValueError`: if any of given values is not correct

        *Examples:*
        | ${settings1}= | Create Dictionary |
        | ... | Retrieval Method | FTP Push to Remote Server |
        | ... | FTP Host | 8.8.8.8 |
        | ... | FTP Directory | logs |
        | ... | FTP Username  | test |
        | ... | FTP Password | test |
        | ${settings2}= | Create Dictionary |
        | ... | Retrieval Method | SCP Push to Remote Server |
        | ... | SCP Host | 8.8.8.8 |
        | ... | SCP Port | 22 |
        | ... | SCP Directory | logs |
        | ... | SCP Username | test |
        | ... | Enable Host Key Checking | ${True} |
        | ... | Host Key Checking | my key |
        | ${settings3}= | Create Dictionary |
        | ... | Retrieval Method | Syslog Push |
        | ... | Hostname | 8.8.8.8 |
        | ... | Syslog Push Protocol | TCP |
        | ... | Facility | auth |
        | Log Subscriptions Edit | my_anti_spam |
        | ... | ${settings1} |
        | Log Subscriptions Edit | my_anti_spam |
        | ... | ${settings2} |
        | Log Subscriptions Edit | my_anti_spam |
        | ... | ${settings3} |
        """
        if self._is_element_present(SUBSCRIPTION_EDIT_LINK(log_name)):
            self.click_link(SUBSCRIPTION_EDIT_LINK(log_name))
        else:
            raise ValueError('Log subscription named "%s" is not found' % \
                             (log_name,))

        controller = self._get_subscription_settings_controller()
        controller.set(settings)
        self._click_submit_button()

    @go_to_page(PAGE_PATH)
    def log_subscriptions_delete(self, log_name):
        """Delete log subscription

        *Parameters:*
        - `log_name`: name of the log subscription to be deleted

        *Exceptions:*
        - `ValueError`: in case of non existing log subscription name

        *Examples:*
        | Log Subscriptions Delete | antispam |
        """
        if self._is_element_present(SUBSCRIPTION_DELETE_LINK(log_name)):
            self.click_element(SUBSCRIPTION_DELETE_LINK(log_name), 'don\'t wait')
        else:
            raise ValueError('Log subscription named "%s" is not found' % \
                             (log_name,))
        self._click_continue_button()

    @go_to_page(PAGE_PATH)
    def log_subscriptions_rollover(self, log_names):
        """Rollover log subscription(s)

        *Parameters:*
        - `log_names`: list containing log names
        to be rolled over. Can be the 'all' string to rollover
        all existing log subscriptions.

        *Exceptions:*
        - `ValueError`: in case of invalid log name

        *Examples:*
        | @{names}= | Create List | antispam | antivirus |
        | Log Subscriptions Rollover | ${names} |
        """
        if not log_names:
            raise ValueError('There should be at least one log name')

        if isinstance(log_names, basestring) and log_names.upper() == 'ALL':
            self._select_checkbox(SUBSCRIPTION_ROLLOVER_ALL_CHECKBOX)
        else:
            if isinstance(log_names, basestring):
                log_names = (log_names,)
            for log_name in log_names:
                if self._is_element_present(SUBSCRIPTION_ROLLOVER_CHECKBOX(log_name)):
                    self._select_checkbox(SUBSCRIPTION_ROLLOVER_CHECKBOX(log_name))
                else:
                    raise ValueError('There is no log subscription named "%s"' % \
                                     (log_name,))
        self.click_button(ROLLOVER_NOW_BUTTON)
        self._check_action_result()

    @go_to_page(PAGE_PATH)
    def log_subscriptions_edit_settings(self, settings={}):
        """Edit log subscriptions global settings

        *Parameters:*
        - `settings`: dictionary whose items are setting names and
        their values. Possible items are:
        | `System Metrics Frequency` | system metrics frequency in seconds |
        | `Message-ID Headers in Mail Logs` | whether to include message-id
        headers in mail logs. Either ${True} or ${False} |
        | `Original Subject Header of Each Message` | whether to include
        original subject header of each message in logs.
        Either ${True} or ${False} |
        | `Remote Response Text in Mail Logs` | whether to include remote
        response text in mail logs. Either ${True} or ${False} |
        | `List of Headers to Record in the Log Files` | comma separated
        list of headers to record in the log files |

        *Exceptions:*
        - `ValueError`: if any setting is not correct

        *Examples:*
        | ${new_settings}= | Create Dictionary |
        | ... | System Metrics Frequency | 20 |
        | ... | Message-ID Headers in Mail Logs | ${False} |
        | ... | Original Subject Header of Each Message | ${False} |
        | ... | Remote Response Text in Mail Logs | ${False} |
        | ... | List of Headers to Record in the Log Files | bla, bla |
        | Log Subscriptions Edit Settings | ${new_settings} |
        """
        self.click_button(EDIT_GLOBAL_SETTINGS_BUTTON)

        controller = self._get_global_settings_controller()
        controller.set(settings)
        self._click_submit_button()

    @go_to_page(PAGE_PATH)
    def log_subscriptions_get_all(self):
        """Get all the configured log subscriptions names

        *Return:*
        List of log subscriptions names

        *Examples:*
        | @{all_subscriptions}= | Log Subscriptions Get All |
        | Log Many | @{all_subscriptions} |
        | List Should Contain Value | ${all_subscriptions} | antispam |
        """
        logs_count = int(self.get_matching_xpath_count(LOG_ROWS))
        all_logs = []
        for index in xrange(2, logs_count + 1):
            all_logs.append(self.get_text(LOG_NAME_CELL(index)))
        return all_logs

    @go_to_page(PAGE_PATH)
    @go_to_log_files
    def log_subscriptions_get_files_details(self, log_name):
        """Get the details of all log files available under
        given log subscription name

        *Parameters:*
        - `log_name`: name of the log subscription to get file details
        from

        *Exceptions:*
        - `ValueError`: if log subscription with given name does not exist

        *Return:*
        List of dictionaries. Each dictionary has the next items:
        | `File Name` | log file name |
        | `Date` | creation date |
        | `Size` | log file size |

        *Examples:*
        | @{details}= | Log Subscriptions Get Files Details | antispam |
        | ${entry0}= | Get From List | @{details} | 0 |
        | Dictionary Should Contain Value | ${entry0} | antispam.current |
        """
        controller = self._get_subscription_files_controller()
        details = controller.get_details()
        self.click_button(BACK_BUTTON)
        return details

    @go_to_page(PAGE_PATH)
    @go_to_log_files
    def log_subscriptions_delete_log_files(self, log_name, file_names):
        """Delete the log file under the given log subscription

        *Parameters:*
        - `log_name`: name of log subscription for which log
        file has to be deleted
        - `file_names`: list of file names to be deleted. Can be the
        "all" string to delete all files

        *Exceptions:*
        - `ValueError`: if log subscription with given name was not found
        or particular file name was not found
        - `ConfigError`: if there are no files for removal in given
        log subscription

        *Examples:*
        | @{details}= | Log Subscriptions Get Files Details |
        | ... | antispam |
        | ${files_count}= | Get Length | ${details} |
        | Run Keyword If | ${files_count} > 1 |
        | ... | Log Subscriptions Delete Log Files | ${STANDARD_SUBSCRIPTION_NAME} |
        | ... | all |
        """
        controller = self._get_subscription_files_controller()
        controller.delete(file_names)
        self.click_button(DELETE_BUTTON, 'don\'t wait')
        try:
            self._click_continue_button()
        except Exception:
            raise guiexceptions.ConfigError('There are no log files present '\
                                            'in log subscription "%s" available '\
                                            'for removal' % (log_name,))
        self.click_button(BACK_BUTTON)

    @go_to_page(PAGE_PATH)
    @go_to_log_files
    def log_subscriptions_download_file(self, log_name, file_name):
        """ Download the file under the given log subscription

        *Parameters:*
        - `log_name`: name of log subscription for which log
        file has to be downloaded
        - `file_name`: file name to download

        *Examples:*
        | Log Subscriptions Download File | ${log_name} | ${file_name} |

        """
        controller = self._get_subscription_files_controller()
        controller.download_file(file_name)

