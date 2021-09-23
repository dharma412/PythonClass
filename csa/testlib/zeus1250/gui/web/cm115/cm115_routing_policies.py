# $Id: //prod/main/sarf_centos/testlib/zeus1250/gui/web/cm115/cm115_routing_policies.py#3 $
# $DateTime: 2019/06/07 02:45:52 $
#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1250/gui/web/cm115/cm115_routing_policies.py#3 $ $DateTime: 2019/06/07 02:45:52 $  $Author: sarukakk $

from coeus1100.gui.manager.routing_policies import RoutingPolicies
class Cm110RoutingPolicies(RoutingPolicies):

    """
    Keywords for Web -> Configuration Master 11.5 -> Routing Policies
    """

    def _open_page(self):
        self._navigate_to('Web', 'Configuration Master 11.5', 'Routing Policies')

    def get_keyword_names(self):
        return [
             'cm115_routing_policies_add',
             'cm115_routing_policies_delete',
             'cm115_routing_policies_edit',
             'cm115_routing_policies_edit_destination',
             'cm115_routing_policies_get_list',
             ]

    def cm115_routing_policies_get_list(self):
        """
        Returns: dictionary of routing_policies from Configuration Master
        Keys are names of policies.
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
        | ${policies}= | CM115 Routing Policies Get List |
        | ${policies}= | Routing Policies Get List |
        | Should Be True | len(${policies}) == 2 |
        """
        return self.routing_policies_get_list()

    def cm115_routing_policies_add(self,
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
        Add new routing policy from Configuration Master 11.5

        *Parameters*
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

        *Exceptions*
        - `GuiFeatureDisabledError`: Routing is disabled. Page displays
           "Routing Policies are currently disabled. To use Routing Policies,
           define at least one upstream proxy (see Network > Upstream Proxies)."
        - `GuiControlNotFoundError`: Membership entities are not editable.
           The exact reason is in message string
        - `ValueError`: Entered data is wrong (was declined before sent
           to the page).

        *Examples*
        | CM115 Routing Policies Add | three | description=Adding policy |
        | ... | order=None | identities=Global Identity Policy |
        | ... | protocols=http, ftpoverhttp | proxy_ports=1234, 5321 |
        | ... | subnets=10.1.1.0/24, 1.2.3.44 | time_range=holidays |
        | ... | url_categories=${webcats.ADULT}, ${webcats.ARTS} |
        | ... | user_agents=ie-all |
        """
        self.routing_policies_add(
            name,
            description=description,
            order=order,
            identities=identities,
            protocols=protocols,
            proxy_ports=proxy_ports,
            subnets=subnets,
            time_range=time_range,
            match_time_range=match_time_range,
            url_categories=url_categories,
            user_agents=user_agents,
            common_user_agents=common_user_agents,
            match_agents=match_agents)

    def cm115_routing_policies_edit(self,
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
        Edit routing policy from Configuration Master 11.5

        *Parameters*
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

        *Exceptions*
        - `GuiFeatureDisabledError`: Routing is disabled. Page displays
          "Routing Policies are currently disabled. To use Routing Policies
           define at least one upstream proxy (see Network > Upstream Proxies)."
        - `GuiControlNotFoundError`: Membership entities are not editable
           (see issue). The exact reason is in message string
        - `ValueError`: Entered data is wrong (was declined before sent
           to the page).

        *Examples*
        | CM115 RoutingPolicies Edit | three | description=Editing policy |
        | ... | order=None | identities=Global Identity Policy |
        | ... | protocols=http, ftpoverhttp |
        | ... | proxy_ports=12345, 54321 | subnets=10.1.1.0/24 |
        | ... | time_range=holidays | match_time_range=False |
        | ... | url_categories=${webcats.ADULT} | user_agents=ie-all, ff3 |
        | CM115 RoutingPolicies Edit | zero | new description |
        """
        self.routing_policies_edit(
            name,
            description=description,
            order=order,
            identities=identities,
            protocols=protocols,
            proxy_ports=proxy_ports,
            subnets=subnets,
            time_range=time_range,
            match_time_range=match_time_range,
            url_categories=url_categories,
            user_agents=user_agents,
            common_user_agents=common_user_agents,
            match_agents=match_agents)

    def cm115_routing_policies_delete(self, name):
        """
        Delete routing policy from Configuration Master 11.5

        *Parameters*
        - `name`: name of the policy to delete.

        *Example*
        | CM115 RoutingPolicies Delete | three |

        """
        self.routing_policies_delete(name)

    def cm115_routing_policies_edit_destination(self, name, proxy_group):
        """
        Setup the destination for given routing policy from Configuration Master 11.5

        Parameters:
        - `name`: name of the routing policy to edit.
        - `proxy_group`: proxy group to set routing to. String.

        *Exceptions*
        - `GuiFeatureDisabledError`: Routing is disabled. Page displays
          "Routing Policies are currently disabled. To use Routing Policies,
           define at least one upstream proxy (see Network > Upstream Proxies)."
        - `ValueError`: Entered data is wrong (was declined before sent
           to the page).
        - `GuiControlNotFoundError`: policy doesn't exist;
           proxy group doesn't exist

        *Examples*
        | CM115 RoutingPolicies Edit Destination| three | upstream2 |
        | CM115 RoutingPolicies Edit Destination| three | Use Global Policy Settings |

        """
        self.routing_policies_edit_destination(name, proxy_group)

