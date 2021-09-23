# $Id: //prod/main/sarf_centos/testlib/zeus1350/gui/web/cm118/cm118_decryption_policies.py#1 $
# $DateTime: 2019/09/18 01:46:35 $
# !/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1350/gui/web/cm118/cm118_decryption_policies.py#1 $ $DateTime: 2019/09/18 01:46:35 $ $Author: sarukakk $

from coeus1180.gui.manager.decryption_policies import DecryptionPolicies


class Cm110DecryptionPolicies(DecryptionPolicies):
    """
    Keywords library for WebUI page Web -> Configuration Master 11.8 -> Decryption Policies
    """

    def _open_decr_policy_page(self):
        self._navigate_to('Web', 'Configuration Master 11.8', 'Decryption Policies')

    def get_keyword_names(self):
        return ['cm118_decryption_policies_add',
                'cm118_decryption_policies_delete',
                'cm118_decryption_policies_edit',
                'cm118_decryption_policies_edit_url_categories',
                'cm118_decryption_policies_edit_default_action',
                'cm118_decryption_policies_edit_wbrs',
                'cm118_decryption_policies_get_list',
                ]

    def cm118_decryption_policies_get_list(self):
        """
        Returns: dictionary of decryption_policies from Configuration Master
        Keys are names of policies.
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
        | ${policies}= | CM118 Decryption Policies Get List |
        | ${policies}= | Decryption Policies Get List |
        | Should Be True | len(${policies}) == 2 |
        """
        return self.decryption_policies_get_list()

    def cm118_decryption_policies_add(self,
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
        """Adds new decryption policy from Configuration Master 11.8

        *Parameters*
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

        *Exceptions*
        - `GuiFeatureDisabledError`: if Decryption Policies are currently
          disabled or one of the following is unavailable in 'Advanced' menu :
          1. Proxy Ports\n
          2. URL Categories\n
          3. Time Range\n
        - `ConfigError`: if Decryption group with such name exist.
        - `ValueError`: if identity has wrong format.

        *Examples*
        | CM118 Decryption Policies Add | myDefaultDecrPol |
        | ... | description=This policy uses Global Identity Policy |
        | ... | identities=Global Identity Policy |
        | CM118 Decryption Policies Add | myOtherDecrPol |
        | ... | description=This policy uses custom identity |
        | ... | identities=myID:authenticated |
        | CM118 Decryption Policies Add | myOtherDecrPol |
        | ... | description=This policy uses custom identity |
        | ... | identities=myID:selected:jsmith |
        """
        self.decryption_policies_add(
            name,
            description=description,
            order=order,
            identities=identities,
            proxy_ports=proxy_ports,
            subnets=subnets,
            time_range=time_range,
            match_time_range=match_time_range,
            url_categories=url_categories,
            user_agents=user_agents,
            match_agents=match_agents)

    def cm118_decryption_policies_delete(self, name):
        """Deletes specified decryption policy from Configuration Master 11.8

        *Parameters*
        - `name`: name of decryption policy to be deleted.

        *Exceptions*
        - `GuiFeatureDisabledError`: if Decryption Policies are currently
          disabled.
        - `GuiControlNotFoundError`: no policy with such name.

        *Example*
        | CM118 Decryption Policies Delete | myDecrPol |
        """
        self.decryption_policies_delete(name)

    def cm118_decryption_policies_edit(self,
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
        """Edits decryption policy from Configuration Master 11.8

        *Parameters*
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

        *Exceptions*
        - `GuiFeatureDisabledError`: if Decryption Policies are currently
          disabled or one of the following is unavailable in 'Advanced' menu :
          1. Proxy Ports\n
          2. URL Categories\n
          3. Time Range\n
        - `ValueError`: if identity has wrong format.
        - `GuiControlNotFoundError`: no policy with such name.

        *Examples*
        | CM118 Decryption Policies Edit | myDecrPol |
        | ... | identities=All Identities:selected:joe.smith |
        | CM118 Decryption Policies Edit | myDecrPol |
        | ... | identities=All Identities:all | time_range=myTime |
        | ... | proxy_ports=3128 |
        | CM118 Decryption Policies Edit | myDecrPol | identities=All Identities |
        | ... | time_range=myTime | proxy_ports=3128 | url_categories=Weapons,Adult |
        """
        self.decryption_policies_edit(
            name,
            new_name=new_name,
            description=description,
            order=order,
            identities=identities,
            proxy_ports=proxy_ports,
            subnets=subnets,
            time_range=time_range,
            match_time_range=match_time_range,
            url_categories=url_categories,
            user_agents=user_agents,
            match_agents=match_agents)

    def cm118_decryption_policies_edit_url_categories(self,
                                                      name,
                                                      url_categories=None,
                                                      uncategorized_action=None,
                                                      all_predefine_url_action=None,
                                                      all_custom_url_action=None):
        """Edits URL categories for specified decryption policy
        from Configuration Master 11.8

        *Parameters*
        - `name`: name of decryption policy to edit.
        - `url_categories`: String of comma-separated pairs
        <url_category>:<action>
        Url categories are described here:
        http://eng.ironport.com/docs/qa/sarf/keyword/common/webcats.rst
        Actions for predefined url categories:
        'global', 'pass', 'monitor', 'decrypt', 'block', 'timebased'.
        Actions for custom url categories:
        'pass', 'monitor', 'decrypt', 'drop', 'timebased'.
        If 'timebased' action is selected next values are time range,
        time based action and other time based action.
        - `uncategorized_action`: specified action for uncategorized
        URLs: 'global', 'pass', 'monitor', 'decrypt', 'drop'. Defaulted to
        'global'.
        - `all_predefine_url_action`: set the same action to all predefined URL
        categories. The possible values are 'global', 'pass', 'monitor',
        'decrypt', 'drop', 'timebased'.
        - `all_custom_url_action`: set the same action to all customed URL
        categories. The possible values are 'pass', 'monitor', 'decrypt',
        'drop', 'timebased'.

       Exceptions:
       - GuiFeatureDisabledError:Decryption Policies are currently disabled
       - GuiControlNotFoundError:<category>
       - ValueError:Time based action does not have select all
       - ValueError:Predefined URL for Global Policy does not have select all global settings
       - ValueError:Time based action does not have select all'
       - ValueError:There is no custom URL categories configured
       - ValueError:Customed URL for Global Policy does not have select all global settings

        *Examples*
        | ${id1} | Set Variable | myPolicy |
        | ${url_cats}= | Set Variable |
        | ... | ${webcats.ADULT}:drop, ${CURL2}:timebased:${TR1}:monitor:drop |
        | CM118 Decryption Policies Edit Url Categories | ${id1} |
        | ... | url_categories=${url_cats} |
        | ... | uncategorized_action=pass |
        | CM118 Decryption Policies Edit Url Categories | ${id1} |
        | ... | all_predefine_url_action=monitor |
        | ... | all_custom_url_action=pass |
        """
        self.decryption_policies_edit_url_categories(
            name,
            url_categories=url_categories,
            uncategorized_action=uncategorized_action,
            all_predefine_url_action=all_predefine_url_action,
            all_custom_url_action=all_custom_url_action)

    def cm118_decryption_policies_edit_wbrs(self,
                                            name,
                                            score_range=None,
                                            no_score_action=None,
                                            setting_type='custom'):
        """Edits Web Reputation settings for decryption policy
        from Configuration Master 11.8

        *Parameters*
        - `name`: name of decryption policy group to edit.
        - `score_range`: the threshold between drop and decrypt
        actions; decrypt and pass through actions. String of 2 values, separated
        by colon.
        - `no_score_action`: specify an action for sites that do not have
        Web Reputation Score. Either 'monitor', 'pass', 'decrypt', or 'drop'.
        - `setting_type`: set type for WBRS; either 'custom', 'global' or
        'disable'. Option 'global' can't be selected for 'Global Policy'.

        *Exceptions*
        - `GuiFeatureDisabledError`: if Decryption Policies are currently
          disabled or Web Reputation Filtering is disabled globall.
        - `GuiControlNotFoundError`: no policy with such name or URL category is
          wrong.

        *Examples*
        | CM118 Decryption Policies Edit Wbrs | myDecrPol | setting_type=disable |
        | CM118 Decryption Policies Edit Wbrs | myDecrPol |
        | ... | score_range=-3:5 | no_score_action=decrypt |
        """
        self.decryption_policies_edit_wbrs(
            name,
            score_range=score_range,
            no_score_action=no_score_action,
            setting_type=setting_type)

    def cm118_decryption_policies_edit_default_action(self, name, action):
        """Edits default action for decryption policy
        from Configuration Master 11.8

        *Parameters*
        - `name`: name of decryption policy to edit.
        - `action`: default action for decryption policy. Possible values are
        'global', 'decrypt', 'pass', 'drop'.

        *Exceptions*
        - `GuiFeatureDisabledError`: if Decryption Policies are currently
          disabled or one of the following is unavailable in 'Advanced' menu :
          1. Proxy Ports\n
          2. URL Categories\n
          3. Time Range\n
        - `ValueError`: if identity has wrong format.
        - `GuiControlNotFoundError`: no policy with such name.

        Example:
        | CM118 Decryption Policies Edit Default Action | myDecrPol | action=decrypt |
        """
        self.decryption_policies_edit_default_action(name, action)
