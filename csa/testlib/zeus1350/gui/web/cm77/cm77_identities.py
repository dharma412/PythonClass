# $Id: //prod/main/sarf_centos/testlib/zeus1350/gui/web/cm77/cm77_identities.py#1 $
# $DateTime: 2019/09/18 01:46:35 $
# $Author: sarukakk $
# !/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1350/gui/web/cm77/cm77_identities.py#1 $ $DateTime: 2019/09/18 01:46:35 $ $Author: sarukakk $

from coeus77.gui.manager.identities import Identities


class Cm77Identities(Identities):
    """
    Keywords library for WebUI page Web -> Configuration Master 7.7 -> Identities
    """

    def _open_page(self):
        self._navigate_to('Web', 'Configuration Master 7.7', 'Identities')

    def get_keyword_names(self):
        return [
            'cm77_identities_add_policy',
            'cm77_identities_edit_policy',
            'cm77_identities_delete_policy',
            'cm77_identities_enable_policy',
            'cm77_identities_disable_policy',
            'cm77_identities_is_enabled_policy',
            'cm77_identities_get_list',
        ]

    def cm77_identities_get_list(self):
        """
        Returns: dictionary of identities from Configuration Master
        Keys are names of identities.
        Each identity is a dictionary with following keys:
        - `order`
        - `user_location`
        - `subnets`
        - `protocols`
        - `authentication`
        - `surrogate_type`
        - `url_categories`
        - `user_agents`
        - `end-user_acknowledgement`

        Examples:

        | ${policies}= | CM77 Identities Get List |
        | Should Be True | len(${policies}) == 4 |
        | Should Be True | ${policies}.has_key('Global Identity Policy') |
        | Should Be True | ${policies}['Global Identity Policy']['authentication'].find('Exempt') > -1 |
        | Should Be True | len(${policies}['CustomPolicy']) == 3 |
        | Should Be True | ${policies}['CustomPolicy']['end-user_acknowledgement'] == 'Required' |
        """
        return self.identities_get_list()

    def cm77_identities_add_policy(self,
                                   name,
                                   description=None,
                                   order=None,
                                   subnet=None,
                                   protocol=None,
                                   auth_method=None,
                                   auth_realm=None,
                                   auth_scheme=None,
                                   trans_id_fails=None,
                                   support_guest=None,
                                   surrogate_type=None,
                                   apply_same_surrogate=None,
                                   proxy_ports=None,
                                   url_categories=None,
                                   user_agents=None,
                                   common_user_agents=None,
                                   match_agent=None,
                                   managed_appliances=None,
                                   user_location=None,
                                   ):
        """Adds new identity policy from Configuration Master 7.7

        *Parameters*
        - `name`: name of identity.
        - `description`: description for identity.
        - `order`: order of identity.
        - `subnet`: a string of comma separated or a list of subnet where
             identity is member.
        - `protocol`: a list of protocols which identity is a member. Allowed
             values: 'socks', 'http', or 'ftp'. Can be 'all' to set all protocols.
        - `auth_method`: type of authentication for identity.  Either 'no',
             'requires', or 'transparent'.
        - `auth_realm`: name of authentication realm if 'auth_method' above
             is set to 'requires'.
        - `auth_scheme`: authentication scheme for NTLM realm.  Either
             'Basic', 'Basic or NTLMSSP', or 'NTLMSSP'
        - `trans_id_fails`: action to perform if transparent user
             identification fails.  Either 'support' or
             'enforce'.
        - `support_guest`: specifiy whether to support guest privileges if a
             user fails authentication.  Either True or False.
        - `surrogate_type`: surrogate type for transparent proxy mode.
             Either 'ip', 'persistent', or 'session'.
        - `apply_same_surrogate`: specifiy whether to apply same surrogate
             settings to explicit forward requests.
             Either True or False.
        - `proxy_ports`: a string of comma separated ports in which
             identity is a member.
        - `url_categories`: a string of comma separated pre-defined or
             custom URL categories in which identity is a
             member.
        - `common_user_agents`: a string of comma separated or a list of
             the following common user agents:
             'ie8', 'ie7', 'ie6', 'pre-ie5', 'ie-all',
             'ff3', 'ff2', 'ff1', 'ff-all', 'ms-update',
             'acro-update'
        - `user_agents`: a string of comma separated or a list of
             custom user agents in which identity is a member.
        - `match_agent`: specify whether to match the selected user agent
             definition.  Either True or False.
        - `managed_appliances` - By default policies apply
         to all appliances that use the configuration master. Use that property
         if you want to restrict the policy to a subset of these appliances.
         Accepted values: "all" or a string of comma-separated security
         appliances: "wsa01.wga, wsa02.wga, wsa03.wga"
        - `user_location`: - Define Members by User Location. Accepted values:
        - . local - These users are connected to the network either physically or
         wirelessly.
        - . remote - These users are connected to the network from a remote
         location using VPN (virtual private network). Users might be located
         in a home office, coffee shop, or hotel, for example. The Web Security
         appliance automatically identifies remote users when both the Cisco
         ASA and Cisco AnyConnect Client are used for VPN access. Otherwise,
         the Web Security appliance administrator must specify remote users by
         configuring a range of IP addresses.
        - .both - local and remote
        - . Note. Assigning user_location requires that
         "AnyConnect Secure Mobility" service is enabled

        *Exceptions*
            - `ValueError`: in case of proxy ports, time ranges, subnet
              membership or url categories is disabled in advanced policy menu.
            - `ValueError`: if invalid protocol is provided.
            - `ValueError`: No authentication realm has been configured or invalid
              authentication action.
            - `ValueError`: invalid authentication schemes or invalid action for
              transparent user.

        *Examples*
           | Identities Add Policy | subnetID |
           | ... | description=This is a subnet identity | subnet=1.2.3.0/24 |
           | Identities Add Policy | protocolID |
           | ... | description=This is a protocol identity | protocol=http |
           | Identities Add Policy | ldapID |
           | ... | description=This identity required LDAP authentication |
           | ... | auth_method=requires | auth_realm=myLdapRealm |
           | Identities Add Policy | ntlmID |
           | ... | description=This identity required NTLM authentication |
           | ... | auth_method=requires | auth_realm=myNtlmRealm |
           | ... | auth_scheme=Basic or NTLMSSP |
           | Identities Add Policy | advancedID |
           | ... | description=This identity has advanced options |
           | ... | url_categories=${webcats.ADULT}, ${webcats.ARTS} |
           | ... | common_user_agents=ie7 | user_agents=string, with, comma |
           | ... | match_agent=${False} |
        """
        self.identities_add_policy(
            name,
            description=description,
            order=order,
            subnet=subnet,
            protocol=protocol,
            auth_method=auth_method,
            auth_realm=auth_realm,
            auth_scheme=auth_scheme,
            trans_id_fails=trans_id_fails,
            support_guest=support_guest,
            surrogate_type=surrogate_type,
            apply_same_surrogate=apply_same_surrogate,
            proxy_ports=proxy_ports,
            url_categories=url_categories,
            user_agents=user_agents,
            common_user_agents=common_user_agents,
            match_agent=match_agent,
            managed_appliances=managed_appliances,
            user_location=user_location
        )

    def cm77_identities_edit_policy(self,
                                    name,
                                    new_name=None,
                                    description=None,
                                    order=None,
                                    subnet=None,
                                    protocol=None,
                                    auth_method=None,
                                    auth_realm=None,
                                    auth_scheme=None,
                                    trans_id_fails=None,
                                    support_guest=None,
                                    surrogate_type=None,
                                    apply_same_surrogate=None,
                                    proxy_ports=None,
                                    url_categories=None,
                                    user_agents=None,
                                    common_user_agents=None,
                                    match_agent=None,
                                    managed_appliances=None,
                                    user_location=None,
                                    ):
        """Edits existing identity policy from Configuration Master 7.7

        Parameters:
        - `name`: name of identity to be edited.
        - `new_name`: new name for identity.
        - `description`: description for identity.
        - `order`: order of identity.
        - `subnet`: a string of comma separated or a list of subnet where
             identity is member.
        - `protocol`: a list of protocols which identity is a member. Allowed
             values: 'socks', 'http', or 'ftp'. Can be 'all' to set all protocols.
        - `auth_method`: type of authentication for identity.  Either 'no',
             'requires', or 'transparent'.
        - `auth_realm`: name of authentication realm if 'auth_method' above
             is set to 'requires'.
        - `auth_scheme`: authentication scheme for NTLM realm.  Either
             'Basic', 'Basic or NTLMSSP', or 'NTLMSSP'.
        - `trans_id_fails`: action to perform if transparent user
             identification fails.  Either 'support' or
             'enforce'.
        - `support_guest`: specifiy whether to support guest privileges if a
             user fails authentication.  Either True or False.
        - `surrogate_type`: surrogate type for transparent proxy mode.
             Either 'ip', 'persistent', or 'session'.
        - `apply_same_surrogate`: specifiy whether to apply same surrogate
             settings to explicit forward requests.
             Either True or False.
        - `proxy_ports`: a string of comma separated ports in which identity
             is a member.
        - `url_categories`: a string of comma separated pre-defined or
             custom URL categories in which identity is a
             member.
        - `common_user_agents`: a string of comma separated or a list of
             the following common user agents:
             'ie8', 'ie7', 'ie6', 'pre-ie5', 'ie-all',
             'ff3', 'ff2', 'ff1', 'ff-all', 'ms-update',
             'acro-update'
        - `user_agents`: a string of comma separated or a list of
             custom user agents in which identity is a member.
        - `match_agent`: specify whether to match the selected user agent
             definition.  Either True or False.
        - `managed_appliances` - By default policies apply
         to all appliances that use the configuration master. Use that property
         if you want to restrict the policy to a subset of these appliances.
         Accepted values: "all" or a string of comma-separated security
         appliances: "wsa01.wga, wsa02.wga, wsa03.wga"
        - `user_location`: - Define Members by User Location. Accepted values:
        - . local - These users are connected to the network either physically or
         wirelessly.
        - . remote - These users are connected to the network from a remote
         location using VPN (virtual private network). Users might be located
         in a home office, coffee shop, or hotel, for example. The Web Security
         appliance automatically identifies remote users when both the Cisco
         ASA and Cisco AnyConnect Client are used for VPN access. Otherwise,
         the Web Security appliance administrator must specify remote users by
         configuring a range of IP addresses.
        - .both - local and remote
        - . Note. Assigning user_location requires that
         "AnyConnect Secure Mobility" service is enabled


        *Exceptions*
            - `ValueError`: if case of proxy ports, time ranges, subnet
              membership or url categories is disabled in advanced policy menu.
            - `ValueError`: if invalid protocol is provided.
            - `ValueError`: No authentication realm has been configured or invalid
              authentication action.
            - `ValueError`: invalid authentication schemes or invalid action for
              transparent user.

        *Examples*
           | Identities Edit Policy | subnetID | new_name=New Name |
           | ... | subnet=1.2.3.0/24 |
           | Identities Edit policy | subnet | proxy_ports=80, 3128 |
        """
        self.identities_edit_policy(
            name,
            new_name=new_name,
            description=description,
            order=order,
            subnet=subnet,
            protocol=protocol,
            auth_method=auth_method,
            auth_realm=auth_realm,
            auth_scheme=auth_scheme,
            trans_id_fails=trans_id_fails,
            support_guest=support_guest,
            surrogate_type=surrogate_type,
            apply_same_surrogate=apply_same_surrogate,
            proxy_ports=proxy_ports,
            url_categories=url_categories,
            user_agents=user_agents,
            common_user_agents=common_user_agents,
            match_agent=match_agent,
            managed_appliances=managed_appliances,
            user_location=user_location
        )

    def cm77_identities_delete_policy(self, name):
        """Deletes existing identity policy from Configuration Master 7.7

        *Parameters*
        - `name`: name of identity to be deleted.

        *Example*
        | CM77 Identities Delete Policy | myID |
        """
        self.identities_delete_policy(name)

    def cm77_identities_enable_policy(self, name):
        """Enables existing identity policy from Configuration Master 7.7

        *Parameters*
        - `name` name of identity to enable

        *Example*
        | CM77 Identities Disable Policy | myID |
        """

        self.identities_enable_policy(name)

    def cm77_identities_disable_policy(self, name):
        """Disables existing identity policy from Configuration Master 7.7

        *Parameters*
        - `name` name of identity to disable

        *Example*
        | CM77 Identities Disable Policy | myID |
        """

        self.identities_disable_policy(name)

    def cm77_identities_is_enabled_policy(self, name):
        """Returns True if existing policy is enabled or False otherwise.

        *Parameters*
        - `name` policy name to check

        *Examples*
            | ${enabled}= | CM77 Identities Is Enabled Policy | myID |
        """

        return self.identities_is_enabled_policy(name)
