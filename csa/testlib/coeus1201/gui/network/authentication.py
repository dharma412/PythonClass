#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/gui/network/authentication.py#1 $
# $DateTime: 2019/08/14 09:58:47 $
# $Author: uvelayut $

import time
import common.gui.guiexceptions as guiexceptions
from common.gui.guicommon import GuiCommon

service_unavailable_radio_button_dict = {
    'permit': "permit",
    'block': "block"
}

log_guest_radio_button_dict = {
    'ip': "guest_ip_address",
    'user': "guest_user_submitted"
}

protocol_option_dict = {
    'ldap': 'LDAP (Basic Authentication)',
    'ntlm': 'Active Directory (Kerberos, NTLMSSP or Basic Authentication)',
}

persistent_conn_radio_button_dict = {
    'off': "persistent_off",
    'unlimited' : "persistent_unlimited",
    'custom' : "persistent_custom"
}

credential_type_radio_button_dict = {
    'anonymous': "UseBindForSearchAnonymous",
    'bind' : "UseBindForSearchBindDN",
}

group_auth_radio_buttons_dict = {
    'off': "GroupLookup_none",
    'group' : "GroupLookup_GroupObject",
    'user' : "GroupLookup_UserObject"
}

auth_label_dict = {
    'cn': "cn",
    'custom': "Custom",
    'group': "(objectclass=group)",
    'groupofnames': "(objectclass=groupofnames)",
    'groupofuniquenames': "(objectclass=groupofuniquenames)",
    'member': "member",
    'memberof': "memberOf",
    'none': "None",
    'objectclass': "(objectclass=person)",
    'samaccountname': "sAMAccountName",
    'uid': "uid",
    'uniquemember': "uniquemember",
}

REALM_TABLE = "//table[@class=\'cols\'][1]"
SEQUENCE_TABLE = "//table[@class=\'cols\'][2]"
LABEL = lambda name:  "%s" % name
LDAP_SERVER_FIELD = lambda index: "Server[%d][Host]" % index
LDAP_PORT_FIELD = lambda index: "Server[%d][LDAPPort]" % index
NAME_FIELD = lambda table, index: "%s//tr[%s]//td[1]" % (table, index)
PROTOCOL_FIELD = lambda table, index: "%s//tr[%s]//td[2]" % (table, index)
NAME_LINK = lambda table, row, column: \
    "xpath=" + table + "//tr[%s]//td[%s]/a" % (row, column)
DELETE_WIDGET = lambda table, row, column: \
    "xpath=" + table + "//tr[%s]//td[%s]/img" % (row, column)
SEQUENCE_REALM_OPTION = lambda index: "realms[%d][realm]" % index
SEQUENCE_REALM_DELETE_WIDGET = lambda index: \
    "xpath=//tr[@id='realms_row%d']/td[3]/img" % index
SEQUENCE_REALM_KERB_OPTION = lambda index: "negotiate_realms[%d][realm]" % index
SEQUENCE_REALM_KERB_DELETE_WIDGET = lambda index: \
    "xpath=//tr[@id='negotiate_realms_row%d']/td[3]/img" % index

ENTRY_REALMS = lambda table, row, col:\
            '//table[@class=\'cols\'][%d]/tbody/tr[%s]/td[%d]' %\
            (table,str(row), col)
SUBMIT_BTN = 'xpath=//input[@value="Submit"]'
CONFIRM_SUBMIT= 'xpath=//div [@id="confirmation_dialog"]//button[text()="Submit"]'

