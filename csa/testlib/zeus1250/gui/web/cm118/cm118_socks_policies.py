# $Id: //prod/main/sarf_centos/testlib/zeus1250/gui/web/cm118/cm118_socks_policies.py#3 $
# $DateTime: 2019/06/07 02:45:52 $
# $Author: sarukakk $

import common.gui.guiexceptions as guiexceptions
from coeus1180.gui.manager.socks_policies import SOCKSPolicies

class Cm110SOCKSPolicies(SOCKSPolicies):
    """
    Keywords for Web -> Configuration Master 11.8 -> SOCKS Policies
    """
    def _open_page(self):
        """Go to SOCKS Policies configuration page."""

        self._navigate_to('Web', 'Configuration Master 11.8', 'SOCKS Policies')
        locator = 'xpath=//div[@class="text-info"]'
        if self._is_element_present(locator):
            txt = self.get_text(locator)
            if 'SOCKS Policies are currently disabled' in txt:
                raise guiexceptions.GuiFeatureDisabledError(txt)

    def get_keyword_names(self):
        return ['cm118_socks_policies_add',
             'cm118_socks_policies_edit',
             'cm118_socks_policies_delete',
             'cm118_socks_policies_edit_destination_ports',
             'cm118_socks_policies_edit_destination_urls',
             'cm118_socks_policies_disable_policy',
             'cm118_socks_policies_enable_policy',
             'cm118_socks_policies_is_enabled_policy',
             'cm118_socks_policies_get_list',
             ]

    def cm118_socks_policies_add(self,
        name,
        description=None,
        order=None,
        identities=None,
        proxy_ports=None,
        subnets=None,
        time_range=None,
        match_time_range=True,
        ):
        """Adds new socks policy.

        Parameters:
        - `name`: name of socks policy.
        - `description`: description for socks policy.
        - `order`: order of socks policy.
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

        Examples:
        - | CM118 SOCKS Policies Add | myDefaultPol | description=This policy uses Global Identity Policy | identities=Global Identity Policy |
        - | CM118 SOCKS Policies Add | myOtherPol | description=This policy uses specified identity | identities=myID:authenticated |
        - | CM118 SOCKS Policies Add | myOtherPol2 | proxy_ports=10110 |

        Exceptions:
        - GuiFeatureDisabledError:SOCKS Policies are currently disabled
        """
        self.socks_policies_add(name, description, order, identities, proxy_ports,
                            subnets, time_range, match_time_range)

    def cm118_socks_policies_delete(self, name):
        """Deletes specified socks policy.

        Parameters:
        - `name`: name of socks policy to be deleted.

        Example:
        - | CM118 SOCKS Policies Delete | myDefaultPol |

        Exceptions:
        - GuiFeatureDisabledError:SOCKS Policies are currently disabled
        """

        self.socks_policies_delete(name)


    def cm118_socks_policies_edit(self,
        name,
        new_name=None,
        description=None,
        order=None,
        identities=None,
        proxy_ports=None,
        subnets=None,
        time_range=None,
        match_time_range=True,
        ):
        """Edits socks policy.

        Parameters:
        - `name`: name of socks policy group to edit.
        - `new_name`: new name for socks policy.
        - `description`: description for socks policy.
        - `order`: order of socks policy.
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

        Examples:
        - | SOCKS Policies Edit | myDecrPol | identities=All Identities:selected:joe.smith |
        - | SOCKS Policies Edit | myDecrPol | identities=All Identities:all | time_range=myTime | proxy_ports=3128 |

        Exceptions:
        - GuiFeatureDisabledError:SOCKS Policies are currently disabled
        """

        self.socks_policies_edit(name, new_name, description, order, identities, proxy_ports,
                                    subnets, time_range, match_time_range)

    def cm118_socks_policies_edit_destination_ports(self,
        name,
        ports_settings=None,
        tcp_ports=None,
        udp_ports=None,
        ):
        """Edits SOCKS connections to destination ports.
        Specifies lists of outbound port numbers or ranges

        Parameters:
        - `ports_settings`: type of settings; accepted values: global and custom
        - `tcp_ports`: list of outbound port numbers or ranges separated
        by comma(s). A port must be a number from 1 to 65535.
        - `udp_ports`: list of outbound port numbers or ranges separated
        by comma(s). A port must be a number from 1 to 65535.

        Examples:
        - | CM118 SOCKS Policies Edit Destination Ports | myPolicy |
        - | ... | ports_settings=custom |
        - | ... | tcp_ports=1000, 1001, 1002-11.0 |
        - | ... | udp_ports=2000-3000, 2 |

        - | SOCKS Policies Edit Destination Ports | myPolicy |
        - | ... | ports_settings=global |

        Exceptions:
        - GuiFeatureDisabledError:SOCKS Policies are currently disabled
        - ValueError: ports_settings should be 'global' or 'custom'
        """

        self.socks_policies_edit_destination_ports(name, ports_settings, tcp_ports, udp_ports)

    def cm118_socks_policies_edit_destination_urls(self,
        name,
        setting_type=None,
        specified_url_categories=None,
        ):
        """Edits Destination URLs / IP Addresses for socks policy.

        Parameters:
        - `name`: name of socks policy group to edit.
        - `setting_type`:
        .    'global' - Use Destinations Global Policy Settings
        .    'block_all' - Do not allow SOCKS connections to any URL or IP Address
        .    'allow_all' - Allow SOCKS connections to any URL or IP Address
        .    'allow_specified' - Allow SOCKS connections only to specified list of
        specified URL categories
        - `specified_url_categories`: 'all' or - comma-separated list of specified
         URL categories

        Examples:
        - | CM118 SOCKS Policies Edit Destination Urls | myPolicy | setting_type=global |
        - | CM118 SOCKS Policies Edit Destination Urls | myPolicy | setting_type=block_all |
        - | CM118 SOCKS Policies Edit Destination Urls | myPolicy | setting_type=allow_all |
        - | CM118 SOCKS Policies Edit Destination Urls | myPolicy | setting_type=allow_specified | specified_url_categories=all |
        - | CM118 SOCKS Policies Edit Destination Urls | myPolicy | setting_type=allow_specified | specified_url_categories=cats, dogs |

        Exceptions:
        - GuiFeatureDisabledError:SOCKS Policies are currently disabled
        - ConfigError:Setting type 'XXX' should be in
        ['global','block_all',allow_all','allow_specified']
        """

        self.socks_policies_edit_destination_urls(name, setting_type, specified_url_categories)

    def cm118_socks_policies_is_enabled_policy(self, name):
        """Returns True if existing policy is enabled or False otherwise.

        Parameters:
            - `name` policy name to check

        Examples:
            | ${enabled}= | CM118 SOCKS Policies Is Enabled Policy | myDefaultAccPol |
        """

        self._open_page()
        return self._is_enabled(name)

    def cm118_socks_policies_get_list(self):
        """
        Returns: dictionary of SOCKS policies. Keys are names of policies.
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

        | ${policies}= | CM118 SOCKS Policies Get List |
        | Should Be True | len(${policies}) == 2 |
        | Should Be True | ${policies}['policy']['subnets'] == '10.1.1.1, 20.2.2.2' |
        """

        self._open_page()
        return self._get_policies()

    def cm118_socks_policies_enable_policy(self, name):
        """Enables existing policy

        Parameters:
            - `name` policy name to enable

        Examples:
            | CM118 SOCKS Policies Enable Policy | myDefaultPol |
        """

        self._open_page()
        self._enable(name)

    def cm118_socks_policies_disable_policy(self, name):
        """Disables existing policy

        Parameters:
            - `name` policy name to enable

        Examples:
            | CM118 SOCKS Policies Disable Policy | myDefaultPol |
        """

        self._open_page()
        self._disable(name)

