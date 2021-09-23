#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1350/gui/web/cm77/cm77_oms_policies.py#1 $ $DateTime: 2019/09/18 01:46:35 $ $Author: sarukakk $

from coeus77.gui.manager.oms_policies import OMS_Policies


class Cm77OmsPolicies(OMS_Policies):
    """
    Keywords library for WebUI page Web -> Configuration Master 7.7 -> Outbound Malware Scanning
    """

    def _open_page(self):
        self._navigate_to('Web', 'Configuration Master 7.7', 'Outbound Malware Scanning')

    def get_keyword_names(self):
        return [
            'cm77_oms_policies_add',
            'cm77_oms_policies_delete',
            'cm77_oms_policies_edit',
            'cm77_oms_policies_edit_destinations',
            'cm77_oms_policies_edit_amw_filters'
        ]

    def cm77_oms_policies_add(self,
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
        """Add new policy from Configuration Master 7.7

        *Parameters*
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

        *Exceptions*
        - `ValueError`: in case of proxy ports, time ranges, subnet membership
            or url categories is disabled in advanced policy menu.

        *Examples*
        | CM77 OMS Policies Add | three | description=Adding policy  |
        | ... | identities=Global Identity Policy | protocols=http, ftpoverhttp |
        | ... | proxy_ports=1234, 5321 | subnets=10.1.1.0/24, 1.2.3.44 |
        | ... | url_categories=${webcats.ADULT}, ${webcats.ARTS} |
        | ... | user_agents=ie-all |
        | CM77 OMS Policies Add | zero | subnets=192.168.20.0/24  |
        """
        self.oms_policies_add(
            name,
            description=description,
            order=order,
            identities=identities,
            protocols=protocols,
            proxy_ports=proxy_ports,
            subnets=subnets,
            url_categories=url_categories,
            user_agents=user_agents,
            common_user_agents=common_user_agents,
            match_agents=match_agents)

    def cm77_oms_policies_edit(self,
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
        """Edits specified policy from Configuration Master 7.7

        *Parameters*
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

        *Exceptions*
        - `ValueError`: in case of proxy ports, time ranges, subnet membership
            or url categories is disabled in advanced policy menu.
        - `ValueError`: if try to edit Global Policy

        *Examples*
        | CM77 OMS Policies Edit | three | description=Editing policy |
        | ... | order=None | identities=Global Identity Policy |
        | ... | protocols=http, ftpoverhttp | proxy_ports=12345, 54321 |
        | ... | subnets=10.1.1.0/24 | url_categories=${webcats.ADULT} |
        | ... | user_agents=ie-all, ff3 |
        | CM77 OMS Policies Edit | zero | subnets=192.168.20.0/24 |
        """
        self.oms_policies_edit(
            name,
            description=description,
            order=order,
            identities=identities,
            protocols=protocols,
            proxy_ports=proxy_ports,
            subnets=subnets,
            url_categories=url_categories,
            user_agents=user_agents,
            common_user_agents=common_user_agents,
            match_agents=match_agents)

    def cm77_oms_policies_delete(self, name):
        """Deletes specified policy from Configuration Master 77
        NOTE: Default policy can not be deleted

        *Parameters*
        - `name`: name of the policy to delete.

        *Exceptions*
        - `GuiControlNotFoundError`: if policy with such name doesn't exist
        - `ValueError`: if trying to delete Global Policy.

        *Example*
        | CM77 OMS Policies Delete | three |
        """
        self.oms_policies_delete(name)

    def cm77_oms_policies_edit_amw_filters(self,
                                           name,
                                           settings_type,
                                           amw_actions=None,
                                           amw_select_all=None,
                                           webroot=None,
                                           av=None,
                                           enable_scanning=None):
        """ Edits anti-malware filtering settings for specified policy
         from Configuration Master 7.7

        *Parameters*
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

        *Exceptions*
        - `ValueError`: because of enabling both AV engine in the same time or
          invalid Key for activation/deactivation AV engine.
        - `GuiFeatureDisableError`: if 'select all' link not available for this
          category.
        - `ValueError`: if unknown action is provided.
        - `GuiFeatureDisableError`: if such AMW category not present.

        *Examples*
        | CM77 OMS Policies Edit AMW Filters | three | global |
        | Cm77 OMS Policies Edit AMW Filters | three | custom |
        | ... | amw_actions=${mwcats.VIRUS}:block, ${mwcats.DIALER}:block} |
        | ... | amw_select_all=Malware:monitor, Other: block |
        | ... | webroot=True | av=sophos: enable |
        """
        self.oms_policies_edit_amw_filters(
            name,
            settings_type,
            amw_actions=amw_actions,
            amw_select_all=amw_select_all,
            webroot=webroot,
            av=av,
            enable_scanning=enable_scanning)

    def cm77_oms_policies_edit_destinations(self,
                                            name,
                                            settings_type,
                                            dest_to_scan=None,
                                            cust_url=None,
                                            cust_url_all=None):
        """Edits destinations settings for specified policy
         from Configuration Master 7.7

        *Parameters*
        - `name`: name of policy to be edited.
        - `settings_type`: settings to use.  Either 'global' or 'custom'.
        - `dest_to_scan`: destinations to scan.  Either 'no', 'all', or 'url'.
        - `cust_url`: string of comma-separated custom URL categories to scan.
        - `cust_url_all`: True to select all defined custom URL categories to
           scan.

        *Exceptions*
        - `ValueError`: because of enabling both AV engine in the same time or
          invalid Key for activation/deactivation AV engine.
        - `GuiFeatureDisableError`: if 'select all' link not available for this
          category.
        - `ValueError`: if unknown action is provided.
        - `GuiFeatureDisableError`: if such AMW category not present.

        *Examples*
        | CM77 OMS Policies Edit AMW Filters | three | global |
        | Cm77 OMS Policies Edit AMW Filters | three | custom |
        | ... | amw_actions=${mwcats.VIRUS}:block, ${mwcats.DIALER}:block} |
        | ... | amw_select_all=Malware:monitor, Other: block |
        | ... | webroot=True | av=sophos: enable |
        """

        self.oms_policies_edit_destinations(
            name,
            settings_type,
            dest_to_scan=dest_to_scan,
            cust_url=cust_url,
            cust_url_all=cust_url_all)
