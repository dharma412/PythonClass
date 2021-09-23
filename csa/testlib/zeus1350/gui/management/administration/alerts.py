#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1350/gui/management/administration/alerts.py#1 $ $DateTime: 2019/09/18 01:46:35 $ $Author: sarukakk $

from common.gui.guicommon import GuiCommon

ALERTS_TYPE_TUPLE = ('system', 'hardware', 'updater', 'all')
ALERTS_SEVERITY_TUPLE = ('critical', 'warning', 'info', 'all')

ALERTS_TABLE = '//table[@class=\'cols\']'
ALERTS_TABLE_ROW = '%s//tr' % (ALERTS_TABLE,)
RECIPIENT_CELL_TEXT = lambda index: '%s//tr[%s]//td[1]' % (ALERTS_TABLE, index)
ALL_ALERTS_CHECKBOX = 'id=all-all'
ADD_RECIPIENT_BUTTON = 'name=action:Add'
EDIT_RECIPIENT_LINK = lambda index: '%s//tr[%s]//td[1]/a' % (ALERTS_TABLE, index)
DELETE_RECIPIENT_LINK = lambda index: '%s//tr[%s]//td[5]/img' % (ALERTS_TABLE, index)
RECIPIENT_TEXTBOX = 'name=recipient'
DEFAULT_FROM_ADDR_RADIOBUTTON = 'id=from_address_default'
CUSTOM_FROM_ADDR_RADIOBUTTON = 'id=from_address_user'
FROM_ADDR_TEXTBOX = 'id=address_user_text'
WAIT_DUPLICATE_CHECKBOX = 'id=debounce_enable'
MIN_DEBOUNCE_TEXTBOX = 'name=initial_debounce_interval'
MAX_DEBOUNCE_TEXTBOX = 'name=maximum_debounce_interval'
ENABLE_AUTOSUPPORT_CHECKBOX = 'id=autosupport_enable'
SEND_COPY_CHECKBOX = 'id=autosupport_all'


