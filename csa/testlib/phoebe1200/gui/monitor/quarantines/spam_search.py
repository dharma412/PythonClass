#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1200/gui/monitor/quarantines/spam_search.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $

from locators import *
from qcommon import QuarantinesCommon
from common.util.misc import Misc
from credentials import DUT_ADMIN
from qexceptions import MessageNotFound, NoMessagesFound
from common.gui.guiexceptions import GuiPageNotFoundError, TimeoutError
from common.gui.decorators import set_speed
import re
from sal.containers.cfgholder import CfgHolder
from common.util.sarftime import CountDownTimer
import time

SPAM_QUARANTINE_PORT = 83


class SpamSearch(QuarantinesCommon):
    """
    *Search in Spam Quarantine*\n
    - `Quarantines Search Spam Open Page` - navigate to Spam Quarantine page.
    - `Quarantines Search Spam Back To Quarantines Page` - navigate to management WUI.
    - `Quarantines Search Spam` - get all messages from Spam Quarantine that fit search criteria.
    - `Quarantines Search Spam Delete` - delete all messages from Spam Quarantine that follow search criteria.
    - `Quarantines Search Spam Release` - release all messages from Spam Quarantine that follow search criteria.
    - `Quarantines Search Spam Message` - open message that was found.
    """
    sq = 'Spam Quarantine'

    def _open_search_page(self):
        self._navigate_to('Monitor', self.sq)
        row_idx, col_idx = \
            self._is_quarantine_present(self.sq, only_clickable=True)
        link = "%s//tr[%s]/td[%s]/a" % (QUARANTINES_TABLE, row_idx, int(col_idx) + 1)
        self.click_element(link, "don't wait")

    def _spam_quarantine_add_certificate(self):
        """Add security certificate for quarantine port.
        All running browser instances should be closed prior to
        adding new certificate
        """
        self.close_all_browsers()
        self._ff_profile.add_certificate(self.dut,
                                         self.dut_version,
                                         SPAM_QUARANTINE_PORT)

    def _wait_for_spam_search_page_loading(self):
        SLEEP_INTERVAL = 1
        TIMEOUT = 60
        tmr = CountDownTimer(TIMEOUT).start()
        while tmr.is_active():
            if self._is_element_present(SPAM_QUARANTINE_TODAY_RANGE):
                return
            time.sleep(SLEEP_INTERVAL)
        raise TimeoutError('Spam search page was not' \
                           ' loaded with %d-seconds timeout' % (TIMEOUT,))

    def _wait_for_page(self, title_part, timeout_sec=5):
        SLEEP_INTERVAL = 0.5
        timer = CountDownTimer(timeout_sec).start()
        while timer.is_active():
            titles = self.get_window_titles()
            for title in titles:
                if title.find(title_part) >= 0:
                    return title
            time.sleep(SLEEP_INTERVAL)
        raise GuiPageNotFoundError(
            'Page title containing "%s" has not been found' \
            ' within %d seconds timeout' % (title_part, timeout_sec))

    def _switch_to_spam_search_page(self):
        dest_title = self._wait_for_page('Message Management')
        self.select_window(dest_title)

    def _switch_to_quarantines_page(self):
        dest_title = self._wait_for_page('Monitor > Quarantine Reports > Spam Quarantine')
        self.select_window(dest_title)

    def _goto_advanced_search(self):
        if self._is_element_present(SPAM_QUARANTINE_ADVANCED_SEARCH):
            self.click_button(SPAM_QUARANTINE_ADVANCED_SEARCH)

    def _clear_search(self):
        if self._is_element_present(SPAM_QUARANTINE_CLEAR_SEARCH):
            self.click_button(SPAM_QUARANTINE_CLEAR_SEARCH)

    def _select_date_range(self, date_range):
        if date_range is None:
            return

        date_range_map = {
            'today': SPAM_QUARANTINE_TODAY_RANGE,
            'week': SPAM_QUARANTINE_LAST_WEEK_RANGE,
        }
        if isinstance(date_range, basestring) and date_range.find(',') > 0:
            date_range = self._convert_to_tuple(date_range)
        if isinstance(date_range, basestring):
            if date_range in date_range_map:
                self._click_radio_button(date_range_map[date_range])
        elif isinstance(date_range, tuple):
            self._click_radio_button(SPAM_QUARANTINE_DATES_RANGE)
            if len(date_range) != 2:
                raise ValueError('Date range should be a tuple of 2.')
            for locator, value in zip(SPAM_QUARANTINE_DATE_RANGE, date_range):
                self.input_text(locator, value)
        else:
            raise ValueError('Invalid %s date range' % (date_range,))

    def _handle_no_messages_found(self, err=None):
        """
        Check if there are messages.
        """
        if any([self._is_text_present(x) for x in \
                ('No messages were found', 'No items found', 'No records found.')]):
            if err:
                raise NoMessagesFound(err)
            else:
                return True
        return False

    def _get_page_info(self):
        res = self.get_text("%s//th[2]" % SPAM_QUARANTINE_SEARCH_TABLE_PAGER_BAR)
        mo = re.search(r'Page (?P<current>\d+) of (?P<count>\d+)', res)
        return {'count': mo.group('count'), 'current': mo.group('current')}

    def _get_page_count(self):
        """
        Get total pages num.
        """
        if self._is_pager_bar_present():
            pages = int(self._get_page_info()['count'])
            self._debug('Number of pages: %s' % pages)
            return pages
        else:
            return 1

    def _get_page_current(self):
        """
        Get number of current page.
        """
        if self._is_pager_bar_present():
            page = int(self._get_page_info()['current'])
            self._debug('Current page: %s' % page)
            return page
        else:
            return 1

    def _go_to_page(self, indicator, by_title=True):
        """
        Common method used for navigation
        """
        if self._is_pager_bar_present():
            if by_title:
                self.click_element("%s//a[@title='%s']" % \
                                   (SPAM_QUARANTINE_SEARCH_TABLE_PAGER_BAR, indicator), "don't wait")
            else:
                self.click_element("%s//a[text()='%s']" % \
                                   (SPAM_QUARANTINE_SEARCH_TABLE_PAGER_BAR, indicator), "don't wait")

    def _go_to_next_page(self):
        self._debug('Go to Next page')
        self._go_to_page('Next page')

    def _go_to_previous_page(self):
        self._debug('Go to Previous page')
        self._go_to_page('Previous page')

    def _go_to_first_page(self):
        self._debug('Go to First page')
        self._go_to_page('First page')

    def _go_to_last_page(self):
        self._debug('Go to Last page')
        self._go_to_page('Last page')

    def _go_to_page_num(self, num):
        """
        Navigate to page by number.
        May be complicated in case when there are many pages,
        WUI shows only part of them in pager bar.
        Rest of pages links appear when navigating forward or backward.
        """
        if num != self._get_page_current():
            self._debug('Go to page #%s' % num)
            self._go_to_page(num, by_title=False)

    def _is_pager_bar_present(self):
        """
        1. pager bar may not appear if all messages fit into single page
        2. pager bar may disappear after items per page increased
        """
        # return self._is_element_present(SPAM_QUARANTINE_SEARCH_TABLE_PAGER_BAR)
        if self._is_element_present(SPAM_QUARANTINE_SEARCH_TABLE_PAGER_BAR):
            col = lambda idx: "%s//th[%s]" % \
                              (SPAM_QUARANTINE_SEARCH_TABLE_PAGER_BAR, idx)
            return all([self._is_element_present(col(x)) for x in range(1, 4)])

    def _search_by_mid(self,
                       mid=None,
                       items_per_page='20',
                       select_only=False):
        """
        Common method to search message by MID.
        Assuming that:
        -- needed quarantine is opened
        -- search was done or was not done, does not matter

        Walks through pages in quarantine looking for given MID.

        *Parameters*:
        - `name`: The name of the quarantine. Has no any functional impact, just for exceptions.
        - `mid`: MID of message to look for.
        - `items_per_page`: The page size (items per page to display).
        Options are as they seen in WUI.
        | 20 |
        | 50 |
        | 100 |
        | 250 |
        - `select_only`: Boolean. If True - just select needed MID and return.

        *Return*:
        - `Boolean`: if 'select_only' is True.

        *Exceptions*:
        - `MessageNotFound`: in case when message with given MID was not found.
        """
        self._handle_no_messages_found('No messages were found')
        self._set_items_per_page(items_per_page)
        pages = self._get_page_count()
        current_page = self._get_page_current()
        on_last_page = (current_page == pages)
        while True:
            # don't count rows yet, quick search for element by id
            if select_only:
                return self._select_mid_checkbox_by_mid(mid)
            if self._select_mid_checkbox_by_mid(mid):
                # now we know that the element is on the page,
                # find the row num of the selected mid to click on subject
                rows = self._count_rows_in_search_results_container()
                _found = None
                for row in xrange(2, rows + 1):
                    if self._is_checked \
                                ("%s//input[@type='checkbox']" % \
                                 QUARANTINE_SEARCH_TABLE_CELL_DATA \
                                             (SPAM_QUARANTINE_SEARCH_TABLE_RESULTS_CONTAINER, row, 1)):
                        _found = row
                        break
                if _found:
                    return self._open_message_in_quarantine(_found)
                else:
                    # for some reason message is not here, possible?
                    raise MessageNotFound \
                        ('The message with mid %s should be in quarantine on page %s,\
                     but it is not there.' % (mid, current_page))
            else:
                if on_last_page:
                    # we checked all pages, no message with such mid
                    raise MessageNotFound \
                        ('There is no message with mid %s in quarantine' % (mid,))
                self._go_to_next_page()
                current_page = self._get_page_current()
            if current_page == pages:
                on_last_page = True

    def _spam_search(self,
                     date_range=None,
                     header_name=None,
                     header_rule=None,
                     header_text=None,
                     recipient_text=None,
                     recipient_rule=None,
                     is_admin=True):
        """
        Common method to perform search in spam quarantine
        """
        if is_admin:
            self._goto_advanced_search()
        self._clear_search()
        self._select_date_range(date_range)
        self.select_from_dropdown_list \
            (SPAM_QUARANTINE_SEARCH_FIELD, header_name)
        self.select_from_dropdown_list \
            (SPAM_QUARANTINE_SEARCH_KIND, header_rule)
        self._input_text_if_not_none(SPAM_QUARANTINE_SEARCH_TERMS, header_text)
        if recipient_rule:
            self.select_from_dropdown_list \
                (SPAM_QUARANTINE_ENV_RECIPIENT_SEARCH_KIND, recipient_rule)
        self._input_text_if_not_none \
            (SPAM_QUARANTINE_ENV_RECIPIENT_SEARCH_TERMS, recipient_text)
        self.click_button(SEARCH_QUARANTINE_SEARCH_BUTTON)

    def _admin_delete_action(self):
        self.click_button(SPAM_QUARANTINE_DELETE_BUTTON, "don't wait")
        self.click_button(SPAM_QUARANTINE_CONFIRM_OK_CANCEL_BUTTON('Delete'))

    def _user_delete_action(self):
        self.select_from_dropdown_list(SPAM_QUARANTINE_ACTION,
                                       'Delete',
                                       starts_with=False,
                                       contains=True)
        self.select_from_dropdown_list(SPAM_QUARANTINE_ACTION,
                                       'Delete')
        self.click_button(SPAM_QUARANTINE_ACTION_SUBMIT_BUTTON, "don't wait")
        self.click_button(SPAM_QUARANTINE_CONFIRM_OK_CANCEL_BUTTON('Delete'))

    def _admin_release_action(self):
        self.click_button(SPAM_QUARANTINE_RELEASE_BUTTON, "don't wait")
        self.click_button(SPAM_QUARANTINE_CONFIRM_OK_CANCEL_BUTTON('Release'))

    def _user_release_action(self):
        self.select_from_dropdown_list(SPAM_QUARANTINE_ACTION,
                                       'Release',
                                       starts_with=False,
                                       contains=True)
        self.click_button(SPAM_QUARANTINE_ACTION_SUBMIT_BUTTON, "don't wait")
        self.click_button(SPAM_QUARANTINE_CONFIRM_OK_CANCEL_BUTTON('Release'))

    def _do_isq_action(self, action_method, items_per_page):
        self._set_items_per_page(items_per_page)
        while True:
            if self._is_text_present('No items found'):
                break
            self._select_checkbox(SPAM_QUARANTINE_SEARCH_TABLE_SELECT_ALL_MIDS)
            action_method()

    def _get_items_per_page(self):
        return int(self._get_selected_label \
                       (SPAM_QUARANTINE_SEARCH_TABLE_ITEMS_PER_PAGE).strip())

    def _set_items_per_page(self, items):
        if items:
            self.select_from_list \
                (SPAM_QUARANTINE_SEARCH_TABLE_ITEMS_PER_PAGE, items)

    def _select_mid_checkbox_by_mid(self, mid):
        """
        Select MID checkbox by id.
        """
        mid_id = "%s//*[@id='mid%s']" % \
                 (SPAM_QUARANTINE_SEARCH_TABLE_RESULTS_CONTAINER, mid)
        # or by value (for Spam Quarantine)
        mid_value = "%s//*[@name='mid[]' and @value='%s']" % \
                    (SPAM_QUARANTINE_SEARCH_TABLE_RESULTS_CONTAINER, mid)
        if self._is_element_present(mid_id):
            self._select_checkbox(mid_id)
            return True
        elif self._is_element_present(mid_value):
            self._select_checkbox(mid_value)
            return True
        else:
            return False

    def _get_table_column_names(self):
        locator = "//*[@id='quarantine_container']//thead"
        cols_num = int(self.get_matching_xpath_count("%s//th" % \
                                                     locator))
        return [self.get_text("%s//th[%s]" % \
                              (locator, col)) \
                for col in xrange(1, cols_num + 1)]

    def _count_rows_in_search_results_container(self):
        """
        Just count rows in table, does not
        matter what items per page value is.
        """
        return int(self.get_matching_xpath_count \
                       ("%s//tr" % SPAM_QUARANTINE_SEARCH_TABLE_RESULTS_CONTAINER))

    def _open_message_in_quarantine(self, row_idx, ):
        self._handle_no_messages_found(err='No messages were found')
        subj_index = self._get_table_column_names().index('Subject') + 1
        self.click_element \
            ("%s//a" % QUARANTINE_SEARCH_TABLE_CELL_DATA \
                (SPAM_QUARANTINE_SEARCH_TABLE_RESULTS_CONTAINER, row_idx, subj_index))
        return True  # if we reached this place - message was opened successfully

    def _grep_cell(self, locator, row_idx, col_idx):
        return self.get_text \
            (QUARANTINE_SEARCH_TABLE_CELL_DATA(locator, row_idx, col_idx)).strip()

    def _grep_row(self,
                  row_idx,
                  cols_names=None,
                  mid_as_key=False):
        """
        Grep data from single row in the table.

        Return dictionary that represents data in the row.
        Each key in the dictionary represents column in the row.
        """
        data = CfgHolder()
        data.mid = self.get_element_attribute \
            ("%s//input[@type='checkbox']@value" % \
             QUARANTINE_SEARCH_TABLE_CELL_DATA \
                 (SPAM_QUARANTINE_SEARCH_TABLE_RESULTS_CONTAINER, row_idx, 1))
        # skip 1st(mid) column
        for col_idx, name in enumerate(cols_names[1:], 2):
            data.__setattr__(self._normalize(name),
                             self._grep_cell \
                                 (SPAM_QUARANTINE_SEARCH_TABLE_RESULTS_CONTAINER, row_idx, col_idx))
        # only mid can be a key in dictionary, because it
        # is only unique for sure
        if mid_as_key:
            mid = data.pop('mid')
            data_by_mid = CfgHolder()
            data_by_mid.__setattr__(mid, data)
            return data_by_mid
        return data

    @set_speed(0)
    def _grep_search_results_table(self, **kwargs):
        """
        Parses separate table(page).

        Returns list of dictionaries.
        Each element of list is a row of a table represented as dictionary.

        Count items per page to have real num of messages,
        do not rely on items per page, as real num of messages
        may be less than items per page.
        """
        res = []
        self._handle_no_messages_found(err='No messages were found')
        rows = self._count_rows_in_search_results_container()
        for row in xrange(1, rows + 1):
            res.append(self._grep_row(row, **kwargs))
        return res

    def _get_all_messages(self,
                          items_per_page=None,
                          **kwargs):
        """
        Getting *all* messages is time consuming if there are a lot of messages.

        *Parameters*:
        - `items_per_page`: The page size (items per page to display).
        Options are as they seen in WUI.
        | 20 |
        | 50 |
        | 100 |
        | 250 |
        - `view_all`: Press View All button.
        - `**kwargs`: Parameters for '_grep_search_results_table' method.

        *Return*:
        List of dictionaries, where each dictionary represents row of table.

        *Exceptions*:
        - `NoMessagesFound`: If `return_all_messages` is True but no messages in quarantine.

        """
        # items per page may be already
        # set during previous activities!
        kwargs['cols_names'] = self._get_table_column_names()
        self._set_items_per_page(items_per_page)
        all_messages = []
        pages = self._get_page_count()
        current_page = self._get_page_current()
        if pages > 1 and current_page != 1:
            self._go_to_first_page()
        on_last_page = (current_page == pages)
        while True:
            _messages = self._grep_search_results_table(**kwargs)
            if _messages:
                all_messages.extend(_messages)
            if on_last_page:
                break
            self._go_to_next_page()
            current_page = self._get_page_current()
            if current_page == pages:
                on_last_page = True
        return all_messages

    ###################### =============== ###########################
    ###################### K E Y W O R D S ###########################
    ###################### =============== ###########################
    def quarantines_search_spam_open_page(self,
                                          user=DUT_ADMIN,
                                          password=None):
        """Open Spam Quarantine Search page.
        Use this method to open Spam Quarantine Search page.
        Note, that security certificate must be added before
        call this method. So all opened browser instances will
        be closed and then reopened with new certificate added.

        Parameters:
           - `user`: name of authorized user.  Defaulted to 'admin'.
           - `password`: password of authorized user.  Defaulted to 'ironport'.

        Example:
        | Spam Quarantine Search Page Open | user=admin | password=newpass |
        """
        if not password:
            password = Misc(None, None).get_admin_password(self.dut)
        self._spam_quarantine_add_certificate()
        self.launch_dut_browser()
        self.log_into_dut(user, password)
        self._open_search_page()
        self._switch_to_spam_search_page()
        self._wait_for_spam_search_page_loading()

    def quarantines_search_spam_back_to_quarantines_page(self):
        """
        Select window with DUT management WUI.

        Use this method to navigate from Spam Quarantine(EUQ) to Management WUI.
        """
        self._switch_to_quarantines_page()

    def quarantines_search_spam(self,
                                date_range=None,
                                header_name=None,
                                header_rule=None,
                                header_text=None,
                                recipient_text=None,
                                recipient_rule=None,
                                is_admin=True,
                                items_per_page=None,
                                mid_as_key=False):
        """
        Perform search in Spam Quarantine using WUI controls at "Quarantines > Spam Quarantine" page.
        Return all message from the result by walking through all pages.

        Rules common for `header_rule`, `recipient_rule`, parameters:
        | Contains |
        | Is |
        | Begins with |
        | Ends with |
        | Does not contain |

        *Parameters*:
        - `date_range`: Can be _today_, _week_ or start and end dates separated with comma.
        - `header_name`: Can be _From_, _To_, _Subject_
        - `header_rule`: Rule to use for `header_text`.
        - `header_text`: Header text field.
        - `recipient_rule`: Rule to use for `recipient_text`.
        - `recipient_text`: Recipient text field.
        - `is_admin`: Does current user belong to quarantine administrative users. Boolean.
        - `items_per_page`: The page size (items per page to display). Options are as the seen in WUI.
        | 25 |
        | 50 |
        | 100 |
        | 250 |
        Does not have any direct impact on end result.
        - `mid_as_key`: Each element in result list will be a dictionary.
        Make MID value key of dictionary or not. Boolean. False by default.

        *Return*:
        List of dictionaries.

        *Examples*:
        | ${res}= | Quarantines Search Spam |
        | ... | date_range=today |
        | ... | header_name=from |
        | ... | header_rule=is |
        | ... | header_text=test@mail.qa |
        | ... | recipient_text=ahrytski@mail.qa |
        | ... | recipient_rule=is |
        | ... | mid_as_key=${True} |
        | Log List | ${res} |

        | @{time}= | Get Time  month day year |
        | ${y}= | Get From List | ${time} | 0 |
        | ${m}= | Get From List | ${time} | 1 |
        | ${d}= | Get From List | ${time} | 2 |
        | ${end_date}= | Catenate | SEPARATOR=/ | ${m} | ${d} | ${y} |
        | @{res}= | Quarantines Search Spam |
        | ... | date_range=01/01/2012, ${end_date} |
        | ... | header_name=from |
        | ... | header_rule=contains |
        | ... | header_text=test |
        | ... | recipient_text=ahrytski |
        | ... | recipient_rule=contains |
        | ... | mid_as_key=${True} |
        | :FOR | ${r} | IN | @{res} |
        | \   Log Dictionary | ${r} |

        *Exceptions*:
        - `NoSuchQuarantine`: If there is no such quarantine.
        - `NoMessagesFound`: If there are no messages in quarantine.
        """
        self._spam_search(date_range=date_range,
                          header_name=header_name,
                          header_rule=header_rule,
                          header_text=header_text,
                          recipient_text=recipient_text,
                          recipient_rule=recipient_rule,
                          is_admin=is_admin)
        return self._get_all_messages \
            (items_per_page=items_per_page, mid_as_key=mid_as_key)

    def quarantines_search_spam_release(self,
                                        date_range=None,
                                        header_name=None,
                                        header_rule=None,
                                        header_text=None,
                                        recipient_text=None,
                                        recipient_rule=None,
                                        is_admin=True,
                                        items_per_page=None):
        """
        Perform search in Spam Quarantine using WUI controls at "Quarantines > Spam Quarantine" page.
        Release all messages returned after search by walking through all pages.

        *Parameters*:
        - `date_range`: Can be _today_, _week_ or start and end dates separated with comma.
        - `header_name`: Can be _From_, _To_, _Subject_
        - `header_rule`: Rule to use for `header_text`.
        - `header_text`: Header text field.
        - `recipient_rule`: Rule to use for `recipient_text`.
        - `recipient_text`: Recipient text field.
        - `is_admin`: Does current user belong to quarantine administrative users. Boolean.
        - `items_per_page`: The page size (items per page to display). Options are as the seen in WUI.
        | 25 |
        | 50 |
        | 100 |
        | 250 |
        Does not have any direct impact on end result.

        *Return*:
        None

        *Examples*:
        | Quarantines Search Spam Release |
        | ... | date_range=today |
        | ... | header_name=from |
        | ... | header_rule=is |
        | ... | header_text=test@mail.qa |
        | ... | recipient_text=ahrytski@mail.qa |
        | ... | recipient_rule=is |
        """
        self._spam_search(date_range=date_range,
                          header_name=header_name,
                          header_rule=header_rule,
                          header_text=header_text,
                          recipient_text=recipient_text,
                          recipient_rule=recipient_rule,
                          is_admin=is_admin)
        release_action = self._admin_release_action if is_admin else \
            self._user_release_action
        self._do_isq_action(release_action, items_per_page)

    def quarantines_search_spam_delete(self,
                                       date_range=None,
                                       header_name=None,
                                       header_rule=None,
                                       header_text=None,
                                       recipient_text=None,
                                       recipient_rule=None,
                                       is_admin=True,
                                       items_per_page=None):
        """
        Perform search in Spam Quarantine using WUI controls at "Quarantines > Spam Quarantine" page.
        Delete all messages returned after search by walking through all pages.

        *Parameters*:
        - `date_range`: Can be _today_, _week_ or start and end dates separated with comma.
        - `header_name`: Can be _From_, _To_, _Subject_
        - `header_rule`: Rule to use for `header_text`.
        - `header_text`: Header text field.
        - `recipient_rule`: Rule to use for `recipient_text`.
        - `recipient_text`: Recipient text field.
        - `is_admin`: Does current user belong to quarantine administrative users. Boolean.
        - `items_per_page`: The page size (items per page to display). Options are as the seen in WUI.
        | 25 |
        | 50 |
        | 100 |
        | 250 |
        Does not have any direct impact on end result.

        *Return*:
        None

        *Examples*:
        | Quarantines Search Spam Delete |
        | ... | date_range=today |
        | ... | header_name=from |
        | ... | header_rule=is |
        | ... | header_text=test@mail.qa |
        | ... | recipient_text=ahrytski@mail.qa |
        | ... | recipient_rule=is |
        """
        self._spam_search(date_range=date_range,
                          header_name=header_name,
                          header_rule=header_rule,
                          header_text=header_text,
                          recipient_text=recipient_text,
                          recipient_rule=recipient_rule,
                          is_admin=is_admin)
        delete_action = self._admin_delete_action if is_admin else \
            self._user_delete_action
        self._do_isq_action(delete_action, items_per_page)

    def quarantines_search_spam_message(self,
                                        date_range=None,
                                        header_name=None,
                                        header_rule=None,
                                        header_text=None,
                                        recipient_text=None,
                                        recipient_rule=None,
                                        is_admin=True,
                                        items_per_page=None,
                                        first_match=True,
                                        mid=None):
        """
        Perform search in Spam Quarantine using WUI controls at "Quarantines > Spam Quarantine" page.
        From the result returned - open first message or message with given MID.

        *Parameters*:
        - `date_range`: Can be _today_, _week_ or start and end dates separated with comma.
        - `header_name`: Can be _From_, _To_, _Subject_
        - `header_rule`: Rule to use for `header_text`.
        - `header_text`: Header text field.
        - `recipient_rule`: Rule to use for `recipient_text`.
        - `recipient_text`: Recipient text field.
        - `is_admin`: Does current user belong to quarantine administrative users. Boolean.
        - `items_per_page`: The page size (items per page to display). Options are as the seen in WUI.
        | 25 |
        | 50 |
        | 100 |
        | 250 |
        Does not have any direct impact on end result.
        - `first_match`: Open first message from the result returned. Boolean. True by default.
        - `mid`: Open message by MID. Will walk through all pages until message with given MID found.

        *Examples*:
        | ${res}= | Quarantines Search Spam Message |
        | ... | date_range=today |
        | ... | header_name=from |
        | ... | header_rule=is |
        | ... | header_text=test@mail.qa |
        | ... | recipient_text=ahrytski@mail.qa |
        | ... | recipient_rule=is |
        | Log | ${res} |
        Now if ${res} is ${True} - we have message opened and can proceed with
        `Quarantines Spam Message Get Details`, `Quarantines Spam Message Delete`,
        `Quarantines Spam Message Release` keywords.

        | ${res}= | Quarantines Search Spam Message |
        | ... | date_range=week |
        | ... | recipient_text=ahrytski |
        | ... | recipient_rule=contains |
        | ... | mid=198 |
        | Log | ${res} |
        Now if ${res} is ${True} - we have message opened and can proceed with
        `Quarantines Spam Message Get Details`, `Quarantines Spam Message Delete`,
        `Quarantines Spam Message Release` keywords.
        """
        self._spam_search(date_range=date_range,
                          header_name=header_name,
                          header_rule=header_rule,
                          header_text=header_text,
                          recipient_text=recipient_text,
                          recipient_rule=recipient_rule,
                          is_admin=is_admin)
        if mid:
            return self._search_by_mid(mid=mid,
                                       items_per_page=items_per_page)
        elif first_match:
            return self._open_message_in_quarantine(1)

    def get_keyword_names(self):
        return ['quarantines_search_spam_open_page',
                'quarantines_search_spam_back_to_quarantines_page',
                'quarantines_search_spam',
                'quarantines_search_spam_delete',
                'quarantines_search_spam_release',
                'quarantines_search_spam_message', ]
