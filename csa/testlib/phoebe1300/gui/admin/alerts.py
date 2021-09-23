#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/phoebe1300/gui/admin/alerts.py#2 $ $DateTime: 2019/07/08 21:55:07 $ $Author: sparampa $

import time

from common.gui.decorators import go_to_page, set_speed
from common.gui.guicommon import GuiCommon
from common.util.sarftime import CountDownTimer
from common.gui.guiexceptions import TimeoutError

from alerts_def.severity_settings import SeveritySettings
from alerts_def.global_settings import AlertsGlobalSettings

# Main page
ADD_ALERT_RCPT_BTN = "//input[@value='Add Recipient...']"
VIEW_TOP_ALERTS_BTN = "//input[@value='View Top Alerts']"
EDIT_SETTINGS_BTN = "//input[@value='Edit Settings...']"

PROFILES_TABLE = "//table[@class='cols']"

PROFILE_EDIT_LINK = lambda name: "%s/descendant::a[contains(normalize-space(), '%s')]" % \
                                 (PROFILES_TABLE, name)

PROFILE_DELETE_LINK = lambda name: "%s//td[normalize-space()='%s']" \
                                   "/following::td[13]/img" % \
                                   (PROFILES_TABLE, name)

PAGE_PATH = ('System Administration', 'Alerts')

CONFIRM_DIALOG = "//div[@id='confirmation_dialog']"
SUBMIT_BUTTON = "//input[@value='Submit']"

ALERT_TABLE_BODY = "//div[@id='basic']//tbody[2]"
ALERT_TABLE_BODY_CELL = lambda num_id, header_name: "%s/tr[%s]/td[contains(@class, '%s')]" % \
                                                    (ALERT_TABLE_BODY, num_id, header_name)
ALERT_TABLE_ALL_ROWS = "%s/tr" % (ALERT_TABLE_BODY)

ALERT_TABLE_ALL_HEADERS = "//div[@id='basic']/div[2]//th"
ALERT_TABLE_HEADERS_CELL = lambda num_id: "//div[@id='basic']/div[2]//th[%s]" % (num_id)
ALERTS_PAGE_OK_BTN = "//button[normalize-space()='OK']"


