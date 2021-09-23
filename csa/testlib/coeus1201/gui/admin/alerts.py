#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/gui/admin/alerts.py#1 $


from constants import (alert_types, alert_levels)
from common.gui.guicommon import GuiCommon

alerts_classes_map = {alert_types.SYSTEM: 'system',
                      alert_types.HARDWARE: 'hardware',
                      alert_types.UPDATER: 'updater',
                      alert_types.PROXY: 'proxy',
                      alert_types.DVS_AMW: 'dvs',
                      alert_types.L4TM: 'trafmon',
                      alert_types.ALL: 'all'}

severity_levels_map = {alert_levels.CRITICAL: 'critical',
                       alert_levels.WARNING: 'warning',
                       alert_levels.INFO: 'info',
                       alert_levels.ALL: 'all'}

ALERTS_TABLE = "//table[@class='cols']"
ALERTS_TABLE_ROW = '%s//tr' % (ALERTS_TABLE,)
RECIPIENT_CELL_TEXT = lambda index: '%s//tr[%s]//td[1]' % (ALERTS_TABLE, index)
ALL_ALERTS_CHECKBOX = 'id=all-all'
ADD_RECIPIENT_BUTTON = "xpath=//input[@value='Add Recipient...']"
EDIT_RECIPIENT_LINK = lambda index: '%s//tr[%s]//td[1]/a' % (ALERTS_TABLE, index)
DELETE_RECIPIENT_LINK = lambda index: '%s//tr[%s]//td[8]/img' % (ALERTS_TABLE, index)
RECIPIENT_TEXTBOX = 'recipient'
DEFAULT_FROM_ADDR_RADIOBUTTON = 'id=from_address_default'
CUSTOM_FROM_ADDR_RADIOBUTTON = 'id=from_address_user'
FROM_ADDR_TEXTBOX = 'id=address_user_text'
WAIT_DUPLICATE_CHECKBOX = 'id=debounce_enable'
MIN_DEBOUNCE_TEXTBOX = 'name=initial_debounce_interval'
MAX_DEBOUNCE_TEXTBOX = 'name=maximum_debounce_interval'
ENABLE_AUTOSUPPORT_CHECKBOX = 'id=autosupport_enable'
SEND_COPY_CHECKBOX = 'id=autosupport_all'
VIEW_TOP_ALERTS_BTN = "//input[@value='View Top Alerts']"

ALERT_TABLE_BODY = "//div[@id='basic']//tbody[2]"
ALERT_TABLE_BODY_CELL = lambda num_id, header_name: "%s/tr[%s]/td[contains(@class, '%s')]" % \
                (ALERT_TABLE_BODY, num_id, header_name)
ALERT_TABLE_ALL_ROWS =  "%s/tr" % (ALERT_TABLE_BODY)

ALERT_TABLE_ALL_HEADERS = "//div[@id='basic']/div[2]//th"
ALERT_TABLE_HEADERS_CELL = lambda num_id: "//div[@id='basic']/div[2]//th[%s]" % (num_id)
ALERTS_PAGE_OK_BTN = "//button[normalize-space()='OK']"

