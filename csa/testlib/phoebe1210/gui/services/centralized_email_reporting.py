#!/usr/bin/env python
# -*- coding: latin-1 -*-
# $Id: //prod/main/sarf_centos/testlib/phoebe1210/gui/services/centralized_email_reporting.py#1 $ $DateTime: 2019/05/07 03:16:10 $ $Author: 

import common.gui.guiexceptions as guiexceptions
from common.gui.guicommon import GuiCommon

ENABLE_BUTTON = 'name=action:Enable'
ENABLE_REPORTING_CHECKBOX = 'id=enabled'
ACCEPT_LICENSE_BUTTON = 'name=action:AcceptLicense'
ADD_GROUP_BUTTON = 'name=action:GroupEdit'
GROUP_NAME_TEXTBOX = 'name=groupname'
APPLIANCES_LIST = 'name=allhosts[]'
GROUP_MEMBERS_LIST = 'name=grouphosts[]'
ADD_MEMBER_BUTTON = u'xpath=//input[@value="Add »"]'
REMOVE_MEMBER_BUTTON = u'xpath=//input[@value="« Remove"]'
EDIT_GROUP_LINK = lambda group: 'link=%s' % (group,)
GROUPS_TABLE_ROW = "//table[@class='cols']//tr"
GROUP_NAME_CELL = lambda row: '%s[%s]/td[1]' % (GROUPS_TABLE_ROW, row)
DELETE_GROUP_LINK = lambda row: '%s[%s]/td[3]/img' % (GROUPS_TABLE_ROW, row)
Local = "xpath=//input[@id='slave_enabled_0']"
Centralized = "xpath=//input[@id='slave_enabled_1']"


class CentralizedEmailReporting(GuiCommon):
    """Keywords for Services--> Reporting
    """

    def get_keyword_names(self):
        return ['centralized_email_reporting_enable',
                ]

    def _open_page(self):
        self._navigate_to('Security Services', 'Reporting')

        err_msg = 'The feature key for this feature has expired or is ' \
                  'unavailable'
        if self._is_text_present(err_msg):
            raise guiexceptions.GuiFeaturekeyMissingError(err_msg)

    def _click_enable_reporting_button(self):
        self.click_button(ENABLE_BUTTON)

    def _accept_license(self):
        if self._is_element_present(ACCEPT_LICENSE_BUTTON):
            self.click_button(ACCEPT_LICENSE_BUTTON)

    def _is_reporting_disabled(self):
        return self._is_text_present(
            'Reporting service is currently disabled.')

    def _are_appliances_available(self):
        return not self._is_text_present('There are no email appliances ' \
                                         'available')

    def _check_reporting_status(self):
        if self._is_reporting_disabled():
            err_msg = 'Centralized Email Reporting is disabled'
        elif not self._are_appliances_available():
            err_msg = 'Email appliances are not available'
        else:
            return

        raise guiexceptions.GuiFeatureDisabledError(err_msg)

    def _uncheck_reporting_checkbox(self):
        self.unselect_checkbox(ENABLE_REPORTING_CHECKBOX)

    def _click_add_group_button(self):
        self.click_button(ADD_GROUP_BUTTON)

    def _fill_reporting_group_info(self, name, appliances):
        if name is not None:
            self._fill_group_name_textbox(name)

        if appliances is not None:
            self._select_appliances(appliances)

    def _fill_group_name_textbox(self, name):
        self.input_text(GROUP_NAME_TEXTBOX, name)

    def _select_appliances(self, appliances):
        self._clear_members_list()

        for appliance in self._convert_to_tuple(appliances):
            available_members = \
                self.get_list_items(APPLIANCES_LIST)
            for member in available_members:
                if appliance in member:
                    self.select_from_list(APPLIANCES_LIST, member)
                    self.click_button(ADD_MEMBER_BUTTON, 'dont wait')
                    break
            else:
                raise guiexceptions.GuiValueError('"%s" appliance does not ' \
                                                  'exist' % (appliance,))

    def _clear_members_list(self):
        members = self.get_list_items(GROUP_MEMBERS_LIST)
        for member in members:
            if member:
                self.select_from_list(GROUP_MEMBERS_LIST, member)
                self.click_button(REMOVE_MEMBER_BUTTON, 'dont wait')

    def _click_edit_group_link(self, name):
        edit_link = EDIT_GROUP_LINK(name)
        if self._is_element_present(edit_link):
            self.click_element(edit_link)

        else:
            raise guiexceptions.GuiValueError('"%s" group does not exist' % \
                                              (name,))

    def _get_table_row_index(self, name):
        starting_row = 2
        num_of_rows = int(self.get_matching_xpath_count(GROUPS_TABLE_ROW))
        for row in xrange(starting_row, num_of_rows + 1):
            if name == self.get_text(GROUP_NAME_CELL(row)):
                return row

    def _click_delete_group_link(self, name):
        table_row = self._get_table_row_index(name)
        if table_row is None:
            raise guiexceptions.GuiValueError('"%s" group does not exist' % (name,))

        self.click_element(DELETE_GROUP_LINK(table_row), 'dont wait')

    def centralized_email_reporting_enable(self):
        """Enable Centralized Email Reporting.

        Examples:
        | Centralized Email Reporting Enable |

        Exceptions:
        - `GuiFeaturekeyMissingError`: in case feature key has expired or is
           unavailable.
        """

        self._open_page()
        self._click_edit_settings_button()
        self._click_radio_button(Centralized)
        self._click_submit_button()
