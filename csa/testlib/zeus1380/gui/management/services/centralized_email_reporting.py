#!/usr/bin/env python
# -*- coding: latin-1 -*-
# $Id: //prod/main/sarf_centos/testlib/zeus1380/gui/management/services/centralized_email_reporting.py#1 $ $DateTime: 2020/05/25 00:19:30 $ $Author: sarukakk $


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


class CentralizedEmailReporting(GuiCommon):

    """Keywords for Management Appliance -> Centralized Services -> Centralized
    Email Reporting
    """

    def get_keyword_names(self):
        return ['centralized_email_reporting_enable',
                'centralized_email_reporting_disable',
                'centralized_email_reporting_group_add',
                'centralized_email_reporting_group_edit',
                'centralized_email_reporting_group_delete',
                ]

    def _open_page(self):
        self._navigate_to('Management', 'Centralized Services',
            'Centralized Reporting')

        err_msg = 'The feature key for this feature has expired or is '\
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
        return not self._is_text_present('There are no email appliances '\
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
            available_members =\
                self.get_list_items(APPLIANCES_LIST)
            for member in available_members:
                if appliance in member:
                    self.select_from_list(APPLIANCES_LIST, member)
                    self.click_button(ADD_MEMBER_BUTTON, 'dont wait')
                    break
            else:
                raise guiexceptions.GuiValueError('"%s" appliance does not '\
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
            raise guiexceptions.GuiValueError('"%s" group does not exist' %\
                (name,))

    def _get_table_row_index(self, name):
        starting_row = 2
        num_of_rows = int(self.get_matching_xpath_count(GROUPS_TABLE_ROW))
        for row in xrange(starting_row, num_of_rows+1):
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

        if not self._is_reporting_disabled():
            return

        self._click_enable_reporting_button()

        self._accept_license()

        self._check_action_result()

    def centralized_email_reporting_disable(self):
        """Disable Centralized Email Reporting.

        Examples:
        | Centralized Email Reporting Disable |

        Exceptions:
        - `GuiFeaturekeyMissingError`: in case feature key has expired or is
           unavailable.
        """

        self._open_page()

        if self._is_reporting_disabled():
            return

        self._click_edit_settings_button()

        self._uncheck_reporting_checkbox()

        self._click_submit_button()

    def centralized_email_reporting_group_add(self, name, appliances):
        """Add Email appliance reporting group.

        Parameters:
        - `name`: name of the reporting group to add.
        - `appliances`: string of comma-separated values of the names or IP
           addresses of the appliances to add to the reporting group.

        Examples:
        | Centralized Email Reporting Group Add | testgroup | esa0, esa1 |
        | Centralized Email Reporting Group Add | newroup | esa2 |

        Exceptions:
        - `GuiValueError`: in case of invalid appliance name.
        - `GuiFeatureDisabledError`: in case there are no email appliances
           available or Email reporting is disabled.
        - `GuiFeaturekeyMissingError`: in case feature key has expired or is
           unavailable.
        """

        self._open_page()

        self._check_reporting_status()

        self._click_add_group_button()

        self._fill_reporting_group_info(name, appliances)

        self._click_submit_button()

    def centralized_email_reporting_group_edit(self, name, new_name=None,
        appliances=None):
        """Edit Email Appliance reporting group.

        Parameters:
        - `name`: name of the group to edit.
        - `new_name`: new name for the reporting group.
        - `appliances`: string of comma-separated values of the names or IP
           addresses of the appliances to add to the reporting group. Previous
           configuration will be wiped out. Empty string to clear the list of
           appliances.

        Examples:
        | Centralized Email Reporting Group Edit | testgroup | newname |
        | Centralized Email Reporting Group Edit | newname |
        | ... | appliances=${EMPTY} |
        | Centralized Email Reporting Group Edit | newname |
        | ... | appliances=esa1, esa2 |

        Exceptions:
        - `GuiValueError`: in case of invalid group name or appliance name.
        - `GuiFeatureDisabledError`: in case there are no email appliances
           available or Email reporting is disabled.
        - `GuiFeaturekeyMissingError`: in case feature key has expired or is
           unavailable.
        """

        self._open_page()

        self._check_reporting_status()

        self._click_edit_group_link(name)

        self._fill_reporting_group_info(new_name, appliances)

        self._click_submit_button()

    def centralized_email_reporting_group_delete(self, name):
        """Delete Email Appliance reporting group.

        Parameters:
        - `name`: name of the group to delete.

        Examples:
        | Centralized Email Reporting Group Delete | testgroup |

        Exceptions:
        - `GuiValueError`: in case of invalid appliance group name.
        - `GuiFeatureDisabledError`: in case there are no email appliances
           available or Email reporting is disabled.
        - `GuiFeaturekeyMissingError`: in case feature key has expired or is
           unavailable.
        """

        self._open_page()

        self._check_reporting_status()

        self._click_delete_group_link(name)

        self._click_continue_button()