class Alerts(GuiCommon):
    """Keywords for interaction with 'System Administration -> Alerts' page."""

    def get_keyword_names(self):
        return ['alerts_add_recipient',
                'alerts_edit_recipient',
                'alerts_delete_recipient',
                'alerts_edit_settings',
                'alerts_get_top_view_details'
                ]

    def _open_alerts_page(self):
        self._navigate_to('System Administration', 'Alerts')

    def _click_add_recipient_button(self):
        self.click_button(ADD_RECIPIENT_BUTTON)

    def _fill_recipient_textbox(self, email_addr):
        self.input_text(RECIPIENT_TEXTBOX, email_addr)

    def _clear_alerts_table(self):
        self.click_element(ALL_ALERTS_CHECKBOX, "don't wait")

        if self._is_checked(ALL_ALERTS_CHECKBOX):
            self.click_element(ALL_ALERTS_CHECKBOX, "don't wait")

    def _fill_alerts_table(self, alerts):

        self._clear_alerts_table()

        if not alerts:
            raise ValueError('Choose at least one alert')
        for sev_level, alert_classes in alerts.iteritems():
            if sev_level not in severity_levels_map:
                raise ValueError('"%s" severity level is invalid.' % \
                                 (sel_level,))

            for alert_class in alert_classes:
                if alert_class not in alerts_classes_map:
                    raise ValueError('"%s" alert class does not exist.' % \
                                     (alert_class,))
                self.select_checkbox('id=%s-%s' % \
                                     (alerts_classes_map[alert_class],
                                      severity_levels_map[sev_level]))

    def _get_recipient_row(self, email_addr):
        starting_row = 2
        entries_num = int(self.get_matching_xpath_count(ALERTS_TABLE_ROW)) - 1

        for index in xrange(starting_row, starting_row + entries_num):
            recipient = self.get_text(RECIPIENT_CELL_TEXT(index))
            if recipient == email_addr:
                return index
        raise ValueError('"%s" recipient does not exist.' % (email_addr,))

    def _click_edit_user_link(self, row_index):
        self.click_element(EDIT_RECIPIENT_LINK(row_index))

    def _click_delete_user_link(self, row_index):
        self.click_element(DELETE_RECIPIENT_LINK(row_index), "don't wait")

    def _fill_from_addr_textbox(self, from_addr):
        self.input_text(FROM_ADDR_TEXTBOX, from_addr)

    def _check_auto_from_address(self, auto_generated=True):
        if auto_generated:
            self._click_radio_button(DEFAULT_FROM_ADDR_RADIOBUTTON)
        else:
            self._click_radio_button(CUSTOM_FROM_ADDR_RADIOBUTTON)

    def _check_wait_before_duplicate(self, check=True):
        if check and not self._is_checked(WAIT_DUPLICATE_CHECKBOX):
            self.click_button(WAIT_DUPLICATE_CHECKBOX, "don't wait")
        elif not check:
            self.unselect_checkbox(WAIT_DUPLICATE_CHECKBOX)

    def _fill_timeout_textboxes(self, min_timeout, max_timeout):
        for timeout, locator in zip((min_timeout, max_timeout),
                                    (MIN_DEBOUNCE_TEXTBOX, MAX_DEBOUNCE_TEXTBOX)):
            if timeout:
                self.input_text(locator, timeout)

    def _check_enable_autosupport(self, enable=True):
        if enable and not self._is_checked(ENABLE_AUTOSUPPORT_CHECKBOX):
            self.click_button(ENABLE_AUTOSUPPORT_CHECKBOX, "don't wait")
        elif not enable:
            self.unselect_checkbox(ENABLE_AUTOSUPPORT_CHECKBOX)

    def _check_send_copy(self, enable):
        if enable:
            self.select_checkbox(SEND_COPY_CHECKBOX)
        else:
            self.unselect_checkbox(SEND_COPY_CHECKBOX)

    def _get_alert_dict(self, all, critical, warning, info):
        alerts_dict = {}
        if all:
            alerts_dict[alert_levels.ALL] = self._convert_to_tuple(all)
        if critical:
            alerts_dict[alert_levels.CRITICAL] = self._convert_to_tuple(critical)
        if warning:
            alerts_dict[alert_levels.WARNING] = self._convert_to_tuple(warning)
        if info:
            alerts_dict[alert_levels.INFO] = self._convert_to_tuple(info)

        return alerts_dict

    def alerts_add_recipient(self,
                             alert_email,
                             all=None,
                             critical=None,
                             warning=None,
                             info=None
                             ):
        """Adds new alert recipient.

        Parameters:
        - `alert_email`: e-mail of the alert recipient.
        - `all`: severity level of alerts 'All'. A comma separated values of
                 alert types. Possible values for alert type are 'All', System',
                 'Hardware', 'Updater', 'Web Proxy', 'DVS and Anti-Malware',
                 'L4 Traffic Monitor'.
        - `critical`: severity level of alerts 'Critical'. A comma separated
                      values of alert types. Possible values for alert type are
                      'All', System', 'Hardware', 'Updater', 'Web Proxy',
                      'DVS and Anti-Malware', 'L4 Traffic Monitor'.
        - `warning`: severity level of alerts 'Warning'. A comma separated
                     values of alert types. Possible values for alert type are
                     'All', System', 'Hardware', 'Updater', 'Web Proxy',
                     'DVS and Anti-Malware', 'L4 Traffic Monitor'.
        - `info`: severity level of alerts 'Critical'. A comma separated
                  values of alert types. Possible values for alert type are
                  'All', System', 'Hardware', 'Updater', 'Web Proxy',
                  'DVS and Anti-Malware', 'L4 Traffic Monitor'.

        Examples:
        | Alerts Add Recipient | testuser@cisco.com,rtestuser@cisco.com | all=All |
        | Alerts Add Recipient | testuser@cisco.com | all=System | warning=Updater,Web Proxy | info=Updater |
        """

        self._open_alerts_page()
        self._click_add_recipient_button()
        self._fill_recipient_textbox(alert_email)



        self._fill_alerts_table(self._get_alert_dict(all, critical, warning,
                                info))
        self._click_submit_button()

    def alerts_edit_recipient(self,
                              alert_email,
                              all=None,
                              critical=None,
                              warning=None,
                              info=None):
        """Edits existent alert recipient.

        Parameters:
        - `alert_email`: email of the alert recipient.
        - `all`: severity level of alerts 'All'. A comma separated values of
                 alert types. Possible values for alert type are 'All', System',
                 'Hardware', 'Updater', 'Web Proxy', 'DVS and Anti-Malware',
                 'L4 Traffic Monitor'.
        - `critical`: severity level of alerts 'Critical' . A comma separated
                      values of alert types. Possible values for alert type are
                      'All', System', 'Hardware', 'Updater', 'Web Proxy',
                      'DVS and Anti-Malware', 'L4 Traffic Monitor'.
        - `warning`: severity level of alerts 'Warning'. A comma separated
                     values of alert types. Possible values for alert type are
                     'All', System', 'Hardware', 'Updater', 'Web Proxy',
                     'DVS and Anti-Malware', 'L4 Traffic Monitor'.
        - `info`: severity level of alerts 'Info'. A comma separated
                  values of alert types. Possible values for alert type are
                  'All', System', 'Hardware', 'Updater', 'Web Proxy',
                  'DVS and Anti-Malware', 'L4 Traffic Monitor'.

        Example:
        | Alerts Edit Recipient | testuser@cisco.com | all=Updater,System | critical=Hardware |
        """

        self._open_alerts_page()
        row_index = self._get_recipient_row(alert_email)
        self._click_edit_user_link(row_index)

        self._fill_alerts_table(self._get_alert_dict(all, critical,
                                                     warning, info))
        self._click_submit_button()

    def alerts_delete_recipient(self, alert_email):
        """Deletes alert recipient.

        Parameters:
        - `alert_email`: email of the alert recipient to delete.

        Example:
        | Alerts Delete Recipient | testuser@cisco.com |
        """

        self._open_alerts_page()
        row_index = self._get_recipient_row(alert_email)
        self._click_delete_user_link(row_index)
        self._click_continue_button()

    def alerts_edit_settings(self, from_addr=None, wait_before_duplicate=None,
                      wait_timeout='', enable_autosupport=None, send_copy=None):
        """Edits alert settings.

        Parameters:
        - `from_addr`: from address to use when sending alerts. If None,
                       automatically generated address will be used.
        - `wait_before_duplicate': wait before sending duplicate alert. If
                                   None, value will be left unchanged.
                                   True/False.
        - `wait_timeout`: a comma separated values of
                          min_value,max_value seconds to wait before sending
                          a duplicate alert. If empty, values will be left
                          unchanged.
        - `enable_autosupport`: enable Cisco IronPort autosupport. If None,
                                value will be left unchanged. True/False.
        - `send_copy`: send copy of weekly AutoSupport reports. If None,
                       value will be left unchanged. True/False.

        Examples:
        | Alerts Edit Settings | from_addr=alert@host.example.com | wait_before_duplicate=${True} | wait_timeout=100,1000 |
        | Alerts Edit Settings | enable_autosupport=${True} |
        | Alerts Edit Settings | wait_before_duplicate=${False} |
        """

        self._open_alerts_page()
        self._click_edit_settings_button()

        if from_addr is not None:
            self._check_auto_from_address(False)
            self._fill_from_addr_textbox(from_addr)
        else:
            self._check_auto_from_address()

        if wait_before_duplicate is not None:
            self._check_wait_before_duplicate(wait_before_duplicate)
            if wait_before_duplicate and wait_timeout:
                wait_timeout = self._convert_to_tuple(wait_timeout)
                self._fill_timeout_textboxes(*wait_timeout)

        if enable_autosupport is not None:
            self._check_enable_autosupport(enable_autosupport)
            if enable_autosupport and send_copy is not None:
                self._check_send_copy(send_copy)

        self._click_submit_button()



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
        self._open_alerts_page()
        if self._is_element_present(VIEW_TOP_ALERTS_BTN):
            self.click_button(VIEW_TOP_ALERTS_BTN, 'don\'t wait')
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