class Alerts(GuiCommon):
    """
    Keyword library for WebUI page  Web Appliance -> System Administration -> Alerts
    """

    def get_keyword_names(self):
        return ['alerts_edit_settings',
                'alerts_delete_recipient',
                'alerts_edit_recipient',
                'alerts_add_recipient',
                ]

    def _open_page(self):
        self._navigate_to('Management', 'System Administration', 'Alerts')

    def _click_add_recipient_button(self):
        self.click_button(ADD_RECIPIENT_BUTTON, "don't wait")
        self._info('Clicked "Add Recipient..." button.')

    def _fill_recipient_textbox(self, email_addr):
        self.input_text(RECIPIENT_TEXTBOX, email_addr)
        self._info('Set recipient address to "%s".' % (email_addr,))

    def _clear_alerts_table(self):
        self.click_button(ALL_ALERTS_CHECKBOX, "don't wait")

        if self._is_checked(ALL_ALERTS_CHECKBOX):
            self.click_button(ALL_ALERTS_CHECKBOX, "don't wait")

    def _fill_alerts_table(self, alerts):
        alerts = alerts.split(',')

        for i in xrange(0, len(alerts)):
            alert_matrix = alerts[i].split("-")

            if len(alert_matrix) != 2:
                raise ValueError("You must provide alerts in format" + \
                                 "'Alert Severities'-'Alert Type'")

            alert_matrix[0] = alert_matrix[0].strip().lower()
            alert_matrix[1] = alert_matrix[1].strip().lower()

            if alert_matrix[0] not in ALERTS_SEVERITY_TUPLE:
                raise ValueError('"%s" severity level does not exist.' % \
                                 (alert_matrix[0],))

            if alert_matrix[1] not in ALERTS_TYPE_TUPLE:
                raise ValueError('"%s" alert type does not exist.' % \
                                 (alert_matrix[1],))

            self.select_checkbox('id=%s-%s' % \
                                 (alert_matrix[1], alert_matrix[0]))
            self._info('Set "%s" severity, "%s" alert type' % \
                       (alert_matrix[0], alert_matrix[1]))

    def _get_recipient_row(self, email_addr):
        if not self._is_element_present(ALERTS_TABLE_ROW):
            raise ValueError('There are no configured recipients')

        starting_row = 2
        entries_num = int(self.get_matching_xpath_count(ALERTS_TABLE_ROW)) - 1

        for index in xrange(starting_row, starting_row + entries_num):
            recipient = self.get_text(RECIPIENT_CELL_TEXT(index))
            if recipient == email_addr:
                return index
        else:
            raise ValueError('"%s" recipient does not exist.' % (email_addr,))

    def _click_edit_user_link(self, row_index):
        self.click_button(EDIT_RECIPIENT_LINK(row_index), "don't wait")
        self._info('Clicked "Edit user" link.')

    def _click_delete_user_link(self, row_index):
        self.click_button(DELETE_RECIPIENT_LINK(row_index), "don't wait")
        self._info('Clicked "Delete" user link.')

    def _fill_from_addr_textbox(self, from_addr):
        self.input_text(FROM_ADDR_TEXTBOX, from_addr)
        self._info('Set from address to "%s".' % (from_addr,))

    def _check_auto_from_address(self, auto_generated=True):
        if auto_generated:
            self.click_button(DEFAULT_FROM_ADDR_RADIOBUTTON, "don't wait")
            self._info('Selected to use automatically generated from address.')
        else:
            self.click_button(CUSTOM_FROM_ADDR_RADIOBUTTON, "don't wait")
            self._info('Selected to use custom from address.')

    def _check_wait_before_duplicate(self, check):
        if check and not \
                self._is_checked(WAIT_DUPLICATE_CHECKBOX):
            self.click_button(WAIT_DUPLICATE_CHECKBOX, "don't wait")
            self._info('Checked "Wait before sending duplicate alert".')
        elif not check:
            self.unselect_checkbox(WAIT_DUPLICATE_CHECKBOX)
            self._info('Unchecked "Wait before sending duplicate alert".')

    def _fill_timeout_textboxes(self, min_timeout, max_timeout):

        for timeout, locator in zip((min_timeout, max_timeout), \
                                    (MIN_DEBOUNCE_TEXTBOX, MAX_DEBOUNCE_TEXTBOX)):

            if timeout == None:
                continue
            else:
                self.input_text(locator, timeout)
        self._info('Set min and max timeouts to %s %s.' % \
                   (min_timeout, max_timeout))

    def _check_enable_autosupport(self, enable=True):
        if enable and not self._is_checked(ENABLE_AUTOSUPPORT_CHECKBOX):
            self.click_button(ENABLE_AUTOSUPPORT_CHECKBOX, "don't wait")
            self._info('Enabled autosupport.')
        else:
            self.unselect_checkbox(ENABLE_AUTOSUPPORT_CHECKBOX)
            self._info('Disabled autosupport.')

    def _check_send_copy(self, enable):
        if enable:
            self.select_checkbox(SEND_COPY_CHECKBOX)
            self._info('Checked send copy checkbox.')
        else:
            self.unselect_checkbox(SEND_COPY_CHECKBOX)
            self._info('Unchecked send copy checkbox.')

    def alerts_add_recipient(self, alert_email, alerts):
        """Add new alert  recipient(s).

        *Parameters*
            - `alert_mail` : either string of one alert recipient or a
               comma-separated string of emails of the alert recipients.
            - `alerts`: alerts to send. A comma-separated string of values, where
               values are severity levels of alerts and values of
               alerts classes to send in format 'Alert Severities'-
               'Alert Type'. Alert Type can be 'hardware', 'system',
               'updater', 'all'. Alert Severities can be 'all',
               'warning', 'critical'.

        *Return*
            None

        *Exceptions*
            - `ValueError`: in case severity level or alert type is invalid or
              bad string format.

        *Examples*
            | Alerts Add Recipient | name1@anysite.com, name2@anysite.com |
            | ... | all-hardware, critical-system |
            | Alerts Add Recipient | name1@anysite.com | all-all |
            | Alerts Add Recipient | name3@mail.local |
            | ... | warning-system |
        """
        self._info('Adding new "%s" alert recipient.' % (alert_email,))

        self._open_page()

        self._click_add_recipient_button()

        self._fill_recipient_textbox(alert_email)

        self._fill_alerts_table(alerts)

        self._click_submit_button(False)

        self._info('Added new "%s"  alert recipient.' % (alert_email,))

    def alerts_edit_recipient(self, alert_email, alerts):
        """Edit existent alert recipient.

        *Parameters*
            - `alert_mail`: email of the alert recipient.
            - `alerts`: alerts to send. A comma-separated string of values, where
               values are severity levels of alerts and values of
               alerts classes to send in format 'Alert Severities'-
               'Alert Type'. Alert Type can be 'hardware', 'system',
               'updater', 'all'. Alert Severities can be 'all',
               'warning', 'critical'.

        *Return*
            None

        *Exceptions*
            - `ValueError`: in case of invalid severity level, alert type or
               alert recipient.

        *Examples*
            | Alerts Edit Recipient | anymail@anysite.com | critical-hardware |
            | Alerts Edit Recipient | anyname@anysite.com |
            | ... | all-system, info-updater |
            | Alerts Edit Recipient | mail@mail.local |
            | ... | info-system |
        """
        self._info('Editing "%s" alert recipient.' % (alert_email,))

        self._open_page()

        row_index = self._get_recipient_row(alert_email)

        self._click_edit_user_link(row_index)

        self._clear_alerts_table()

        self._fill_alerts_table(alerts)

        self._click_submit_button(False)

        self._info('Edited "%s" alert recipient.' % (alert_email,))

    def alerts_delete_recipient(self, alert_email):
        """Delete alert recipient.

        *Parameters*
            - `alert_email`: email of the alert recipient to delete.

        *Return*
            None.

        *Exceptions*
            - `ValueError`: in case of invalid alert recipient.

        *Examples*
            | Alerts Delete Recipient | anyname@anysite.com |
            | Alerts Delete Recipient | anymail@anyhost.com |
        """
        self._info('Removing "%s" alert recipient.' % (alert_email,))

        self._open_page()

        row_index = self._get_recipient_row(alert_email)

        self._click_delete_user_link(row_index)

        self._click_continue_button()

        self._info('Removed "%s" alert recipient.' % (alert_email,))

    def alerts_edit_settings(self, from_addr=None,
                             wait_before_duplicate=None, wait_timeout_min=None,
                             wait_timeout_max=None, enable_autosupport=None, send_copy=None):
        """Edit alert settings.

        *Parameters*
            - `from_addr`: from address to use when sending alerts. If None,
                 automatically generated address will be used.
            - `wait_before_duplicate': wait before sending duplicate alert.
                Argument must be boolean or None object. If None, value will be
                left unchanged.
            - `wait_timeout_min`: minimun seconds to wait before sending a
                duplicate alert. String, number or None. If None, values will
                be left unchanged.
            - `wait_timeout_max`: maximum seconds to wait before sending a
                dublicate alert. String, number or None. If None, values will
                be left unchnaged.
            - `enable_autosupport`: enable IronPort autosupport. Argument must
                be boolean or None object. If None, value will be left unchanged.
            - `send_copy`: send copy of weekly AutoSupport reports. Argument
                must be boolean or None object. If None, value will be left
                unchanged.

        *Return*
            None.

        *Exceptions*
            None.

        *Examples*
            | Alerts Edit Settings | any@any.com | ${True} | ${30} | 700 | ${True} |
            | ... | ${False} |
            | Alerts Edit Settings | anymail@anyhost.com |
            | Alerts Edit Settings | wait_before_duplicate=${True} |
            | ... | wait_timeout_min=40 | wait_timeout_max=1700 |
            | Alerts Edit Settings | from_addr=any@any.com |
            | ... | wait_before_duplicate=${True} | wait_timeout_min=40 |
            | ... | send_copy=${False} |
        """
        self._info('Editing alert settings.')

        self._open_page()

        self._click_edit_settings_button()

        if from_addr != None:
            self._check_auto_from_address(False)
            self._fill_from_addr_textbox(from_addr)
        else:
            self._check_auto_from_address()

        if wait_before_duplicate != None:
            self._check_wait_before_duplicate(wait_before_duplicate)
            if wait_before_duplicate:
                self._fill_timeout_textboxes(wait_timeout_min, \
                                             wait_timeout_max)

        if enable_autosupport != None:
            self._check_enable_autosupport(enable_autosupport)
            if enable_autosupport and send_copy != None:
                self._check_send_copy(send_copy)

        self._click_submit_button(False)

        self._info('Edited alert settings.')
