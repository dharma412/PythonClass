#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/gui/manager/offbox_dlp_policies.py#1 $
# $DateTime: 2019/08/14 09:58:47 $
# $Author: uvelayut $

import common.gui.guiexceptions as guiexceptions
from common.gui.guicommon import GuiCommon
from policybase import PolicyBase

class OffboxDlpPolicies(GuiCommon, PolicyBase):
    """Keywords for Web Security Manager -> External Data Loss Prevention
    """

    policy_name_column = 2
    destinations_column = 3
    delete_column = 4

    def get_keyword_names(self):
        return [
                'offbox_dlp_policies_add',
                'offbox_dlp_policies_delete',
                'offbox_dlp_policies_edit',
                'offbox_dlp_policies_edit_destinations',
                'offbox_dlp_policies_get_list',
                ]

    def offbox_dlp_policies_get_list(self):
        """
        Returns: dictionary of offbox_dlp policies. Keys are names of policies.
        Each policy is a dictionary with following keys:
        - `order`
        - `identity`
        - `proxy_ports`
        - `subnets`
        - `url_categories`
        - `protocols`
        - `user_agents`
        - `destinations`

        Examples:

        | ${policies}= | Offbox DLP Policies Get List |
        | Should Be True | len(${policies}) == 2 |
        | Should Be True | ${policies}['policy']['applications'] == '(global policy)' |
        """

        self._open_page()
        return self._get_policies()

    def _open_page(self):
        """
        Go to configuration page.
        """
        self._navigate_to('Web Security Manager', 'External Data Loss Prevention')

    def offbox_dlp_policies_add(self,
            name,
            description=None,
            order=1,
            identities='Global Identification Profile',
            protocols=None,
            proxy_ports=None,
            subnets=None,
            url_categories=None,
            user_agents=None,
            match_agents=True):
        """Add new DLP policy.

        Parameters:
        - `name`: name for the policy group to add. String.
        - `description`: description for the policy. String.
        - `order`: the processing order. String.
        - `identities`: String of comma separated values of identities. Format
           of an identity is described <a href="policy_base.html#identities">here</a>
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
        - `match_agents`: match selected user agents. Boolean. Default to True.

        Example:
        | Offbox DLP Policies Add |
        | |  three |
        | | description=Adding policy  |
        | | order=1 |
        | | identities=Global Identification Profile |
        | | protocols=http, ftpoverhttp |
        | | proxy_ports=1234, 5321 |
        | | subnets=10.1.1.0/24, 1.2.3.44 |
        | | url_categories=${webcats.ADULT}, ${webcats.ARTS} |
        | | user_agents=ie-all |
        | | match_agents=${False} |
        """
        self._info('Adding "%s" DLP policy' % (name,))

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
            match_agents=match_agents)
        self._click_submit_button()

    def offbox_dlp_policies_delete(self, name):
        """Delete DLP policy.

        Parameters:
        - `name`: name of the policy to delete.

        Example:
        | Offbox DLP Policies Delete |
        | | three |
        """
        self._info('Deleting "%s" DLP policy' % (name,))
        self._open_page()
        self._delete_policy(name, self.delete_column)

    def offbox_dlp_policies_edit(self,
            name,
            new_name=None,
            description=None,
            order=None,
            identities=None,
            protocols=None,
            proxy_ports=None,
            subnets=None,
            url_categories=None,
            user_agents=None,
            match_agents=True):
        """Edit DLP policy.
        Parameters:
        - `name`: name for the policy group to add. String.
        - `new_name`: new name for the policy. Optional. String
        - `description`: description for the policy. String.
        - `order`: the processing order. String.
        - `identities`: String of comma separated values of identities. Format
           of an identity is described <a href="policy_base.html#identities">here</a>
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
        - `match_agents`: match selected user agents. Boolean. Default to True.

        Example:
        | Offbox DLP Policies Edit |
        | | three |
        | | description=Editing policy |
        | | order=1 |
        | | identities=Global Identification Profile |
        | | protocols=http, ftpoverhttp |
        | | proxy_ports=12345, 54321 |
        | | subnets=10.1.1.0/24 |
        | | time_range=holidays |
        | | match_time_range=False |
        | | url_categories=${webcats.ADULT} |
        | | user_agents=ie-all, ff3 |
        """
        self._info('Editing "%s" DLP policy' % (name,))
        self._open_page()
        self._click_edit_policy_link(name, self.policy_name_column)
        self._fill_policy_page(new_name, description, order)

        if identities is not None:
            self._edit_identity_membership(identities)

        self._edit_advanced_settings(
            protocols=protocols,
            proxy_ports=proxy_ports,
            subnets=subnets,
            url_categories=url_categories,
            user_agents=user_agents,
            match_agents=match_agents)
        self._click_submit_button()

    def offbox_dlp_policies_edit_destinations(self,
            name,
            scan_uploads=None,
            url_categories=None,
            settings_type=None):
        """Edit the WBRS and anti-malware for the DLP policy.

        Parameters:
        - `name`: name of the policy to edit.
        - `scan_uploads`:
           * off -> Do not scan any uploads
           * all  -> Scan all uploads
           * except -> Scan uploads to specified custom URL categories
        - `url_categories`: List of excluded in scan custom URL categories
        - `settings_type`: settings type to use. Accepted values:
           * 'global' - Use Destinations scanning Global Policy Settings
           * 'custom' - Define Destinations scanning Custom Settings
           * 'disable' - Disable Destinations scanning for this Policy

        Example:
        It is expected that custom url categories 'cat1' and 'dog2' exist

        | OffboxDLP Policies Edit Destinations |
        | | three |
        | | scan_uploads=except |
        | | url_categories=cat1, dog2 |
        | | settings_type=custom |
        """
        self._open_page()
        self._click_edit_policy_link(name, self.destinations_column)

        if settings_type is not None:
            self._select_destination_settings(settings_type)

        if scan_uploads is not None:
            self._edit_scan_uploads_settings(scan_uploads.lower())

        if scan_uploads is not None and \
                scan_uploads.lower() == 'except' \
                and url_categories is not None:
            self._edit_url_categories_settings \
                    (self._convert_to_tuple(url_categories))

        self._click_submit_button()

    def _edit_scan_uploads_settings(self, scan_uploads):
        scan_uploads_map = {
            'off': 'scan_enabled_none',
            'all': 'scan_enabled_all',
            'except': 'scan_enabled_specified'
            }
        self._click_radio_button(scan_uploads_map[scan_uploads])

        self._info('Scan Uploads settings have been changed')

    def _select_destination_settings(self, settings):
        object_settings = {
            'global':  'value=use_global',
            'custom':  'value=custom',
            'disable': 'value=disabled'
        }

        if settings not in object_settings:
            raise ValueError, 'Invalid "%s" object blocking settings' \
                % (settings)

        self.select_from_list('id=settings_type', object_settings[settings])

        self._info('Selected "%s" blocking settings' % (settings,))

    def _edit_url_categories_settings(self, url_categories):
        edit_link_locator = \
            'xpath=//a[contains(text(), "Edit custom categories list")]'
        CELL_LOC = \
            lambda row, col: 'xpath=//table[@class="cols"]//tr[%s]/td[%s]' % \
                (row, col)
        CATS_COUNT_LOC = \
            '//div[contains(@id, "::customCheckBox::destinations[]")]'

        self.click_element(edit_link_locator)
        available_cats = {}
        count = int(self.get_matching_xpath_count(CATS_COUNT_LOC))

        for i in range(3, count + 3):
            txt = self.get_text(CELL_LOC(i, 1))
            available_cats[txt] = i

        self._info("available_cats=" + str(available_cats))

        for cat in url_categories:
            self._info("processing category " + str(cat))
            if cat not in available_cats:
                raise guiexceptions.GuiControlNotFoundError(
                        'Category: "%s"' % (cat,), self.get_location())
            # the side trick: The hidden control `input` contains some data if
            # category is already selected
            txt = self.get_text(CELL_LOC(available_cats[cat], 2) + '/div/input')
            if not txt:
                self.click_element(CELL_LOC(available_cats[cat], 2) + '/div', \
                                   "don't wait")

            self._info('Enabled "%s" category' % (cat,))

        self._click_done_button()
