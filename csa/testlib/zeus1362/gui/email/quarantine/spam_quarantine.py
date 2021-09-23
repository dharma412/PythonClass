# $Id: //prod/main/sarf_centos/testlib/zeus1362/gui/email/quarantine/spam_quarantine.py#1 $ $DateTime: 2020/06/10 22:29:20 $ $Author: sarukakk $

import time

import common.gui.guiexceptions as guiexceptions
from common.gui.guicommon import GuiCommon
from common.util.sarftime import CountDownTimer

# ISQ search locators
CLEAR_SEARCH_LINK = '//a[text()=\'Clear Search\']'
ADVANCED_SEARCH_LINK = '//a[text()=\'Advanced Search\']'
SEARCH_BUTTON = 'xpath=//input[@value=\'Search\' and @type=\'submit\']'
FIRST_PAGE_BUTTON = """//a[contains(@href, "javascript:goPage(1, '&action=Param' , '');")]"""
NEXT_PAGE = '//a[text()=\'Next\']'
DELETE_BUTTON = 'id=delete_selected1'
CONFIRM_BUTTON = 'id=confirm_ok'
RELEASE_BUTTON = 'id=release_selected1'
USER_ACTIONS_LIST = 'id=message_action1'
USER_SUBMIT_BUTTON = 'id=process_selected1'
SELECT_ALL_CHECKBOX = 'name=toggle_msg'

TODAY_RANGE_RADIO = 'xpath=//input[@id=\'date1\']'
WEEK_RANGE_RADIO = 'xpath=//input[@id=\'date2\']'
DATE_RANGE_RADIO = 'xpath=//input[@id=\'date3\']'
DATE_RANGE_TEXTBOXES = ('xpath=//input[@id=\'date_from\']', 'xpath=//input[@id=\'date_to\']')

HEADER_NAME_LIST = '//select[@name=\'search_field\']'
HEADER_CMP_LIST = '//select[@name=\'search_kind\']'
HEADER_TEXTBOX = 'name=ignore_escapes:search_terms'

RECIPIENT_KIND_LIST = 'name=recipient_kind'
RECIPIENT_TEXTBOX = 'name=ignore_escapes:recipient_text'

MSG_INFO_ROW = '//tbody[@class=\'yui-dt-data\']/tr'
MSG_MID_COLUMN = lambda row: '%s[%s]/td[1]/div/input@value' % (MSG_INFO_ROW, row)
MSG_INFO_COLUMN = lambda row, column: '%s[%s]/td[%s]/div' % (MSG_INFO_ROW, row, column)


QUARANTINE_PORT = 83

