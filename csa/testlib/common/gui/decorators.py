#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/common/gui/decorators.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $

import functools

from robot.libraries.BuiltIn import BuiltIn


def go_to_page(page_path):
    """Decorator used for GuiCommon class
    descendants for navigating to the necessary page.

    *Parameters:*
    - `page_path`: tuple containing page path elements, for example
    ('System Administration', 'LDAP')
    """

    def decorator(func):
        @functools.wraps(func)
        def worker(self, *args, **kwargs):
            self._debug('Navigating to "%s"' % (' -> '.join(page_path),))
            self.navigate_to(*page_path)
            return func(self, *args, **kwargs)

        return worker

    return decorator


def set_speed(speed, selenium_obj_name=None):
    """Decorator used for GuiCommon class descendants for
    setting the delay that is waited after each Selenium command.

    *Parameters:*
    - `speed`: Time in seconds. May be given in Robot Framework time format.
    - `selenium_obj_name`: the name of object attribute that contains selenium's
    set_selenium_speed method. `self` is taken by default

    By default selenium has 1 second delay between each command,
    This makes tests extremely slow when parsing large tables
    (like message tracking results, quarantines etc).
    There is no reason to have such delay when parsing static tables.

    Sets old selenium speed after job is done.
    """

    def wrapper(func):
        @functools.wraps(func)
        def worker(self, *args, **kwargs):
            if selenium_obj_name is not None:
                selenium_obj = getattr(self, selenium_obj_name)
            else:
                selenium_obj = self
            old = selenium_obj.set_selenium_speed(speed)
            BuiltIn().log('Changed selenium speed: %s => %s' % (old, speed))
            try:
                result = func(self, *args, **kwargs)
            finally:
                selenium_obj.set_selenium_speed(old)
                BuiltIn().log('Changed selenium speed: %s => %s' % (speed, old))
            return result

        return worker

    return wrapper


def visit_page(page_path, urlpath, wait=True):
    """Decorator used for GuiCommon class
    descendants for navigating to the necessary page.

    *Parameters:*
    - `page_path`: tuple containing page path elements, for example
    PAGE xpath
    """

    def decorator(func):
        @functools.wraps(func)
        def worker(self, *args, **kwargs):
            self._debug('Visiting to "%s %s"' % (page_path, wait))
            self._visit_to(page_path, urlpath, wait=wait)
            return func(self, *args, **kwargs)

        return worker

    return decorator
