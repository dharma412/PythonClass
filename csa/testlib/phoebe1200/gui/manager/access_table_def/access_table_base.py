#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/phoebe1200/gui/manager/access_table_def/access_table_base.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $

import functools
import time

from common.gui.guicommon import GuiCommon
import common.gui.guiexceptions as guiexceptions
from common.util.sarftime import CountDownTimer

LISTENER_DROPDOWN = '//select[@name=\'listener_id\']'


def navigate_to_page(self, page_path):
    self._debug('Opening "%s" page' % (' -> '.join(page_path),))
    self._navigate_to(*page_path)
    if self._is_text_present('There are no configured listeners.'):
        raise guiexceptions.ConfigError('There are no ' \
                                        'configured listeners.')


def go_to_access_table(page_path, listener_opts=None):
    """Decorator intended for startup method navigation

    *Parameters:*
    - `page_path`: tuple, contains path to page in menu
    passed to _navigate_to method
    - `listener_opts`: tuple, contains listener combo locator
    and locator of an element to wait for after combo item
    selection. If None then Selenium will only navigate to
    page by page_path

    *Notes:*
    If listener_opts is not None then this decorator can only be
    applied for class methods whose first parameter (after self)
    is target listener name
    """

    def decorator(func):
        if listener_opts:
            @functools.wraps(func)
            def worker(self, listener_name, *args, **kwargs):
                navigate_to_page(self, page_path)
                self._go_to_listener_option(listener_name, *listener_opts)
                return func(self, listener_name, *args, **kwargs)

            return worker
        else:
            @functools.wraps(func)
            def worker(self, *args, **kwargs):
                navigate_to_page(self, page_path)
                return func(self, *args, **kwargs)

            return worker

    return decorator


class AccessTableBase(GuiCommon):
    """Base class for GUI interaction with
    HAT and RAT
    """

    def _go_to_listener_option(self, listener_name, listener_dropdown_locator,
                               target_control_locator):
        """Selects corresponding listener for access table

        *Parameters*:
        - `listener_name`: listener name to be selected
        - `listener_dropdown_locator`: combo box locator
        - `target_control_locator`: target control to wait for after
        combo box value is changed

        *Exceptions:*
        - `ValueError`: if listener with given name does not exist
        """
        listener_list = self._get_available_options_from_select(listener_dropdown_locator)
        listener_option = filter(lambda x: x.find(listener_name) >= 0,
                                 listener_list)
        if listener_option:
            if self.get_value(listener_dropdown_locator) != listener_option[0]:
                self.select_from_list(listener_dropdown_locator,
                                      listener_option[0])
                self._wait_for_element(target_control_locator)
        else:
            raise ValueError('"%s" listener not found' % (listener_name,))

    def _wait_for_element(self, locator, max_wait_time=10):
        """Waits till given element appears on page

        *Parameters:*
        - `locator`: target element locator
        - `max_wait_time`: maximum seconds to wait for

        *Exceptions:*
        - `guiexceptions.TimeoutError`: if target element is not found
        within acceptable time range
        """
        assert max_wait_time > 2
        timer = CountDownTimer(max_wait_time).start()
        while timer.is_active():
            # Tricky check for AJAX requests
            is_element_really_present = True
            for check_num in xrange(2):
                if not self._is_element_present(locator):
                    is_element_really_present = False
                    break
                time.sleep(1.0)
            if is_element_really_present:
                return
            time.sleep(1.0)
        raise guiexceptions.TimeoutError('Element with locator "%s" has not been populated' \
                                         ' within %d seconds timeout' % (locator,
                                                                         max_wait_time))
