#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/gui/manager/decryption_policies.py#2 $
# $DateTime: 2019/12/11 00:21:44 $
# $Author: psreeram $
import common.gui.guiexceptions as guiexceptions
from common.gui.guicommon import GuiCommon
from policybase import PolicyBase
webcat_time_actions = [
    'global',
    'pass',
    'monitor',
    'decrypt',
    'drop',
    ]
webcat_actions = [
    'global',
    'pass',
    'monitor',
    'decrypt',
    'drop',
    'quotabased',
    'timebased',
    ]
custcat_time_actions = webcat_time_actions
custcat_actions = webcat_actions
global_policy_actions = webcat_actions[1:]

class DecryptionPolicies(GuiCommon, PolicyBase):
    """GUI configurator for 'Web Security Manager -> Decryption Policies' page.
    """

    policy_name_column = 2
    url_categories_column = 3
    wbrs_column = 4
    default_action_column = 5
    delete_column = 6
    # method required by RF
    # return a list with all public methods

    def get_keyword_names(self):
        return ['decryption_policies_add',
                'decryption_policies_delete',
                'decryption_policies_edit',
                'decryption_policies_edit_url_categories',
                'decryption_policies_edit_default_action',
                'decryption_policies_edit_wbrs',
                'decryption_policies_get_list',
                ]

    def decryption_policies_get_list(self):
        """
        Returns: dictionary of decryption policies. Keys are names of policies.
        Each policy is a dictionary with following keys:
        - `order`
        - `identity`
        - `proxy_ports`
        - `subnets`
        - `time_range`
        - `url_categories`
        - `user_agents`
        - `user_location`
        - `url_filtering`
        - `web_reputation`
        - `default_action`
        Examples:
        | ${policies}= | Decryption Policies Get List |
        | Should Be True | len(${policies}) == 2 |
        | Should Be True | ${policies}['policy']['subnets'] == '10.1.1.1, 20.2.2.2' |
        """

        self._open_decr_policy_page()
        return self._get_policies()

    def _open_decr_policy_page(self):
        locator = 'xpath=//div[@class="text-info"]'
        self._navigate_to('Web Security Manager', 'Decryption Policies')
        if self._is_element_present(locator):
            txt = self.get_text(locator)
            if 'Decryption Policies are currently disabled' in txt:
                raise guiexceptions.GuiFeatureDisabledError(txt)

    def decryption_policies_add(self,
                                name,
                                description=None,
                                order=None,
                                identities=None,
                                proxy_ports=None,
                                subnets=None,
                                time_range=None,
                                match_time_range=True,
                                url_categories=None,
                                user_agents=None,
                                match_agents=True):
        """Adds new decryption policy.
        Parameters:
        - `name`: name of decryption policy.
        - `description`: description for decryption policy.
        - `order`: order of decryption policy.
        - `identities`: a string of comma separated values of identity groups to
        apply to this policy, where each identity is presented in the following
        format (see identities specification document.)
        - `proxy_ports`: membership is defined by proxy ports. String of comma
        separated values of proxy ports.
        - `subnets`: string of comma separated values of one or more subnet
        where policy is a member.
        - `time_range`: time range where policy is a member.
        - `match_time_range`: specify whether a policy group should apply to the
                              times inside or outside the selected time range.
                              Defaulted to True. Otherwise False.
        - `url_categories`: string of comma separated values of URL categories
        in which policy is a member.
        - `user_agents`: user agents where policy is a member. A comma separated
                         values of custom user agents.
        - `match_agents`: specify whether to match the selected user agents.
                          Defaulted to True. Otherwise False - match all except
                          the selected user agents.
        Examples:
        | Decryption Policies Add | myDefaultDecrPol | description=This policy uses Global Identification Profile | identities=Global Identification Profile |
        | Decryption Policies Add | myOtherDecrPol | description=This policy uses custom identity | identities=myID:authenticated |
        | Decryption Policies Add | myOtherDecrPol | description=This policy uses custom identity | identities=myID:selected:jsmith |
        """

        self._open_decr_policy_page()
        if self._is_element_present('xpath=//table[@class="cols"]/tbody'
                             '/tr/td/a[substring-after(@href, "%s")="%s"]' % \
                             (name, name)):
            raise guiexceptions.ConfigError('Decryption group with the '
                                            'name %s already exists.' % name)
        self._click_add_policy_button()
        self._fill_policy_page(name, description, order)
        if identities:
            self._edit_identity_membership(identities)
        self._edit_advanced_settings(proxy_ports=proxy_ports,
                                     subnets=subnets,
                                     time_range=time_range,
                                     match_range=match_time_range,
                                     url_categories=url_categories,
                                     user_agents=user_agents,
                                     match_agents=match_agents)
        self._click_submit_button()

    def decryption_policies_delete(self, name):
        """Deletes specified decryption policy.
        Parameters:
        - `name`: name of decryption policy to be deleted.
        Example:
        | Decryption Policies Delete | myDecrPol |
        """
        self._open_decr_policy_page()
        self._delete_policy(name, self.delete_column)

    def decryption_policies_edit(self,
                                 name,
                                 new_name=None,
                                 description=None,
                                 order=None,
                                 identities=None,
                                 proxy_ports=None,
                                 subnets=None,
                                 time_range=None,
                                 match_time_range=True,
                                 url_categories=None,
                                 user_agents=None,
                                 match_agents=True):
        """Edits decryption policy.
        Parameters:
        - `name`: name of decryption policy group to edit.
        - `new_name`: new name for decryption policy.
        - `description`: description for decryption policy.
        - `order`: order of decryption policy.
        - `identities`: string of comma separated values of identity groups to
        apply to this policy, where each identity is presented in the following
        format (see identities specification document.)
        - `proxy_ports`: membership is defined by proxy ports. string of comma
        separated values of proxy ports.
        - `subnets`: string of comma separated values of one or more subnet
        where policy is a member.
        - `time_range`: time range where policy is a member.
        - `match_time_range`: specify whether a policy group should apply to the
                              times inside or outside the selected time range.
                              Defaulted to True. Otherwise False.
        - `url_categories`: string of comma separated values of URL categories
        in which policy is a member.
        - `user_agents`: user agents where policy is a member. A comma separated
                         values of custom user agents.
        - `match_agents`: specify whether to match the selected user agents.
                          Defaulted to True. Otherwise False - match all except
                          the selected user agents.
        Examples:
        | Decryption Policies Edit | myDecrPol | identities=All Identities:selected:joe.smith |
        | Decryption Policies Edit | myDecrPol | identities=All Identities:all | time_range=myTime | proxy_ports=3128 |
        | Decryption Policies Edit | myDecrPol | identities=All Identities | time_range=myTime | proxy_ports=3128 | url_categories=Weapons,Adult |
        """

        self._open_decr_policy_page()
        self._click_edit_policy_link(name, self.policy_name_column)
        if any((new_name, description, order)):
            self._fill_policy_page(new_name, description, order)
        if identities:
            self._edit_identity_membership(identities)
        self._edit_advanced_settings(proxy_ports=proxy_ports,
                                     subnets=subnets,
                                     time_range=time_range,
                                     match_range=match_time_range,
                                     url_categories=url_categories,
                                     user_agents=user_agents,
                                     match_agents=match_agents)
        self._click_submit_button(wait=False)

    def decryption_policies_edit_url_categories(self,
                                                name,
                                                url_categories=None,
                                                uncategorized_action=None,
                                                all_predefine_url_action=None,
                                                all_custom_url_action=None,
						enable_overall_quota=None,
                                                overall_quota=None):
        """Edits URL categories for specified decryption policy.
        Parameters:
        - `name`: name of decryption policy to edit.
        - `url_categories`: String of comma-separated pairs
        <url_category>:<action>
        Url categories are described here:
        http://eng.ironport.com/docs/qa/sarf/keyword/common/webcats.rst
        Actions for predefined url categories:
        'global', 'pass', 'monitor', 'decrypt', 'drop', 'timebased', 'quotabased'.
        Actions for custom url categories:
        'pass', 'monitor', 'decrypt', 'drop', 'timebased', 'quotabased'.
        If 'timebased' action is selected next values are time range,
        time based action and other time based action.
        - `uncategorized_action`: specified action for uncategorized
        URLs: 'global', 'pass', 'monitor', 'decrypt', 'drop'. Defaulted to
        'global'.
        - `all_predefine_url_action`: set the same action to all predefined URL
        categories. The possible values are 'global', 'pass', 'monitor',
        'decrypt', 'drop', 'timebased', 'quotabased'.
        - `all_custom_url_action`: set the same action to all customed URL
        categories. The possible values are 'pass', 'monitor', 'decrypt',
        'drop', 'timebased', 'quotabased'.
        -  `enable_overall_quota`:'True' To enable Time quota Notification
            'False' To disable time quota and 'None' To use current or default value
        -  `overall_quota=None`:quota profile name to be used
        Examples:
        | ${id1} | Set Variable | myPolicy |
        | ${url_cats}= | Set Variable |
        | ... | ${webcats.ADULT}:drop, ${CURL2}:timebased:${TR1}:monitor:drop |
        | ${url_cats}= | Set Variable |
        | ... | ${webcats.ADULT}:drop, ${CURL2}:quotabased:${QB1} |
        | Decryption Policies Edit Url Categories | ${id1} |
        | ... | url_categories=${url_cats} |
        | ... | uncategorized_action=pass |
        | ... | enable_overall_quota=${True} |
        | ... | overall_quota=${QB2} |
        | Decryption Policies Edit Url Categories | ${id1} |
        | ... | all_predefine_url_action=monitor |
        | ... | all_custom_url_action=pass |
        """

        self._open_decr_policy_page()
        self._click_edit_policy_link(name, self.url_categories_column)
        custom_cats = self._get_custom_url_categories()
        predefined_cats = self._get_predefined_url_categories()
        url_categories = self._convert_to_tuple(url_categories)
        if url_categories is not None:
            for item in url_categories:
                item = self._convert_to_tuple_from_colon_separated_string(item)
                cat = item[0]
                action = item[1].lower()
                if action.strip().lower() == 'timebased':
                    cat, action, timerange, tb_action, tb_otherwise = item
                    redirect_link = None
                    quota= None
                elif action.lower() == 'quotabased':
                    cat, action, quota = item
                    timerange = None
                    tb_action = None
                    tb_otherwise = None
                    redirect_link = None
                else:
                    cat, action = item
                    timerange = None
                    tb_action = None
                    tb_otherwise = None
                    redirect_link = None
                    quota= None
                if cat in custom_cats:
                    self._edit_url_category(action, custom_cats[cat], timerange,
                                        tb_action, tb_otherwise, redirect_link, quota)
                elif cat in predefined_cats:
                    self._edit_url_category(action, predefined_cats[cat], timerange,
                                        tb_action, tb_otherwise, redirect_link, quota)
                else:
                    raise guiexceptions.GuiControlNotFoundError(
                                       cat, self.get_location())
        if all_predefine_url_action:
            auc_disabled_text = \
                'Acceptable Use Controls feature is currently disabled'
            if self._is_text_present(auc_disabled_text):
                raise guiexceptions.GuiFeatureDisabledError(auc_disabled_text)
            if all_predefine_url_action == 'timebased':
                raise ValueError, ('Time based action does not have select '
                                   'all')
            if name.lower() == 'global policy' and \
                all_predefine_url_action == 'global':
                    raise ValueError, ('Predefined URL for Global Policy does '
                        'not have select all global settings')
            self._set_select_all_predefine(name, all_predefine_url_action)
        if all_custom_url_action:
            if all_custom_url_action == 'timebased':
                raise ValueError, ('Time based action does not have select '
                                   'all')
            if not custom_cats:
                raise ValueError, ('There is no custom URL categories '
                                   'configured')
            if name.lower() == 'global policy' and \
                all_custom_url_action == 'global':
                    raise ValueError, ('Customed URL for Global Policy does '
                        'not have select all global settings')
            self._set_select_all_custom(name, custom_cats,
                                        all_custom_url_action)
        if enable_overall_quota is None:
            self._info("Overall quota not applied")
        elif enable_overall_quota:
            self.select_from_list('prequota_profile', overall_quota)
            self._info("Overall quota applied")
        else:
            self.select_from_list('prequota_profile', 'Select Time and Volume Quota ...')
        if uncategorized_action:
            self._select_uncategorized_urls_action(uncategorized_action)
        self._click_submit_button()

    def decryption_policies_edit_wbrs(self,
                                      name,
                                      score_range=None,
                                      no_score_action=None,
                                      setting_type='custom'):
        """Edits Web Reputation settings for decryption policy.
        Parameters:
        - `name`: name of decryption policy group to edit.
        - `score_range`: the threshold between drop and decrypt
        actions; decrypt and pass through actions. String of 2 values, separated
        by colon.
        - `no_score_action`: specify an action for sites that do not have
        Web Reputation Score. Either 'monitor', 'pass', 'decrypt', or 'drop'.
        - `setting_type`: set type for WBRS; either 'custom', 'global' or
        'disable'. Option 'global' can't be selected for 'Global Policy'.
        Examples:
        | Decryption Policies Edit Wbrs | myDecrPol | setting_type=disable |
        | Decryption Policies Edit Wbrs | myDecrPol | score_range=-3:5 | no_score_action=decrypt |
        """

        self._open_decr_policy_page()
        # SeleniumClientException refers to the link being absent
        # Which mostly mean that feature is disabled globally
        try:
            self._click_edit_policy_link(name, self.wbrs_column)
        except guiexceptions.GuiControlNotFoundError:
            raise guiexceptions.GuiFeatureDisabledError(
                    'Web Reputation Filtering is disabled globally')
        # However for Global Identification Profile link is available but opened page
        # displays a message "Web Reputation Filtering is currently disabled
        # globally"
        if self._is_text_present('is not currently enabled.'):
            raise guiexceptions.GuiFeatureDisabledError(
                    'Web Reputation Filtering is disabled globally')
        if self._is_text_present('Decryption Policies: Reputation Settings:'):
            self._select_wbrs_settings(setting_type)
        else:
            raise guiexceptions.GuiFeatureDisabledError(
                'Web Reputation is Not Available cannot change the state')
        if setting_type == 'custom':
            if score_range:
                self._set_wbrs_score_range(
                self._convert_to_tuple_from_colon_separated_string(score_range))
            if no_score_action:
                self._select_no_score_action(no_score_action)
        self._click_submit_button()

    def decryption_policies_edit_default_action(self, name, action):
        """Edits default action for decryption policy.
        Parameters:
        - `name`: name of decryption policy to edit.
        - `action`: default action for decryption policy. Possible values are
        'global', 'decrypt', 'pass', 'drop'.
        Example:
        | Decryption Policies Edit Default Action | myDecrPol | action=decrypt |
        """
        self._open_decr_policy_page()
        self._click_edit_policy_link(name, self.default_action_column)
        self._select_default_action(action)
        self._click_submit_button()

    def _select_wbrs_settings(self, option):
        wbrs_settings = {
            'global': 'Use Global Web Reputation Settings',
            'custom': 'Define Custom Web Reputation Settings',
            'disable': 'Disable Web Reputation for this Policy'
        }
        settings_id = 'id=settings_type'
        settings_option = wbrs_settings.get(option.lower().strip())
        if settings_option is None:
            raise ValueError, 'Invalid WBRS settings - %s' % (option,)
        self.select_from_list(settings_id, settings_option)

    def _set_wbrs_score_range(self, score_range):
        block_id = 'custom_block_boundary'
        allow_id = 'custom_allow_boundary'
        for value, score_type in zip(score_range,
                                     (block_id, allow_id)):
            self._set_input_value_with_javascript(score_type, value)

    def _select_no_score_action(self, no_score_action):
        actions_list = 'name=wbrs_no_score_action'
        no_score_action_map = lambda action: \
            {'decrypt': 'decrypt',
             'monitor': 'scan',
             'pass': 'pass',
             'drop': 'drop'}[action.lower().strip()]
        if no_score_action not in webcat_time_actions:
            raise ValueError, 'Invalid no score action - "%s"' % \
                                                (no_score_action,)
        self.select_from_list(actions_list,
            no_score_action_map(no_score_action))

    def _select_default_action(self, action):
        valid_actions = {'global': 'id=default_action_global',
                         'decrypt': 'id=default_action_decrypt',
                         'pass': 'id=default_action_pass',
                         'drop': 'id=default_action_drop'}
        action_id = valid_actions.get(action.lower().strip())
        if action_id is None:
            raise ValueError, 'Invalid "%s" default action' % (action,)
        self._click_radio_button(action_id)

    def _set_select_all_predefine(self, name, action):
        if name.lower().strip() == 'global policy':
            SELECT_ALL_LINK = lambda index: "xpath=//table[@id='predefinedHeaderGrid']" \
                                                        "/tbody/tr[3]/th[%s]/nobr/a/span" % index
            self.click_element(
                    SELECT_ALL_LINK(global_policy_actions.index(action) + 1),"don't wait")
        else:
            SELECT_ALL_LINK = lambda index: "xpath=//table[@id='predefinedHeaderGrid']" \
                                                        "/tbody/tr[4]/th[%s]/nobr/a/span" % index
            self.click_element(
                            SELECT_ALL_LINK(webcat_actions.index(action) + 1), "don't wait")

    def _set_select_all_custom(self, name, custom_cats, action):
        custom_cats_error = ("Can't set global settings since all custom URL "
                             "is still excluded from Global Policy")
        GLOBAL_SETTING_SELECTION = ("img_global_customRadio_customActions"
		                                                      "[0][action]")
        SELECT_ALL_LINK = lambda index: "xpath=//tr[@id='custom_select_all_head" \
		                                          "ers']/th[%s]/nobr/a/span" % index
        action_list = custcat_actions
        if name.lower().strip() == 'global policy':
            action_list = global_policy_actions
        if self._is_visible(SELECT_ALL_LINK(1)):
            custom_cat_in_global_policy = False
            try:
                custom_cat_in_global_policy = self._is_visible(
				                       GLOBAL_SETTING_SELECTION)
            except Exception:
                pass
            if not custom_cat_in_global_policy and \
                action.lower().strip() == 'global':
                raise ValueError, (custom_cats_error)
            self.click_element(
			     SELECT_ALL_LINK(action_list.index(action) + 1), "don't wait")
        else:
            # If custom URL categories are not in Global Policy, won't be able
            # configure global settings for 'Select All'.  Throw error to
            # notify user.
            if name.lower() != 'global policy' and \
                action.lower().strip() == 'global':
                raise ValueError, (custom_cats_error)
            for cat in custom_cats:
                self._edit_url_category(action, custom_cats[cat],
				                action_list, custcat_time_actions)

    def _select_uncategorized_urls_action(self, uncategorized_action):
        actions_list = 'id=uncategorized_action'
        if uncategorized_action not in webcat_time_actions:
            raise ValueError, 'Unknown uncategorized URLs action - "%s"' % \
                               (uncategorized_action,)
        self._select_action_combo(actions_list, uncategorized_action)
