#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1362/cli/keywords/ldap_config.py#1 $ $DateTime: 2020/06/10 22:29:20 $ $Author: sarukakk $

from common.cli.clicommon import (CliKeywordBase, DEFAULT)
from common.cli.cliexceptions import ConfigError


class LDAPConfig(CliKeywordBase):

    """Keywords for ldapconfig CLI command."""

    def get_keyword_names(self):
        return [
            'ldap_config_new',
            'ldap_config_edit_server_name',
            'ldap_config_edit_server_hostname',
            'ldap_config_edit_server_port',
            'ldap_config_edit_server_type',
            'ldap_config_edit_server_authtype',
            'ldap_config_edit_server_base',
            'ldap_config_edit_server_cache',
            'ldap_config_edit_server_compatibility',
            'ldap_config_edit_server_connection',
            'ldap_config_add_externalauth',
            'ldap_config_edit_externalauth_name',
            'ldap_config_edit_externalauth_user',
            'ldap_config_edit_externalauth_membership',
            'ldap_config_edit_externalauth_accountbase',
            'ldap_config_edit_externalauth_groupbase',
            'ldap_config_edit_externalauth_fullname',
            'ldap_config_edit_externalauth_groupname',
            'ldap_config_edit_externalauth_groupmember',
            'ldap_config_edit_externalauth_expiration',
            'ldap_config_delete_externalauth',
            'ldap_config_add_isqauth',
            'ldap_config_edit_isqauth_name',
            'ldap_config_edit_isqauth_query',
            'ldap_config_edit_isqauth_emailattribute',
            'ldap_config_activate_isqauth',
            'ldap_config_delete_isqauth',
            'ldap_config_add_isqalias',
            'ldap_config_edit_isqalias_name',
            'ldap_config_edit_isqalias_query',
            'ldap_config_edit_isqalias_emailattribute',
            'ldap_config_activate_isqalias',
            'ldap_config_delete_isqalias',
            'ldap_config_delete',
            'ldap_config_setup',
            'ldap_config_advanced_new_domain_based_query',
            'ldap_config_advanced_edit_domain_based_new',
            'ldap_config_advanced_edit_domain_based_edit',
            'ldap_config_advanced_edit_domain_based_delete',
            'ldap_config_advanced_edit_domain_based_default',
            'ldap_config_advanced_edit_domain_based_activate',
            'ldap_config_advanced_new_chained_query',
            'ldap_config_advanced_edit_chained_insert',
            'ldap_config_advanced_edit_chained_delete',
            'ldap_config_advanced_edit_chained_activate',
            'ldap_config_advanced_delete',
            'ldap_config_advanced_print',
        ]

    def ldap_config_new(self, name, address, use_ssl=DEFAULT,
        auth_type=DEFAULT, username=None, password=None,
        validate_settings=DEFAULT, server_type=None, port=DEFAULT,
        base=DEFAULT):
        """Create a new server configuration.

        Parameters:
        - `name`: name for the server configuration.
        - `address`: fully qualified hostname or IP.
        - `use_ssl`: use SSL to connect to the LDAP server.
        - `auth_type`: authentication method to use for the server
           configuration.
        - `username`: bind username if `auth_type` is 'password based'.
        - `password`: bind password if `auth_type` is 'password based'.
        - `validate_settings`: connect to LDAP server to validate setting.
        - `server_type`: server type to use for the server configuration.
        - `port`: port to connect to the server.
        - `base`: base DN of the server.

        Examples:
        | LDAP Config New | myLDAP | qa19.qa.sbr.ironport.com |
        | LDAP Config New | myLDAP | sully.qa | yes | password based |
        | ... | admin | ironport | yes | port=389 | base=dc=qa |

        Exceptions:
        - `ConfigError`: in case no password was provided when using
           password-based authentication.
        """
        input_dict = {
            'server_name': name,
            'host_name': address,
            'ssl_using': self._process_yes_no(use_ssl),
            'auth_type': auth_type,
            'validate_setting': self._process_yes_no(validate_settings),
            'port': port,
            'base': base,
        }

        if username is not None:
            if password is None:
                raise ConfigError('Password must be provided')
            input_dict.update({'password': password, 'username': username})

        if server_type is not None:
            input_dict.update({'server_type': server_type})

        self._cli.ldapconfig().new(input_dict)

    def ldap_config_edit_server_name(self, name, newname=DEFAULT):
        """Change the name of the server configuration.

        Parameters:
        - `name`: name of the server configuration to edit.
        - `newname`: new name for the server configuration.

        Examples:
        | LDAP Config Edit Server Name | old_name | new_name |
        """
        self._cli.ldapconfig().edit(name).server().name(newname)

    def ldap_config_edit_server_hostname(self, name, hostname=DEFAULT):
        """Change the hostname of the server configuration.

        Parameters:
        - `name`: name of the server configuration to edit.
        - `hostname`: new hostname value for the server configuration.

        Examples:
        | LDAP Config Edit Server Hostname | myLDAP | ldap.example.com |
        """
        self._cli.ldapconfig().edit(name).server().hostname(hostname)

    def ldap_config_edit_server_port(self, name, port=DEFAULT):
        """Change the port number of the server configuration.

        Parameters:
        - `name`: name of the server configuration to edit.
        - `port`: new port number for the server configuration.

        Examples:
        | LDAP Config Edit Server Port | myLDAP | 123 |
        """
        self._cli.ldapconfig().edit(name).server().port(port)

    def ldap_config_edit_server_type(self, name, server_type=DEFAULT):
        """Change the server type of the server configuration.

        Parameters:
        - `name`: name of the server configuration to edit.
        - `server_type`: name of the server type for the server configuration.

        Examples:
        | LDAP Config Edit Servert Type | myLDAP | Active Directory |
        | LDAP Config Edit Servert Type | myLDAP | Unknown |
        """
        self._cli.ldapconfig().edit(name).server().servertype(server_type)

    def ldap_config_edit_server_authtype(self, name, auth_type=DEFAULT,
        username=None, password=None, use_ssl=DEFAULT, port=None):
        """Change the authentication type of the server configuration.

        Parameters:
        - `name`: name of the server configuration to edit.
        - `auth_type`: name of the authentication type for the server
           configuration.
        - `username`: bind username.
        - `password`: bind password.
        - `use_ssl`: use SSL to connect to the LDAP server.
        - `port`: port number to use for SSL.

        Examples:
        | LDAP Config Edit Server Authtype | myLDAP | Password based |
        | ... | testuser | ironport | yes | 123 |
        | LDAP Config Edit Server Authtype | myLDAP | Anonymous | use_ssl=no |
        """
        input_dict = {
            'auth_type': auth_type,
            'ssl_using': self._process_yes_no(use_ssl),
        }

        if username is not None:
            input_dict.update({'username': username})

        if password is not None:
            input_dict.update({'password': password})

        if port is not None:
            input_dict.update({'port': port})

        self._cli.ldapconfig().edit(name).server().authtype(input_dict)

    def ldap_config_edit_server_base(self, name, base=DEFAULT):
        """Change query base of the server configuration.

        Parameters:
        - `name`: name of the server configuration to edit.
        - `base`: query base for the server configuration.

        Examples:
        | LDAP Config Edit Server Base | myLDAP | dc=qa |
        """
        self._cli.ldapconfig().edit(name).server().base(base)

    def ldap_config_edit_server_cache(self, name, cache_ttl=DEFAULT,
        max_entries=DEFAULT):
        """Edit cache settings of the server configuration

        Parameters:
        - `name`: name of the server configuration to edit.
        - `cache_ttl`: cache TTL in seconds.
        - `max_entries`: the maximum number of cache entries to retain.

        Examples:
        | LDAP Config Edit Server Cache | myLDAP | max_entries=9000 |
        | LDAP Config Edit Server Cache | myLDAP | 10000 | 3000 |
        """
        self._cli.ldapconfig().edit(name).server().cache(cache_ttl=cache_ttl,
            max_entries=max_entries)

    def ldap_config_edit_server_compatibility(self, name, enable_mse=DEFAULT,
        advanced=None, attribute=None, search_scope=DEFAULT):
        """Edit LDAP protocol compatibility options of the server
        configuration.

        Parameters:
        - `name`: name of the server configuration to edit.
        - `enable_mse`: enable Microsoft Exchange LDAP compatibility mode.
        - `advanced`: configure advanced LDAP compatibility settings.
        - `attribute`: attribute to use for existence-only queries.
        - `search_scope`: LDAP search scope.

        Examples:
        | LDAP Config Edit Server Compatibility | myLDAP | yes | yes |
        | ... | objectClass |
        | LDAP Config Edit Server Compatibility | myLDAP | no |
        | ... | search_scope=Single level |
        """
        input_dict = {
            'enabling': self._process_yes_no(enable_mse),
            'search_scope': search_scope
        }

        if advanced is not None:
            input_dict.update({'settings_en': self._process_yes_no(advanced)})

        if attribute is not None:
            input_dict.update({'attribute': attribute})

        self._cli.ldapconfig().edit(name).server().compatibility(input_dict)

    def ldap_config_edit_server_connection(self, name, max_conn=DEFAULT,
        mult_host_option=DEFAULT):
        """Edit connection options of the server configuration.

        Parameters:
        - `name`: name of the server configuration to edit.
        - `max_conn`: he number of simultaneous connections for each the host.
        - `mult_host_option`: feature to use when connecting to multiple LDAP
           servers.

        Examples:
        | LDAP Config Edit Server Connection | myLDAP | 4 | Failover |
        | LDAP Config Edit Server Connection | myLDAP |
        | ... | mult_host_option=load balancing |
        """
        self._cli.ldapconfig().edit(name).server().connection(
            connection=max_conn, request=mult_host_option)

    def ldap_config_add_externalauth(self, name, query_name=DEFAULT,
        base_dn=DEFAULT, user_records=DEFAULT, full_name_attr=DEFAULT,
        deny_expired=DEFAULT, group_base_dn=DEFAULT, group_member=DEFAULT,
        username_attr=DEFAULT, group_name_attr=DEFAULT, test_query='no',
        identity=None, password=None):
        """Enable external authentication query for server configuration.

        Parameters:
        - `name`: name of the server configuration to enable query for.
        - `query_name`: name for the query.
        - `base_dn`: base DN under which user records will be found.
        - `user_records`: query string for user records.
        - `full_name_attr`: attribute containing the user's full name.
        - `deny_expired`: deny login to expired accounts.
        - `group_base_dn`: base DN under which group records will be found.
        - `group_member`: query string to determine if a user is a member of
           a group.
        - `username_attr`: attribute that holds each member's username.
        - `group_name_attr`: attribute containing the group name.
        - `test_query`: test this query.
        - `identity`: identity to use in test query.
        - `password`: password to use in test query.

        Examples:
        | LDAP Config Add Externalauth | myLDAP |
        | LDAP Config Add Externalauth | myLDAP | test.query | dc=qa |
        | ... | (&(objectClass=posixAccount)(uid={u})) | gecos | no | dc=qa |
        | ... | (&(objectClass=posixGroup)(memberUid={u})) | memberUid | cn |
        | ... | yes | testuser | ironport |

        Exceptions:
        - `ConfigError`: in case no identity or password was provided when
           running test of the query.
        """
        input_dict = {
            'name': query_name,
            'user_base_dn': base_dn,
            'user_query': user_records,
            'full_name_attr': full_name_attr,
            'deny': self._process_yes_no(deny_expired),
            'grp_base_dn': group_base_dn,
            'grp_query': group_member,
            'member_attr': username_attr,
            'grp_attr': group_name_attr,
            'testing': self._process_yes_no(test_query)
        }

        if input_dict.get('testing') == 'Y':
            if None in (identity, password):
                raise ConfigError('Identity and password must be provided '\
                    'in order to perform the test of the query')

            input_dict.update(
                {'test_user_id': identity,
                 'bind_password': password})

        self._cli.ldapconfig().edit(name).externalauth(input_dict)

    def ldap_config_edit_externalauth_name(self, name, query_name=DEFAULT):
        """Edit external authentication query name.

        Parameters:
        - `name`: name of the server configuration to edit.
        - `auth_name`: name of the external authetication query name to set.

        Examples:
        | LDAP Config Edit Externalauth Name | myLDAP | query.name |
        """
        self._cli.ldapconfig().edit(name).externalauth().name(query_name)

    def ldap_config_edit_externalauth_user(self, name, query=DEFAULT):
        """Edit external authentication user query.

        Parameters:
        - `name`: name of the server configuration to edit.
        - `query`: user query string.

        Examples:
        | LDAP Config Edit Externalauth User | myLDAP | (uid={w}) |
        """
        self._cli.ldapconfig().edit(name).externalauth().user(query)

    def ldap_config_edit_externalauth_membership(self, name, query=DEFAULT):
        """Edit external authentication membership query.

        Parameters:
        - `name`: name of the server configuration to edit.
        - `query`: membership query string.

        Examples:
        | LDAP Config Edit Externalauth Membership | myLDAP | (memberUid={u}) |
        """
        self._cli.ldapconfig().edit(name).externalauth().membership(query)

    def ldap_config_edit_externalauth_accountbase(self, name, base_dn=DEFAULT):
        """Edit external authentication base DN for user records.

        Parameters:
        - `name`: name of the server configuration to edit.
        - `base_dn`: base DN for user records.

        Examples:
        | LDAP Config Edit Externalauth Accountbase | myLDAP | dc=qa |
        """
        self._cli.ldapconfig().edit(name).externalauth().accountbase(base_dn)

    def ldap_config_edit_externalauth_groupbase(self, name, base_dn=DEFAULT):
        """Edit external authentication base DN for group records.

        Parameters:
        - `name`: name of the server configuration to edit.
        - `base_dn`: base DN for group records.

        Examples:
        | LDAP Config Edit Externalauth Groupbase | myLDAP | dc=qa |
        """
        self._cli.ldapconfig().edit(name).externalauth().groupbase(base_dn)

    def ldap_config_edit_externalauth_fullname(self, name, attr=DEFAULT):
        """Edit external authentication user's full name attribute.

        Parameters:
        - `name`: name of the server configuration to edit.
        - `attr`: user's full name attribute.

        Examples:
        | LDAP Config Edit Externalauth Fullname | myLDAP | gecos |
        """
        self._cli.ldapconfig().edit(name).externalauth().fullname(attr)

    def ldap_config_edit_externalauth_groupname(self, name, attr=DEFAULT):
        """Edit external authentication group name attribute.

        Parameters:
        - `name`: name of the server configuration to edit.
        - `attr`: group name attribute.

        Examples:
        | LDAP Config Edit Externalauth Groupname | myLDAP | cn |
        """
        self._cli.ldapconfig().edit(name).externalauth().groupname(attr)

    def ldap_config_edit_externalauth_groupmember(self, name, attr=DEFAULT):
        """Edit external authentication group member attribute.

        Parameters:
        - `name`: name of the server configuration to edit.
        - `attr`: group member attribute.

        Examples:
        | LDAP Config Edit Externalauth Groupmember | myLDAP | memberUid |
        """
        self._cli.ldapconfig().edit(name).externalauth().groupmember(attr)

    def ldap_config_edit_externalauth_expiration(self, name, deny=DEFAULT):
        """Edit external authentication account expiration settings.

        Parameters:
        - `name`: name of the server configuration to edit.
        - `deny`: deny login to expired accounts.

        Examples:
        | LDAP Config Edit Externalauth Expiration | myLDAP | yes |
        """
        self._cli.ldapconfig().edit(name).externalauth().expiration(
            self._process_yes_no(deny))

    def ldap_config_delete_externalauth(self, name):
        """Delete external authentication query.

        Parameters:
        - `name`: name of the server configuration to remove query from.

        Examples:
        | LDAP Config Delete Externalauth | myLDAP |
        """
        self._cli.ldapconfig().edit(name).externalauth().delete()

    def ldap_config_add_isqauth(self, name, query_name=DEFAULT,
        query_string=DEFAULT, email_attr=DEFAULT, activate=DEFAULT,
        test_query='no', identity=None, password=None):
        """Enable ISQ End-User Authentication query for server configuration.

        Parameters:
        - `name`: name of the server configuration to enable query for.
        - `query_name`: name for the query.
        - `query_string`: LDAP query string.
        - `email_attr`: email attribute.
        - `activate`: activate query.
        - `test_query`: test this query.
        - `identity`: identity to use in query test.
        - `password`: password to use in query test.

        Examples:
        | LDAP Config Add ISQAuth | myLDAP |
        | LDAP Config Add ISQAuth | myLDAP | test.query | (uid={u}) | mail |
        | ... | yes | yes | testuser | ironport |

        Exceptions:
        - `ConfigError`: in case no identity or password was provided when
           testing LDAP query.
        """
        input_dict = {
            'name': query_name,
            'query': query_string,
            'attr_list': email_attr,
            'activate': self._process_yes_no(activate),
            'testing': self._process_yes_no(test_query),

        }

        if input_dict.get('testing') == 'Y':
            if None in (identity, password):
                raise ConfigError('Identity and password must be provided '\
                    'in order to perform the test of the query')

            input_dict.update(
                {'test_user_id': identity,
                 'isq_passwd': password})

        self._cli.ldapconfig().edit(name).isqauth(input_dict)

    def ldap_config_edit_isqauth_name(self, name, query_name=DEFAULT):
        """Edit ISQ end-user authentication query name.

        Parameters:
        - `name`: name of the server configuration to edit.
        - `auth_name`: new name for the ISQ end-user authetication query.

        Examples:
        | LDAP Config Edit ISQAuth Name | myLDAP | query.name |
        """
        self._cli.ldapconfig().edit(name).isqauth().name(query_name)

    def ldap_config_edit_isqauth_query(self, name, query_string=DEFAULT):
        """Edit ISQ end-user authentication query string.

        Parameters:
        - `name`: name of the server configuration to edit.
        - `query_string`: LDAP query string.

        Examples:
        | LDAP Config Edit ISQAuth Query | myLDAP | (uid={u}) |
        """
        self._cli.ldapconfig().edit(name).isqauth().query(query_string)

    def ldap_config_edit_isqauth_emailattribute(self, name, attr=DEFAULT):
        """Edit ISQ end-user authentication LDAP email attribute.

        Parameters:
        - `name`: name of the server configuration to edit.
        - `attr`: LDAP email atribute.

        Examples:
        | LDAP Config Edit ISQAuth Emailattribute | myLDAP | mail |
        """
        self._cli.ldapconfig().edit(name).isqauth().emailattribute(attr)

    def ldap_config_activate_isqauth(self, name, confirm='Yes'):
        """Activate ISQ end-user authentication query.

        Parameters:
        - `name`: name of the server configuration to activate query for.
        - `confirm`: confirm query activation.

        Examples:
        | LDAP Config Activate ISQAuth | test_query | yes |
        | LDAP Config Activate ISQAuth | test_query | no |
        """
        self._cli.ldapconfig().edit(name).isqauth().activate(
            self._process_yes_no(confirm))

    def ldap_config_delete_isqauth(self, name):
        """Delete ISQ end-user authentication query.

        Parameters:
        - `name`: name of the server configuration to delete query for.

        Examples:
        | LDAP Config Delete ISQAuth | my_isqauth_q |
        """
        self._cli.ldapconfig().edit(name).isqauth().delete()

    def ldap_config_add_isqalias(self, name, query_name=DEFAULT,
        query_string=DEFAULT, email_attr=DEFAULT, activate=DEFAULT,
        test_query='no', address=None):
        """Enable ISQ Alias Consolidation query for server configuration.

        Parameters:
        - `name`: name of the server configuration to enable query for.
        - `query_name`: name for the query.
        - `query_string`: LDAP query string.
        - `email_attr`: email attribute.
        - `activate`: activate query.
        - `test_query`: test this query.
        - `address`: address to use in query test.

        Examples:
        | LDAP Config Add ISQAlias | myLDAP |
        | LDAP Config Add ISQAlias | myLDAP | test.isqlaias | (mail={a}) |
        | ... | mail | yes | yes | test@example.com |

        Exceptions:
        - `ConfigError`: in case no email address was provided when performing
           query testing.
        """
        input_dict = {
            'name': query_name,
            'query': query_string,
            'attr_list': email_attr,
            'activate': self._process_yes_no(activate),
            'testing': self._process_yes_no(test_query),

        }

        if input_dict.get('testing') == 'Y':
            if address is None:
                raise ConfigError('Email address must be provided '\
                    'in order to perform query testing')

            input_dict.update({'test_addr': address})

        self._cli.ldapconfig().edit(name).isqalias(input_dict)

    def ldap_config_edit_isqalias_name(self, name, query_name=DEFAULT):
        """Edit ISQ alias consolidation query name.

        Parameters:
        - `name`: name of the server configuration to edit.
        - `query_name`: name for the ISQ alias consolidation query.

        Examples:
        | LDAP Config Edit ISQAlias Name | myLDAP | query.name |
        """
        self._cli.ldapconfig().edit(name).isqalias().name(query_name)

    def ldap_config_edit_isqalias_query(self, name, query_string=DEFAULT):
        """Edit ISQ alias consolidation query string.

        Parameters:
        - `name`: name of the server configuration to edit.
        - `query_string`: LDAP query string.

        Examples:
        | LDAP Config Edit ISQAlias Query | myLDAP | (mail={a}) |
        """
        self._cli.ldapconfig().edit(name).isqalias().query(query_string)

    def ldap_config_edit_isqalias_emailattribute(self, name, attr=DEFAULT):
        """Edit ISQ alias consolidation LDAP email attribute.

        Parameters:
        - `name`: name of the server configuration to edit.
        - `attr`: LDAP email atribute.

        Examples:
        | LDAP Config Edit ISQAlias Emailattribute | myLDAP | mail |
        """
        self._cli.ldapconfig().edit(name).isqalias().emailattribute(attr)

    def ldap_config_activate_isqalias(self, name, confirm='yes'):
        """Activate ISQ alias consolidation query.

        Parameters:
        - `name`: name of the server configuration to activate query for.
        - `confirm`: confirm query activation.

        Examples:
        | LDAP Config Activate ISQAlias | my_query | yes |
        | LDAP Config Activate ISQAlias | my_query | no |
        """
        self._cli.ldapconfig().edit(name).isqalias().activate(
            self._process_yes_no(confirm))

    def ldap_config_delete_isqalias(self, name):
        """Delete ISQ alias consolidation query.

        Parameters:
        - `name`: name of the server configuration to delete query for.

        Examples:
        | LDAP Config Delete ISQAlias | myLDAP |
        """
        self._cli.ldapconfig().edit(name).isqalias().delete()

    def ldap_config_delete(self, name):
        """Remove server configuration.

        Parameters:
        - `name`: name of the server configuration to delete.

        Examples:
        | LDAP Config Delete | myLDAP |
        """
        self._cli.ldapconfig().delete(name)

    def ldap_config_setup(self, interface=DEFAULT, treat_negative=DEFAULT):
        """Configure LDAP options.

        Parameters:
        - `interface`: name of the IP interface for LDAP traffic.
        - `treat_negative`: treat group queries that fail to complete as
           having negative results.

        Examples:
        | LDAP Config Setup | Management | Yes |
        | LDAP Config Setup | Auto | No |
        """
        self._cli.ldapconfig().setup(interface,
            self._process_yes_no(treat_negative))

    def ldap_config_advanced_new_domain_based_query(self, name, query_mapping,
        query_type=DEFAULT, use_default=DEFAULT, default_query=DEFAULT,
        activate=DEFAULT):
        """Add advanced domain based LDAP query

        Parameters:
        - `name`: name for the domain based query.
        - `query_mapping`: a string of 'domain_name:query_name' mapping.
        - `query_type`: type of the query.
        - `use_default`: default query to be used if no domain table entries
           are matched.
        - `default_query`: query name to use as the default.
        - `activate`: activate query.

        Examples:
        | LDAP Config Advanced New Domain Based Query | dbquery |
        | ... | example.com:query2 |
        | LDAP Config Advanced New Domain Based Query | dbquery |
        | ... | test.com:myquery | End-User | Yes | myquery | Yes |

        Exceptions:
        - `ValueError`: in case of invalid format of `query_mapping`
           parameter.
        """
        input_dict = {
            'name': name,
            'type': 'Domain-based',
            'query_type': query_type,
            'use_default_query': self._process_yes_no(use_default),
            'activate': self._process_yes_no(activate),
            'more_domain': 'no',
        }

        if input_dict.get('use_default') == 'Y':
            input_dict.update({'default_query': default_query})

        try:
            domain, query = query_mapping.split(':')
        except ValueError:
            raise ValueError('`query_mapping` must be in '\
            '`domain_name:query_name` format')
        else:
            input_dict.update({'domain': domain, 'query_domain': query})

        self._cli.ldapconfig().advanced().new(input_dict)

    def ldap_config_advanced_edit_domain_based_new(self, name, domain,
        query=DEFAULT):
        """Create new table entry for domain based query.

        Parameters:
        - `name`: name of the domain based query to add entry for.
        - `domain`: domain to match addresses against.
        - `query`: query to associate with the matching domain.

        Examples:
        | LDAP Config Advanced Edit Domain Based New | dombquery |
        | ... | example.com |
        """
        input_dict = {
            'domain': domain,
            'query': query,
        }
        self._cli.ldapconfig().advanced().edit(name).new(input_dict)

    def ldap_config_advanced_edit_domain_based_edit(self, name, entry=DEFAULT,
        domain=DEFAULT, query=DEFAULT):
        """Edit table entry of domain based query.

        Parameters:
        - `name`: name of the domain based query to edit entry for.
        - `entry`: name of the table entry to edit.
        - `domain`: domain to match addresses against.
        - `query`: query to associate with the matching domain.

        Examples:
        | LDAP Config Advanced Edit Domain Based Edit | dombquery |
        | ... | example.com | domain.com |
        """
        self._cli.ldapconfig().advanced().edit(name).edit(entry, domain, query)

    def ldap_config_advanced_edit_domain_based_delete(self, name,
        entry=DEFAULT):
        """Delete table entry of domain based query.

        Parameters:
        - `name`: name of the domain based query to delete entry for.
        - `entry`: name of the table entry to delete.

        Examples:
        | LDAP Config Advanced Edit Domain Based Delete | test.com |
        """
        self._cli.ldapconfig().advanced().edit(name).delete(entry)

    def ldap_config_advanced_edit_domain_based_default(self, name,
        entry=DEFAULT):
        """Change default table entry of domain based query.

        Parameters:
        - `name`: name of the domain based query to change default entry for.
        - `entry`: name of the table entry to make default.

        Examples:
        | LDAP Config Advanced Edit Domain Based Default | dombquery |
        | ... | test.com |
        """
        self._cli.ldapconfig().advanced().edit(name).default('Y', entry)

    def ldap_config_advanced_edit_domain_based_activate(self, name,
        confirm=DEFAULT):
        """Activate domain based query.

        Parameters:
        - `name`: name of the domain based query to change default entry for.
        - `confirm`: confirm activation of the query.

        Examples:
        | LDAP Config Advanced Edit Domain Based Activate | dombquery | no |
        | LDAP Config Advanced Edit Domain Based Activate | dombquery | yes |
        """
        self._cli.ldapconfig().advanced().edit(name).activate(
            self._process_yes_no(confirm))

    def ldap_config_advanced_new_chained_query(self, name, query_name,
        query_type=DEFAULT, activate=DEFAULT):
        """Add advanced chained LDAP query.

        Parameters:
        - `name`: name for the advanced query.
        - `query_name`: query name to add to the chain.
        - `query_type`: type of the query.
        - `activate`: activate query.

        Examples:
        | LDAP Config Advnaced New Chained Query | myquery | ldapq1 |
        | LDAP Config Advnaced New Chained Query | myquery | ldapq2 |
        | ... | Consolidation | Yes |
        """
        input_dict =  {
            'name': name,
            'type': 'Chained',
            'query_type': query_type,
            'activate': self._process_yes_no(activate),
            'query_chain': query_name,
        }
        self._cli.ldapconfig().advanced().new(input_dict)

    def ldap_config_advanced_edit_chained_insert(self, name, query=DEFAULT,
        position=DEFAULT):
        """Insert a list entry into chained query.

        Parameters:
        - `name`: name of the chained query to insert list entry into.
        - `query`: name of the query to insert.
        - `position`: insertion point for the query.

        Examples:
        | LDAP Config Advanced Edit Chained Insert | myLDAP | testq | 2 |
        """
        self._cli.ldapconfig().advanced().edit(name).insert(query, position)

    def ldap_config_advanced_edit_chained_delete(self, name, query=DEFAULT):
        """Delete list entry from chained query.

        Parameters:
        - `name`: name of the chained query to delete entry for.
        - `query`: name of the query to delete.

        Examples:
        | LDAP Config Advanced Edit Chained Delete | chained_name | chained1 |
        """
        self._cli.ldapconfig().advanced().edit(name).delete(query)

    def ldap_config_advanced_edit_chained_activate(self, name,
        confirm=DEFAULT):
        """Activate chained query.

        Parameters:
        - `name`: name of chained query to activate.
        - `confirm`: confirm activation of the query.

        Examples:
        | LDAP Config Advanced Edit Chained Activate | myquery | Yes |
        """
        self._cli.ldapconfig().advanced().edit(name).activate(
            self._process_yes_no(confirm))

    def ldap_config_advanced_delete(self, name):
        """Delete advanced LDAP query.

        Parameters:
        - `name`: name of the query to delete.

        Examples:
        | LDAP Config Advanced Delete | myAdvquery |
        """
        self._cli.ldapconfig().advanced().delete(name)

    def ldap_config_advanced_print(self, name):
        """Print advanced query.

        Parameters:
        - `name`: name of advanced query to print.

        Return:
        An output of print subcommand.

        Examples:
        | ${result} = | LDAP Config Advanced Print | testquery |
        """
        return self._cli.ldapconfig().advanced().print_advanced(name)


