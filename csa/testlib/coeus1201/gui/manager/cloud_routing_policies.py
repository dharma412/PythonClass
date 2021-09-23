#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/gui/manager/cloud_routing_policies.py#1 $
# $DateTime: 2019/08/14 09:58:47 $
# $Author: uvelayut $
import time
import common.gui.guiexceptions as guiexceptions
from common.gui.guicommon import GuiCommon
from policybase import PolicyBase

class CloudRoutingPolicies(GuiCommon, PolicyBase):
    """
    Keywords for Web Security Manager -> Routing Policies
    """
    policy_name_column = 2
    destination_column = 3
    delete_column = 4

    def get_keyword_names(self):
        return [
                'cloud_routing_policies_add',
                'cloud_routing_policies_delete',
                'cloud_routing_policies_edit',
                'cloud_routing_policies_edit_destination',
                'cloud_routing_policies_get_list',
               ]

    def cloud_routing_policies_get_list(self):
        """
        Returns: dictionary of cloud routing policies. Keys are names of policies.
        Each policy is a dictionary with following keys:
        - `order`
        - `identity`
        - `proxy_ports`
        - `subnets`
        - `url_categories`
        - `user_agents`
        - `user_location`
        - `routing_destination`

        Examples:

        | ${policies}= | Cloud Routing Policies Get List |
        | Should Be True | len(${policies}) == 2 |
        | Should Be True | ${policies}['policy']['subnets'] == '10.1.1.1, 20.2.2.2' |
        """

        self._open_page()
        return self._get_policies()

    def _open_page(self):
        """
        Go to Routing Policies configuration page.
        """
        self._navigate_to('Web Security Manager', 'Cloud Routing Policies')

    def cloud_routing_policies_add(self,
            name,
            description=None,
            order=None,
            identities=None,
            proxy_ports=None,
            subnets=None,
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
        - `proxy_ports`: The ports where policy is a member. String of comma
           separated values
        - `subnets`: the nets where policy is member. String of comma separated
           values in format of IP, IP range or CIDR.
        - `url_categories`: the URL categories where poicy is a member.
           String of comma separated values.
        - `user_agents`: the user agents where policy is a member.
           String of comma separated values
        - `common_user_agents`: String of comma separated values of
           common user agents: 'ie8', 'ie7', 'ie6', 'pre-ie5', 'ie-all', 'ff3',
           'ff2', 'ff1', 'ff-all', 'ms-update', 'acro-update'
        - `match_agents`: match selected user agents. Boolean. Default to True.

        Example:
        | Cloud Routing Policies Add | three |
        | | description=Adding policy  |
        | | order=None |
        | | identities=Global Identification Profile |
        | | proxy_ports=1234, 5321 |
        | | subnets=10.1.1.0/24, 1.2.3.44 |
        | | url_categories=${webcats.ADULT}, ${webcats.ARTS} |
        | | user_agents=ie-all |

        Exceptions:
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
            proxy_ports=proxy_ports,
            subnets=subnets,
            url_categories=url_categories,
            user_agents=user_agents,
            common_user_agents=common_user_agents,
            match_agents=match_agents)

        self._click_submit_button()

    def cloud_routing_policies_delete(self, name):
        """
        Delete routing policy.

        Parameters:
        - `name`: name of the policy to delete.

        Example:
        | CloudRoutingPolicies Delete | three |

        """
        self._info('Deleting %s routing policy' % (name,))

        self._open_page()
        self._delete_policy(name, self.delete_column)

    def cloud_routing_policies_edit(self,
            name,
            description=None,
            order=None,
            identities=None,
            proxy_ports=None,
            subnets=None,
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
        - `proxy_ports`: The ports where policy is a member. String of comma separated values
        - `subnets`: the nets where policy is member. String of comma separated values
           in format of IP, IP range or CIDR.
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
        | CloudRoutingPolicies Edit | three |
        | | description=Editing policy |
        | | order=None |
        | | identities=Global Identification Profile |
        | | proxy_ports=12345, 54321 |
        | | subnets=10.1.1.0/24 |
        | | url_categories=${webcats.ADULT} |
        | | user_agents=ie-all, ff3 |

        Exceptions:
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
            proxy_ports=proxy_ports,
            subnets=subnets,
            url_categories=url_categories,
            user_agents=user_agents,
            common_user_agents=common_user_agents,
            match_agents=match_agents)
        self._click_submit_button()

    def cloud_routing_policies_edit_destination(self, name, destination):
        """
        Setup the destination for given routing policy.

        Parameters:
        - `name`: name of the routing policy to edit.
        - `destination`: One of the following: global, direct, OR cloud

        Exceptions:
        - `ValueError`: Destination xxx should be in
         ['global', 'direct', 'cloud']

        Examples:
        | CloudRoutingPolicies Edit Destination| three | global |
        | CloudRoutingPolicies Edit Destination| three | cloud |

        """
        self._info('Editing destination for "%s" routing policy' % (name,))

        self._open_page()
        self._click_edit_policy_link(name, self.destination_column)
        self._select_destination(destination)
        self._click_submit_button()
    def _select_destination(self, destination):
        DESTINATIONS = {
            'global' : 0,
            'direct' : 1,
            'cloud'  : 2,
        }
        if destination not in DESTINATIONS.keys():
            raise ValueError("Destination %s should be in %s" % \
                             (destination, DESTINATIONS.keys()))
        destination_id = 'id=proxy_group'
        self.select_from_list(destination_id, 'index=%d' % \
            DESTINATIONS[destination])
        self._info('Selected "%s"' % (destination,))
