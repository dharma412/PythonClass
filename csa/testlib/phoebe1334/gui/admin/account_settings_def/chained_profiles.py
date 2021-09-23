#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1350/gui/admin/account_settings_def/chained_profiles.py#1 $
# $DateTime: 2020/01/06 01:25:43 $
# $Author: saurgup5 $

from common.gui.inputs_owner import InputsOwner, get_module_inputs_pairs
from common.logging import Logger

PROFILE_NAME = ('Profile Name', "//input[@id='chained_profile_name']")
DESCRIPTION = ('Description', "//textarea[@id='chained_profile_desc']")
CHAINED_PROFILES_TABLE = "//table[@id='profiles_of_cp']"
CHAINED_PROFILES_TABLE_ALL_ROWS = "%s/tbody/tr" % CHAINED_PROFILES_TABLE
CHAINED_PROFILES_ADD_MAR_PROFILE = \
                lambda idx: "%s//select[@id='profiles_of_cp[%s][profile_name]']" \
                % (CHAINED_PROFILES_TABLE, idx)
CHAINED_PROFILES_DELETE_MAR_PROFILE = \
                lambda idx: "%s//select[@id='profiles_of_cp[%s][profile_name]']" \
                "/following-sibling::td[3]/img" % (CHAINED_PROFILES_TABLE, idx)
CHAINED_PROFILES_ADD_ACCOUNT_PROFILE_BUTTON = \
                "//input[@id='profiles_of_cp_domtable_AddRow']"
MAR_PROFILES_LIST = ('Mar Profiles', "//select[@id='profiles_of_cp[0][profile_name]']")
CHAINED_PROFILE_EDIT_MAR_PROFILES = ('Mar Profile Settings', 'dummy')
CHAINED_PROFILE_EDIT_MAR_PROFILES_TABLE_ROWS = \
                "%s/tbody[@id='profiles_of_cp_rowContainer']/tr" % CHAINED_PROFILES_TABLE

class ChainedProfiles(InputsOwner, Logger):
    def _get_registered_inputs(self):
        return get_module_inputs_pairs(__name__)

    def set(self, new_value):
        number_of_profiles = len(new_value['Mar Profiles'])
        self._set_edits(new_value, PROFILE_NAME, DESCRIPTION)
        for index in range(number_of_profiles):
            self.gui.select_from_list_by_label(
                    CHAINED_PROFILES_ADD_MAR_PROFILE(index),
                    new_value['Mar Profiles'][index])
            if number_of_profiles > 1 and index != (number_of_profiles - 1):
                self.gui.click_button(
                        CHAINED_PROFILES_ADD_ACCOUNT_PROFILE_BUTTON,
                        "don't wait")

    def edit(self, new_value):
        self._set_edits(new_value, DESCRIPTION)
        mar_profile_settings = new_value['Mar Profile Settings']
        all_rows = int(self.gui.get_matching_xpath_count(CHAINED_PROFILES_TABLE_ALL_ROWS))
        number_of_mar_profiles = int(all_rows) - 2
        for setting in mar_profile_settings:
            (profile, action, new_profile)= setting.split(':')
            if action.lower() == 'alter':
                row_index = self._get_row_index(profile)
                if row_index:
                    row_edit_xpath = "%s[%s]/td[1]/select" % \
                        (CHAINED_PROFILE_EDIT_MAR_PROFILES_TABLE_ROWS, row_index)
                    self.gui.select_from_dropdown_list(row_edit_xpath, new_profile)
                else:
                    raise ValueError('Could not find row index for MAR profile edit')
            elif action.lower() == 'add':
                self.gui.click_button(
                        CHAINED_PROFILES_ADD_ACCOUNT_PROFILE_BUTTON,
                        "don't wait")
                row_index = self._get_row_index('-- Select Profile --')
                if row_index:
                    row_edit_xpath = "%s[%s]/td[1]/select" % \
                        (CHAINED_PROFILE_EDIT_MAR_PROFILES_TABLE_ROWS, row_index)
                    self.gui.select_from_dropdown_list(row_edit_xpath, new_profile)
                else:
                    raise ValueError('Could not find row index for MAR profile add')
            elif action.lower() == 'delete':
                row_index = self._get_row_index(profile)
                if row_index:
                    row_delete_xpath = "%s[%s]/td[1]/following-sibling::td[3]/img" % \
                        (CHAINED_PROFILE_EDIT_MAR_PROFILES_TABLE_ROWS, row_index)
                    self.gui.click_button(row_delete_xpath, "don't wait")
                else:
                    raise ValueError('Could not find row index for MAR profile delete')
            else:
                raise ValueError('"%s" operation is not permitted. '\
                        'Allowed operations are: add | alter | delete')

    def _get_row_index(self, profile_name):
        """
        This method is to find the row index of the MAR profiles configured
        under a chained profile. This how it works:
            * Finds the number of rows for configured MAR profiles
            * Iterates over each row and
                ** Finds the list items from the drop down list of the first.
                   column (td[1]) which will return all the available MAR profile
                   names.
                ** Iterates over each list attribute and find the SELECTED one.
                ** Checks if the SELECTED one matches the profile names passed.
                ** If YES then returns the row index Else continues with the
                   next option.
        """
        number_of_rows = int(self.gui.get_matching_xpath_count(\
                             CHAINED_PROFILE_EDIT_MAR_PROFILES_TABLE_ROWS))
        self._debug('number_of_rows: %s' % number_of_rows)
        for row in xrange(1, number_of_rows + 1):
            td1_xpath = "%s[%s]/td[1]/select" % (CHAINED_PROFILE_EDIT_MAR_PROFILES_TABLE_ROWS, row)
            selected_option = self.gui._get_selected_label(td1_xpath)
            self._debug('row - %s, selected option - %s' % (row, selected_option))
            if profile_name.lower() == selected_option.lower():
                self._debug('Found matching row index - %s' % row)
                return row
            else:
                self._debug('Looking into next row')
        return None
