#!/usr/bin/env python

import time

import common.gui.guiexceptions as guiexceptions
from common.gui.guicommon import GuiCommon

ADD_MODULE_BUTTON = "//div[contains(@class,'add_module')]"
OK_BUTTON = "//div[@id='add_module_dlg']//button[text()='OK']"
MODULES_NAMES="//span[contains(@class,'display_name')]"
CONFIRM_BUTTON = "//div[@id='confirmation_dialog']//button[text()='Confirm']"
AJAX_TIMEOUT = 10

SECTION_TABLES = {
        'System Overview':"//table[contains(@class,'dashboard-container')]",
        'Time Range': "//table[contains(@class,'date_range_box-container')]"
    }

class MyReports(GuiCommon):
    """Additional keywords to work with Reporting -> My Report page.
    """

    def get_keyword_names(self):
        return [
            'my_reports_add_module',
            'my_reports_get_modules_list',
            'my_reports_delete_module',
        ]

    def _open_page(self):
        self._navigate_to('Web','Reporting', 'My Reports')
        time.sleep(AJAX_TIMEOUT)

    def my_reports_add_module(self, section, report, module):
        """Add module to My Reports page by report name and module name

        Parameters:
            - `section`: the section that will contain the module. Mandatory.
                Currently there are two sections: 'System Overview' and
                'Time Range'
            - `report`: name of report which contain module. Mandatory.
            - `module`: module name to add. Mandatory.

        Return:
            None

        Example:
        | My Reports Add Module |
        | ... | System Overview
        | ... | System Status |
        | ... | System Uptime |

        | My Reports Add Module |
        | ... | Time Range
        | ... | URL Categories |
        | ... | Top URL Categories: Total Transactions |

        """

        self._open_page()
        self._click_add_module_button(section)
        time.sleep(5)
        self._select_module_from_list(report, module)
        self._click_ok_button()

        ready_msg = 'successfully added'
        self.wait_until_page_contains(ready_msg, AJAX_TIMEOUT)

    def my_reports_get_modules_list(self):
        """Returns list of modules on My Reports page.

        Parameters:
            None

        Return:
            List of text strings with names of modules

        Example:
        | ${names}= | My Reports Get Modules List |
        """
        modules = []

        self._open_page()
        count = int(self.get_matching_xpath_count(MODULES_NAMES))
        self._debug('found %d modules' % (count,))
        for i in xrange(1, count):
            name = self.get_text('xpath=(' + MODULES_NAMES + ')[%s]' % i)
            if name not in SECTION_TABLES.keys():
                modules.append(name)
        return modules

    def my_reports_delete_module(self, display_name=''):
        """Delete module from My Reports page by module display name

        Parameters:
            - `display_name`: module name to delete.
            If display_name is empty deletes all modules from My Reports page

        Return:
            None

        Example:
        | My Reports Delete Module |
        | ... | Overview > Total Web Proxy Activity |
        """
        if display_name:
            self._open_page()
            self._delete_module(display_name)
        else:
            modules = self.my_reports_get_modules_list()
            for display_name in modules:
                self._delete_module(display_name)


    def _click_add_module_button(self, section):
        if section not in SECTION_TABLES.keys():
            raise guiexceptions.GuiValueError('Bad section name: %s' % (section,))
        self.click_element(SECTION_TABLES[section] + ADD_MODULE_BUTTON, "don't wait")

    def _delete_module(self, display_name):
        self._click_delete_module_button(display_name)
        self._click_confirm_button()

        ready_msg = 'successfully removed'
        self.wait_until_page_contains(ready_msg, AJAX_TIMEOUT)

    def _click_ok_button(self):
        self.click_button(OK_BUTTON, "don't wait")

    def _click_delete_module_button(self, display_name):
        NAME_SELECTOR = "//span[contains(@class,'display_name') and (text()='%s')]" \
                    % display_name
        DELETE_SELECTOR = NAME_SELECTOR + "/ancestor::tr[1]//div[contains(@class,'delete')]"
        self.click_element(DELETE_SELECTOR, "don't wait")

    def _click_confirm_button(self):
        self.click_button(CONFIRM_BUTTON, "don't wait")

    def _select_module_from_list(self, report_name, module_name):
        SELECT = "//select[@id='select_module']"
        LIST_ELEMENT = "//optgroup[@label='%s']/option[text()='%s']" \
            % (report_name, module_name)
        VALUE_SELECTOR = SELECT + LIST_ELEMENT
        self._debug('searching for value using xpath: %s' % (VALUE_SELECTOR,))
        value = self.get_value(VALUE_SELECTOR)
        self._debug('found value: %s' % (value,))
        if not value:
            raise guiexceptions.GuiValueError('Cannot add module')

        self.select_from_list(SELECT, value)