class Alerts(GuiCommon):
    """Keywords for interaction with ESA GUI System Administration ->
    Alerts page
    """

    def get_keyword_names(self):
        return ['alerts_recipient_add',
                'alerts_recipient_edit',
                'alerts_recipient_delete',

                'alerts_not_exists',
                'alerts_settings_edit',
                'alerts_get_top_view_details']

    def _get_severity_settings_controller(self):
        if not hasattr(self, '_severity_settings_controller'):
            self._severity_settings_controller = SeveritySettings(self)
        return self._severity_settings_controller

    def _get_global_settings_controller(self):
        if not hasattr(self, '_alerts_settings_controller'):
            self._alerts_settings_controller = AlertsGlobalSettings(self)
        return self._alerts_settings_controller

    def _wait_for_alert_page_loading(self):
        SLEEP_INTERVAL = 3
        TIMEOUT = 60
        tmr = CountDownTimer(TIMEOUT).start()
        while tmr.is_active():
            time.sleep(SLEEP_INTERVAL)
            if self._is_element_present(ALERT_TABLE_ALL_ROWS):
                return
        raise TimeoutError('View Alert Top page was not' \
                           ' loaded with %d-seconds timeout' % (TIMEOUT,))

    def alerts_not_exists(self, timeout=None):
        ACTION = "DISMISS"
        self.handle_alert(ACTION, timeout)
        self._debug('Alert cancelled')

    @go_to_page(PAGE_PATH)
    def alerts_recipient_add(self, rcpt_addr, release_support_notify, settings={}):
        """Add alert recipient

        *Parameters:*
        - `rcpt_addr`: alert recipient email. Separate multiple email addresses with commas
        - `release_support_notify`: Enable release and support notifications.
           Either ${True} or ${False}
        - `settings`: dictionary, whose items are:
        |   `All` | all alert severities to receive | Either ${True} or ${False} | do not need suffix |
        |   `System` | system alert severities to receive | Either ${True} or ${False} |
        |   `Hardware` | hardware alert severities to receive  | Either ${True} or ${False} |
        |   `Updater` | updater alert severities to receive | Either ${True} or ${False} |
        |   `Outbreak Filters` | outbreak-filters alert severities to receive | Either ${True} or ${False} |
        |   `Anti-Virus` | anti-virus alert severities to receive | Either ${True} or ${False} |
        |   `Anti-Spam` | anti-spam alert severities to receive | Either ${True} or ${False} |
        |   `Directory Harvest Attack Prevention` | dhap alert severities to receive | Either ${True} or ${False} |
            with suffixes options that are valid to be added to item name: |
        "All" , "Critical", "Warning", "Info" |

        e.g. :

        | All |
        | Anti-Virus Critical |
        | System All |
        | Directory Harvest Attack Prevention Warning |


        *Exceptions:*
        - `ValueError`: if any of passed values is not valid

        *Examples:*
        | ${alert_settings}= | Create Dictionary |
        | ... | All | ${True} |
        | ... | System All | ${False} |
        | ... | Anti-Virus Critical | ${False} |
        | ... | Outbreak Filters | ${True} |
        | ... | Directory Harvest Attack Prevention All | ${True} |
        | Alerts Recipient Add | wossap@testing.com | ${alert_settings} |
        """
        self.click_button(ADD_ALERT_RCPT_BTN)

        controller = self._get_severity_settings_controller()
        settings.update({'Recipient Address': rcpt_addr})
        settings.update({'Release and Support Notifications': release_support_notify})
        controller.set(settings)
        self._click_submit_button()

    @go_to_page(PAGE_PATH)
    def alerts_recipient_delete(self, rcpt_addr):
        """Delete alert recipient.

        *Parameters:*
        - `rcpt_addr`: email of existing alert recipient to delete.

        *Exceptions:*
        - `ValueError`: in case alert recipient with given email does not exist

        *Examples:*
        | Alerts Recipient Delete | alert_rcpt |
        """
        if self._is_element_present(PROFILE_DELETE_LINK(rcpt_addr)):
            self.click_element(PROFILE_DELETE_LINK(rcpt_addr), "don't wait")
        else:
            raise ValueError('There is no alert recipient named "%s"' % \
                             (rcpt_addr,))
        self._click_continue_button('Delete')

    @go_to_page(PAGE_PATH)
    def alerts_recipient_edit(self, rcpt_addr, release_support_notify, settings={}):
        """Edit alerts recipient.

        *Parameters:*
        - `rcpt_addr`: email address of the existing alerts recipient
        - `release_support_notify`: Enable release and support notifications
           Either ${True} or ${False}
        - `settings`: dictionary, whose items are:

        |   `All` | all alert severities to receive | Either ${True} or ${False} | do not need suffix |
        |   `System` | system alert severities to receive | Either ${True} or ${False} |
        |   `Hardware` | hardware alert severities to receive  | Either ${True} or ${False} |
        |   `Updater` | updater alert severities to receive | Either ${True} or ${False} |
        |   `Outbreak Filters` | outbreak-filters alert severities to receive | Either ${True} or ${False} |
        |   `Anti-Virus` | anti-virus alert severities to receive | Either ${True} or ${False} |
        |   `Anti-Spam` | anti-spam alert severities to receive | Either ${True} or ${False} |
        |   `Directory Harvest Attack Prevention` | dhap alert severities to receive | Either ${True} or ${False} |
            with suffixes options that are valid to be added to item name: |
        "All" , "Critical", "Warning", "Info" |

        *Exceptions:*
        - `ValueError`: if any of passed values is not valid or
        if alerts recipient with given name does not exist

        *Examples:*

        | ${alerts_settings}= | Create Dictionary |
        | ...  | Anti-Virus All |  ${True} |
        | ...  | Anti-Virus Critical |  ${False} |
        | ...  | Directory Harvest Attack Prevention All |  ${True} |
        | ...  | Hardware All |  ${True} |
        | ...  | System All |  ${True} |
        | ...  | System Critical |  ${False} |
        | Alerts Recipient Edit | test@test.com | ${alerts_settings} |
        """
        if self._is_element_present(PROFILE_EDIT_LINK(rcpt_addr)):
            self.click_link(PROFILE_EDIT_LINK(rcpt_addr))
        else:
            raise ValueError('There is no alerts recipient named "%s"' % \
                             (rcpt_addr,))

        controller = self._get_severity_settings_controller()
        settings.update({'Release and Support Notifications': release_support_notify})
        controller.set(settings)
        self._click_submit_button()

    @go_to_page(PAGE_PATH)
    def alerts_settings_edit(self, settings={}):
        """Edit global alerts recipient settings.

        *Parameters:*
        - `settings`: dictionary, whose items are:
        |  `From Address to Use When Sending Alerts` | choose option what email address to use when sending alerts.
                                             Either custom 'From address user' or default 'From address default' |
        |  `From Address to Use When Sending Alerts User Text` | input field for custom email to use when sending alerts.
                                            Can be used with the 'From address user' option only. |
        |  `Wait Before Sending a Duplicate Alert` |  checkbox to enable number of seconds to wait
                                            before sending alerts | Either ${True} or ${False} |
        |  `Initial Number of Seconds to Wait Before Sending a Duplicate Alert` | initial number of seconds
                                            to wait before sending alerts |
        |  `Maximum Number of Seconds to Wait Before Sending a Duplicate Alert` | maximum number of seconds
                                            to wait before sending alerts |
        |   `IronPort AutoSupport Enable` | enable IronPort autosupport | Either ${True} or ${False} |
        |   `IronPort AutoSupport Send Copy` | send copy of weekly AutoSupport reports to System Information Alert recipients.
                                            Either ${True} or ${False} |

        *Exceptions:*
        - `ValueError`: if any of passed values is not valid or
        if alerts recipient with given name does not exist

        *Examples:*

        | ${alerts_settings}= | Create Dictionary |
        | ...  | From Address to Use When Sending Alerts |  From address user |
        | ...  | From Address to Use When Sending Alerts User Text |  ${ALERT_EMAIL_RCPT} |
        | ...  | Wait Before Sending a Duplicate Alert |  ${True} |
        | ...  | IronPort AutoSupport Enable |  ${True} |
        | ...  | Initial Number of Seconds to Wait Before Sending a Duplicate Alert |  700 |
        | Alerts Settings Edit | ${alert_global_settings} |
        """

        self.click_button(EDIT_SETTINGS_BTN)

        settings_controller = self._get_global_settings_controller()
        settings_controller.set(settings)
        self._click_submit_button()

    @go_to_page(PAGE_PATH)
    @set_speed(0)
    def alerts_get_top_view_details(self):
        """View Top Alerts details.

        *Exceptions:*
        - `ValueError`: if there is no "View Top Alerts" button on the page

        *Return*
        - Returns dictionary with the following keys / values :
            | 'Date' | list of dates when the alert was generated |
            | 'Level' | list of error alert level |
            | 'Class' | list of alert class |
            | 'Text' | list of alerts text |
            | 'Recipient' | list of alert recipients |

        *Examples:*

        | ${top_alerts_dict}= |  Alerts Get Top View Details |
        | ${top_alerts_dict}= |  Alerts Get Top View Details |
        | ${keys}  |  Get Dictionary Keys  |   ${top_alerts_dict} |
        | ${rcpt_list} |  Get From Dictionary |  ${top_alerts_dict} |  Recipient |
        | ${list_length}|  Get Length |  ${rcpt_list} |
        """
        if self._is_element_present(VIEW_TOP_ALERTS_BTN):
            self.click_button(VIEW_TOP_ALERTS_BTN, 'don\'t wait')
            self._wait_for_alert_page_loading()
        else:
            raise ValueError('There is no "View Top Alerts" button on the page')

        tbl_row_count = int(self.get_matching_xpath_count(ALERT_TABLE_ALL_ROWS))
        tbl_heads_count = int(self.get_matching_xpath_count(ALERT_TABLE_ALL_HEADERS))
        top_alerts_dict = {}
        for item in xrange(1, tbl_heads_count + 1):
            key = self._get_text(ALERT_TABLE_HEADERS_CELL(item))
            cell_list = []
            for item in xrange(1, tbl_row_count + 1):
                cell_content = self._get_text(ALERT_TABLE_BODY_CELL(item, key)).strip()
                cell_list.append(cell_content)
            top_alerts_dict[key] = cell_list

        self.click_button(ALERTS_PAGE_OK_BTN, 'don\'t wait')
        return top_alerts_dict
