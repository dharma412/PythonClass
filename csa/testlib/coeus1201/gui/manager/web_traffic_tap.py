#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/gui/manager/web_traffic_tap.py#2 $
# $DateTime: 2020/03/12 22:59:36 $
# $Author: kathirup $

import common.gui.guiexceptions as guiexceptions
from common.gui.guicommon import GuiCommon
from policybase import PolicyBase
import re

SUBMIT = "xpath=//input[@class='submit']"
UNCATEGORIZED_SUBMIT= "xpath=//input[@value='Submit'][2]"
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

    def get_keyword_names(self):
        return [
            'add_web_traffic_policies',
            'set_url_filtering',
            'delete_web_traffic_policies',
            'web_traffic_policies_get_list'
            ]

    def _open_page(self):
        self._navigate_to('Web Security Manager', 'Web Traffic Tap Policies')

    def web_traffic_policies_get_list(self):
        self._open_page()
        return self._get_policies()

    def add_web_traffic_policies(self,
                                 name,
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
        self._open_page()
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

    def set_url_filtering(self):
        self.click_link(URL_FILTERING)
        self._wait_until_element_is_present(TAP_ALL)
        self.click_element(TAP_ALL)
        self.click_element(Uncategorized_URLs_tap)
        try:
            self._click_submit_button(wait=False)
        except:
            self.click_button(UNCATEGORIZED_SUBMIT)

    def delete_web_traffic_policies(self, name, description=None):
         self._open_page()
         self._delete_policy(name, 4)
