#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1350/gui/web/utilities/web_traffic_tap.py#1 $
# $DateTime: 2019/09/18 01:46:35 $
# $Author: sarukakk $

import common.gui.guiexceptions as guiexceptions
from common.gui.guicommon import GuiCommon
from coeus1201.gui.manager.policybase import PolicyBase
import re

SUBMIT = "xpath=//input[@class='submit']"

POLICY_NAME = "xpath=//input[@id='policy_group_id']"
POLICY_DESCRIPTION = "xpath=//input[@id='description']"
ADD_POLICY = "xpath=//input[@value='Add Policy...']"
advanced = "xpath=//a[@onclick='toggleAdvanced();']"
select_protocols = "xpath=//a[@id='adv_membership_link_protocols']"
CHECK_HTTP = "xpath=//label[@class='label' and contains(text(),'HTTP')]"
CHECK_HTTPS = "xpath=//label[@class='label' and contains(text(),'HTTPS')]"
URL_FILTERING = "xpath=//a[contains(text(),'(global policy)')]"
TAP_ALL = "xpath=//table[@id='predefinedHeaderGrid']/tbody/tr[4]/th[2]/nobr/a/span[@class='select_all_link' and contains(text(),'Select all')]"
Uncategorized_URLs_tap = "xpath=//select[@id='uncategorized_action']/option[2][@value='tap']"
WTT_TABLE = '//table[@class=\'cols\']'
DELETE_POLICY = lambda index: '%s//tr[%s]//td[last()]/img' % (WTT_TABLE, index)
WTT_TABLE_ROW = '%s//tr' % (WTT_TABLE,)
WTTPOLICY_DATA_CELL = lambda row, column: '%s//tr[%s]//td[%s]' % (WTT_TABLE, row, column)
WTTPOLICY_CELL_TEXT = lambda row: WTTPOLICY_DATA_CELL(row, 2)


class WebTrafficTap(GuiCommon, PolicyBase):
    url_categories_column = 3

    def get_keyword_names(self):
        return [
            'add_web_traffic_policies',
            'set_url_filtering',
            'delete_web_traffic_policies',
            'web_traffic_policies_edit_url_categories',
            'wtt_policies_get_list'
        ]

    def add_web_traffic_policies(self,
                                 name,
                                 cm='',
                                 description=None,
                                 order=None,
                                 identities=None,
                                 protocols=None,
                                 subnets=None,
                                 time_range=None,
                                 match_time_range=True,
                                 url_categories=None,
                                 user_agents=None,
                                 match_agents=True):
        self._navigate_to('Web', cm, 'Web Traffic Tap Policies')
        self.click_button(ADD_POLICY, 'dont wait')
        self.input_text(POLICY_NAME, text=name)
        if description is not None:
            self.input_text(POLICY_DESCRIPTION, text=name)
        if identities:
            self._edit_identity_membership(identities)
        self._edit_advanced_settings(subnets=subnets,
                                     time_range=time_range,
                                     match_range=match_time_range,
                                     url_categories=url_categories,
                                     user_agents=user_agents,
                                     match_agents=match_agents)
        if protocols != None:
            self.click_link(advanced)
            expose_advanced = 'id=arrow_closed'
            if self._is_element_present(expose_advanced):
                if self._is_visible(expose_advanced):
                    self.click_element(expose_advanced, "don't wait")
            self.click_link(select_protocols)
            self._select_checkbox(CHECK_HTTP)
            self._select_checkbox(CHECK_HTTPS)
            self.click_button(SUBMIT, 'dont wait')
        self._click_submit_button(wait=False)

    def set_url_filtering(self, cm=''):
        self._navigate_to('Web', cm, 'Web Traffic Tap Policies')
        self.click_link(URL_FILTERING)
        self.click_element(TAP_ALL)
        self.click_element(Uncategorized_URLs_tap)
        self._click_submit_button(wait=False)

    def web_traffic_policies_edit_url_categories(self,
                                                 name,
                                                 cm='',
                                                 url_categories=None,
                                                 uncategorized_action=None,
                                                 all_predefine_url_action=None,
                                                 all_custom_url_action=None):
        self._navigate_to('Web', cm, 'Web Traffic Tap Policies')
        self._click_edit_policy_link(name, self.url_categories_column)
        custom_cats = self._get_custom_url_categories()
        predefined_cats = self._get_predefined_url_categories()
        url_categories = self._convert_to_tuple(url_categories)
        if url_categories is not None:
            for item in url_categories:
                item = self._convert_to_tuple_from_colon_separated_string(item)
                cat = item[0]
                action = item[1].lower()
                if cat in custom_cats:
                    self._edit_url_category(action, custom_cats[cat])
                elif cat in predefined_cats:
                    self._edit_url_category(action, predefined_cats[cat])
                else:
                    raise guiexceptions.GuiControlNotFoundError(
                        cat, self.get_location())
        if all_predefine_url_action:
            auc_disabled_text = \
                'Acceptable Use Controls feature is currently disabled'
            if self._is_text_present(auc_disabled_text):
                raise guiexceptions.GuiFeatureDisabledError(auc_disabled_text)
            if name.lower() == 'global policy' and \
                    all_predefine_url_action == 'global':
                raise ValueError, ('Predefined URL for Global Policy does '
                                   'not have select all global settings')
            self._set_select_all_predefine(name, all_predefine_url_action)
        if all_custom_url_action:
            if not custom_cats:
                raise ValueError, ('There is no custom URL categories '
                                   'configured')
            if name.lower() == 'global policy' and \
                    all_custom_url_action == 'global':
                raise ValueError, ('Customed URL for Global Policy does '
                                   'not have select all global settings')
            self._set_select_all_custom(name, custom_cats,
                                        all_custom_url_action)
        if uncategorized_action:
            self._select_uncategorized_urls_action(uncategorized_action)
        self._click_submit_button()

    def _get_wtt_row_index(self, policyname):
        table_rows = int(self.get_matching_xpath_count(WTT_TABLE_ROW))
        for index in xrange(2, table_rows + 1):
            name = self.get_text(WTTPOLICY_CELL_TEXT(index))
            if name == policyname:
                return index
            else:
                return None

    def _click_delete_wttpolicy_link(self, policyname):
        row_index = self._get_wtt_row_index(policyname)
        if row_index is None:
            raise ValueError('"%s" policy does not exist' % (policyname,))

        self.click_element(DELETE_POLICY(row_index), "don't wait")
        self._click_continue_button()

    def delete_web_traffic_policies(self, name, cm='', description=None):
        self._navigate_to('Web', cm, 'Web Traffic Tap Policies')

        self._click_delete_wttpolicy_link(policyname)

    def wtt_policies_get_list(self, cm=''):
        """
        Returns: dictionary of access policies. Keys are names of policies.
        Each policy is a dictionary with following keys:
        - `order`
        - `identity`
        - `protocols_and_user_agents`
        - `url_filtering`
        - `applications`
        - `objects`
        - `anti_malware_and_reputation`

        Examples:
        """
        self._navigate_to('Web', cm, 'Web Traffic Tap Policies')
        return self._get_policies()
