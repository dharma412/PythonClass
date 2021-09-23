#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/gui/manager/oms_policies.py#1 $
# $DateTime: 2019/08/14 09:58:47 $
# $Author: uvelayut $

import common.gui.guiexceptions as guiexceptions
from common.gui.guicommon import GuiCommon
from policybase import PolicyBase

EDIT_CUST_URL_LINK = 'edit_custom_categories_list'
SETTINGS_TYPE_LOC = 'id=settings_type'
WEBROOT_CHECKBOX = 'enable_webroot'
ADAPTIVE_SCANNING = 'enable_adaptivescanning'
AV_CHECKBOX = 'select_engine'
AV_SELECT = 'av_engine'
MALWARE_SEL = lambda index: \
 'xpath=//tbody[@id=\'malware_custom_header\']/tr[2]/th[%d]/nobr/a/span' % \
 (index,)
OTHER_CAT_SEL = lambda index: \
 'xpath=//table[@id="malware_custom"]/tbody[not(@id)]/tr/th[%d]//span[@class="select_all_link"]' \
 % (index)

class OMS_Policies(PolicyBase, GuiCommon):
    """Keywords for Web Security Manager -> Outbound Malware Scanning
    """

    policy_name_column = 2
    destination_column = 3
    delete_column = 5
    amw_filtering_column = 4

    def get_keyword_names(self):
        return [
                'oms_policies_add',
                'oms_policies_delete',
                'oms_policies_edit',
                'oms_policies_edit_destinations',
                'oms_policies_edit_amw_filters',
                'oms_policies_get_list',
                ]

    def oms_policies_get_list(self):
        """
        Returns: dictionary of oms policies. Keys are names of policies.
        Each policy is a dictionary with following keys:
        - `order`
        - `identity`
        - `proxy_ports`
        - `subnets`
        - `url_categories`
        - `protocols`
        - `user_agents`
        - `destinations`
        - `anti-malware_filtering`

        Examples:

        | ${policies}= | Oms Policies Get List |
        | Should Be True | len(${policies}) == 2 |
        | Should Be True | ${policies}['policy']['applications'] == '(global policy)' |
        """

        self._open_page()
        return self._get_policies()

    def _open_page(self):
        self._navigate_to \
         ('Web Security Manager', 'Outbound Malware Scanning')

    def oms_policies_add(self,
            name,
            description=None,
            order=None,
            identities=None,
            protocols=None,
            proxy_ports=None,
            subnets=None,
            url_categories=None,
            user_agents=None,
            common_user_agents=None,
            match_agents=None):
        """Add new policy.

         Parameters:
        - `name`: name for the policy group to add. String.
        - `description`: description for the policy. String.
        - `order`: the processing order. Integer or string.
        - `identities`: String of comma separated values of identities. Format
           of an identity is described <a href="Library.html#identities">here</a>
        - `protocols`: the protocols where policy is a member. String of comma
           separated values. The following values are currently accepted:
           * http
           * ftpoverhttp
           * nativeftp
           * others
           * https
        - `proxy_ports`: The ports where policy is a member. String of comma
           separated values
        - `subnets`: the nets where policy is member. String of comma separated
           values in format of IP, IP range or CIDR.
        - `url_categories`: the URL categories where policy is a member.
           String of comma separated values. The categories are described here:
           http://eng.ironport.com/docs/qa/sarf/keyword/common/webcats.rst
        - `user_agents`: the user agents where policy is a member.
           String of comma separated values
        - `common_user_agents`: String of comma separated values of
           common user agents: 'ie8', 'ie7', 'ie6', 'pre-ie5', 'ie-all', 'ff3',
           'ff2', 'ff1', 'ff-all', 'ms-update', 'acro-update'
        - `match_agents`: match selected user agents. Boolean. Default to True.

        Example:
        | OMS Policies Add | three |
        | | description=Adding policy  |
        | | identities=Global Identification Profile |
        | | protocols=http, ftpoverhttp |
        | | proxy_ports=1234, 5321 |
        | | subnets=10.1.1.0/24, 1.2.3.44 |
        | | url_categories=${webcats.ADULT}, ${webcats.ARTS} |
        | | user_agents=ie-all |
        """
        self._open_page()
        self._click_add_policy_button()
        self._fill_policy_page(name, description, order)
        if identities is not None:
            self._edit_identity_membership(identities)
        self._edit_advanced_settings(
            protocols=protocols,
            proxy_ports=proxy_ports,
            subnets=subnets,
            url_categories=url_categories,
            user_agents=user_agents,
            common_user_agents=common_user_agents,
            match_agents=match_agents)
        self._click_submit_button()

    def oms_policies_edit(self,
            name,
            description=None,
            order=None,
            identities=None,
            protocols=None,
            proxy_ports=None,
            subnets=None,
            url_categories=None,
            user_agents=None,
            common_user_agents=None,
            match_agents=None):
        """Edits specified policy.

         Parameters:
        - `name`: name for the policy group to add. String.
        - `description`: description for the policy. String.
        - `order`: the processing order. Integer or string.
        - `identities`: String of comma separated values of identities. Format
           of an identity is described <a href="Library.html#identities">here</a>
        - `protocols`: the protocols where policy is a member. String of comma
           separated values. The following values are currently accepted:
           * http
           * ftpoverhttp
           * nativeftp
           * others
           * https
        - `proxy_ports`: The ports where policy is a member. String of comma
           separated values
        - `subnets`: the nets where policy is member. String of comma separated
           values in format of IP, IP range or CIDR.
        - `url_categories`: the URL categories where policy is a member.
           String of comma separated values. The categories are described here:
           http://eng.ironport.com/docs/qa/sarf/keyword/common/webcats.rst
        - `user_agents`: the user agents where policy is a member.
           String of comma separated values
        - `common_user_agents`: String of comma separated values of
           common user agents: 'ie8', 'ie7', 'ie6', 'pre-ie5', 'ie-all', 'ff3',
           'ff2', 'ff1', 'ff-all', 'ms-update', 'acro-update'
        - `match_agents`: match selected user agents. Boolean. Default to True.

        Example:
        | OMS Policies Edit | three |
        | | description=Editing policy |
        | | order=None |
        | | identities=Global Identification Profile |
        | | protocols=http, ftpoverhttp |
        | | proxy_ports=12345, 54321 |
        | | subnets=10.1.1.0/24 |
        | | url_categories=${webcats.ADULT} |
        | | user_agents=ie-all, ff3 |
        """
        if name == 'Global Policy':
            raise ValueError, '"%s" cannot be edited' % (name)

        self._open_page()
        self._click_edit_policy_link(name, self.policy_name_column)
        self._fill_policy_page(None, description, order)

        if identities is not None:
            self._edit_identity_membership(identities)
        self._edit_advanced_settings(
            protocols=protocols,
            proxy_ports=proxy_ports,
            subnets=subnets,
            url_categories=url_categories,
            user_agents=user_agents,
            common_user_agents=common_user_agents,
            match_agents=match_agents)

        self._click_submit_button()

    def oms_policies_edit_amw_filters(self,
                         name,
                         settings_type,
                         amw_actions=None,
                         amw_select_all=None,
                         webroot=None,
                         av=None,
                         enable_scanning=None):

        """ Edits anti-malware filtering settings for specified policy.

        Parameters:
        - `name`: name of policy to be edited.
        - `settings_type`: settings to use.  Either 'global' or 'custom'.
        - `amw_actions`: actions to be taken for malware.
           String of comma-separated pairs <malware_category>:<action>
           * malware_category; the categories are described here:
             http://eng.ironport.com/docs/qa/sarf/keyword/common/mwcats.rst
           * action can be 'block' or 'monitor'
        - `amw_select_all`: set all AMW categories to either 'monitor' or
          'block'. String of comma-separated pairs
          . `Malware`: Malware Categories, can be set to 'monitor' or 'block'
          . `Other`: Other Categories, can be set to 'monitor' or 'block'
        - `webroot`: specify whether to enable Webroot. ${True} or ${False}
           That parameter can be used only when adaptive scanning is enabled
        - `av`: specify whether to enable anti-virus.
           String of comma-separated pairs to enable/disable 'McAfee' or 'Sophos'
           i.e. mcafee:enable
           That parameter can be used only when adaptive scanning is enabled
        - `enable_scanning`: Enable Anti-Malware Scanning (Webroot, McAfee, and Sophos)
           Possible values: ${True} or ${False}.
           That parameter can be used only when adaptive scanning is disabled

        Example:
        | OMS Policies Edit AMW Filters | three | global |

        Example:
        | OMS Policies Edit AMW Filters | three | custom |
        | | amw_actions=${mwcats.VIRUS}:block, ${mwcats.DIALER}:block} |
        | | amw_select_all=Malware:monitor, Other: block |
        | | webroot=True |
        | | av=sophos: enable |
        """
        amw_settings = {
         'global': 'Use Anti-Malware Global Policy Settings',
         'custom': 'Define Anti-Malware Custom Settings'
        }
        self._open_page()
        self._click_edit_policy_link(name, self.amw_filtering_column)
        if name != 'Global Policy':
            self._select_settings(amw_settings, settings_type)
        if enable_scanning is not None:
            self._enable_scanning(enable_scanning)
            self._click_submit_button()
            self._open_page()
            self._click_edit_policy_link(name, self.amw_filtering_column)
            self._enable_scanning(enable_scanning)
        if webroot is not None:
            self._manipulate_webroot(webroot)
        if av is not None:
            self._manipulate_av(self._convert_to_dictionary(av))
        if amw_select_all is not None:
            self._click_amw_select_all(\
                self._convert_to_dictionary(amw_select_all))
        if amw_actions is not None:
            self._edit_amw_categories_settings(\
                self._convert_to_dictionary(amw_actions))

        self._click_submit_button()

    def oms_policies_edit_destinations(self,
                          name,
                          settings_type,
                          dest_to_scan=None,
                          cust_url=None,
                          cust_url_all=None):
        """Edits destinations settings for specified policy.

        Parameters:
        - `name`: name of policy to be edited.
        - `settings_type`: settings to use.  Either 'global' or 'custom'.
        - `dest_to_scan`: destinations to scan.  Either 'no', 'all', or 'url'.
        - `cust_url`: string of comma-separated custom URL categories to scan.
        - `cust_url_all`: True to select all defined custom URL categories to
           scan.

        Example:
        | OMS Policies Edit Destinations | three | global |
        | | dest_to_scan=url |
        | | cust_url_all=True |
        | OMS Policies Edit Destinations | three | global |
        | | dest_to_scan=url |
        | | cust_url=cat1 |
        """
        dest_settings = {
         'global': 'Use Destinations scanning Global Policy Settings',
         'custom': 'Define Destinations scanning Custom Settings'
        }
        self._open_page()
        self._click_edit_policy_link(name, self.destination_column)
        if name != 'Global Policy':
            self._select_settings(dest_settings, settings_type)
        if settings_type.lower() == 'custom':
            if dest_to_scan is not None:
                self._set_dest_to_scan(dest_to_scan)
            if cust_url or cust_url_all:
                if not dest_to_scan == 'url':
                    raise ValueError('First set dest_to_scan - \'url\' to '\
                                             'select custom URL categories')
                self.click_element(EDIT_CUST_URL_LINK)
                self._edit_cust_url(cust_url, cust_url_all)
                self._click_done_button()
        self._click_submit_button()

    def oms_policies_delete(self, name):
        """Deletes specified policy
        NOTE: Default policy can not be deleted

        Parameters:
        - `name`: name of the policy to delete.

        Example:
        | OMS Policies Delete | three |
        """
        if name == 'Global Policy':
            raise ValueError, '"%s" cannot be deleted' % (name)
        self._open_page()
        self._delete_policy(name, self.delete_column)

    def _click_add_policy_button(self):
        add_policy_button = "xpath=//input[@value='Add Policy...']"
        self.click_button(add_policy_button)

    def _select_settings(self, set_for, settings):
        settings = settings.lower()
        if not set_for.has_key(settings):
            raise ValueError, 'Invalid "%s" setting type' % (settings)
        self.select_from_list(SETTINGS_TYPE_LOC, set_for[settings])

    def _set_dest_to_scan(self, dest_to_scan):

        dest_scan_radio_button = {
                'no': 'scan_enabled_none',
                'all': 'scan_enabled_all',
                'url': 'scan_enabled_specified'}
        dest_to_scan = dest_to_scan.lower()
        if not dest_scan_radio_button.has_key(dest_to_scan):
            raise ValueError, 'Invalid input for Destinations to Scan: "%s"'\
                                                             % (dest_to_scan)
        self._click_radio_button(dest_scan_radio_button[dest_to_scan])

    def _get_custom_url_cat(self):

        customcat_element = "//input[@name='destinations[]']"
        custom_categories = {}
        starting_row = 3

        if self._is_element_present(customcat_element):
            # Getting the number of custom categories
            customcatsnum = int(self.get_matching_xpath_count(customcat_element))
            if customcatsnum > 0:
            # Populating the custom_categoriess dict with
            # {custom category name: link to this custom category on the page}
                for i in xrange(starting_row, starting_row + customcatsnum):
                    category_name = self.get_text('xpath=//tr[%s]' % (i,))
                    custom_categories[category_name] = \
                        'xpath=//tr[%s]/td[2]/div' % (i,)
        return custom_categories

    def _select_cust_url_membership(self, categories):

        custom_categories = self._get_custom_url_cat()
        for category in categories:
            if category in custom_categories:
                self.click_element(custom_categories[category], "don't wait")
            else:
                raise ValueError, \
                    '"%s" URL category is not present' % (category,)
            self._info('Selected "%s" URL category' % (category,))

    def _edit_cust_url(self, cust_url, cust_url_all):

        select_all_link = 'link=Select all'
        if cust_url is not None:
            # clean all first
            self.click_element(select_all_link, "don't wait")
            self.click_element(select_all_link, "don't wait")
            # Now select the specified
            self._select_cust_url_membership(self._convert_to_list(cust_url))
        # no need to pass cust_url_all='False'
        if cust_url_all is not None:
            self.click_element(select_all_link, "don't wait")

    def _manipulate_webroot(self, webroot):

        if webroot:
            self.select_checkbox(WEBROOT_CHECKBOX)
        else:
            self.unselect_checkbox(WEBROOT_CHECKBOX)

    def _enable_scanning(self, enable_scanning):

        if enable_scanning:
            self.select_checkbox(ADAPTIVE_SCANNING)
        else:
            self.unselect_checkbox(ADAPTIVE_SCANNING)

    def _manipulate_av(self, av):

        av_engine_keys = {
            'mcafee': 'label=McAfee',
            'sophos': 'label=Sophos'}
        if len(av) != 1:
            raise ValueError('McAfee and Sophos cannot be enabled '\
                 'at the same time. \'av\' should be of length 1')
        if av.keys()[0].lower() not in av_engine_keys.keys():
            raise ValueError\
                  ('Invalid Key \'%s\' to enable/disable AV engine. '\
                   'Here are the valid keys '\
                   '%s' % (av.keys()[0], av_engine_keys.keys()))
        if 'disable' in av.values()[0].lower():
            if self._is_checked(AV_CHECKBOX):
                self.click_element(AV_CHECKBOX, "dont_wait")
        else: # assuming value 'enabled'
            if not self._is_checked(AV_CHECKBOX):
                self.click_element(AV_CHECKBOX, "dont_wait")
            self.select_from_list(AV_SELECT,
                                   av_engine_keys[av.keys()[0].lower()])

    def _click_amw_select_all(self, amw_select_all):

        cat_index = {'malware': (MALWARE_SEL(1), MALWARE_SEL(2),),
                     'other': (OTHER_CAT_SEL(1), OTHER_CAT_SEL(2),)}
        action_index = {'monitor': 0, 'block': 1}

        for cat in amw_select_all.keys():
            if not self._is_visible\
                        (cat_index[cat.lower()][action_index['monitor']]):
                raise guiexceptions.GuiFeatureDisabledError\
                ("Link 'Select all' not available for '%s categories'" % cat)

        for cat, action in amw_select_all.iteritems():
            if cat.lower() not in cat_index.keys():
                raise ValueError\
                  ('Invalid category \'%s\' to click select all.'\
                   'Here are the valid categories '\
                   '%s' % (cat, cat_index.keys()))
            if action.lower() not in action_index.keys():
                raise ValueError\
                      ('Invalid action \'%s\' to click select all.'\
                       'Here are the valid actions '\
                       '%s' % (action, action_index.keys()))
            action_sel = action_index[action.lower()]
            link_sel_all = cat_index[cat.lower()][action_sel]
            self.click_element(link_sel_all, "don't wait")

    def _edit_amw_categories_settings(self, amw_categories):
        MONITOR_COLUMN = 2
        BLOCK_COLUMN = 3
        try:
            for cat in amw_categories.keys():
                action = amw_categories[cat].lower()
                self._info('Setting "%s" action for "%s" category' % (action, cat))
                if (action == "block"):
                    self.click_element(\
                    "xpath=//span[normalize-space(text()) = '%s']/../../../td[%d]" % \
                    (cat, BLOCK_COLUMN), "don't wait")
                elif (action == "monitor"):
                    self.click_element(\
                    "xpath=//span[normalize-space(text()) = '%s']/../../../td[%d]" % \
                    (cat, MONITOR_COLUMN), "don't wait")
                else:
                    raise ValueError, 'Unknown action - "%s". Should be "block"'\
                                   'or "monitor"' % (action)
                self._info('Set "%s" action for "%s" category' % (action, cat))
        except:
            raise guiexceptions.GuiFeatureDisabledError\
                ("Failure while setting AMW category '%s' to %s" % (cat, action))
