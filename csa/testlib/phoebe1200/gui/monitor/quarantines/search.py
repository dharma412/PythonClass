#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1200/gui/monitor/quarantines/search.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $

from locators import *
from qcommon import QuarantinesCommon
from qexceptions import MessageNotFound, NoMessagesFound, NoMessagesInQuarantine
from common.gui.guiexceptions import GuiPageNotFoundError, TimeoutError
from common.gui.decorators import set_speed
from common.gui.guicommon import GuiCommon
import re
from sal.containers.cfgholder import CfgHolder
from common.util.sarftime import CountDownTimer
import time
from js_templates import js


class Search(QuarantinesCommon):
    """
    Class to interact with 'Monitor > Policy, Virus and Outbreak Quarantines' page.
    Provides search functionality.
    """

    # This method may be redundant, but it does not add any delay,
    # so it is better to leave it here for now
    def _wait_until_message_list_loaded(self, timeout=60):
        tmr = CountDownTimer(timeout).start()
        while tmr.is_active():
            if not self._is_visible("//td[@class='yui-dt-loading']"):
                return
            time.sleep(1)
        raise TimeoutError \
            ('Search page was not loaded with %d-seconds timeout' % (timeout,))

    def _open_quarantine_search_page(self, quarantine_name=None, only_clickable=True):
        if quarantine_name:
            self._open_page()
            row_idx, col_idx = self._is_quarantine_present \
                (quarantine_name, strict_match=True, only_clickable=only_clickable)
            messages_count = int(self.get_text("%s//tr[%s]/td[%s]" % \
                                               (QUARANTINES_TABLE, row_idx, int(col_idx) + 2)))
            if messages_count == 0:
                raise NoMessagesInQuarantine("There are no messages in quarantine.")
            link = "%s//tr[%s]/td[%s]/a" % (QUARANTINES_TABLE, row_idx, int(col_idx) + 2)
            self.click_element(link)
            self._wait_until_message_list_loaded()

    def _press_view_all_messages_button(self):
        # button may be present but disabled
        if self._is_element_present(QUARANTINE_SEARCH_TABLE_VIEW_ALL_MESSAGES_BUTTON):
            if 'disabled' not in self.get_element_attribute \
                        ("%s@class" % QUARANTINE_SEARCH_TABLE_VIEW_ALL_MESSAGES_BUTTON):
                self.click_button(QUARANTINE_SEARCH_TABLE_VIEW_ALL_MESSAGES_BUTTON)
                self._wait_until_message_list_loaded()
                return True
        return False

    def _get_items_per_page(self):
        return int(self._get_selected_label \
                       (QUARANTINE_SEARCH_TABLE_ITEMS_PER_PAGE).strip())

    def _set_items_per_page(self, items):
        if items:
            self.select_from_dropdown_list \
                (QUARANTINE_SEARCH_TABLE_ITEMS_PER_PAGE, items)
            self._wait_until_message_list_loaded()

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

    def _handle_confirm_dialog(self,
                               locator,
                               ok_text,
                               cancel_text,
                               confirm=True,
                               timeout=60,
                               func=None,
                               **kwargs):
        tmr = CountDownTimer(timeout).start()
        while tmr.is_active():
            time.sleep(1)
            if self._is_visible(locator):
                if func is not None:
                    func(**kwargs)
                if confirm:
                    self.click_button \
                        (QUARANTINE_SEARCH_TABLE_HANLDE_DIALOG_OK_CANCEL_BUTTON \
                             (locator, ok_text))
                else:
                    self.click_button \
                        (QUARANTINE_SEARCH_TABLE_HANLDE_DIALOG_OK_CANCEL_BUTTON \
                             (locator, cancel_text), "don't wait")
                self._debug \
                    ("Time elapsed while waiting for confirm dialog: %s" % \
                     tmr.time_elapsed())
                break

    def _get_messages_displayed_text(self):
        """
        Get text containing number of messages displayed of total number.
        Just for info purpose.
        """
        return self.get_text \
            ("%s//div[@class='left']" % QUARANTINE_SEARCH_TABLE_PAGER_BAR)

    def _get_page_info(self):
        res = self.get_text \
            ("%s//div[@class='pages_center']" % QUARANTINE_SEARCH_TABLE_PAGER_BAR)
        mo = re.search(r'Page (?P<current>\d+) of (?P<count>\d+)', res)
        if mo == None:
            return {'count': 1, 'current': 1}
        return {'count': mo.group('count'), 'current': mo.group('current')}

    def _get_page_count(self):
        """
        Get total pages num.
        """
        pages = int(self._get_page_info()['count'])
        self._debug('Number of pages: %s' % pages)
        return pages

    def _get_page_current(self):
        """
        Get number of current page.
        """
        page = int(self._get_page_info()['current'])
        self._debug('Current page: %s' % page)
        return page

    def _go_to_page(self, indicator, by_title=True):
        """
        Common method used for navigation
        """
        if by_title:
            self.click_element("%s//a[@title='%s']" % \
                               (QUARANTINE_SEARCH_TABLE_PAGER_BAR, indicator), "don't wait")
        else:
            self.click_element("%s//a[text()='%s']" % \
                               (QUARANTINE_SEARCH_TABLE_PAGER_BAR, indicator), "don't wait")
        self._wait_until_message_list_loaded()

    def _go_to_next_page(self):
        self._debug('Go to Next page')
        self._go_to_page('Next Page')

    def _go_to_previous_page(self):
        self._debug('Go to Previous page')
        self._go_to_page('Previous Page')

    def _go_to_first_page(self):
        self._debug('Go to First page')
        self._go_to_page('First Page')

    def _go_to_last_page(self):
        self._debug('Go to Last page')
        self._go_to_page('Last Page')

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

    def _count_rows_in_search_results_container(self):
        """
        Just count rows in table, does not
        matter what items per page value is.
        """
        return int(self.get_matching_xpath_count \
                       ("%s//tr" % QUARANTINE_SEARCH_TABLE_MESSAGE_LIST))

    def _grep_cell(self, locator, row_idx, col_idx):
        return self.get_text \
            (QUARANTINE_SEARCH_TABLE_CELL_DATA(locator, row_idx, col_idx)).strip()

    def _select_mid_checkbox_by_mid(self, mid):
        """
        Select MID checkbox.
        """
        mid_id = "%s//*[@id='mid%s']" % \
                 (QUARANTINE_SEARCH_TABLE_MESSAGE_LIST, mid)
        # or by value (for Spam Quarantine)
        mid_value = "%s//*[@name='mid[]' and @value='%s']" % \
                    (QUARANTINE_SEARCH_TABLE_MESSAGE_LIST, mid)
        self._wait_until_message_list_loaded()
        if self._is_element_present(mid_id):
            self.execute_javascript \
                (js.SimulateEventAndClickOnElement(mid_id, 'mouseover'))
            return True
        elif self._is_element_present(mid_value):
            self.execute_javascript \
                (js.SimulateEventAndClickOnElement(mid_value, 'mouseover'))
            return True
        return False

    def _get_table_column_names(self):
        cols_num = int(self.get_matching_xpath_count("%s//thead//th" % \
                                                     QUARANTINE_SEARCH_TABLE_MESSAGE_LIST_CONTAINER))
        return [self.get_text("%s//thead//th[%s]" % \
                              (QUARANTINE_SEARCH_TABLE_MESSAGE_LIST_CONTAINER, col)) \
                for col in xrange(1, cols_num + 1)]

    def _click_link(self, row_idx, lookup_text):
        col_index = self._get_table_column_names().index(lookup_text) + 1
        self.click_element \
            ("%s//a" % QUARANTINE_SEARCH_TABLE_CELL_DATA \
                (QUARANTINE_SEARCH_TABLE_MESSAGE_LIST, row_idx, col_index))
        return True  # if we reached this place - message was opened successfully

    def _open_message_in_quarantine(self, row_idx):
        self._handle_no_messages_found(err='No messages were found')
        return self._click_link(row_idx, 'Subject')

    def _view_tracking_details(self, row_idx):
        return self._click_link(row_idx, 'Tracking')

    def _select_message_in_first_row(self):
        """
        Just select MID checkbox in the first row in the table.
        """
        self._handle_no_messages_found(err='No messages were found')
        locator = "%s//input" % QUARANTINE_SEARCH_TABLE_CELL_DATA \
            (QUARANTINE_SEARCH_TABLE_MESSAGE_LIST, 1, 1)
        self.execute_javascript \
            (js.SimulateEventAndClickOnElement(locator, 'mouseover'))

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
                 (QUARANTINE_SEARCH_TABLE_MESSAGE_LIST, row_idx, 1))
        # skip 1st(mid) column
        for col_idx, name in enumerate(cols_names[1:], 2):
            data.__setattr__(self._normalize(name),
                             self._grep_cell \
                                 (QUARANTINE_SEARCH_TABLE_MESSAGE_LIST, row_idx, col_idx))
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
        self._handle_no_messages_found(err='No messages were found')
        self._debug(self._get_messages_displayed_text())
        rows = self._count_rows_in_search_results_container()
        res = []
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
        """
        all_messages = []
        kwargs['cols_names'] = self._get_table_column_names()
        self._set_items_per_page(items_per_page)
        pages = self._get_page_count()
        current_page = self._get_page_current()
        if pages > 1 and current_page != 1:
            # lets begin from 1st page
            # no matter where we were before
            self._go_to_first_page()
        on_last_page = (current_page == pages)
        while True:
            _messages = self._grep_search_results_table(**kwargs)
            if _messages:
                all_messages.extend(_messages)
            current_page = self._get_page_current()
            if current_page == pages:
                on_last_page = True
            if on_last_page:
                break
            self._go_to_next_page()
        return all_messages

    def _wait_until_action_finished(self, timeout=60):
        res = None
        tmr = CountDownTimer(timeout).start()
        while tmr.is_active():
            time.sleep(1)
            try:
                res = self._get_result()
            except:  # catch all
                pass
            if res:
                if re.search('Attention', res):
                    self._debug('Action is in progress: %s' % res)
                else:
                    # TODO wait for final success message?!
                    return res
            return res
        # TODO raise error or warning?!

    def _select_action_on(self, item):
        if item is not None:
            self.select_from_dropdown_list \
                (QUARANTINE_SEARCH_TABLE_MESSAGE_ACTION_ON_ALL, item)

    def _is_action_on_all(self):
        if 'Action on All' in self._get_selected_label \
                    (QUARANTINE_SEARCH_TABLE_MESSAGE_ACTION_ON_ALL):
            return True
        return False

    def _fill_copy_to(self, address=None):
        # looks silly, but need this function to be passed as parameter
        self._input_text_if_not_none \
            (QUARANTINE_SEARCH_TABLE_COPY_DIALOG_COPY_RECIPIENTS, address)

    def _select_dest_quarantine(self, destination=None):
        # looks silly, but need this function to be passed as parameter
        self.select_from_dropdown_list \
            (QUARANTINE_SEARCH_TABLE_MOVE_DIALOG_DST, destination)

    def _apply_action_to_messages(self,
                                  action,
                                  address=None,
                                  destination=None,
                                  scheduler=None):
        """
        Apply action to messages in the message list table.
        Some actions do not take any arguments, while others need additional arguments.

        :param action: Action to apply.
        :param address: Needed if action is 'Send Copy'
        :param destination: Needed if action is 'Move'
        :param scheduler: Needed if action is 'Scheduled Exit'
        :return: Action result
        """
        supported_actions = ('delete', 'release', 'send copy', 'move', 'scheduled exit')
        if not action.lower() in supported_actions:
            raise ValueError \
                ('Invalid action: %s. Must be on from: %s' % \
                 (action, ', '.join(supported_actions)))
        if action.lower() == 'delete':
            self.click_button \
                (QUARANTINE_SEARCH_TABLE_MESSAGE_ACTION_DELETE, "don't wait")
            self._click_submit_button_custom('Confirm',
                                             'Cancel',
                                             need_confirm=True,
                                             confirm=True)
        elif action.lower() == 'release':
            self.click_button \
                (QUARANTINE_SEARCH_TABLE_MESSAGE_ACTION_RELEASE, "don't wait")
            self._click_submit_button_custom('Confirm',
                                             'Cancel',
                                             need_confirm=True,
                                             confirm=True)
        elif action.lower() == 'send copy':
            self.select_from_dropdown_list \
                (QUARANTINE_SEARCH_TABLE_MESSAGE_ACTION_MORE, action)
            self._handle_confirm_dialog(QUARANTINE_SEARCH_TABLE_COPY_DIALOG,
                                        'Send',
                                        'Cancel',
                                        func=self._fill_copy_to,
                                        address=address)
        elif action.lower() == 'move':
            self.select_from_dropdown_list \
                (QUARANTINE_SEARCH_TABLE_MESSAGE_ACTION_MORE, action)
            self._handle_confirm_dialog(QUARANTINE_SEARCH_TABLE_MOVE_DIALOG,
                                        'Move',
                                        'Cancel',
                                        func=self._select_dest_quarantine,
                                        destination=destination)
        elif action.lower() == 'scheduled exit':
            more_actions = self.get_list_items \
                (QUARANTINE_SEARCH_TABLE_MESSAGE_ACTION_MORE)
            available_schedulers = \
                ', '.join([opt.strip() for opt in more_actions if \
                           opt.strip().startswith('--')])
            if not re.search(scheduler, available_schedulers, re.I):
                raise ValueError \
                    ("Invalid option for scheduled exit: %s. Must be one from: %s" % \
                     (scheduler, available_schedulers))
            self.select_from_dropdown_list(QUARANTINE_SEARCH_TABLE_MESSAGE_ACTION_MORE,
                                           scheduler)
            self._click_submit_button_custom('Confirm',
                                             'Cancel',
                                             need_confirm=True,
                                             confirm=True)
        return self._wait_until_action_finished()

    def _fill_received_parameters(self, received):
        if received is None:
            return
        received_tuple = self._convert_to_tuple(received)
        if received.lower() not in \
                ('today', 'last 7 days') and len(received_tuple) != 2:
            raise ValueError("The 'received' option is invalid: %s" % received)
        if received.lower() == 'today':
            self._click_radio_button(SEARCH_QUARANTINE_RECEIVED('period_today'))
        elif received.lower() == 'last 7 days':
            self._click_radio_button(SEARCH_QUARANTINE_RECEIVED('period_last_week'))
        else:
            if len(received_tuple) != 2:
                raise ValueError \
                    ("The 'received' time range option requires two values. Got %s" % received)
            self._click_radio_button(SEARCH_QUARANTINE_RECEIVED('period_range'))
            self._input_text_if_not_none(SEARCH_QUARANTINE_RECEIVED_START, received_tuple[0])
            self._input_text_if_not_none(SEARCH_QUARANTINE_RECEIVED_END, received_tuple[1])

    def _fill_matching_parameters(self, option, text):
        self.select_from_dropdown_list(option[0], option[1])
        self._input_text_if_not_none(text[0], text[1])

    def _fill_attachment_parameters(self, attachment_name, attachment_size):
        self._input_text_if_not_none \
            (SEARCH_QUARANTINE_ATTACHMENT_TEXT, attachment_name)
        if attachment_size is None:
            return
        conditions = self.get_list_items \
            (SEARCH_QUARANTINE_ATTACHMENT_SIZE_CONDITION)
        condition, size = attachment_size.split(':', 1)
        if not any(condition.lower() in x.lower() for x in conditions):
            raise ValueError \
                ("Invalid attachment size condition: %s. Must be one from: %s" % \
                 (condition, ', '.join(conditions)))
        self.execute_javascript \
            (js.SimulateSelectEventAndClickOnElement \
                 (SEARCH_QUARANTINE_ATTACHMENT_SIZE_CONDITION, condition))
        condition_selected = self._get_selected_label \
            (SEARCH_QUARANTINE_ATTACHMENT_SIZE_CONDITION)
        if condition_selected.strip().lower() == 'range':
            size = self._convert_to_tuple(size)
            self._input_text_if_not_none \
                (SEARCH_QUARANTINE_ATTACHMENT_SIZE_1, size[0])
            self._input_text_if_not_none \
                (SEARCH_QUARANTINE_ATTACHMENT_SIZE_2, size[1])
        else:
            # we have 'less than' or 'more than'
            self._input_text_if_not_none \
                (SEARCH_QUARANTINE_ATTACHMENT_SIZE_1, size)

    def _fill_quarantines_parameters(self, quarantines):
        if quarantines is None:
            return
        if quarantines == 'All':
            return self._click_radio_button(QUARANTINES_SEARCH_ACROSS_ALL)
        self._click_radio_button(QUARANTINES_SEARCH_ACROSS_SELECT)
        available_quarantines = \
            self.get_list_items(QUARANTINES_SEARCH_ACROSS_SELECT_MULTIPLE)
        quarantines = self._convert_to_tuple(quarantines)
        if not all(x in available_quarantines for x in quarantines):
            raise ValueError \
                ('Available values: %s. Values provided: %s' % \
                 (', '.join(available_quarantines), ', '.join(quarantines)))
        self.select_from_list(QUARANTINES_SEARCH_ACROSS_SELECT_MULTIPLE, *quarantines)

    def _quarantines_search_fill_query_params(self,
                                              name=None,
                                              received=None,
                                              sender_rule=None,
                                              sender_text=None,
                                              recipient_rule=None,
                                              recipient_text=None,
                                              subject_rule=None,
                                              subject_text=None,
                                              attachment_name=None,
                                              attachment_size=None,
                                              only_clickable=True):
        """
        Common method that implements search functionality using WUI controls at
        "Quarantines > Search Quarantine" page.

        Rules common for `sender_rule`, `recipient_rule`, `subject_rule` parameters:
        | Contains |
        | Starts with |
        | Ends with |
        | Matches exactly |
        | Does Not Contain |
        | Does Not Start With |
        | Does Not End With |
        | Does Not Match |

        *Parameters*:
        - `name`: The name of the quarantine to open.
        - `received`: The period when message was received. Options as they are seen in WUI.
        | Today |
        | Last 7 days |
        | Between date range|
        To define _Between date range_ - provide start and end dates in format: mm/dd/yyyy.
        Separate start and end dates with comma.
        - `sender_rule`: Rule to use for Envelope Sender field. See available options above.
        - `sender_text`: Envelope sender field.
        - `recipient_rule`: Rule to use for Recipient field. See available options above.
        - `recipient_text`: Recipient field.
        - `subject_rule`: Rule to use for Subject field. See available options above.
        - `subject_text`: Subject field.
        - `attachment_name`: Attachment name.
        - `attachment_size`: Attachment size. Must be in format: size_condition: size.
        If size condition is range, then pass size1 and size 2 separated by comma.
        Available size conditions are:
        | Less than |
        | More than |
        | Range |
        - `only_clickable`: Whether the quarantined policy is clickable or not. Default value is 'True'.

        *Return*:
        None

        *Exceptions*:
        - `NoSuchQuarantine`: If there is no such quarantine.
        """
        self._open_quarantine_search_page(quarantine_name=name, only_clickable=only_clickable)
        self.click_button(QUARANTINE_SEARCH_TABLE_BUTTON)
        self._fill_received_parameters(received)
        self._fill_matching_parameters(
            (SEARCH_QUARANTINE_ENVELOPE_SENDER_METHOD, sender_rule),
            (SEARCH_QUARANTINE_ENVELOPE_SENDER_TEXT, sender_text)
        )
        self._fill_matching_parameters(
            (SEARCH_QUARANTINE_ENVELOPE_RCPT_METHOD, recipient_rule),
            (SEARCH_QUARANTINE_ENVELOPE_RCPT_TEXT, recipient_text)
        )
        self._fill_matching_parameters(
            (SEARCH_QUARANTINE_SUBJECT_METHOD, subject_rule),
            (SEARCH_QUARANTINE_SUBJECT_TEXT, subject_text)
        )
        self._fill_attachment_parameters(attachment_name, attachment_size)
        self.click_button(SEARCH_QUARANTINE_SEARCH_BUTTON)

    def _search_by_mid(self,
                       mid=None,
                       items_per_page='20',
                       select_only=False,
                       call_method='_open_message_in_quarantine'):
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
        self._handle_no_messages_found('No messages found')
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
                for row in xrange(1, rows + 1):
                    if self._is_checked \
                                ("%s//input[@type='checkbox']" % \
                                 QUARANTINE_SEARCH_TABLE_CELL_DATA \
                                             (QUARANTINE_SEARCH_TABLE_MESSAGE_LIST, row, 1)):
                        _found = row
                        break
                if _found:
                    return reduce(getattr(self, call_method), _found)
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

    ###################### =============== ###########################
    ###################### K E Y W O R D S ###########################
    ###################### =============== ###########################
    def quarantines_search_is_empty_quarantine(self, quarantine_name):
        """
        Open quarantine search page.

        *Parameters*:
        - `name`: The name of the quarantine to open.

        *Return*:
        Boolean. True if there are no messages in quarantine.

        *Examples*:
        | ${is_empty}= | Quarantines Search Is Empty Quarantine | Virus |

        *Exceptions*:
        - `NoSuchQuarantine`: If `name` was given and there is no such quarantine.
        """
        self._open_page()
        row_idx, col_idx = self._is_quarantine_present \
            (quarantine_name, strict_match=True, only_clickable=True)
        return not int(self.get_text("%s//tr[%s]/td[%s]" % \
                                     (QUARANTINES_TABLE, row_idx, int(col_idx) + 2)))

    def quarantines_search_open_quarantine(self, name):
        """
        Open quarantine search page. If there are no messages in quarantine,
        then search page for this quarantine can't be opened.

        *Parameters*:
        - `name`: The name of the quarantine to open.

        *Return*:
        None.

        *Examples*:
        | Quarantines Search Open | Virus |

        *Exceptions*:
        - `NoSuchQuarantine`: If `name` was given and there is no such quarantine.
        - `NoMessagesInQuarantine`: If quarantine is present but it has '0' messages.
        """
        self._open_quarantine_search_page(quarantine_name=name)

    def quarantines_search_view_all_messages(self, name=None):
        """
        Open quarantine if needed. Press _View All Messages_ button.

        *Parameters*:
        - `name`: The name of the quarantine to open. Optional.
        Assume we are at needed page if `name` not given.

        *Return*:
        Boolean. True if _View All Messages_ was pressed.

        *Examples*:
        Open quarantine and press button.
        | ${res}= | Quarantines Search View All Messages | name=Virus |
        Assume we are at needed page, just press button.
        | ${res}= | Quarantines Search View All Messages |

        *Exceptions*:
        - `NoSuchQuarantine`: If `name` was given and there is no such quarantine.
        - `NoMessagesInQuarantine`: If quarantine is present but it has '0' messages.
        """
        self._open_quarantine_search_page(quarantine_name=name)
        return self._press_view_all_messages_button()

    def quarantines_search(self,
                           name=None,
                           received=None,
                           sender_rule=None,
                           sender_text=None,
                           recipient_rule=None,
                           recipient_text=None,
                           subject_rule=None,
                           subject_text=None,
                           attachment_name=None,
                           attachment_size=None,
                           only_clickable=True):
        """
        Performs search in quarantine using WUI controls.
        Does not return any results, just runs search query.

        Rules common for `sender_rule`, `recipient_rule`, `subject_rule` parameters:
        | Contains |
        | Starts with |
        | Ends with |
        | Matches exactly |
        | Does Not Contain |
        | Does Not Start With |
        | Does Not End With |
        | Does Not Match |

        *Parameters*:
        - `name`: The name of the quarantine to open. Optional.
        Assume we are at needed page if this parameter was not given.
        - `received`: The period when message was received. Options as they are seen in WUI.
        | Today |
        | Last 7 days |
        | Between |
        To define _Between_ - provide start and end dates in format: mm/dd/yyyy.
        Separate start and end dates with comma.
        - `sender_rule`: Rule to use for Envelope Sender field. See available options above.
        - `sender_text`: Envelope sender field.
        - `recipient_rule`: Rule to use for Recipient field. See available options above.
        - `recipient_text`: Recipient field.
        - `subject_rule`: Rule to use for Subject field. See available options above.
        - `subject_text`: Subject field.
        - `attachment_name`: Attachment name.
        - `attachment_size`: Attachment size. Must be in format: size_condition: size.
        If size condition is range, then pass size1 and size2 separated by comma.
        Available size conditions are:
        | Less than |
        | More than |
        | Range |
        - `only_clickable`: Whether the quarantined policy is clickable or not. Default value is 'True'.

        *Return*:
        None.

        *Examples*:
        | Quarantines Search |
        | ... | name=Virus |
        | ... | sender_rule=matches exactly |
        | ... | sender_text=test@mail.qa |
        | ... | received=last 7 days |
        | ... | recipient_rule=matches exactly |
        | ... | recipient_text=ahrytski@mail.qa |

        | Quarantines Search |
        | ... | name=Policy |
        | ... | sender_rule=Starts with |
        | ... | sender_text=test |
        | ... | received=08/08/2012, 08/10/2012 |
        | ... | recipient_rule=Does Not Contain |
        | ... | recipient_text=mail.qa |
        | ... | attachment_size=less than: 512 |
        | ... | attachment_name=babar.jar |

        | Quarantines Search |
        | ... | name=Quarantine1 |
        | ... | sender_rule=Contains |
        | ... | sender_text=mail.qa |
        | ... | received=last week |
        | ... | subject_rule=Does Not Start With |
        | ... | subject_text=warning |

        | Quarantines Search |
        | ... | name=Policy |
        | ... | received=today |
        | ... | attachment_name=babar.exe |

        | Quarantines Search |
        | ... | name=Quarantine2 |
        | ... | received=last 7 days |
        | ... | attachment_size=range: 1500, 3000 |
        | @{res}= | Quarantines Search Get Messages |
        | Log List | ${res} |
        | :FOR | ${r} | IN | @{res} |
        | \   Log Dictionary | ${r} |
        | \   Should Contain | ${r.size} | 2M |

        | Quarantines Search |
        | ... | name=${q1} |
        | ... | attachment_size=less: 1000 |

        | Quarantines Search |
        | ... | name=${q1} |
        | ... | attachment_size=more than: 1500 |

        *Exceptions*:
        - `NoSuchQuarantine`: If there is no such quarantine.
        - `NoMessagesInQuarantine`: If quarantine is present but it has '0' messages.
        """
        self._quarantines_search_fill_query_params(name=name,
                                                   received=received,
                                                   sender_rule=sender_rule,
                                                   sender_text=sender_text,
                                                   recipient_rule=recipient_rule,
                                                   recipient_text=recipient_text,
                                                   subject_rule=subject_rule,
                                                   subject_text=subject_text,
                                                   attachment_name=attachment_name,
                                                   attachment_size=attachment_size,
                                                   only_clickable=only_clickable)

    def quarantines_search_across(self,
                                  received=None,
                                  sender_rule=None,
                                  sender_text=None,
                                  recipient_rule=None,
                                  recipient_text=None,
                                  subject_rule=None,
                                  subject_text=None,
                                  quarantines=None,
                                  attachment_name=None,
                                  attachment_size=None):
        """
        Performs search across quarantines using WUI controls.
        Does not return any results, just runs search query.

        Rules common for `sender_rule`, `recipient_rule`, `subject_rule` parameters:
        | Contains |
        | Starts with |
        | Ends with |
        | Matches exactly |
        | Does Not Contain |
        | Does Not Start With |
        | Does Not End With |
        | Does Not Match |

        *Parameters*:
        - `received`: The period when message was received. Options as they are seen in WUI.
        | Today |
        | Last 7 days |
        | Between |
        To define _Between_ - provide start and end dates in format: mm/dd/yyyy.
        Separate start and end dates with comma.
        - `sender_rule`: Rule to use for Envelope Sender field. See available options above.
        - `sender_text`: Envelope sender field.
        - `recipient_rule`: Rule to use for Recipient field. See available options above.
        - `recipient_text`: Recipient field.
        - `subject_rule`: Rule to use for Subject field. See available options above.
        - `subject_text`: Subject field.
        - `quarantines`: Quarantines to search in. Use 'All' to search in all quarantines,
        or specify a list of quarantines names or string of comma-separated values. Optional.
        - `attachment_name`: Attachment name.
        - `attachment_size`: Attachment size. Must be in format: size_condition: size.
        If size condition is range, then pass size1 and size2 separated by comma.
        Available size conditions are:
        | Less than |
        | More than |
        | Range |

        *Return*:
        None.

        *Examples*:
        | Quarantines Search |
        | ... | sender_rule=matches exactly |
        | ... | sender_text=test@mail.qa |
        | ... | received=last 7 days |
        | ... | quarantines=${list_of_quarantines} |

        | Quarantines Search |
        | ... | sender_rule=Starts with |
        | ... | sender_text=test |
        | ... | received=08/08/2012, 08/10/2012 |
        | ... | recipient_rule=Does Not Contain |
        | ... | recipient_text=mail.qa |
        | ... | quarantines=Policy, Outbreak |

        | Quarantines Search |
        | ... | quarantines=All |
        """
        self._open_page()
        self.click_button(SEARCH_QUARANTINE_SEARCH_ACROSS_BUTTON)
        self._fill_received_parameters(received)
        self._fill_matching_parameters(
            (SEARCH_QUARANTINE_ENVELOPE_SENDER_METHOD, sender_rule),
            (SEARCH_QUARANTINE_ENVELOPE_SENDER_TEXT, sender_text)
        )
        self._fill_matching_parameters(
            (SEARCH_QUARANTINE_ENVELOPE_RCPT_METHOD, recipient_rule),
            (SEARCH_QUARANTINE_ENVELOPE_RCPT_TEXT, recipient_text)
        )
        self._fill_matching_parameters(
            (SEARCH_QUARANTINE_SUBJECT_METHOD, subject_rule),
            (SEARCH_QUARANTINE_SUBJECT_TEXT, subject_text)
        )
        self._fill_quarantines_parameters(quarantines)
        self._fill_attachment_parameters(attachment_name, attachment_size)
        self.click_button(SEARCH_QUARANTINE_SEARCH_BUTTON)

    def quarantines_search_get_messages(self,
                                        items_per_page=None,
                                        mid_as_key=False):
        """
        Return messages from search resutls table.

        *Parameters*:
        - `items_per_page`: The page size (items per page to display). Options are as the seen in WUI.
        | 20 |
        | 50 |
        | 100 |
        | 250 |
        Does not have any direct impact on end result.
        - `mid_as_key`: Each element in result list will be a dictionary.
        Make MID value key of dictionary or not. Boolean. False by default.

        *Examples*:
        | @{res}= | Quarantines Search Get Messages |
        | ... | items_per_page=50 |
        | ... | mid_as_key=${True} |
        | Log List | ${res} |
        | :FOR | ${r} | IN | @{res} |
        | \   Log Dictionary | ${r} |

        *Return*:
        List of dictionaries.

        *Exceptions*:
        - `NoMessagesFound`: If there are no messages in quarantine.
        """
        self._handle_no_messages_found(err='No messages were found')
        return self._get_all_messages \
            (items_per_page=items_per_page, mid_as_key=mid_as_key)

    def quarantines_search_get_all_messages(self,
                                            name=None,
                                            items_per_page=None,
                                            mid_as_key=False):
        """
        Get all messages under given quarantine.

        *Parameters*:
        - `name`: The name of the quarantine to open. Optional.
        Assume we are at needed page if this parameter was not given.
        - `items_per_page`: The page size (items per page to display).
        Options are as they seen in WUI.
        | 20 |
        | 50 |
        | 100 |
        | 250 |
        - `mid_as_key`: Each element in result list will be a dictionary.
        Make MID value key of dictionary or not. Boolean. False by default.

        *Return*:
        List of dictionaries.

        *Examples*:
        | ${res}= | Quarantines Search Get All Messages | name=Virus |
        | Log List | ${res} |

        | ${res}= | Quarantines Search Get All Messages | name=Virus | mid_as_key=${True} |
        | Log List | ${res} |

        *Exceptions*:
        - `NoSuchQuarantine`: If there is no such quarantine.
        - `NoMessagesInQuarantine`: If quarantine is present but it has '0' messages.
        - `NoMessagesFound`: If there are no messages in quarantine.
        """
        self._open_quarantine_search_page(quarantine_name=name)
        self._press_view_all_messages_button()
        self._handle_no_messages_found(err='No messages were found')
        return self._get_all_messages \
            (items_per_page=items_per_page, mid_as_key=mid_as_key)

    def quarantines_search_message_by_mid(self,
                                          name=None,
                                          mid=None,
                                          items_per_page=None):
        """
        Does not invoke search activities with WUI controls.
        Instead walks through pages in quarantine looking for given MID.
        If MID was found - open quarantined message.

        *Parameters*:
        - `name`: The name of the quarantine to open. Optional.
        Assume we are at needed page if this parameter was not given.
        - `mid`: Open message by MID. Will walk through all pages until message with given MID found.
        - `items_per_page`: The page size (items per page to display). Options are as the seen in WUI.
        | 20 |
        | 50 |
        | 100 |
        | 250 |
        Does not have any direct impact on end result.

        *Return*:
        Boolean. True - if message was found and opened.

        *Exceptions*:
        - `NoSuchQuarantine`: If there is no such quarantine.
        - `NoMessagesInQuarantine`: If quarantine is present but it has '0' messages.
        - `NoMessagesFound`: If there are no messages in quarantine.

        *Examples*:
        | ${res}= | Quarantines Search Message By Mid | name=Policy | mid=535 |
        | Log | ${res} |
        """
        self._open_quarantine_search_page(quarantine_name=name)
        return self._search_by_mid(mid=mid, items_per_page=items_per_page)

    def quarantines_search_message_open(self,
                                        items_per_page=None,
                                        mid=None,
                                        first_message=True):
        """
        Open first message or message with given MID.

        *Parameters*:
        - `items_per_page`: The page size (items per page to display). Options are as the seen in WUI.
        | 20 |
        | 50 |
        | 100 |
        | 250 |
        Does not have any direct impact on end result.
        - `first_message`: Open first message from the results. True by default.
        - `mid`: Open message by MID. Will walk through all pages until message with given MID found.

        *Return*:
        Boolean. True - if message was found and opened.

        *Examples*:
        This keyword finds and opens message.

        | ${res}= | Quarantines Search Message Open |
        | ... | name=Virus |
        | ... | mid=898234728364872 |

        | ${res}= | Quarantines Search Message Open |
        | ... | name=Policy |

        Now we have message opened and we can proceed with other keywords,
        like `Quarantines Message Release`, `Quarantines Message Delete`,
        `Quarantines Message Rescan`, `Quarantines Message Get Details`.

        *Exceptions*:
        - `NoMessagesFound`: If there are no messages in quarantine.
        """
        if mid:
            return self._search_by_mid(mid=mid,
                                       items_per_page=items_per_page)
        elif first_message:
            return self._open_message_in_quarantine(1)

    def quarantines_search_message_view_tracking_details(self,
                                                         items_per_page=None,
                                                         mid=None,
                                                         first_message=True):
        """
        Drill down to tracking details of first message or message with given MID.

        *Parameters*:
        - `items_per_page`: The page size (items per page to display). Options are as the seen in WUI.
        | 20 |
        | 50 |
        | 100 |
        | 250 |
        Does not have any direct impact on end result.
        - `first_message`: Open tracking details of first message from the results. True by default.
        - `mid`: Open tracking details of message by MID. Will walk through all pages until message with given MID found.

        *Return*:
        Boolean. True - if message was found and tracking details opened.

        *Examples*:

        | ${res}= | Quarantines Search Message View Tracking Details |
        | ... | name=Virus |
        | ... | mid=898234728364872 |

        | ${res}= | Quarantines Search Message View Tracking Details |
        | ... | name=Policy |

        *Exceptions*:
        - `NoMessagesFound`: If there are no messages in quarantine.
        """
        if mid:
            return self._search_by_mid(mid=mid,
                                       items_per_page=items_per_page,
                                       call_method='_view_tracking_details')
        elif first_message:
            return self._view_tracking_details(1)

    def quarantines_search_release(self,
                                   items_per_page=None,
                                   action_on=None,
                                   mid=None,
                                   first_message=True):
        """
        Release message(s) from the quarantine.

        *Parameters*:
        - `items_per_page`: The page size (items per page to display). Options are as the seen in WUI.
        | 20 |
        | 50 |
        | 100 |
        | 250 |
        Does not have any direct impact on end result.
        - `action_on`: Items to apply action to.
        | Action on selected items |
        | Action on All _NUMBER_ items |
        - `mid`: Select message by MID. Will walk through all pages until message with given MID found.
        - `first_message`: Select first message from results.

        *Return*:
        Action result. String.

        *Examples:*
        First perform search.
        | Quarantines Search |
        | ... | name=Policy |
        | ... | received=today |
        | ... | recipient_rule=contains |
        | ... | recipient_text=${policy_to} |
        Then release first message.
        | ${res}= | Quarantines Search Release |
        Or release message by MID value.
        | ${res}= | Quarantines Search Release | mid=345123 |
        Or release all messages that matched the query.
        | ${res}= | Quarantines Search Release | action_on=all |

        *Exceptions*:
        - `NoMessagesFound`: If there are no messages in quarantine.
        """
        self._handle_no_messages_found(err='No messages were found')
        self._set_items_per_page(items_per_page)
        self._select_action_on(action_on)
        if self._is_action_on_all():
            return self._apply_action_to_messages('Release')
        elif first_message:
            self._select_message_in_first_row()
        elif mid is not None:
            self._search_by_mid \
                (mid=mid, items_per_page=items_per_page, select_only=True)
        return self._apply_action_to_messages('Release')

    def quarantines_search_delete(self,
                                  items_per_page=None,
                                  action_on=None,
                                  mid=None,
                                  first_message=True):
        """
        Delete message(s) from the quarantine.

        *Parameters*:
        - `items_per_page`: The page size (items per page to display).
        Options are as they seen in WUI.
        | 20 |
        | 50 |
        | 100 |
        | 250 |
        Does not have any direct impact on end result.
        - `action_on`: Items to apply action to.
        | Action on selected items |
        | Action on All NUMBER items |
        - `mid`: Select message by MID. Will walk through all pages until message with given MID found.
        - `first_message`: Select first message from results.

        *Return*:
        Action result. String.

        *Examples*:
        First perform search query.
        | Quarantines Search |
        | ... | name=Virus |
        | ... | received=today |
        | ... | subject_rule=contains |
        | ... | subject_text=${viral_subj} |
        Then delete first message that mathed the query.
        | ${res}= | Quarantines Search Delete | action_on=selected items |
        | Log | ${res} |

        Or delete all messages that mathed the query.
        | ${res}= | Quarantines Search Delete | action_on=all |
        | Log | ${res} |

        Or just delete all messages under quarantine.
        | ${res}= | Quarantines Search View All Messages | name=Virus |
        | Quarantines Search Delete | action_on=all |
        | Log | ${res} |

        *Exceptions*:
        - `NoMessagesFound`: If there are no messages in quarantine.
        """
        self._handle_no_messages_found(err='No messages were found')
        self._set_items_per_page(items_per_page)
        self._select_action_on(action_on)
        if self._is_action_on_all():
            return self._apply_action_to_messages('Delete')
        elif first_message:
            self._select_message_in_first_row()
        elif mid is not None:
            self._search_by_mid \
                (mid=mid, items_per_page=items_per_page, select_only=True)
        return self._apply_action_to_messages('Delete')

    def quarantines_search_schedule_exit_by(self,
                                            delay_by,
                                            items_per_page=None,
                                            action_on=None,
                                            mid=None,
                                            first_message=True):
        """
        Schedule exit for messages.

        *Parameters*:
        - `delay_by`: Scheduled exit. Mandatory.
        | 8 Hours |
        | 24 Hours |
        | 48 Hours |
        | 1 Week |
        - `items_per_page`: The page size (items per page to display). Options are as the seen in WUI.
        | 20 |
        | 50 |
        | 100 |
        | 250 |
        Does not have any direct impact on end result.
        - `action_on`: Items to apply action to.
        | Action on selected items |
        | Action on All NUMBER items |
        - `mid`: Select message by MID. Will walk through all pages until message with given MID found.
        - `first_message`: Select first message from results.

        *Return*:
        Action result. String.

        *Examples:*
        | Quarantines Search |
        | ... | name=Policy |
        | ... | received=today |
        | ... | subject_rule=contains |
        | ... | subject_text=babar |
        | ${res}= | Quarantines Search Schedule Exit By | 8 hours | action_on=all |
        | Log | ${res} |

        *Exceptions*:
        - `NoMessagesFound`: If there are no messages in quarantine.
        """
        self._handle_no_messages_found(err='No messages were found')
        self._set_items_per_page(items_per_page)
        self._select_action_on(action_on)
        if self._is_action_on_all():
            return self._apply_action_to_messages \
                ('scheduled exit', scheduler=delay_by)
        elif first_message:
            self._select_message_in_first_row()
        elif mid is not None:
            self._search_by_mid \
                (mid=mid, items_per_page=items_per_page, select_only=True)
        return self._apply_action_to_messages \
            ('scheduled exit', scheduler=delay_by)

    def quarantines_search_send_copy_to(self,
                                        address,
                                        items_per_page=None,
                                        action_on=None,
                                        mid=None,
                                        first_message=True):
        """
        Send copy of message(s) to email address.

        *Parameters*:
        - `address`: An email address to send copy to. Mandatory.
        - `items_per_page`: The page size (items per page to display). Options are as the seen in WUI.
        | 20 |
        | 50 |
        | 100 |
        | 250 |
        Does not have any direct impact on end result.
        - `action_on`: Items to apply action to.
        | Action on selected items |
        | Action on All NUMBER items |
        - `mid`: Select message by MID. Will walk through all pages until message with given MID found.
        - `first_message`: Select first message from results.

        *Return*:
        Action result. String.

        *Examples:*
        | Quarantines Search |
        | ... | name=${q1} |
        | ... | sender_rule=matches exactly |
        | ... | sender_text=${custom_from} |
        | ... | received=today |
        | ... | recipient_rule=matches exactly |
        | ... | recipient_text=${custom_to} |
        | ${res}= | Quarantines Search Send Copy To | testuser@${CLIENT} |

        *Exceptions*:
        - `NoMessagesFound`: If there are no messages in quarantine.
        """
        self._handle_no_messages_found(err='No messages were found')
        self._set_items_per_page(items_per_page)
        self._select_action_on(action_on)
        if self._is_action_on_all():
            return self._apply_action_to_messages('Send Copy', address=address)
        elif first_message:
            self._select_message_in_first_row()
        elif mid is not None:
            self._search_by_mid \
                (mid=mid, items_per_page=items_per_page, select_only=True)
        return self._apply_action_to_messages('Send Copy', address=address)

    def quarantines_search_move_to(self,
                                   destination,
                                   items_per_page=None,
                                   action_on=None,
                                   mid=None,
                                   first_message=True):
        """
        Move message(s) to another quarantine.

        *Parameters*:
        - `items_per_page`: The page size (items per page to display). Options are as the seen in WUI.
        | 20 |
        | 50 |
        | 100 |
        | 250 |
        Does not have any direct impact on end result.
        - `action_on`: Items to apply action to.
        | Action on selected items |
        | Action on All NUMBER items |
        - `mid`: Select message by MID. Will walk through all pages until message with given MID found.
        - `first_message`: Select first message from results.

        *Return*:
        Action result. String.

        *Examples:*
        | Quarantines Search View All Messages | name=Policy |
        | ${res}= | Quarantines Search Schedule Move To | Quarantine1 | action_on=all |

        *Exceptions*:
        - `NoMessagesFound`: If there are no messages in quarantine.
        """
        self._handle_no_messages_found(err='No messages were found')
        self._set_items_per_page(items_per_page)
        self._select_action_on(action_on)
        if self._is_action_on_all():
            return self._apply_action_to_messages \
                ('Move', destination=destination)
        elif first_message:
            self._select_message_in_first_row()
        elif mid is not None:
            self._search_by_mid \
                (mid=mid, items_per_page=items_per_page, select_only=True)
        return self._apply_action_to_messages \
            ('Move', destination=destination)
