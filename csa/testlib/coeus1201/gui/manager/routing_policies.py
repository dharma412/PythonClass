#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/gui/manager/routing_policies.py#1 $
# $DateTime: 2019/08/14 09:58:47 $
# $Author: uvelayut $

from common.gui.guicommon import GuiCommon
from policybase import PolicyBase

class RoutingPolicies(GuiCommon, PolicyBase):
    """
    Keywords for Web Security Manager -> Routing Policies
    """
    policy_name_column = 2
    destination_column = 3
    delete_column = 4

    def get_keyword_names(self):
        return [
                'routing_policies_add',
                'routing_policies_delete',
                'routing_policies_edit',
                'routing_policies_edit_destination',
                'routing_policies_get_list',
                ]

    def routing_policies_get_list(self):
        """
        Returns: dictionary of routing policies. Keys are names of policies.
        Each policy is a dictionary with following keys:
        - `order`
        - `identity`
        - `proxy_ports`
        - `subnets`
        - `time_range`
        - `url_categories`
        - `protocols`
        - `routing_destination`

        Examples:

        | ${policies}= | Routing Policies Get List |
        | Should Be True | len(${policies}) == 2 |
        | Should Be True | ${policies}['policy']['subnets'] == '10.1.1.1, 20.2.2.2' |
        """

        self._open_page()
        return self._get_policies()

    def _open_page(self):
        """
        Go to Routing Policies configuration page.
        """
        self._navigate_to('Web Security Manager', 'Routing Policies')

    def routing_policies_add(self,
            name,
            description=None,
            order=None,
            identities=None,
            protocols=None,
            proxy_ports=None,
            subnets=None,
            time_range=None,
            match_time_range=True,
            url_categories=None,
            user_agents=None,
            common_user_agents=None,
            match_agents=True):
        """
        Add new routing policy.

        Parameters:
        - `name`: name for the policy group to add. String.
        - `description`: description for the policy. String.
        - `order`: the processing order. Integer or string.
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
        - `time_range`: the time range where policy is a member. String.
        - `match_time_range`: match selected time range. Default to True.
        - `url_categories`: the URL categories where poicy is a member.
           String of comma separated values.
        - `user_agents`: the user agents where policy is a member.
           String of comma separated values
        - `common_user_agents`: String of comma separated values of
           common user agents: 'ie8', 'ie7', 'ie6', 'pre-ie5', 'ie-all', 'ff3',
           'ff2', 'ff1', 'ff-all', 'ms-update', 'acro-update'
        - `match_agents`: match selected user agents. Boolean. Default to True.

        Example:
        | Routing Policies Add | three |
        | | description=Adding policy  |
        | | order=None |
        | | identities=Global Identification Profile |
        | | protocols=http, ftpoverhttp |
        | | proxy_ports=1234, 5321 |
        | | subnets=10.1.1.0/24, 1.2.3.44 |
        | | time_range=holidays  |
        | | url_categories=${webcats.ADULT}, ${webcats.ARTS} |
        | | user_agents=ie-all |

        Exceptions:
        - `GuiFeatureDisabledError`: Routing is disabled. Page displays
           "Routing Policies are currently disabled. To use Routing Policies,
           define at least one upstream proxy (see Network > Upstream Proxies)."
        - `GuiControlNotFoundError`: Membership entities are not editable.
           The exact reason is in message string
        - `ValueError`: Entered data is wrong (was declined before sent
           to the page).
        """
        self._info('Adding "%s" routing policy' % (name,))
        self._open_page()
        self._click_add_policy_button()

        self._fill_policy_page(name, description, order)

        if identities is not None:
            self._edit_identity_membership(identities)

        self._edit_advanced_settings(
            protocols=protocols,
            proxy_ports=proxy_ports,
            subnets=subnets,
            time_range=time_range,
            match_range=match_time_range,
            url_categories=url_categories,
            user_agents=user_agents,
            common_user_agents=common_user_agents,
            match_agents=match_agents)

        self._click_submit_button()

    def routing_policies_delete(self, name):
        """
        Delete routing policy.

        Parameters:
        - `name`: name of the policy to delete.

        Example:
        | RoutingPolicies Delete | three |

        """
        self._info('Deleting %s routing policy' % (name,))

        self._open_page()
        self._delete_policy(name, self.delete_column)

    def routing_policies_edit(self,
            name,
            description=None,
            order=None,
            identities=None,
            protocols=None,
            proxy_ports=None,
            subnets=None,
            time_range=None,
            match_time_range=True,
            url_categories=None,
            user_agents=None,
            common_user_agents=None,
            match_agents=True):
        """
        Edit routing policy.

        Parameters:
        - `name`: name for the policy group to edit. String.
        - `description`: description for the policy. String.
        - `order`: the processing order. Integer or string.
        - `identities`: String of comma separated values of identities
           Format of an identity is described <a href="policy_base.html#identities">here</a>
        - `protocols`: the protocols where policy is a member. String of comma
        separated values. The following values are currently accepted:
           * http
           * ftpoverhttp
           * nativeftp
           * others
           * https
        - `proxy_ports`: The ports where policy is a member. String of comma separated values
        - `subnets`: the nets where policy is member. String of comma separated values
           in format of IP, IP range or CIDR.
        - `time_range`: the time range where policy is a member. String.
        - `match_time_range`: match selected time range. Default to True.
        - `url_categories`: the URL categories where policy is a member.
           String of comma separated values.
        - `user_agents`: the user agents where policy is a member. String of
           comma separated values
        - `common_user_agents`: a comma separate string or a list of one or
           more of the following common user agents: 'ie8',
          'ie7', 'ie6', 'pre-ie5', 'ie-all', 'ff3', 'ff2',
          'ff1', 'ff-all', 'ms-update', 'acro-update'
        - `match_agents`: match selected user agents. Boolean. Default to True.

        Example:
        | RoutingPolicies Edit | three |
        | | description=Editing policy |
        | | order=None |
        | | identities=Global Identification Profile |
        | | protocols=http, ftpoverhttp |
        | | proxy_ports=12345, 54321 |
        | | subnets=10.1.1.0/24 |
        | | time_range=holidays |
        | | match_time_range=False |
        | | url_categories=${webcats.ADULT} |
        | | user_agents=ie-all, ff3 |

        Exceptions:
        - `GuiFeatureDisabledError`: Routing is disabled. Page displays
          "Routing Policies are currently disabled. To use Routing Policies
           define at least one upstream proxy (see Network > Upstream Proxies)."
        - `GuiControlNotFoundError`: Membership entities are not editable
           (see issue). The exact reason is in message string
        - `ValueError`: Entered data is wrong (was declined before sent
           to the page).
        """
        self._info('Editing "%s" routing policy' % (name,))

        self._open_page()
        self._click_edit_policy_link(name, self.policy_name_column)
        self._fill_policy_page(None, description, order)

        if identities is not None:
            self._edit_identity_membership(identities)

        self._edit_advanced_settings(
            protocols=protocols,
            proxy_ports=proxy_ports,
            subnets=subnets,
            time_range=time_range,
            match_range=match_time_range,
            url_categories=url_categories,
            user_agents=user_agents,
            common_user_agents=common_user_agents,
            match_agents=match_agents)
        self._click_submit_button()

    def routing_policies_edit_destination(self, name, proxy_group):
        """
        Setup the destination for given routing policy.

        Parameters:
        - `name`: name of the routing policy to edit.
        - `proxy_group`: proxy group to set routing to. String.

        Exceptions:
        - `GuiFeatureDisabledError`: Routing is disabled. Page displays
          "Routing Policies are currently disabled. To use Routing Policies,
           define at least one upstream proxy (see Network > Upstream Proxies)."
        - `ValueError`: Entered data is wrong (was declined before sent
           to the page).
        - `GuiControlNotFoundError`: policy doesn't exist;
           proxy group doesn't exist

        Examples:
        | RoutingPolicies Edit Destination| three | upstream2 |
        | RoutingPolicies Edit Destination| three | Use Global Policy Settings |

        """
        self._info('Editing destination for "%s" routing policy' % (name,))

        self._open_page()
        self._click_edit_policy_link(name, self.destination_column)
        self._select_proxy_group(proxy_group)

        self._click_submit_button()

    def _select_proxy_group(self, proxy_group):
        proxy_group_id = 'id=proxy_group'
        self.select_from_list(proxy_group_id, proxy_group)
        self._info('Selected "%s" proxy group' % (proxy_group,))
