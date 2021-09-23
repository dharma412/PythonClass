#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/gui/manager/identities.py#2 $
# $DateTime: 2020/02/18 22:32:48 $
# $Author: kathirup $

from common.gui.guicommon import GuiCommon
from policybase import PolicyBase

POLICY_LINK_TMPL = "xpath=//a/strong[normalize-space(text())='%s']"
ENABLE_POLICY_CHECKBOX = "xpath=//input[@type='checkbox' and @id='enabled']"
MACHINE_SELECT_ID = 'id=mid_auth_enabled'

class Identities(GuiCommon, PolicyBase):

    """GUI configurator for 'Web Security Manager -> Identification Profiles'.

       *Variable file for URL Categories*

        When configuring an identity, that has URL categories membership, the
        webcats constant can be used to specify input for `url_categories`
        parameter below.  Beside the benefit of less typing, it also prevents
        misspell of longer string input that might cause test to fail.  To use
        this constant, do the followings:

        Import constants.py variable file for usage by specifying it in the
        'Settings' table of test script:
        | *Settings* |  *Value*     |
        | Variables  | constants.py |

        Then reference ${webcats.XXXX} in test case as follow:
        | *Test Case* | *Action* | *Argument* | *Argument* | *Argument* |
        | Example | Identities Add Policy | advancedID | description=This identity has advanced options | url_categories=${webcats.ADULT}, ${webcats.ARTS} |
        | | | common_user_agents=ie7 | user_agents=string, with, comma | match_agent=${False} |

        Full content of webcats constant can be found here:
        http://eng.ironport.com/docs/qa/sarf/keyword/common/webcats.rst
        """

    policy_name_column = 2
    edit_ack_column = 3
    delete_column = 5

    # method required by RF
    # return a list with all public methods
    def get_keyword_names(self):
        return ['identities_add_policy',
                'identities_edit_policy',
                'identities_delete_policy',
                'identities_enable_policy',
                'identities_disable_policy',
                'identities_is_enabled_policy',
                'identities_get_list',
                ]

    def identities_get_list(self):
        """
        Returns: dictionary of identities. Keys are names of identities.
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

        | ${policies}= | Identities Get List |
        | Should Be True | len(${policies}) == 4 |
        | Should Be True | ${policies}.has_key('Global Identification Profile') |
        | Should Be True | ${policies}['Global Identification Profile']['authentication'].find('Exempt') > -1 |
        | Should Be True | len(${policies}['CustomPolicy']) == 3 |
        | Should Be True | ${policies}['CustomPolicy']['end-user_acknowledgement'] == 'Required' |
        """

        self._open_page()
        return self._get_policies()

    def identities_add_policy(self,
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
        ftp_surrogate_type=None,
        socks_surrogate_type=None,
        proxy_ports=None,
        url_categories=None,
        user_agents=None,
        common_user_agents=None,
        match_agent=None,
        managed_appliances=None,
        user_location=None,
        use_machine_id=None,
        machine_ids=None,
        machine_groups=None,
        ise_fallback=None
        ):
        """Adds new identity policy.

        Parameters:
        - `name`: name of identity.
        - `description`: description for identity.
        - `order`: order of identity.
        - `subnet`: a string of comma separated or a list of subnet where
                       identity is member.
        - `protocol`: protocols which identity is a member.  Either 'socks',
                         'http', and/or 'ftp'.
        - `auth_method`: type of authentication for identity:
           . no: No Authentication or Identification,
           . requires: Authenticate Users
           . edir: Identify Users Transparently
           . asa: Identify Users Transparently through Cisco ASA Integration
           . ise: Transparently identify users with ISE

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
                               Either 'ip', 'persistent', 'session' or 'no'.
                               Last option can be used only if Web Proxy set up
                               in forward mode.
        - `apply_same_surrogate`: specifiy whether to apply same surrogate
                                   settings to explicit forward requests.
                                   Either True or False.
         - `ftp_surrogate_type`: surrogate type for transparent proxy mode.
                               Either 'ip' or 'no'.
         - `socks_surrogate_type`: surrogate type for transparent proxy mode.
                               Either 'ip' or 'no'.
        - `proxy_ports`: a string of comma separated ports in which
                            identity is a member.
        - `url_categories`: a string of comma separated pre-defined or
                               custom URL categories in which identity is a
                               member.
        - `use_machine_id`: specify whether to use machine ID for auth or not
                            Either True or False.
        - `machine_ids`: Comma separated machineID Names.
        - `machine_groups`: Comma separated machineGroup Names
        - `common_user_agents`: a string of comma separated or a list of
                                   the following common user agents:
                                   'ie8', 'ie7', 'ie6', 'pre-ie5', 'ie-all',
                                   'ff3', 'ff2', 'ff1', 'ff-all', 'ms-update',
                                   'acro-update'
        - `user_agents`: a string of comma separated or a list of
                            custom user agents in which identity is a member.
        - `match_agent`: specify whether to match the selected user agent
                            definition.  Either True or False.
        - `managed_appliances` - That parameter is used only when the method
         is called from a sma library.
         By default policies apply
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

        Exceptions:
        - ValueError: Invalid protocol selection: "xxx". Valid are:['socks', 'http', 'ftp']
        - ValueError: No authentication realm has been configured.
        - ValueError: Invalid authentication action: xxx.  Valid are: ['no', 'requires', 'edit']
        - ValueError: Invalid authentication schemes: xxx.  Valid are: ['Basic', 'Kerberos', 'Kerberos or NTLMSSP', 'Kerberos or Basic', 'NTLMSSP or Basic', 'NTLMSSP', 'Kerberos or NTLMSSP or Basic']
        - ValueError: Invalid action for transparent user identification failure: xxx.  Valid are:['support', 'enforce']

        Examples:
        | Identities Add Policy | subnetID | description=This is a subnet identity | subnet=1.2.3.0/24 |
        | Identities Add Policy | protocolID | description=This is a protocol identity | protocol=http, socks |
        | Identities Add Policy | ldapID | description=This identity required LDAP authentication | auth_method=requires |
        | | auth_realm=myLdapRealm |
        | Identities Add Policy | ntlmID | description=This identity required NTLM authentication |
        | |  auth_method=requires | auth_realm=myNtlmRealm | auth_scheme=Basic or NTLMSSP |
        | Identities Add Policy | advancedID | description=This identity has advanced options | url_categories=${webcats.ADULT}, ${webcats.ARTS} |
        | |  common_user_agents=ie7 | user_agents=string, with, comma | match_agent=${False} |
        """

        self._open_page()
        self._click_add_policy_button()
        self._fill_policy_page(name, description, order)
        self._set_managed_appliances(managed_appliances)
        if subnet is not None:
            self._fill_subnets(subnet)
        if use_machine_id is not None:
            self._fill_machine_id(use_machine_id, machine_ids, machine_groups)
        if protocol is not None:
            self._select_protocol_membership(protocol)
        if auth_method is not None:
            self._set_auth(auth_method, auth_realm, auth_scheme, trans_id_fails,
                           support_guest, surrogate_type, apply_same_surrogate,
                           ftp_surrogate_type, socks_surrogate_type,ise_fallback)
        if proxy_ports is not None or url_categories is not None or \
            user_agents is not None or common_user_agents is not None:
            self._edit_advanced_settings(proxy_ports, url_categories,
                                 user_agents, common_user_agents, match_agent)
        if user_location is not None:
            self._set_user_location(user_location)

        self._click_submit_button(wait=False)

    def identities_edit_policy(self,
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
        ftp_surrogate_type=None,
        socks_surrogate_type=None,
        proxy_ports=None,
        url_categories=None,
        user_agents=None,
        common_user_agents=None,
        match_agent=None,
        managed_appliances=None,
        user_location=None,
        ise_fallback=None
        ):
        """Edits existing identity policy.

        Parameters:
        - `name`: name of identity to be edited.
        - `new_name`: new name for identity.
        - `description`: description for identity.
        - `order`: order of identity.
        - `subnet`: a string of comma separated or a list of subnet where
                       identity is member.
        - `protocol`: a list of protocols which identity is a member. Allowed
             values: 'socks', 'http', or 'ftp'. Can be 'all' to set all protocols.
        - `auth_method`: type of authentication for identity:
           . no: No Authentication or Identification,
           . requires: Authenticate Users
           . edir: Identify Users Transparently
           . asa: Identify Users Transparently through Cisco ASA Integration
           . ise: Transparently identify users with ISE

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
                               Either 'ip', 'persistent', 'session' or 'no'.
                               Last option can be used only if Web Proxy set up
                               in forward mode.
        - `apply_same_surrogate`: specifiy whether to apply same surrogate
                                   settings to explicit forward requests.
                                   Either True or False.
        - `ftp_surrogate_type`: surrogate type for transparent proxy mode.
                               Either 'ip' or 'no'.
        - `socks_surrogate_type`: surrogate type for transparent proxy mode.
                               Either 'ip' or 'no'.
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
        - `managed_appliances` - That parameter is used only when the method
         is called from a sma library.
         By default policies apply
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

        Exceptions:
        - ValueError: Invalid protocol selection: "xxx". Valid are:['socks', 'http', 'ftp']
        - ValueError: No authentication realm has been configured.
        - ValueError: Invalid authentication action: xxx.  Valid are: ['no', 'requires', 'edit']
        - ValueError: Invalid authentication schemes: xxx.  Valid are: ['Basic', 'Kerberos', 'Kerberos or NTLMSSP', 'Kerberos or Basic', 'NTLMSSP or Basic', 'NTLMSSP', 'Kerberos or NTLMSSP or Basic']
        - ValueError: Invalid action for transparent user identification failure: xxx.  Valid are:['support', 'enforce']

        Example:
        | Identities Edit Policy | subnetID | new_name=New Name | subnet=1.2.3.0/24 |
        """

        self._open_page()
        self._click_edit_policy_link(name, self.policy_name_column)
        if new_name is not None or description is not None or \
            order is not None:
            self._fill_policy_page(new_name, description, order)
        self._set_managed_appliances(managed_appliances)
        if subnet is not None:
            self._fill_subnets(subnet)
        if protocol is not None:
            self._select_protocol_membership(protocol)
        if auth_method is not None:
            self._set_auth(auth_method, auth_realm, auth_scheme, trans_id_fails,
                support_guest, surrogate_type, apply_same_surrogate,
                ftp_surrogate_type, socks_surrogate_type,ise_fallback)
        if proxy_ports is not None or url_categories is not None or \
            user_agents is not None or common_user_agents is not None:
            self._edit_advanced_settings(proxy_ports, url_categories,
                                 user_agents, common_user_agents, match_agent)
        if user_location is not None:
            self._set_user_location(user_location)
        self._click_submit_button(wait=False, accept_confirm_dialog=True)

    def identities_delete_policy(self, name):
        """Deletes existing identity policy.

        Parameters:
        - `name`: name of identity to be deleted.

        Example:
        | Identities Delete Policy | myID |
        """

        self._open_page()
        self._delete_policy(name, self.delete_column)

    def identities_enable_policy(self, name):
        """Enables existing identity policy.

        Parameters:
        - `name` name of identity to enable

        Example:
        | Identities Disable Policy | myID |
        """

        self._open_page()
        self._enable(name)

    def identities_disable_policy(self, name):
        """Disables existing identity policy.

        Parameters:
        - `name` name of identity to disable

        Example:
        | Identities Disable Policy | myID |
        """

        self._open_page()
        self._disable(name)

    def identities_is_enabled_policy(self, name):
        """Returns True if existing policy is enabled or False otherwise.

        Parameters:
        - `name` policy name to check

        Examples:
        | ${enabled}= | Identities Is Enabled Policy | myID |
        """

        self._open_page()
        return self._is_enabled(name)


    def _open_page(self):
        """Go to Identities configuration page."""

        self._navigate_to('Web Security Manager', 'Identification Profiles')

    def _fill_subnets(self, subnet):
        """Interaction with define members by subnet setting."""

        subnet_field = 'members_ip'

        subnet = self._convert_to_tuple(subnet)
        self.input_text(subnet_field, ', '.join(subnet))

    def _fill_machine_id(self,
                         use_machine_id=None,
                         machine_ids=None,
                         machine_groups=None
                         ):
        """Define Members by Machine ID."""
        if use_machine_id:
                self.select_from_list(MACHINE_SELECT_ID,
                'label=Define User Authentication Policy Based on Machine ID')
                if machine_ids is not None:
                    self.click_link('No machine IDs entered')
                    self.input_text('id=members_mid_machines', machine_ids)
                    self._click_done_button()
                if machine_groups is not None:
                    self.click_link('No machine groups entered')
                    for grp in machine_groups.split(','):
                        self.input_text('id=filter_auth_group', grp)
                        self.click_button('id=add_member_button', "don't wait")
                    self._click_done_button()
        else:
            self.select_from_list(MACHINE_SELECT_ID,
                                  'label=Do Not Use Machine ID In This Policy')

    def _check_protocol(self, protocol):
        """Check the protocol"""

        PROTO_LOC = lambda protocol: 'id=protocol_%s' % protocol
        allowed_protocols = ('http', 'ftp', 'socks')

        if not protocol in allowed_protocols:
            raise ValueError('Invalid protocol selection: "%s". Valid are: '
                '%s' % (protocol, allowed_protocols))

        loc = PROTO_LOC(protocol)
        self._info('Checking protocol "%s"' % protocol)
        self._select_checkbox(loc)

    def _uncheck_protocol(self, protocol):
        """Un-Check the protocol"""

        PROTO_LOC = lambda protocol: 'id=protocol_%s' % protocol
        loc = PROTO_LOC(protocol)
        if self._is_element_present(loc):
            self._info('Un-Checking protocol "%s"' % protocol)
            self._unselect_checkbox(loc)


    def _select_protocol_membership(self, protocol):
        """Interaction with define members by protocol setting."""

        allowed_protocols = ('http', 'ftp', 'socks')
        selected_protocols = self._convert_to_tuple(protocol)
        PROTO_LOC = lambda protocol: 'id=protocol_%s' % protocol

        for item in allowed_protocols:
            if item not in selected_protocols:
                self._uncheck_protocol(item)

        for item in selected_protocols:
            if item == 'all':
                self._check_protocol('http')
                self._check_protocol('ftp')
                if self._is_element_present(PROTO_LOC('socks')):
                    self._check_protocol('socks')
            else:
                self._check_protocol(item)

    def _set_auth(self, auth_method, auth_realm, auth_scheme, trans_id_fails,
                  support_guest, surrogate_type, apply_same_surrogate,
                  ftp_surrogate_type, socks_surrogate_type,ise_fallback=None):
        """Interaction with define members by authentication setting."""

        realm_missing_text = ('Define an authentication realm for additional'
                              ' options')
        auth_methods_map = {
            'no': 'No Authentication or Identification',
            'requires': 'Authenticate Users',
            'edir': 'Transparently identify users with authentication realm',
            'asa': 'Identify Users Transparently through Cisco ASA Integration',
            'ise': 'Transparently identify users with ISE',
        }

        ise_fallback_map = {
            'guest': 'Support Guest Privileges',
            'req_auth': 'Require Authentication',
            'block': 'Block Transactions'
        }

        AUTH_METHOD_LABEL = lambda m: auth_methods_map.get(m)
        ISE_FALLBACK_LABEL = lambda m: ise_fallback_map.get(m)

        if self._is_text_present(realm_missing_text):
            raise ValueError('No authentication realm has been configured.')

        if auth_method not in auth_methods_map:
            raise ValueError('Invalid authentication action: %s.  Valid '
                             'are: %s' % \
                             (auth_method, auth_methods_map.keys()))
        self.select_from_list('auth_method',
                              AUTH_METHOD_LABEL(auth_method))
        if auth_method == 'ise':
            if ise_fallback is not None:
                self.select_from_list('id=ise_fallback_mode', ISE_FALLBACK_LABEL(ise_fallback))
        if auth_method != 'no':
            self._set_realm(auth_method, auth_realm, auth_scheme,
                            trans_id_fails, support_guest)
            if surrogate_type is not None or ftp_surrogate_type is not None or \
                socks_surrogate_type is not None:
                self._set_surrogates(surrogate_type, apply_same_surrogate,
                                     ftp_surrogate_type, socks_surrogate_type)

    def _set_realm(self, auth_method, auth_realm, auth_scheme, trans_id_fails,
                   support_guest):
        """Interaction with authentication realm selection."""

        schemes = ('Basic', 'Kerberos', 'Kerberos or NTLMSSP', 'Kerberos or Basic',
            'NTLMSSP or Basic', 'NTLMSSP', 'Kerberos or NTLMSSP or Basic')
        schema_translation_map = { \
            'Basic or NTLMSSP' : 'NTLMSSP or Basic',
        }

        if auth_realm is not None:
            self.select_from_list('id=auth_sequence', auth_realm)
        if auth_scheme:
            if auth_scheme in schema_translation_map.keys():
                auth_scheme = schema_translation_map[auth_scheme]
            elif auth_scheme not in schemes:
                raise ValueError('Invalid authentication schemes: %s.  Valid '
                                 'are: %s' % (auth_scheme, schemes))
            self.select_from_list('id=auth_scheme', 'Use '+ auth_scheme)

        if auth_method == 'edir' and trans_id_fails is not None:
            trans_id_fails_radio_button = \
                {'support':'no_prompt_on_sso_failure_id',
                 'enforce' :'prompt_on_sso_failure_id'}
            if trans_id_fails not in trans_id_fails_radio_button:
                raise ValueError('Invalid action for transparent user '
                    'identification failure: %s.  Valid are: %s' % \
                    (trans_id_fails, trans_id_fails_radio_button.keys()))
            self._click_radio_button(trans_id_fails_radio_button
                                       [trans_id_fails])
        if support_guest is not None:
            self._select_guests_support(support_guest)

    def _edit_advanced_settings(self, proxy_ports, url_categories, user_agents,
                                common_user_agents, match_agent):

        # advanced membership options may be invisible. Make them visible
        if self._is_visible('id=arrow_closed'):
            self.click_element('arrow_closed', "don't wait")

        if proxy_ports is not None:
            self._edit_proxy_ports_membership(proxy_ports)

        if url_categories is not None:
            url_categories = self._convert_to_tuple(url_categories)
            self._edit_url_categories_membership(url_categories)

        edit_user_agents = False
        if user_agents is not None:
            user_agents = self._convert_to_tuple(user_agents)
            edit_user_agents = True
        if common_user_agents is not None:
            common_user_agents = self._convert_to_tuple(common_user_agents)
            edit_user_agents = True
        if edit_user_agents:
            self._edit_user_agents_membership(user_agents, common_user_agents,
                                              match_agent)

    def _set_surrogates(self, surrogate_type, apply_same_surrogate,
                        ftp_surrogate_type, socks_surrogate_type):
        http_surrogates_map = {'ip':'http_auth_surrogate_ip',
                               'persistent':'http_auth_surrogate_persistent',
                               'session':'http_auth_surrogate_session',
                               'no':'http_auth_surrogate_no'}

        ftp_surrogates_map = {'ip':'ftp_auth_surrogate_ip',
                              'no':'ftp_auth_surrogate_no'}

        socks_surrogates_map = {'ip':'socks_auth_surrogate_ip',
                                'no':'socks_auth_surrogate_no'}

        SAME_SURROGATE_LOC = 'use_forward_surrogates_id'

        if surrogate_type is not None:
            self._click_radio_button("xpath=//input[@id='%s']" \
                                 % http_surrogates_map[surrogate_type])

        if apply_same_surrogate is not None:
            if apply_same_surrogate:
                self.select_checkbox(SAME_SURROGATE_LOC)
            else:
                self.unselect_checkbox(SAME_SURROGATE_LOC)
        if ftp_surrogate_type is not None:
            self._click_radio_button("xpath=//input[@id='%s']" \
                                 % ftp_surrogates_map[ftp_surrogate_type])

        if socks_surrogate_type is not None:
            self._click_radio_button("xpath=//input[@id='%s']" \
                                 % socks_surrogates_map[socks_surrogate_type])

    def _select_guests_support(self, guest_priv):
        guests_priv_checkbox = 'guest_priv'

        if guest_priv:
            self.select_checkbox(guests_priv_checkbox)
        else:
            self.unselect_checkbox(guests_priv_checkbox)

    def _set_managed_appliances(self, managed_appliances):
        LINK = 'xpath=//a [ @id="appliances_list_link"]'
        SELECT = 'xpath=//select [ @id="appliance_opt"]'
        ALL_APPLIANCES = 'All appliances'
        SELECTED_APPLIANCES = 'Manually selected appliances'

        if managed_appliances is None: return

        self.click_link(LINK)
        if managed_appliances == 'all':
            self.select_from_list(SELECT, ALL_APPLIANCES)
        else:
            self.select_from_list(SELECT, SELECTED_APPLIANCES)
            self._check_selected_appliances(self._convert_to_tuple(managed_appliances))
        self._click_done_button()

    def _check_selected_appliances(self, managed_appliances):
        CHECKBOX_ALL = 'xpath=//input[@id="identities_appliance_select_all"]'
        CHECKBOX = lambda wsa: 'xpath=//input [@type="checkbox" and @value="%s"]' % wsa

        # Clicking twice unchecks all appliances
        self.click_element(CHECKBOX_ALL, "don't wait")
        self.click_element(CHECKBOX_ALL, "don't wait")

        for appliance in managed_appliances:
            self._info('Checking appliance "%s"' % appliance)
            self.click_element(CHECKBOX(appliance), "don't wait")

    def _set_user_location(self, user_location):
        _map = {
            'local': 'xpath=//input[@id="location_local"]',
            'remote': 'xpath=//input[@id="location_remote"]',
            'both': 'xpath=//input[@id="location_both"]',
            }

        if not user_location in _map.keys():
            raise ValueError('Invalid user_location: "%s". Valid are: '
                '%s' % (user_location, _map.keys()))

        self._click_radio_button(_map[user_location])