class Authentication(GuiCommon):

    """GUI configurator for 'Network -> Authentication' page.
    """

    realm_name_column = 1
    protocol_option = "authenticationRealmType"

    # method required by RF
    # return a list with all public methods
    def get_keyword_names(self):
        return ['authentication_add_ldap_realm',
                'authentication_edit_ldap_realm',
                'authentication_edit_ldap_group_authorization',
                'authentication_is_external_ldap_enabled',
                'authentication_add_ntlm_realm',
                'authentication_edit_ntlm_realm',
                'authentication_delete_realm',
                'authentication_test_realm',
                'authentication_join_domain',
                'authentication_add_sequence',
                'authentication_edit_sequence',
                'authentication_delete_sequence',
                'authentication_edit_global_settings',
                'authentication_edit_sequence_all_realms',
                'authentication_get_realms',
                'authentication_get_realm_sequences',
                ]

    def _open_page(self):
        """Go to ' Network -> Authentication' configuration page """

        self._navigate_to("Network", "Authentication")

    def authentication_get_realms(self):
        """ Gets existing authentication realms

        Parameters:
        None

        Return:
         - dictionary of existing authentication realms

        Exception:
        None

        Examples:
        | @{Realms} | Authentication Get Realms |
        """
        self._info('authentication_get_realms')
        self._open_page()

        entries = {}
        num_of_entries = int(self.get_matching_xpath_count(ENTRY_REALMS(1, '*', 1))) + 2
        for row in xrange(2, num_of_entries):
            name = self.get_text(ENTRY_REALMS(1, row, 1))
            protocol = self.get_text(ENTRY_REALMS(1, row, 2))
            schemes = self.get_text(ENTRY_REALMS(1, row, 3))
            servers = self.get_text(ENTRY_REALMS(1, row, 4))
            tui = self.get_text(ENTRY_REALMS(1, row, 5))
            base_dn = self.get_text(ENTRY_REALMS(1, row, 6))
            entries[name] = [protocol, schemes, servers, tui, base_dn]
        return entries

    def authentication_get_realm_sequences(self):
        """ Gets existing realm sequences

        Parameters:
        None

        Return:
         - dictionary of existing realm sequences

        Exception:
        None

        Examples:
        | @{RealmSequences} | Authentication Get Realm Sequences |
        """
        self._info('authentication_get_realm_sequences')
        self._open_page()

        entries = {}
        num_of_entries = int(self.get_matching_xpath_count(ENTRY_REALMS(2, '*', 1))) + 3
        for row in xrange(4, num_of_entries):
            name  = self.get_text(ENTRY_REALMS(2, row, 1))
            order = self.get_text(ENTRY_REALMS(2, row, 2))
            entries[name] = order
        return entries

    def authentication_is_external_ldap_enabled(self, name=None):
        """ Gets status of External LDAP Realm

        Parameters:
        name = LDAP Realm name, if name is None it will check add Realm Option

        Return:
         - Status of the External LDAP query in LDAP Realm.

        None

        Examples:
        | ${status} | Authentication Is External Ldap Enabled |
        """
        self._open_page()
        if name is not None:
            self._click_realm_link(name, self.realm_name_column)
            status = self._is_checked('//input [@id="externalauth_enable"]')
            if status:
                return self._is_visible('//input [@id="account_base"]')
            else:
	        return status
        elif name is None:
            self._click_add_realm_button()
            status = self._is_checked('//input [@id="externalauth_enable"]')
            if status:
                return self._is_visible('//input [@id="account_base"]')
            else:
                return status


    def authentication_add_ldap_realm(self,
        name,
        servers,
        version=None,
        use_ldaps=None,
        source_interface='Management',
        supp_edir=None,
        persist_conn=None,
        cust_persist_conn=None,

        # User / Group Queries
        user_queries_enable=None,
        base_dn=None,
        uname_attr='uid',
        cust_uname_attr=None,
        ufilter_qry=None,
        cust_ufilter_qry=None,
        qry_type=None,
        bind_dn=None,
        bind_pw=None,

        # External Authentication Queries
        ext_queries_enable=None,
        ext_user_base_dn=None,
        ext_user_query=None,
        ext_user_attr=None,
        ext_deny_login=None,
        ext_group_base_dn=None,
        ext_group_query=None,
        ext_mem_name=None,
        ext_group_name=None,

        run_test=False,
    ):

        """ Adds LDAP authentication realm.

        Parameters:
           - `name`: name of realm.
           - `servers`: either a comma separated string or a list of at least
                        1 and up to a maximum of 3 LDAP <server:port>.
           - `version`: LDAP version.  Either '2' or '3'.
           - `use_ldaps`: specify whether to use secure LDAP or not.  Either
                          True or False.
           - `source_interface`:  specify whether Management or P1
           - `supp_edir`: specify whether to support Novell eDirectory or not.
                          Either True or False.
           - `persist_conn`: type of LDAP persistent connections.  Either 'off',
                             'unlimited', or 'custom'.
           - `cust_persist_conn`: number of requests per connection if
                                  'persist_conn' is set to custom.

           User / Group Queries
           This query defines the set of authentication groups which can be
            used in Web Security Manager policies
           - `user_queries_enable`: enable/disable User / Group Queries
            'yes', 'no', or None
           - `base_dn`: base DN to use for LDAP authentication.
           - `uname_attr`: user name attribute.  Either 'cn', 'uid',
                           'samaccountname', or 'custom'.  Defaulted to 'uid'.
           - `cust_uname_attr`: custom string if 'uname_attr' is set to custom.
           - `ufilter_qry`: user filter query.  Either 'none', 'objectclass',
                           or 'custom'.
           - `cust_ufilter_qry`: custom string if 'ufilter_qry' is set to
                                 custom.
           - `qry_type`: type of query credentials.  Either 'anonymous' or
                         'bind'.
           - `bind_dn`: DN to use for bind query.
           - `bind_pw`: password to use for bind query.

           External Authentication Queries
           This query defines the administrative users who can log in to this
            appliance
           - `ext_queries_enable`: enable/disable External Authentication Queries
            'yes', 'no', or None
           - `ext_user_base_dn`: Base DN for User Authentication
           - `ext_user_query`: Query String for User Authentication
           - `ext_user_attr`: Attribute containing user's full name
           - `ext_deny_login`: Deny login to expired accounts based on RFC 2307
            account expiration LDAP attributes; 'yes', 'no', or None

           This query defines the the set of groups associated with
           administrative users. The mapping of LDAP groups to appliance user
           roles is set using
            System Administration > Users > External Authentication
           - `ext_group_base_dn`: Base DN for Group Membership
           - `ext_group_query`: Query String to determine if a user is a
            member of a group
           - `ext_mem_name`: Attribute n these records that holds each
            member's username
           - `ext_group_name`: Attribute in these records that contains the
            group name

           - `run_test`: specify whether or not to run test during
                         configuration of realm.  Either True or False.
                         Defaulted to False. If run_test is True, we can return
                         the output of the start test.

        Examples:
        | Authentication Add LDAP Realm | myLdapRealm | ldap1.wga | version=2 |
        | | base_dn=ou=automation,dc=qa |
        | Authentication Add LDAP Realm | myLdapRealm | ldap1.wga | base_dn=ou=automation,dc=qa |
        | | uname_attr=custom | cust_uname_attr=foo | ufilter_qry=custom |
        | | cust_ufilter_qry=bar |
        | Authentication Add LDAP Realm | myLdapRealm | ldap1.wga, ldap2.wga:394, ldap3.wga:636 | use_ldaps=${True} |
        | | supp_edir=${True} | persist_conn=off | ldap_base_dn=ou=automation,dc=qa |
        | @{servers} | Set Variable | ldap1.wga | ldap2.wga:394 |
        | | ldap3.wga:636 |
        | Authentication Add LDAP Realm | myLdapRealm | @{servers} | persist_conn=custom |
        | | cust_persist_conn=15 | base_dn=ou=automation,dc=qa | qry_type=bind |
        | | bind_dn=cn=ldapuser,ou=automation,dc=qa | bind_pw=ironport | run_test=${True} |
        ${out}   Authentication Add LDAP Realm  ldap_ext
        ...     ${LDAP_AUTH_SERVER}
        ...     persist_conn=custom
        ...     cust_persist_conn=10
        ...     user_queries_enable=yes
        ...     base_dn=${LDAP_BASE_DN}
        ...     uname_attr=${USER_NAME_ATTR}
        ...     qry_type=bind
        ...     bind_dn=${LDAP_BIND_BASE_DN}
        ...     bind_pw=${LDAP_BIND_BASE_PW}
        ...     ext_queries_enable=yes
        ...     ext_user_base_dn=c=a
        ...     ext_user_query=(&(objectClass=user)(sAMAccountName={u}))
        ...     ext_user_attr=sss
        ...     ext_deny_login=yes
        ...     ext_group_base_dn=a=a
        ...     ext_group_query=(&(objectClass=user)(sAMAccountName={u}))
        ...     ext_mem_name=sdf
        ...     ext_group_name=ert
        ...     run_test=${True}
        """

        self._open_page()
        self._click_add_realm_button()
        self._fill_in_name(name)
        self._select_auth_protocol('ldap')
        servers = self._convert_to_tuple(servers)
        self._check_for_number_of_server(servers)

        self._fill_in_ldap_version(version, use_ldaps, supp_edir)
        self._fill_in_ldap_servers(servers, source_interface)
        self._fill_in_ldap_advanced(persist_conn, cust_persist_conn)
        self._fill_in_user_queries(
            user_queries_enable,
            base_dn,
            uname_attr,
            cust_uname_attr,
            ufilter_qry,
            cust_ufilter_qry,
            qry_type,
            bind_dn,
            bind_pw,
        )
        self._fill_in_external_queries(
            ext_queries_enable,
            ext_user_base_dn,
            ext_user_query,
            ext_user_attr,
            ext_deny_login,
            ext_group_base_dn,
            ext_group_query,
            ext_mem_name,
            ext_group_name,
        )

        if run_test:
            test_result = self._test('LDAP')

        self._click_submit_button(skip_wait_for_title=True)

        if run_test:
            return test_result

    def authentication_edit_ldap_realm(self,
        name,
        new_name=None,
        servers=None,
        version=None,
        use_ldaps=None,
        source_interface='Management',
        supp_edir=None,
        persist_conn=None,
        cust_persist_conn=None,

        # User / Group Queries
        user_queries_enable=None,
        base_dn=None,
        uname_attr=None,
        cust_uname_attr=None,
        ufilter_qry=None,
        cust_ufilter_qry=None,
        qry_type=None,
        bind_dn=None,
        bind_pw=None,

        # External Authentication Queries
        ext_queries_enable=None,
        ext_user_base_dn=None,
        ext_user_query=None,
        ext_user_attr=None,
        ext_deny_login=None,
        ext_group_base_dn=None,
        ext_group_query=None,
        ext_mem_name=None,
        ext_group_name=None,

        run_test=False,
        ):

        """ Edits existing LDAP authentication realm.

        Parameters:
           - `name`: name of LDAP realm to be edited.
           - `new_name` : edit old name to this new name.
           - `servers`: either a comma separated string or a list of at least
                        1 and up to a maximum of 3 LDAP <server:port>.  If
                        defined, all existing <server:port> will be replaced.
           - `version`: LDAP version.  Either '2' or '3'.
           - `use_ldaps`: specify whether to use secure LDAP or not.  Either
                          True or False.
           - `source_interface`:  specify whether Management or P1
           - `supp_edir`: specify whether to support Novell eDirectory or not.
                          Either True or False.
           - `persist_conn`: type of LDAP persistent connections.  Either 'off',
                             'unlimited', or 'custom'.
           - `cust_persist_conn`: number of requests per connection if
                                  'persist_conn' is set to custom.

           User / Group Queries
           This query defines the set of authentication groups which can be
            used in Web Security Manager policies
           - `user_queries_enable`: enable/disable User / Group Queries
            'yes', 'no', or None
           - `base_dn`: base DN to use for LDAP authentication.
           - `uname_attr`: user name attribute.  Either 'cn', 'uid',
                           'samaccountname', or 'custom'.  Defaulted to 'uid'.
           - `cust_uname_attr`: custom string if 'uname_attr' is set to custom.
           - `ufilter_qry`: user filter query.  Either 'none', 'objectclass',
                           or 'custom'.
           - `cust_ufilter_qry`: custom string if 'ufilter_qry' is set to
                                 custom.
           - `qry_type`: type of query credentials.  Either 'anonymous' or
                         'bind'.
           - `bind_dn`: DN to use for bind query.
           - `bind_pw`: password to use for bind query.

           External Authentication Queries
           This query defines the administrative users who can log in to this
            appliance
           - `ext_queries_enable`: enable/disable External Authentication Queries
            'yes', 'no', or None
           - `ext_user_base_dn`: Base DN for User Authentication
           - `ext_user_query`: Query String for User Authentication
           - `ext_user_attr`: Attribute containing user's full name
           - `ext_deny_login`: Deny login to expired accounts based on RFC 2307
            account expiration LDAP attributes; 'yes', 'no', or None

           This query defines the the set of groups associated with
           administrative users. The mapping of LDAP groups to appliance user
           roles is set using
            System Administration > Users > External Authentication
           - `ext_group_base_dn`: Base DN for Group Membership
           - `ext_group_query`: Query String to determine if a user is a
            member of a group
           - `ext_mem_name`: Attribute n these records that holds each
            member's username
           - `ext_group_name`: Attribute in these records that contains the
            group name

           - `run_test`: specify whether or not to run test during
                         configuration of realm.  Either True or False.
                         Defaulted to False.

        Examples:
        | Authentication Edit LDAP Realm | myLdapRealm | servers=ldap1.wga, ldap2.wga:555 | version=2 |
        | | persist_conn=custom | cust_persist_conn=15 |  qry_type=bind |
        | | bind_dn=cn=ldapuser,ou=automation,dc=qa | bind_pw=ironport | run_test=${True} |
        | Authentication Edit LDAP Realm | myLdapRealm | new_name=myNewLdapRealm | base_dn=ou=new,dc=qa |
        | | uname_attr=custom | cust_uname_attr=foo | ufilter_qry=custom |
        | | cust_ufilter_qry=bar |
        | Authentication Edit LDAP Realm | myLdapRealm | servers=ldap3.wga, ldap2.wga:394, ldap1.wga:636 | use_ldaps=${True} |
        | | supp_edir=${True} | persist_conn=off | ldap_base_dn=ou=automation,dc=qa |
        | @{servers} | Set Variable | ldap2.wga:394 | ldap3.wga:636 |
        | Authentication Edit LDAP Realm | myLdapRealm | servers=@{servers} | qry_type=anonymous |
        Authentication Edit LDAP Realm  ldap_ext
        ...    new_name=ldap_ext_new
        ...    servers=iaf-ad1.wga, openldap.qa:389, qa37.qa:789
        ...    persist_conn=custom
        ...    cust_persist_conn=11
        ...    user_queries_enable=yes
        ...    base_dn=${LDAP_BASE_DN}
        ...    uname_attr=${USER_NAME_ATTR}
        ...    qry_type=bind
        ...    bind_dn=${LDAP_BIND_BASE_DN}
        ...    bind_pw=${LDAP_BIND_BASE_PW}
        ...    ext_queries_enable=yes
        ...    ext_user_base_dn=c=aaaa
        ...    ext_user_query=(&(objectClass=user)(sAMAccountName={u}))
        ...    ext_user_attr=sss2
        ...    ext_deny_login=no
        ...    ext_group_base_dn=a=a2
        ...    ext_group_query=(&(objectClass=user)(sAMAccountName={u}))
        ...    ext_mem_name=sdf2
        ...    ext_group_name=ert2
        ...    run_test=${False}
        """

        self._open_page()
        self._click_realm_link(name, self.realm_name_column)
        protocol = self.get_value(self.protocol_option)
        self._info('protocol=' + str(protocol))
        self._edit_old_name(new_name)
        if servers is not None:
            if isinstance(servers, (str, unicode)):
                servers = [server.strip() for server in servers.split(',')]
            self._check_for_number_of_server(servers)
            for i in range(3 - len(servers)):
                servers.append(':')
            servers = self._convert_to_tuple(servers)
        self._fill_in_ldap_version(version, use_ldaps, supp_edir)
        self._fill_in_ldap_servers(servers, source_interface)
        self._fill_in_ldap_advanced(persist_conn, cust_persist_conn)
        self._fill_in_user_queries(
            user_queries_enable,
            base_dn,
            uname_attr,
            cust_uname_attr,
            ufilter_qry,
            cust_ufilter_qry,
            qry_type,
            bind_dn,
            bind_pw,
        )
        self._fill_in_external_queries(
            ext_queries_enable,
            ext_user_base_dn,
            ext_user_query,
            ext_user_attr,
            ext_deny_login,
            ext_group_base_dn,
            ext_group_query,
            ext_mem_name,
            ext_group_name,
        )

        if run_test:
            self._test('LDAP')
        self._click_submit_button(skip_wait_for_title=True)

    def authentication_edit_ldap_group_authorization(self,
                                                     name,
                                                     type=None,
                                                     membership_attr=None,
                                                     membership_attr_str=None,
                                                     membership_attr_dn=None,
                                                     grp_name_attr=None,
                                                     grp_name_attr_str=None,
                                                     qry_string=None,
                                                     qry_string_str=None):

        """ Edits LDAP group authorization.

        Parameters:
           - `type`: type of group authorization.  Either 'off', 'group', or
                     'user'.
           - `membership_attr`: group membership attribute.  Either 'member',
                                'memberof', 'uniquemember', or 'custom'.
           - `membership_attr_str`: custom string if group membership attribute
                                    is set to 'custom'.
           - `membership_attr_dn`: specify if group membership attribute is a
                                   DN.  Either True or False.
           - `grp_name_attr`: attribute that contains the group name.  Either
                              'cn' or 'custom'.
           - `grp_name_attr_str`: custom string if attribute that contains the
                                  group name is set to 'custom'.
           - `qry_string`: query string to determine if object is a group.
                           Either 'groupofnames', 'groupofuniquenames',
                           'group' or 'custom'.
           - `qry_string_str`: custom string if query string to determine if
                               object is a group is set to 'custom'.

        Examples:
        | Authentication Edit LDAP Group Authorization | myLdapRealm | type=off |
        | Authentication Edit LDAP Group Authorization | myLdapRealm | type=group | membership_attr=custom |
        | | membership_attr_str=foo | grp_name_attr=custom | grp_name_attr_str=bar | qry_string=custom |
        | | qry_string_str=whatever |
        | Authentication Edit LDAP Group Authorization | myLdapRealm | type=user | membership_attr=custom |
        | | membership_attr_str=foo | membership_attr_dn=${True} | grp_name_attr=custom | grp_name_attr_str=bar |
        | | qry_string=custom | qry_string_str=whatever |
        | Authentication Edit LDAP Group Authorization | myLdapRealm | type=user | membership_attr=custom |
        | | membership_attr_str=foo | membership_attr_dn=${False} |
        """

        self._open_page()
        self._click_realm_link(name, self.realm_name_column)
        protocol = self.get_value(self.protocol_option)
        self._info("protocol=%s" % (protocol,))
        self._fill_in_group_auth(type, membership_attr, membership_attr_str,
            membership_attr_dn, grp_name_attr, grp_name_attr_str,
            qry_string, qry_string_str)
        self._click_submit_button(skip_wait_for_title=True)

    def authentication_add_ntlm_realm(self,
        name,
        servers,
        domain,
        source_interface='Management',
        net_domain=None,
        join_domain=True,
        domain_user=None,
        domain_pw=None,
        client_signing=None,
        enable_transparent=None,
        primary_ad_server=None,
        primary_ad_secret=None,
        backup_ad_server=None,
        backup_ad_secret=None,
        enable_client_signing_required=None,
        enable_keytab_authentication=None,
        kerberos_ha_user=None,
        kerberos_ha_pw=None,
	    location=None,
        run_test=False):

        """ Adds NTLM authentication realm.

        Parameters:
           - `name`: name of realm.
           - `source_interface`:  specify whether Management or P1
           - `servers`: either a comma separated string or a list of at least
                        1 and up to a maximum of 3 AD servers.
           - `domain`: domain of AD server.
           - `net_domain`: NetBIOS domain of AD server.
           - `join_domain`: specify whether or not to join domain during
                            configuration of new NTLM realm.  Either True or
                            False.  Defaulted to True.
           - `domain_user`: user uses to join AD domain.
           - `domain_pw`: password uses to join AD domain.
           - `client_signing`: specify whether client signing is required.
                               Either True or False.
           - `enable_transparent`: Enable Transparent User Identification using
              Active Directory Agent
              accepted values: True - enable, False - disable, None - do not change
           - `primary_ad_server`: Primary Active Directory Agent Server.
              Required if Transparent User Identification is enabled.
              Should be None if Transparent User Identification is disabled.
           - `primary_ad_secret`: Primary Active Directory Agent Shared Secret.
              Required if Transparent User Identification is enabled.
              Should be None if Transparent User Identification is disabled.
           - `backup_ad_server`: Backup Active Directory Agent Server(Optional).
              Should be None if Transparent User Identification is disabled.
           - `backup_ad_secret`:Backup Active Directory Agent Shared Secret.
           - `enable_client_signing_required`: Client Signing Required
              accepted values: True - enable, False - disable, None - do not change
           - `enable_keytab_authentication`: Use keytab authentication
              accepted values: True - enable, False - disable, None - do not change
           - `kerberos_ha_user`: Kerberos High Availability Username.
              Required if Keytab authentication is enabled.
              Should be None if Keytab authentication is disabled.
           - `kerberos_ha_pw`: Kerberos High Availability Password.
              Required if Keytab authentication is enabled.
              Should be None if Keytab authentication is disabled.
           - `run_test`: specify whether or not to run test during
                         configuration of realm.  Either True or False.
                         Defaulted to False.

        Examples:
        | Authentication Add NTLM Realm | myNtlmRealm | ad.wga | MY_DOMAIN |
        | | domain_user=admin | domain_pw=ironport | run_test=${True} |
        | Authentication Add NTLM Realm | myNtlmRealm | ad1.wga, ad2.wga, ad3.wga | MY_DOMAIN |
        | | net_domain=MY_NET_DOMAIN | domain_user=admin | domain_pw=ironport | client_signing={True} |
        | @{servers} | Set Variable | ad1.wga | ad3.wga |
        | Authentication Add NTLM Realm | myNtlmRealm | @{servers} | MY_DOMAIN |
        | | join_domain=${False} | client_signing={True} |
        | Authentication Add NTLM Realm | myNtlmRealm | @{servers} | MY_DOMAIN |
        | | location=Servers | join_domain=${True} | domain_user=admin | domain_pw=ironport |
        """

        self._open_page()
        self._click_add_realm_button()
        self._fill_in_name(name)
        self._select_auth_protocol('ntlm')
        servers = self._convert_to_tuple(servers)
        self._check_for_number_of_server(servers, type='AD')
        self._fill_in_ntlm_realm(
            source_interface, servers, domain, net_domain, join_domain,
            domain_user, domain_pw, client_signing,
            enable_transparent,
            primary_ad_server,
            primary_ad_secret,
            backup_ad_server,
            backup_ad_secret,
            enable_client_signing_required,
            run_test,
	        location,
            enable_keytab_authentication,
            kerberos_ha_user,
            kerberos_ha_pw)

    def authentication_edit_ntlm_realm(self,
        name,
        new_name=None,
        source_interface='Management',
        servers=None,
        domain=None,
        net_domain=None,
        join_domain=False,
        domain_user=None,
        domain_pw=None,
        client_signing=None,
        enable_transparent=None,
        primary_ad_server=None,
        primary_ad_secret=None,
        backup_ad_server=None,
        backup_ad_secret=None,
        enable_client_signing_required=None,
        run_test=False,
        location=None):

        """ Edits existing NTLM authentication realm.

        Parameters:
           - `name`: name of realm.
           - `new_name` : edit old name to this new name.
           - `source_interface`:  specify whether Management or P1
           - `servers`: either a comma separated string or a list of at least
                        1 and up to a maximum of 3 AD servers.  If defined,
                        all existing servers will be replaced.
           - `domain`: domain of AD server.
           - `net_domain`: NetBIOS domain of AD server.
           - `join_domain`: specify whether or not to join domain during
                            configuration of new NTLM realm.  Either True or
                            False.  Defaulted to True.
           - `domain_user`: user uses to join AD domain.
           - `domain_pw`: password uses to join AD domain.
           - `client_signing`: specify whether client signing is required.
                               Either True or False.
           - `enable_transparent`: Enable Transparent User Identification using
              Active Directory Agent
              accepted values: True - enable, False - disable, None - do not change
           - `primary_ad_server`: Primary Active Directory Agent Server.
              Required if Transparent User Identification is enabled.
              Should be None if Transparent User Identification is disabled.
           - `primary_ad_secret`: Primary Active Directory Agent Shared Secret.
              Required if Transparent User Identification is enabled.
              Should be None if Transparent User Identification is disabled.
           - `backup_ad_server`: Backup Active Directory Agent Server(Optional).
              Should be None if Transparent User Identification is disabled.
           - `backup_ad_secret`:Backup Active Directory Agent Shared Secret.
           - `enable_client_signing_required`: Client Signing Required
              accepted values: True - enable, False - disable, None - do not change
           - `run_test`: specify whether or not to run test during
                         configuration of realm.  Either True or False.
                         Defaulted to False.

        Examples:
        | Authentication Edit NTLM Realm | myNtlmRealm | new_name=myNewNtlmRealm | domain=MY_DOMAIN |
        | | domain_user=admin | domain_pw=ironport | run_test=${True} |
        | Authentication Edit NTLM Realm | myNtlmRealm | server=ad2.wga, ad3.wga | domain=MY_DOMAIN |
        | | net_domain=MY_NET_DOMAIN | join_domain=${False} | client_signing={True} |
        | @{servers} | Set Variable | ad1.wga | ad3.wga |
        | | ad4.wga  |
        | Authentication Edit NTLM Realm | myNtlmRealm | server=@{servers} | domain=MY_DOMAIN |
        | | domain_user=admin | domain_pw=ironport | run_test={True} |
        | Authentication Edit NTLM Realm | myNtlmRealm | server=ad2.wga, ad3.wga | domain=MY_DOMAIN |
        | | location=Servers | join_domain=${True} | domain_user=admin | domain_pw=ironport |
        """

        self._open_page()
        self._click_realm_link(name, self.realm_name_column)
        protocol = self.get_value(self.protocol_option)
        self._info('protocol=' + str(protocol))
        self._edit_old_name(new_name)
        if servers is not None:
            if isinstance(servers, (str, unicode)):
                servers = [server.strip() for server in servers.split(',')]
            self._check_for_number_of_server(servers, type='NTLM')
            for i in range(3 - len(servers)):
                servers.append('')
            servers = self._convert_to_tuple(servers)
        self._fill_in_ntlm_realm(
            source_interface, servers, domain, net_domain, join_domain,
            domain_user, domain_pw, client_signing,
            enable_transparent,
            primary_ad_server,
            primary_ad_secret,
            backup_ad_server,
            backup_ad_secret,
            enable_client_signing_required,
            run_test,
            location)

    def authentication_join_domain(self, name, user, password):
        """ Perform join domain of the specified NTLM realm.

        Parameters:
           - `name`: name of existing NTLM realm to perform join domain.
           - `user` : user name to join domain.
           - `password`: password to join domain.

        Example:
        | Authentication Join Domain | myNtlmRealm | admin | ironport |
        """

        self._open_page()
        if self._get_realm_protocol(name) != 'Active Directory':
            raise guiexceptions.ConfigError, '"%s" realm is not an ' \
                'Active Directory realm' % name
        self._click_realm_link(name, self.realm_name_column)
        self._join_domain(user, password)
        self._click_submit_button(skip_wait_for_title=True)

    def authentication_test_realm(self, name):
        """ Tests the specified authentication realm.

        Parameters:
           - `name`: name of existing authentication realm to perform test.

        Examples:
        | Authentication Test Realm | myNtlmRealm |
        | Authentication Test Realm | myLdapRealm |
        """

        self._open_page()
        protocol = self._get_realm_protocol(name).upper()
        self._click_realm_link(name, self.realm_name_column)
        return self._test(protocol)

    def authentication_delete_realm(self, name):
        """ Deletes the specified authentication realm.

        Parameters:
           - `name`: name of existing authentication realm to be deleted.

        Examples:
        | Authentication Delete Realm | myLdapRealm |
        | Authentication Delete Realm | myNtlmRealm |
        """

        # column of the realm table where the trash can image is showing
        delete_column = 7
        self._open_page()
        self._delete_realm(name, delete_column)

    def authentication_add_sequence(self, name,
        realms=None,
        realm_ntlmssp=None,
        realms_kerb=None,
        ):

        """ Adds new realm sequence.

        Parameters:
        - `name`: name of realm sequence.
        - `realms`: Realm Sequence for Basic Scheme - string of comma-separated
         strings. If the client provides Basic credentials, multiple realms
         which support Basic authentication will be queried in the order
         they appear in the Authentication Realm Sequence.
        - `realm_ntlmssp`: Realm for NTLMSSP Scheme. If the client provides
         NTLMSSP credentials, and if an NTLMSSP realm is specified below,
         the NTLM realm will be queried instead of Basic Scheme
        - `realms_kerb`: If the client provides Kerberos credentials,
         multiple realms which support Kerberos authentication will be queried
         in the order they appear in the Authentication Realm Sequence.
         Generally, the client will choose the authentication scheme.
         If desired, the Identity configuration can specify that only
         specific schemes will be requested for clients on a particular subnet.

        Examples:
        | Authentication Add Sequence | mySequence1 | realm_ntlmssp=ntlmRealm1 |
        | Authentication Add Sequence | mySequence2 | realms=ldapRealm2 |
        | Authentication Add Sequence | mySequence3 | realms_kerb=kerb1 |
        | Authentication Add Sequence | mySequence4 | realm_ntlmssp=ntlmRealm1 |
        | ... | realms=ldapRealm2, another_realm |
        | ... | realms_kerb=kerb1, bogus_realm |
        """

        realms = self._convert_to_tuple(realms)
        self._check_uniquness_of_realms(realms)
        realms_kerb = self._convert_to_tuple(realms_kerb)
        self._check_uniquness_of_realms(realms_kerb)

        self._open_page()
        self._check_realms_existence(realms)
        self._click_add_sequence_button()
        self._fill_in_name(name)
        self._put_realm_kerb_in_order(realms_kerb)
        self._put_realm_in_order(realms)
        self._set_ntlmssl_realm(realm_ntlmssp)
        self._click_submit_button(skip_wait_for_title=True)

    def authentication_edit_sequence(self,
        name,
        new_name=None,
        realms=None,
        realm_ntlmssp=None,
        ):

        """ Edits existing realm sequence.

        Parameters:
           - `name`: name of existing realm sequence to be edited.
           - `new_name` : edit old name to this new name.
           - `realms`: Realm Sequence for Basic Scheme - string of comma-separated
             strings. If the client provides Basic credentials, multiple realms
             which support Basic authentication will be queried in the order
             they appear in the Authentication Realm Sequence.
           - `realm_ntlmssp`: Realm for NTLMSSP Scheme. If the client provides
            NTLMSSP credentials, and if an NTLMSSP realm is specified below,
            the NTLM realm will be queried instead of Basic Scheme

        Examples:
        | Authentication Edit Sequence | mySequence | realms=ntlmRealm, ldapRealm, ldapRealm2 |
        | @{realm_seq} | Set Variable | ldapRealm1 | ntlmRealm |
        | Authentication Edit Sequence | mySequence | new_name=myNewSequence | realms=@{realm_seq} |
        | Authentication Edit Sequence | All Realms | realms=ldapRealm, ntlmRealm |

        """
        realms = self._convert_to_tuple(realms)
        self._check_uniquness_of_realms(realms)

        self._open_page()
        if realms is not None:
            self._check_realms_existence(realms)
        self._click_sequence_link(name, self.realm_name_column)
        if name == 'All Realms':
            self._edit_all_realms_sequence(realms)
        else:
            self._edit_old_name(new_name)
            self._edit_sequence(realms)
        self._set_ntlmssl_realm(realm_ntlmssp)
        self._click_submit_button(skip_wait_for_title=True)

    def authentication_delete_sequence(self, name):
        """ Deletes the specified sequence.

        Parameters:
           - `name`: name of the sequence to be deleted.

        Example:
        | Authentication Delete Sequence | mySequence |
        """

        # column of the sequence table where the trash can image is showing
        delete_column = 3

        if name == 'All Realms':
            raise guiexceptions.GuiValueError, 'Deletion of "%s" sequence is ' \
                'not allowed'  % (name,)
        self._open_page()
        self._delete_sequence(name, delete_column)

    def authentication_edit_global_settings(self,
                             service_unavailable_action=None,
                             log_guest_user_by=None,
                             enable_reauth=None,
                             token_ttl=None,
                             use_encrypted_https=None,
                             https_redirect_port=None,
                             redirect_hostname=None,
                             surrogate_timeout=None,
                             idle_timeout=None,
                             cache_size=None,
                             session_restriction=None,
                             restriction_timeout=None,
                             cert_file=None,
                             key_file=None,
                             key_is_encrypted=None,
                             key_password=None,
                             ):

        """ Edits global authentication settings.

        Parameters:
           - `service_unavailable_action`: action if authentication service
                                           unavailable.  Either 'permit' or
                                           'block'.
           - `log_guest_user_by` : if failed authentication handling,
                                   log guest user by.  Either 'ip' or 'user'.
           - `enable_reauth` : enable re-authentication prompt if end user
                               blocked by URL category.  Either True or False.
           - `token_ttl` : basic authentication token TTL.
           - `use_encrypted_https` : use encrypted HTTPS connection for
                                     authentication.  Either True or False.
           - `https_redirect_port` : HTTPS redirect port.
           - `redirect_hostname` : redirect hostname.
           - `surrogate_timeout` : surrogate timeout.
           - `idle_timeout` : client IP idle timeout.
           - `cache_size` : number of entries for cache size.
           - `session_restriction` : prohibit an authenticated user from
                                     accessing the Internet from a different
                                     IP address.  Either True or False.
           - `restriction_timeout` : user session restrictions timeout.
           - `cert_file` : location of certificate file to upload.
           - `key_file` : location of key file to upload.
           - `key_is_encrypted`: Either 'True' or 'False'
           - `key_password`: password for encrypted key
        Examples:
        | Authentication Edit Global Settings | service_unavailable_action=permit | log_guest_user_by=user | enable_reauth=${True} |
        | | token_ttl=3601 | use_encrypted_https=${True} | https_redirect_port=444 |
        | | redirect_hostname=foo.bar | surrogate_timeout=3601 | idle_timeout=3601 |
        | | cache_size=8193 | session_restriction=${True} | restriction_timeout=3602 |
        | ${test_data_dir} | Set Variable | tests/coeus75/unittests/testdata |
        | Authentication Edit Global Settings | enable_reauth=${False} | use_encrypted_https=${False} | session_restriction=${False} |
        | | cert_file=%{SARF_HOME}/${test_data_dir}/auth.cert | key_file=%{SARF_HOME}/${test_data_dir}/auth.key |
        | ... | key_is_encrypted=${True} |
        | ... | key_password=Secret |
        """

        enable_re_auth_check_box = "reAuthOnRequestDenied"
        token_ttl_field = "authenticateTtl"
        https_redirect_port_field = "authRedirectPort"
        redirect_hostname_field = "transparentAuthServer"
        surrogate_timeout_field = "authTimeout"
        idle_timeout_field = "clientIpIdleTimeout"
        cache_size_field = "maxAuthCacheEntries"
        session_restriction_check_box = "preventMultipleLogin"
        restriction_timeout_field = "associationInactivityTimeout"
        certificate_location_field = "uploadCertificate"
        key_location_field = "uploadKey"
        upload_files_button = "uploadFiles"
        advanced_link_open = "arrow_open"
        advanced_link_close = "arrow_closed"

        self._open_page()
        self._click_edit_global_settings_button()
        if service_unavailable_action is not None:
            self._click_radio_button(service_unavailable_radio_button_dict
                                     [service_unavailable_action.lower()])
        if log_guest_user_by is not None:
            self._click_radio_button(log_guest_radio_button_dict
                                     [log_guest_user_by.lower()])
        if enable_reauth is not None:
            if enable_reauth:
                self.select_checkbox(enable_re_auth_check_box)
            else:
                self.unselect_checkbox(enable_re_auth_check_box)
        if token_ttl is not None:
            self.input_text(token_ttl_field, token_ttl)
        use_encrypted_https = self._set_credential_encryption(use_encrypted_https)
        if use_encrypted_https and https_redirect_port is not None:
            self.input_text(https_redirect_port_field, https_redirect_port)
        if redirect_hostname is not None:
            self.input_text(redirect_hostname_field, redirect_hostname)
        if surrogate_timeout is not None:
            self.input_text(surrogate_timeout_field, surrogate_timeout)
        if idle_timeout is not None:
            self.input_text(idle_timeout_field, idle_timeout)
        if cache_size is not None:
            self.input_text(cache_size_field, cache_size)
        if session_restriction is not None:
            if session_restriction and not \
                self._is_checked(session_restriction_check_box):
                self.click_element(session_restriction_check_box, "don't wait")
            elif not session_restriction and \
                    self._is_checked(session_restriction_check_box):
                self.click_element(session_restriction_check_box, "dont't wait")
        if restriction_timeout is not None and session_restriction:
            self.input_text(restriction_timeout_field, restriction_timeout)
        if cert_file is not None and key_file is not None:
            if not self._is_visible(advanced_link_open):
                self.click_element(advanced_link_close, "don't wait")
            self.choose_file(certificate_location_field, cert_file)
            self.choose_file(key_location_field, key_file)
            self._set_key_is_encrypted(key_is_encrypted)
            self._set_key_password(key_password)
            self.click_button(upload_files_button)
            result = self.check_for_warning()
            self._check_action_result()
        else:
            result = ''
        if use_encrypted_https:
            self._click_submit_button(wait=False, skip_wait_for_title=True)
            if self._is_element_present("xpath=//button[@type='button']"):
                self._click_continue_button()
        else:
            self._click_submit_button(skip_wait_for_title=True)
        return result

    def _set_credential_encryption(self, encryption):
        CHECKBOX = 'xpath=//input [@id="useSecureClientAuth"]'

        is_checked = self._is_checked(CHECKBOX)
        if encryption is None:
            encryption = is_checked
        else:
            if encryption != is_checked:
                self.click_element(CHECKBOX, "don't wait")
        self._debug('encryption' + str(encryption))
        return encryption

    def authentication_edit_sequence_all_realms(self,
        realms  = None,
        realm_ntlmssp = None,
        ):
        """ Edits all realms' sequence.

        Parameters:
           - `realms`: string of comma separated values of realms.
           If the client provides Basic credentials, multiple realms which
           support Basic authentication will be queried in the order they
           are specified here.
           - `realm_ntlmssp` - NTLMSSP realm. If the client provides
            NTLMSSP credentials, and if that parameter is specified here,
            realm_ntlmssp will be queried instead of basic scheme

        Exceptions:
        - ConfigError: realm xxx specified in realms is not defined
        - ConfigError: realm xxx specified in realm_ntlmssp is not defined
        - ConfigError: realm xxx is specified in realms more than once

        Examples:
        | Authentication Edit Sequence All Realms | realms=realm1, realm2, realm3 | realm_ntlmssp=realm2 |
        | Authentication Edit Sequence All Realms | realms=realm2, realm3, i1 |
        | Run Keyword And Expect An Error | ConfigError: realm * is specified in realms more than once | Authentication Edit Sequence All Realms | realms=realm3, realm1, realm2, realm3, realm2 |
    """
        realms = self._convert_to_tuple(realms)
        self._check_uniquness_of_realms(realms)

        self._open_page()
        self._click_sequence_link('All Realms', self.realm_name_column)
        self._edit_all_realms_sequence(realms)
        self._set_ntlmssl_realm(realm_ntlmssp)
        self._click_submit_button(skip_wait_for_title=True)

    def _check_for_number_of_server(self, servers, type='LDAP'):

        if len(servers) > 3:
            raise guiexceptions.ConfigError, 'Only a maximum of 3 ' \
                               '%s servers is allowed' % type

    def _check_realms_existence(self, realms):
        for realm in realms:
            if self._get_realm_row_index(realm) is None:
                raise guiexceptions.ConfigError, \
                    '"%s" realm does not exist' % realm

    def _fill_in_name(self, name):

        realm_name_field = "realm_name"

        if name is not None:
            self.input_text(realm_name_field, name)

    def _edit_old_name(self, name):

        realm_name_field = "realm_name"

        if name is not None:
            self.input_text(realm_name_field, name)

    def _select_auth_protocol(self, protocol):

        # check the status of 'Authentication Protocol and Scheme(s)' option
        # button.  If an NTLM realm is already configured, it won't be
        # visible to configure another NTLM realm.  Thus, throw an exception
        protocol_option_visible = self._is_visible(self.protocol_option)
        if protocol.lower() == 'ntlm' and not protocol_option_visible:
            raise guiexceptions.ConfigError, ('An NTLM authentication realm '
                                              'already existed')
        if protocol and protocol_option_visible:
            self.select_from_list(self.protocol_option,
                                  LABEL(protocol_option_dict[protocol.lower()]))

    def _fill_in_ntlm_realm(self,
        source_interface, servers, domain, net_domain, join_domain,
        domain_user, domain_pw, usetls,
        enable_transparent,
        primary_ad_server,
        primary_ad_secret,
        backup_ad_server,
        backup_ad_secret,
        enable_client_signing_required,
        run_test,
        location=None,
        enable_keytab_authentication=None,
        kerberos_ha_user=None,
        kerberos_ha_pw=None):

        SERVER_FIELD = lambda index: "ADServer[%d][Host]" % index
        domain_field = "ADDomain"
        net_domain_field = "NetBIOSDomain"
        client_signing_required_checkbox = "UseTLS"
        location_field = "location"

        SELECT = 'xpath=//select [ @id="ADServer_Interface"]'
        set_source_interface_checkbox = "ADSinterface_confirm"
        self.select_checkbox(set_source_interface_checkbox)
        self.select_from_list(SELECT, source_interface)

        if servers is not None:
            servers = self._convert_to_tuple(servers)
            for i, server in enumerate(servers):
                self.input_text(SERVER_FIELD(i), server)
        if domain is not None:
            self.input_text(domain_field, domain)
        if net_domain is not None:
            if not self._is_visible(net_domain_field):
                raise guiexceptions.ConfigError, ('NetBIOS Domain field is not '
                    'available to input %s' % net_domain)
            self.input_text(net_domain_field, net_domain)
        if location is not None:
            self._info("into location field...")
            self.input_text(location_field, location)
        if usetls is not None:
            if usetls:
                self.select_checkbox(client_signing_required_checkbox)
            else:
                self.unselect_checkbox(client_signing_required_checkbox)
        if enable_transparent is not None:
            self._enable_transparent(enable_transparent)
        if primary_ad_server is not None:
            self._set_primary_ad(primary_ad_server, primary_ad_secret)
        if backup_ad_server is not None:
            self._set_backup_ad(backup_ad_server, backup_ad_secret)
        if enable_client_signing_required is not None:
            self._enable_client_signing_required(enable_client_signing_required)
        if enable_keytab_authentication is not None:
            self._enable_keytab_authentication(enable_keytab_authentication)
        if kerberos_ha_user is not None:
            self._kerberos_ha_user(kerberos_ha_user, kerberos_ha_pw)
        if join_domain:
            self._join_domain(domain_user, domain_pw)
            if run_test:
                self._test('NTLM')
            self._click_submit_button(wait=False, accept_confirm_dialog=True,
                skip_wait_for_title=True,
                )
        else:
            self.click_button(SUBMIT_BTN, "don't wait")
            time.sleep(2)
            if self._is_element_present(CONFIRM_SUBMIT):
                self.click_button(CONFIRM_SUBMIT)
            self._check_action_result()

    def _enable_transparent(self, enable_transparent):
        CHECKBOX = 'xpath=//input [@id="EnableSSOAD"]'

        if enable_transparent != self._is_checked(CHECKBOX):
            self.click_element(CHECKBOX, "don't wait")

    def _set_primary_ad(self, server, secret):
        SERVER_FIELD = 'xpath=//input[@name = "PrimaryAgentAddress"]'
        SECRET_FIELD = 'xpath=//input[@name = "PrimaryAgentSecret"]'

        self.input_text(SERVER_FIELD, server)
        self.input_text(SECRET_FIELD, secret)

    def _set_backup_ad(self, server, secret):
        SERVER_FIELD = 'xpath=//input[@name = "BackupAgentAddress"]'
        SECRET_FIELD = 'xpath=//input[@name = "BackupAgentSecret"]'

        self.input_text(SERVER_FIELD, server)
        self.input_text(SECRET_FIELD, secret)

    def _enable_client_signing_required(self, enable_client_signing_required):
        CHECKBOX = 'xpath=//input [@id="UseTLS"]'

        if enable_client_signing_required != self._is_checked(CHECKBOX):
            self.click_element(CHECKBOX, "don't wait")

    def _enable_keytab_authentication(self, enable_keytab_authentication):
        CHECKBOX = 'xpath=//input [@id="UseKeytab"]'

        if enable_keytab_authentication != self._is_checked(CHECKBOX):
            self.click_element(CHECKBOX, "don't wait")

    def _kerberos_ha_user(self, kerberos_ha_user, kerberos_ha_pw):
        SERVER_FIELD = 'xpath=//input[@name = "KeytabUsername"]'
        SECRET_FIELD = 'xpath=//input[@name = "KeytabPassword"]'

        self.input_text(SERVER_FIELD, kerberos_ha_user)
        self.input_text(SECRET_FIELD, kerberos_ha_pw)

    def _join_domain(self, user, password):

        join_domain_button = "join_domain"
        user_field = "dialog_username"
        password_field = "dialog_passwd"

        self.click_button(join_domain_button, "don't wait")
        self.input_text(user_field, user)
        self.input_text(password_field, password)
        self._click_continue_button(text='Create Account')

    def _fill_in_ldap_realm(self, version, use_ldaps, supp_edir, servers,
                            persist_conn, cust_persist_conn, base_dn,
                            uname_attr, cust_uname_attr, ufilter_qry,
                            cust_ufilter_qry, qry_type, bind_dn, bind_pw,
                            run_test):

        self._fill_in_ldap_version(version, use_ldaps, supp_edir)
        self._fill_in_ldap_servers(servers, source_interface)
        self._fill_in_ldap_advanced(persist_conn, cust_persist_conn)
        self._fill_in_ldap_user_authentication(base_dn, uname_attr,
            cust_uname_attr, ufilter_qry, cust_ufilter_qry)
        self._fill_in_query_credentials(qry_type, bind_dn, bind_pw)
        if run_test:
            self._test('LDAP')

    def _fill_in_ldap_version(self, version, use_ldaps, support_edir):

        ldap_version_option = "Version"
        use_secure_ldap_checkbox = "UseSecureLDAP"
        support_edir_checkbox = "enable_sso_edir"
        valid_ldap_version = ('2', '3')

        if version is not None:
            if version not in valid_ldap_version:
                raise guiexceptions.ConfigError, 'Invalid LDAP version.  ' \
                        'Either 2 or 3 only'
            if version == '2':
                if use_ldaps:
                    raise guiexceptions.ConfigError, 'Version 2 LDAP does ' \
                        'not support secure LDAP'
                if support_edir:
                    raise guiexceptions.ConfigError, 'Version 2 LDAP does ' \
                        'not support Novell eDirectory'
            self.select_from_list(ldap_version_option, LABEL("Version %s" % \
                                   version))
        if use_ldaps is not None:
            if use_ldaps:
                self.select_checkbox(use_secure_ldap_checkbox)
            else:
                self.unselect_checkbox(use_secure_ldap_checkbox)
        if support_edir is not None:
            if support_edir:
                self.select_checkbox(support_edir_checkbox)
            else:
                self.unselect_checkbox(support_edir_checkbox)

    def _fill_in_ldap_servers(self, servers, source_interface):

        SELECT = 'xpath=//select [ @id="LDAPServer_Interface"]'
        set_source_interface_checkbox = "LDAPinterface_confirm"
        self.select_checkbox(set_source_interface_checkbox)
        self.select_from_list(SELECT, source_interface)

        for i, server in enumerate(servers):
            server = server.split(':')
            self.input_text(LDAP_SERVER_FIELD(i), server[0])
            if len(server) == 2:
                self.input_text(LDAP_PORT_FIELD(i), server[1])

    def _fill_in_ldap_advanced(self, persist_conn, cust_persist_conn):

        advanced_link_open = "arrow_open"
        advanced_link_close = "arrow_closed"
        persistent_custom_count_field = "PersistentConnectionCount"

        if persist_conn is not None:
            if not self._is_visible(advanced_link_open):
                self.click_element(advanced_link_close, "don't wait")
            self._click_radio_button(persistent_conn_radio_button_dict
                                     [persist_conn.lower()])
            if persist_conn.lower() == 'custom':
                self.input_text(persistent_custom_count_field,
                                cust_persist_conn)

    def _fill_in_external_queries(self,
            ext_queries_enable,
            ext_user_base_dn,
            ext_user_query,
            ext_user_attr,
            ext_deny_login,
            ext_group_base_dn,
            ext_group_query,
            ext_mem_name,
            ext_group_name,
        ):
        CHECKBOX_ENABLE = 'xpath=//input [@id="externalauth_enable"]'
        USER_BASEDN = 'xpath=//input [@id="account_base"]'
        USER_QUERY = 'xpath=//input [@id="user_query"]'
        USER_ATTR = 'xpath=//input [@id="gecos_attribute"]'
        DENY_LOGIN = 'xpath=//input [@id="deny_login"]'
        GROUP_BASEDN = 'xpath=//input [@id="group_base"]'
        GROUP_QUERY = 'xpath=//input [@id="membership_query"]'
        MEM_NAME = 'xpath=//input [@id="member_attribute"]'
        GROUP_NAME = 'xpath=//input [@id="group_name_attribute"]'

        if ext_queries_enable:
            if ext_queries_enable =='yes':
                self.select_checkbox(CHECKBOX_ENABLE)
            elif ext_queries_enable == 'no':
                self.unselect_checkbox(CHECKBOX_ENABLE)
        self._input_text_if_not_none(USER_BASEDN, ext_user_base_dn)
        self._input_text_if_not_none(USER_QUERY, ext_user_query)
        self._input_text_if_not_none(USER_ATTR, ext_user_attr)
        if ext_deny_login:
            if ext_deny_login =='yes':
                self.select_checkbox(DENY_LOGIN)
            elif ext_deny_login == 'no':
                self.unselect_checkbox(DENY_LOGIN)
        self._input_text_if_not_none(GROUP_BASEDN, ext_group_base_dn)
        self._input_text_if_not_none(GROUP_QUERY, ext_group_query)
        self._input_text_if_not_none(MEM_NAME, ext_mem_name)
        self._input_text_if_not_none(GROUP_NAME, ext_group_name)

    def _fill_in_user_queries(self,
            user_queries_enable,
            base_dn,
            uname_attr,
            cust_uname_attr,
            ufilter_qry,
            cust_ufilter_qry,
            qry_type,
            bind_dn,
            bind_pw,
        ):
        CHECKBOX_ENABLE = 'xpath=//input [@id="EnableUserGroup"]'
        if self._is_visible(CHECKBOX_ENABLE) and \
            not user_queries_enable and \
            (base_dn or \
            uname_attr or \
            cust_uname_attr or \
            ufilter_qry or \
            cust_ufilter_qry or \
            qry_type or \
            bind_dn or \
            bind_pw):
            user_queries_enable = 'yes'
        if user_queries_enable:
            if user_queries_enable =='yes':
                self.select_checkbox(CHECKBOX_ENABLE)
            elif user_queries_enable == 'no':
                self.unselect_checkbox(CHECKBOX_ENABLE)
        self._fill_in_ldap_user_authentication(
            base_dn,
            uname_attr,
            cust_uname_attr,
            ufilter_qry,
            cust_ufilter_qry,
        )
        self._fill_in_query_credentials(
            qry_type,
            bind_dn,
            bind_pw,
        )

    def _fill_in_ldap_user_authentication(self, base_dn, uname_attr,
                                          cust_uname_attr, ufilter_qry,
                                          cust_ufilter_qry):

        base_dn_field = "BaseDN"
        user_name_attr_option = "UserNameAttribute"
        user_name_attr_custom_str_field = "UserNameAttributeCustom"
        user_filter_qry_option = "UserFilterQuery"
        user_filter_qry_custom_str_field = "UserFilterQueryCustom"

        if base_dn is not None:
            self.input_text(base_dn_field, base_dn)
        if uname_attr is not None:
            self.select_from_list(user_name_attr_option,
                                  auth_label_dict[uname_attr.lower()])
            if uname_attr.lower() == 'custom' and  \
                cust_uname_attr is not None:
                self.input_text(user_name_attr_custom_str_field,
                                cust_uname_attr)
        if ufilter_qry is not None:
            self.select_from_list(user_filter_qry_option,
                                  auth_label_dict[ufilter_qry.lower()])
            if ufilter_qry.lower() == 'custom' and  \
                cust_ufilter_qry is not None:
                self.input_text(user_filter_qry_custom_str_field,
                                cust_ufilter_qry)

    def _fill_in_query_credentials(self, qry_type, bind_dn, bind_pw):

        bind_dn_field = "BindDN"
        bind_passwd_field = "BindPassword"
        bind_passwd_confirm_field = "BindPasswordConfirm"

        if qry_type is not None:
            self._click_radio_button(credential_type_radio_button_dict
                                    [qry_type.lower()])
            if qry_type.lower() == 'bind':
                if bind_dn is not None:
                    self.input_text(bind_dn_field, bind_dn)
                if bind_pw is not None:
                    self.input_text(bind_passwd_field, bind_pw)
                    self.input_text(bind_passwd_confirm_field, bind_pw)

    def _fill_in_group_auth(self, type, membership_attr, membership_attr_str,
                            membership_attr_dn, grp_name_attr,
                            grp_name_attr_str, qry_string, qry_string_str):

        self._click_radio_button(group_auth_radio_buttons_dict[type.lower()])
        if type.lower() == 'group':
            self._fill_in_grp_auth(membership_attr, membership_attr_str,
                grp_name_attr, grp_name_attr_str, qry_string, qry_string_str)
        if type.lower() == 'user':
            self._fill_in_user_auth(membership_attr, membership_attr_str,
                membership_attr_dn, grp_name_attr, grp_name_attr_str,
                qry_string, qry_string_str)

    def _fill_in_grp_auth(self, membership_attr, membership_attr_str,
                          grp_name_attr, grp_name_attr_str, qry_string,
                          qry_string_str):

        grp_membership_attr_opt_button = "GroupMembershipAttribute_GroupObject"
        grp_membership_attr_custom_field = \
                                   "GroupMembershipAttributeCustom_GroupObject"
        grp_name_attr_opt_button = "GroupNameAttribute_GroupObject"
        grp_name_attr_custom_field = "GroupNameAttributeCustom_GroupObject"
        grp_query_string_opt_button = "GroupFilterQuery_GroupObject"
        grp_query_string_custom_field = "GroupFilterQueryCustom_GroupObject"

        if membership_attr is not None:
            self.select_from_list(grp_membership_attr_opt_button,
                                  auth_label_dict[membership_attr.lower()])
            if membership_attr.lower() == 'custom' and \
                             membership_attr_str is not None:
                self.input_text(grp_membership_attr_custom_field,
                                membership_attr_str)
        if grp_name_attr is not None:
            self.select_from_list(grp_name_attr_opt_button,
                                  auth_label_dict[grp_name_attr.lower()])
            if grp_name_attr.lower() == 'custom' and \
                                grp_name_attr_str is not None:
                self.input_text(grp_name_attr_custom_field, grp_name_attr_str)
        if qry_string is not None:
            self.select_from_list(grp_query_string_opt_button,
                                  auth_label_dict[qry_string.lower()])
            if qry_string.lower() == 'custom' and \
                                 qry_string_str is not None:
                self.input_text(grp_query_string_custom_field, qry_string_str)

    def _fill_in_user_auth(self, membership_attr, membership_attr_str,
                           membership_attr_dn, grp_name_attr,
                           grp_name_attr_str, qry_string, qry_string_str):

        usr_membership_attr_opt_button = "GroupMembershipAttribute_UserObject"
        usr_membership_attr_custom_field = \
                                   "GroupMembershipAttributeCustom_UserObject"
        attr_is_a_dn_checkbox = "IsUserGroupMembershipAttributeDN"
        usr_name_attr_opt_button = "GroupNameAttribute_UserObject"
        usr_name_attr_custom_field = "GroupNameAttributeCustom_UserObject"
        usr_query_string_opt_button = "GroupFilterQuery_UserObject"
        usr_query_string_custom_field = "GroupFilterQueryCustom_UserObject"

        if membership_attr is not None:
            self.select_from_list(usr_membership_attr_opt_button,
                                  auth_label_dict[membership_attr.lower()])
            if membership_attr.lower() == 'custom' and \
                               membership_attr_str is not None:
                self.input_text(usr_membership_attr_custom_field,
                                membership_attr_str)
        if membership_attr_dn is not None:
            if membership_attr_dn:
                self.select_checkbox(attr_is_a_dn_checkbox)
                if grp_name_attr is not None:
                    self.select_from_list(usr_name_attr_opt_button,
                                       auth_label_dict[grp_name_attr.lower()])
                    if grp_name_attr.lower() == 'custom' and \
                                     grp_name_attr_str is not None:
                        self.input_text(usr_name_attr_custom_field,
                                        grp_name_attr_str)
                if qry_string is not None:
                    self.select_from_list(usr_query_string_opt_button,
                                           auth_label_dict[qry_string.lower()])
                    if qry_string.lower() == 'custom' and \
                                  qry_string_str is not None:
                        self.input_text(usr_query_string_custom_field,
                                        qry_string_str)
            else:
                self.unselect_checkbox(attr_is_a_dn_checkbox)

    def _put_realm_kerb_in_order(self, realms_kerb):

        add_row_button = "negotiate_realms_domtable_AddRow"

        if realms_kerb:
            number_of_realm = len(realms_kerb)
            if number_of_realm > 2:
                additional_row = number_of_realm - 2
                for i in range(additional_row):
                    self.click_button(add_row_button, "don't wait")

            for i, realm in enumerate(realms_kerb):
                self.select_from_list(
                    SEQUENCE_REALM_KERB_OPTION(i), LABEL(realm))

    def _put_realm_in_order(self, realms):

        add_row_button = "realms_domtable_AddRow"

        if realms is not None:
            number_of_realm = len(realms)
            if number_of_realm > 2:
                additional_row = number_of_realm - 2
                for i in range(additional_row):
                    self.click_button(add_row_button, "don't wait")

            for i, realm in enumerate(realms):
                self.select_from_list(SEQUENCE_REALM_OPTION(i), LABEL(realm))

    def _set_ntlmssl_realm(self, realm_ntlmssp):
        if realm_ntlmssp == None: return
        drop_list = '//select[@id="ntlm_ssp_realm"]'
        self.select_from_list(drop_list, realm_ntlmssp)

    def _edit_sequence(self, realms):

        sequence_realm_table = "//table[@id='realms']//tbody[2]//tr"
        add_row_button = "realms_domtable_AddRow"

        if realms is not None:
            number_of_realm = len(realms)
            number_of_rows = int(self.get_matching_xpath_count(
                                 sequence_realm_table))
            for i in xrange(number_of_rows - 1,0,-1):
                self.click_element(SEQUENCE_REALM_DELETE_WIDGET(i), "don't wait")
            if number_of_realm > 1:
                additional_row = number_of_realm - 1
                for i in xrange(additional_row):
                    self.click_button(add_row_button, "don't wait")
            for i, realm in enumerate(realms):
                if i == 0:
                    self.select_from_list(SEQUENCE_REALM_OPTION(i),
                                         LABEL(realm))
                else:
                    self.select_from_list(
                                    SEQUENCE_REALM_OPTION((i-1)+number_of_rows),
                                    LABEL(realm))

    def _check_uniquness_of_realms(self, realms):
        # Verify that realms in the sequence are unique
        if realms == None: return
        list_of_realms = []
        for realm in realms:
            if not list_of_realms.__contains__(realm):
                list_of_realms.append(realm)
            else:
                raise guiexceptions.ConfigError(
                    "realm %s is specified in %s more than once" % \
                    (realm, realms))

    def _edit_all_realms_sequence(self, realms):

        up_arrow = "xpath=//img[@onclick='moveUp(%s)']"

        if realms is not None:
            index = 1
            for realm in realms:
                index += 1
                print "index=", index
                row = self._get_all_realms_sequence_row_index(realm)
                print "realm=", realm, "row=", row
                if row > index: # will move the realm up
                    for i in range(row, index, -1):
                        print 'i=', i
                        self.click_element(up_arrow % (i - 2,), "don't wait")

    def _test(self, protocol):
        test_button_dict = {
           'ACTIVE DIRECTORY'   : "AD_start_test",
           'LDAP'               : "LDAP_start_test",
           'NTLM'               : "AD_start_test",
        }
        test_result_dict = {
           'ACTIVE DIRECTORY'   : "AD_container",
           'LDAP'               : "LDAP_container",
           'NTLM'               : "AD_container",
        }

        self.click_button(test_button_dict[protocol])
        while not self._is_visible(test_button_dict[protocol]):
            pass
        test_result = self.get_text(test_result_dict[protocol])
        self._info(test_result)
        if test_result.find('successfully')  == -1:
            raise guiexceptions.AuthTestError, '%s test failed.  Check ' \
                'log run for result output' % (protocol,)
        return test_result

    def _click_add_realm_button(self):

        add_realm_button = "xpath=//input[@value='Add Realm...']"

        self.click_button(add_realm_button)

    def _click_add_sequence_button(self):

        add_seq_button = "xpath=//input[@value='Add Sequence...']"

        if not self._is_element_present(add_seq_button):
            raise guiexceptions.ConfigError, 'Not enough realm to create ' \
                'realm sequence'

        self.click_button(add_seq_button)

    def _click_edit_global_settings_button(self):

        edit_global_settings_button = \
                           "xpath=//input[@value='Edit Global Settings...']"

        self.click_button(edit_global_settings_button)

    def _delete_sequence(self, name, delete_column):

        sequence_row = self._get_sequence_row_index(name)
        if sequence_row is None:
            raise guiexceptions.ConfigError, '"%s" sequence does not exist' % \
                name
        self.click_element(DELETE_WIDGET(SEQUENCE_TABLE,
                                   sequence_row, delete_column), "don't wait")
        self._click_continue_button()

    def _delete_realm(self, name, delete_column):

        realm_row = self._get_realm_row_index(name)
        if realm_row is None:
            raise guiexceptions.ConfigError, '"%s" realm does not exist' % name
        self.click_element(
            DELETE_WIDGET(REALM_TABLE, realm_row, delete_column), "don't wait")
        self._click_continue_button()

    def _get_realm_row_index(self, name):

        number_of_rows = self.get_matching_xpath_count(REALM_TABLE + "//tr")
        for i in xrange(2, int(number_of_rows) + 1):
            realm_name = self.get_text(
                                   NAME_FIELD(REALM_TABLE, i)).split(' \n')[0]
            if realm_name == name:
                return i
        return None

    def _get_all_realms_sequence_row_index(self, name):

        all_realms_sequence_table = "//form[@id='form']//table//table"
        NAME_FIELD = lambda table, index: "%s//tr[%s]//td[2]" % (table, index)
        number_of_rows = int(self.get_matching_xpath_count
                             (all_realms_sequence_table + "//tr"))
        for i in xrange(2, number_of_rows + 1):
            realm_name = self.get_text(NAME_FIELD(all_realms_sequence_table,
                             i)).split(' \n')[0]
            if realm_name == name:
                return i
        return None

    def _get_sequence_row_index(self, name):
        number_of_rows = self.get_matching_xpath_count(SEQUENCE_TABLE + "//tr")
        for i in xrange(4, int(number_of_rows) + 1):
            sequence_name = self.get_text(
                                NAME_FIELD(SEQUENCE_TABLE, i)).split(' \n')[0]
            if sequence_name == name:
                return i
        return None

    def _get_realm_protocol(self, name):
        realm_row = self._get_realm_row_index(name)
        if realm_row is None:
            raise guiexceptions.ConfigError, '"%s" realm does not exist' % name
        return self.get_text(
            PROTOCOL_FIELD(REALM_TABLE, realm_row)).split(' \n')[0]

    def _click_realm_link(self, name, column):
        realm_row = self._get_realm_row_index(name)
        if realm_row is None:
            raise guiexceptions.ConfigError, '"%s" realm does not exist' % name
        self.click_link(NAME_LINK(REALM_TABLE, realm_row, column))

    def _click_sequence_link(self, name, column):
        sequence_row = self._get_sequence_row_index(name)
        if sequence_row is None:
            raise guiexceptions.ConfigError, \
                '"%s" sequence does not exist' % name
        self.click_link(NAME_LINK(SEQUENCE_TABLE, sequence_row, column))

    def _submit(self):
        submit_button = "xpath=//input[@value='Submit']"
        CONFIRM_DLG = 'xpath=//div[@id="confirmation_dialog"]'
        CONFIRM_BTN = ('%s/div/span/button[text()="%s"]' %
                       (CONFIRM_DLG, "Submit"))

        self.click_button(submit_button, "don't wait")
        time.sleep(2)
        try:
            if self._is_visible(CONFIRM_DLG):
                self.click_button(CONFIRM_BTN)
        except:
            pass