class SpamQuarantine(GuiCommon):
    """Spam Quarantine page interaction class.

    This class designed to interact with GUI elements of Email -> Message
    Quarantine -> Spam Quarantine. Use keywords, listed below,
    to manipulate with Spam Quarantine page.

    Note, that you must call 'Spam Quarantine Search Page Open' keyword
    before use quarantine message handling routines
    """

    def get_keyword_names(self):
        return ['spam_quarantine_search_page_open',
                'spam_quarantine_advanced_search',
                'spam_quarantine_delete_messages',
                'spam_quarantine_release_messages']

    def _open_page(self):
        self._navigate_to('Email', 'Message Quarantine', 'Spam Quarantine')

        err_msg = 'This feature is currently disabled.'
        if self._is_text_present(err_msg):
            raise guiexceptions.GuiFeatureDisabledError(err_msg)

    def _click_spam_quarantine_link(self):
        self.click_element(
            "xpath=//a[@title='Spam Quarantine (open in new window)']",
            "don't wait")

    def _wait_for_page(self, title_part, timeout_sec=5):
        SLEEP_INTERVAL = 0.5

        timer = CountDownTimer(timeout_sec).start()
        while timer.is_active():
            titles = self.get_window_titles()
            for title in titles:
                if title.find(title_part) >= 0:
                    return title
            time.sleep(SLEEP_INTERVAL)
        raise guiexceptions.GuiPageNotFoundError(
                'Page title containing "%s" has not been not found'\
                ' within %d seconds timeout' % (title_part, timeout_sec))

    def _switch_to_spam_search_page(self):
        dest_title = self._wait_for_page('Message Management')
        self.select_window(dest_title)

    def _wait_for_spam_search_page_loading(self):
        SLEEP_INTERVAL = 1
        TIMEOUT = 60

        tmr = CountDownTimer(TIMEOUT).start()
        while tmr.is_active():
            if self._is_element_present(TODAY_RANGE_RADIO):
                return
            time.sleep(SLEEP_INTERVAL)
        raise guiexceptions.TimeoutError('Spam search page was not'\
                ' loaded with %d-seconds timeout' % (TIMEOUT,))

    def _spam_quarantine_add_certificate(self, override_type):
        """Add security certificate for quarantine port.
        All running browser instances should be closed prior to
        adding new certificate
        """
        self.close_all_browsers()
        self._ff_profile.add_certificate(self.dut,
                                         self.dut_version,
                                         QUARANTINE_PORT, override_type)

    def spam_quarantine_search_page_open(self,
                                         user='admin',
                                         password='ironport'):
        """Open Spam Quarantine Search page.
        Use this method to open Spam Quarantine Search page.
        Note, that security certificate must be added before
        call this method. So all opened browser instances will
        be closed and then reopened with new certificate added

        Parameters:
           - `user`: name of authorized user.  Defaulted to 'admin'.
           - `password`: password of authorized user.  Defaulted to 'ironport'.

        Example:
        | Spam Quarantine Search Page Open | user=admin | password=newpass |
        """
        self.launch_dut_browser()
        self.log_into_dut(user, password)

        self._open_page()
        self._click_spam_quarantine_link()
        try:
            self._switch_to_spam_search_page()
        except:
            self.launch_dut_browser()
            self.log_into_dut(user, password)

            self._open_page()
            self._click_spam_quarantine_link()
            self._switch_to_spam_search_page()
        self._wait_for_spam_search_page_loading()

    def _goto_advanced_search(self):
        if self._is_element_present(ADVANCED_SEARCH_LINK):
            self.click_button(ADVANCED_SEARCH_LINK)

    def _clear_search(self):
        if self._is_element_present(CLEAR_SEARCH_LINK):
            self.click_button(CLEAR_SEARCH_LINK)

    def _select_date_range(self, date_range):
        if date_range is None:
            return

        date_range_map = {
            'today': TODAY_RANGE_RADIO,
            'week': WEEK_RANGE_RADIO,
        }

        if isinstance(date_range, basestring):
            if date_range in date_range_map:
                self._click_radio_button(date_range_map[date_range])
        elif isinstance(date_range, tuple):
            self._click_radio_button(DATE_RANGE_RADIO)
            if len(date_range) != 2:
                raise ValueError('Date range should be a tuple of 2.')

            for locator, value in zip(DATE_RANGE_TEXTBOXES, date_range):
                self.input_text(locator, value)

        else:
            raise ValueError('Invalid %s date range' % (date_range,))

    def _goto_first_page(self):
        if self._is_element_present(FIRST_PAGE_BUTTON):
            self.click_button(FIRST_PAGE_BUTTON)

    def _admin_delete_action(self):
        self.click_button(DELETE_BUTTON, 'don\'t wait')
        self.click_button(CONFIRM_BUTTON)

    def _user_delete_action(self):
        self.select_from_list(USER_ACTIONS_LIST, '-- Delete')
        self.click_button(USER_SUBMIT_BUTTON, 'don\'t wait')
        self.click_button(CONFIRM_BUTTON)

    def _admin_release_action(self):
        self.click_button(RELEASE_BUTTON, 'don\'t wait')
        self.click_button(CONFIRM_BUTTON)

    def _user_release_action(self):
        self.select_from_list(USER_ACTIONS_LIST, '-- Release')
        self.click_button(USER_SUBMIT_BUTTON, 'don\'t wait')
        self.click_button(CONFIRM_BUTTON)

    def _select_list_item(self, list_locator, item_value, list_name):
        if item_value is None:
            return

        items = self.get_list_items(list_locator)
        for item in items:
            if item_value.lower() == item.lower():
                self.select_from_list(list_locator, item)
                break
        else:
            raise ValueError('%s item is not present in %s list' % \
                (item_value, list_name))

    def _search_msgs(self, date_range, header_name, header_cmp, header_value,
        recipient_cmp, recipient_value, is_admin):

        date_range_map = {
            'today': TODAY_RANGE_RADIO,
            'week': WEEK_RANGE_RADIO,
        }

        if is_admin:
            self._goto_advanced_search()

        self._clear_search()

        self._select_date_range(date_range)

        for list_locator, value, list_name in (\
            (HEADER_NAME_LIST, header_name, 'header name'),
            (HEADER_CMP_LIST, header_cmp, 'header comparator'),
            (RECIPIENT_KIND_LIST, recipient_cmp, 'recipient comparator')):
            self._select_list_item(list_locator, value, list_name)

        if header_value is not None:
            self.input_text(HEADER_TEXTBOX, header_value)

        if recipient_value is not None:
            self.input_text(RECIPIENT_TEXTBOX, recipient_value)

        self.click_button(SEARCH_BUTTON)

        self._goto_first_page()

    def _get_all_msgs_on_current_page(self, columns):
        rows_num = int(self.get_matching_xpath_count(MSG_INFO_ROW))
        msg_list = []
        for row in xrange(1, rows_num + 1):
            msg_dict = {}
            msg_dict['mid'] = self.get_element_attribute(MSG_MID_COLUMN(row))
            for column, name in enumerate(columns, 2):
                msg_dict[name] = self.get_text(MSG_INFO_COLUMN(row, column))
            msg_list.append(msg_dict)
        return msg_list

    def _retrieve_all_msgs(self, is_admin):
        if self._is_text_present('No items found'):
            return []

        if is_admin:
            columns = ('from', 'rcpt_to', 'to', 'subject', 'date' , 'size')
        else:
            columns = ('from', 'subject', 'date', 'size')

        msg_list = self._get_all_msgs_on_current_page(columns)

        while self._is_element_present(NEXT_PAGE):
            self.click_button(NEXT_PAGE)
            msgs = self._get_all_msgs_on_current_page(columns)
            msg_list.extend(msgs)

        return msg_list

    def _do_isq_action(self, action_method):
        for i in xrange(100):
            if self._is_text_present('No items found'):
                break
            self._select_checkbox(SELECT_ALL_CHECKBOX)
            action_method()

    def spam_quarantine_advanced_search(self,
                                        is_admin=True,
                                        date_range=None,
                                        header_name=None,
                                        header_cmp=None,
                                        header_value=None,
                                        recipient_cmp=None,
                                        recipient_value=None):
        """Search messages in ISQ.

        Parameters:
            - `is_admin`: boolean flag. Leave it default if you have logged
            in as an administrator
            - `date_range`: date range to search through. Can be name of
            period ('today', 'week') or 'MM/DD/YYYY, MM/DD/YYYY' to search
            through specific date range.
            - `header_name`: name of the header to search through ('To',
            'Subject', etc)
            - `header_cmp`: comparator for header value search. Can be one of
            'contains', 'is', 'begins with', 'ends with', 'does not contain'.
            - `header_value`: value of the header to search for.
            - `recipient_cmp`: comparator for recipient header value search.
            - `recipient_value`: recipient header value to search for.

        Return:
            List of quarantined messages. Each message is represented as
            dictionary where keys are the names of the columns and values are
            corresponding values of each column.

        Exceptions:
            - `ValueError`: in case of invalid value for any of the input
                            parameters.

        Example:
        | Spam Quarantine Advanced Search | header_name=Subject |
        | ... | header_cmp=contains | header_value=bob |
        | ... | recipient_cmp=contains | recipient_value=alice |
        """
        if isinstance(date_range, basestring) and date_range.find(',') > 0:
            date_range = self._convert_to_tuple(date_range)
        self._search_msgs(
            date_range=date_range,
            header_name=header_name,
            header_cmp=header_cmp,
            header_value=header_value,
            recipient_cmp=recipient_cmp,
            recipient_value=recipient_value,
            is_admin=is_admin
        )

        return self._retrieve_all_msgs(is_admin)

    def spam_quarantine_delete_messages(self,
                                       is_admin=True,
                                       date_range=None,
                                       header_name=None,
                                       header_cmp=None,
                                       header_value=None,
                                       recipient_cmp=None,
                                       recipient_value=None):
        """Delete messages from ISQ that match search parameters.

        Parameters:
            - `is_admin`: boolean flag. Leave it default if you have logged
            in as an administrator
            - `date_range`: date range to search through. Can be name of
            period ('today', 'week') or 'MM/DD/YYYY, MM/DD/YYYY' to search
            through specific date range.
            - `header_name`: name of the header to search through ('To',
            'Subject', etc)
            - `header_cmp`: comparator for header value search. Can be one of
            'contains', 'is', 'begins with', 'ends with', 'does not contain'.
            - `header_value`: value of the header to search for.
            - `recipient_cmp`: comparator for recipient header value search.
            - `recipient_value`: recipient header value to search for.

        Exceptions:
            - `ValueError`: in case of invalid value for any of the input
            parameters.

        Example:
        | Spam Quarantine Delete Messages | date_range=05/04/2012,06/04/2012 |
        | ... | header_cmp=is | header_value=For Bob |
        """
        if isinstance(date_range, basestring) and date_range.find(',') > 0:
            date_range = self._convert_to_tuple(date_range)
        self._search_msgs(
            date_range=date_range,
            header_name=header_name,
            header_cmp=header_cmp,
            header_value=header_value,
            recipient_cmp=recipient_cmp,
            recipient_value=recipient_value,
            is_admin=is_admin
        )

        delete_action = self._admin_delete_action if is_admin else \
                        self._user_delete_action
        self._do_isq_action(delete_action)

    def spam_quarantine_release_messages(self,
                                        is_admin=True,
                                        date_range=None,
                                        header_name=None,
                                        header_cmp=None,
                                        header_value=None,
                                        recipient_cmp=None,
                                        recipient_value=None):
        """Release messages from ISQ that match search parameters.

        Parameters:
            - `is_admin`: boolean flag. Leave it default if you have logged
            in as an administrator
            - `date_range`: date range to search through. Can be name of
            period ('today', 'week') or 'MM/DD/YYYY, MM/DD/YYYY' to search
            through specific date range.
            - `header_name`: name of the header to search through ('To',
            'Subject', etc)
            - `header_cmp`: comparator for header value search. Can be on of
                            'contains', 'is', 'begins with', 'ends with', 'does
                            not contain'.
            - `header_value`: value of the header to search for.
            - `recipient_cmp`: comparator for recipient header value search.
            - `recipient_value`: recipient header value to search for.

        Exceptions:
            - `ValueError`: in case of invalid value for any of the input
            parameters.

        Example:
        | Spam Quarantine Delete Messages | is_admin=${False} |
        | date_range=today | recipient_cmp=is | header_value=alice@example.com |
        """
        if isinstance(date_range, basestring) and date_range.find(',') > 0:
            date_range = self._convert_to_tuple(date_range)
        self._search_msgs(
            date_range=date_range,
            header_name=header_name,
            header_cmp=header_cmp,
            header_value=header_value,
            recipient_cmp=recipient_cmp,
            recipient_value=recipient_value,
            is_admin=is_admin
        )

        release_action = self._admin_release_action if is_admin else \
                         self._user_release_action
        self._do_isq_action(release_action)
