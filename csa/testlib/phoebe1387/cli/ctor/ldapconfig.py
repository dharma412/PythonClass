#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1350/cli/ctor/ldapconfig.py#1 $ $DateTime: 2020/01/06 01:25:43 $ $Author: saurgup5 $

"""
CLI ctor - ldapconfig
"""

import clictorbase as ccb
from sal.deprecated.expect import EXACT
from sal.containers.yesnodefault import YES, NO
from copy import deepcopy
import re

REQUIRED = ccb.REQUIRED
DEFAULT = ccb.DEFAULT


class ldapconfig(ccb.IafCliConfiguratorBase):

    """ldapconfig
    """
    newlines = 1
    def __init__(self,sess):
        ccb.IafCliConfiguratorBase.__init__(self, sess)
        self._set_local_err_dict({
            ('Please answer Yes or No', EXACT): ccb.IafCliValueError,
            ('The value cannot be blank.', EXACT): ccb.IafCliValueError,
            ('A hostname is a string that must match the following rules:',
                                       EXACT): ccb.IafCliValueError,
            ('The LDAP Server Hostname should be the hostname',
                                       EXACT): ccb.IafCliValueError,
            ('The LDAP Server Port should', EXACT): ccb.IafCliValueError,
            ('You must enter a value', EXACT): ccb.IafCliValueError,
            })

    def __call__(self):
        self._writeln('ldapconfig')
        return self

    def new(self, input_dict=None, **kwargs):
        param_map = ccb.IafCliParamMap(end_of_command = 'Choose the operation')
        param_map['server_name'] = ['create a name for this server', REQUIRED]
        param_map['host_name']   = ['hostname or IP', REQUIRED]
        param_map['ssl_using']   = ['Use SSL to connect', DEFAULT]
        param_map['auth_type']   = ['Select the authentication method',
                                     DEFAULT, 1]
        param_map['username']   = ['Please enter the bind username', REQUIRED]
        param_map['password']   = ['Please enter the bind passphrase', REQUIRED]
        param_map['retype_passwd'] = ['enter the new passphrase again', REQUIRED]
        param_map['validate_setting'] = ['validate setting', DEFAULT]
        param_map['server_type'] = ['Select the server type', DEFAULT, True]
        param_map['port']        = ['enter the port number', DEFAULT]
        param_map['base']        = ['enter the base or enter', DEFAULT]

        args = input_dict or kwargs
        param_map.update(args)
        self._query_response('NEW')
        self._process_input(param_map)
        newserver = ldapconfigOperation(self._get_sess())
        newserver.set_server_name(param_map['server_name']['answer'])
        return newserver

    def edit(self, name):
        self._query_response('EDIT')
        self._query_response(name)
        return ldapconfigEdit(self._get_sess())

    def setup(self, interface=DEFAULT, negative=DEFAULT):
        self._query_response('SETUP')
        self._query_select_list_item(interface)
        self._query_response(negative)
        self._to_the_top(self.newlines)

    def advanced(self):
        self._query_response('ADVANCED')
        return ldapconfigAdvanced(self._get_sess())

    def delete(self, name):
        self._query_response('DELETE')
        self._query_response(name)
        if self._query('Are you sure you want', \
                       'No LDAP server configurations.') == 0:
            # Confirmation to delete.
            # Question: Are you sure you want to delete them?
            self._query_response(YES)
        self._to_the_top(self.newlines)


class ldapconfigEdit(ccb.IafCliConfiguratorBase):

    """ldapconfig -> EDIT """
    newlines = 3
    __param_map = ccb.IafCliParamMap(end_of_command = 'Choose the operation')

    def __init__(self,sess):
        ccb.IafCliConfiguratorBase.__init__(self, sess)
        self._set_local_err_dict({
            ('The Query should be the actual text',
                                   EXACT): ccb.IafCliValueError,
            ('The LDAP Query Name should be a string',
                                   EXACT): ccb.IafCliValueError,
            ('The LDAP Query TTL should be the time to live in',
                                   EXACT): ccb.IafCliValueError,
            ('The LDAP Query cache size should', EXACT): ccb.IafCliValueError,
            })

        self.__param_map['name']         = ['a name for this query:', DEFAULT]
        self.__param_map['query']        = ['Enter the LDAP query string',
                                            DEFAULT]
        self.__param_map['user_base_dn'] = ['what base DN will user records',
                                             DEFAULT]
        self.__param_map['user_query']    = ['query string for user records',
                                              REQUIRED]
        self.__param_map['full_name_attr'] = ['attribute will contain the user',
                                              DEFAULT]
        self.__param_map['deny']           = ['wish to deny login to expired',
                                              DEFAULT]
        self.__param_map['grp_base_dn'] = ['what base DN will group records',
                                            DEFAULT]
        self.__param_map['grp_query']   = ['query string may be used to',
                                            REQUIRED]
        self.__param_map['member_attr'] = ['these records holds each member',
                                            DEFAULT]
        self.__param_map['grp_attr']    = ['records will contain the group',
                                            DEFAULT]
        self.__param_map['activate']      = ['activate this query', DEFAULT]
        self.__param_map['testing']       = ['Do you want to test this',
                                             DEFAULT]
        self.__param_map['test_user_id']  = ['identity to use in query:',
                                              REQUIRED]
        self.__param_map['test_group'] = ['Group name to use in query', DEFAULT]
        self.__param_map['bind_password'] = ['for testing LDAP bind:',
                                             REQUIRED]
        self.__param_map['test_grp_id']   = ['Group identity to use in query:',
                                             REQUIRED]
        self.__param_map['test_addr']     = ['Address to use in query:',
                                             REQUIRED]
        self.__param_map['isq_passwd'] = ['Passphrsae to use in query', REQUIRED]
        self.__param_map['attr_list']= ['email attribute', DEFAULT]
        self.__param_map['recpt_addr'] = ['full rfc822 email address for the recipient', DEFAULT]
        self.__param_map['mailhost'] = ['alternate mailhost for the recipient', DEFAULT]
        self.__param_map['sending'] = ['query requires one of the attributes', DEFAULT]
        self.__param_map['attribute'] = ['externally visible full rfc822 email address.', DEFAULT]
        self.__param_map['overwrite'] = ['replace the entire friendly portion', DEFAULT]
        self.__param_map['grp_member'] = ['group membership attribute', DEFAULT]
        self.__param_map['threads'] = ['concurrent connections to dedicate', DEFAULT]
        self.__param_map['smtpauth_type'] = ['BIND or by fetching the passphrase', DEFAULT, 1]
        self.__param_map['test_smtpauth'] = ['check if SMTP AUTH allowed', DEFAULT]

    def server(self):
        self._query_response('SERVER')
        return ldapconfigEditServer(self._get_sess())

    def externalauth(self, input_dict=None, **kwargs):
        self._query_response('EXTERNALAUTH')
        if self._query('Choose the operation','Please create') == 1:
            self.__param_map.update(input_dict or kwargs)
            self._process_input(deepcopy(self.__param_map))
        else:
            return ldapconfigEditExternalauth(self._get_sess())

    def isqauth(self, input_dict=None, **kwargs):
        self._query_response('ISQAUTH')
        if self._query('Choose the operation','Please create') == 1:
            self.__param_map.update(input_dict or kwargs)
            self._process_input(deepcopy(self.__param_map))
        else:
            return ldapconfigEditISQAuth(self._get_sess())

    def isqalias(self, input_dict=None, **kwargs):
        self._query_response('ISQALIAS')
        if self._query('Choose the operation','Please create') == 1:
            self.__param_map.update(input_dict or kwargs)
            self._process_input(deepcopy(self.__param_map))
        else:
            return ldapconfigEditISQAlias(self._get_sess())

    def ldapaccept(self, input_dict = None, **kwargs):
        self._query_response('LDAPACCEPT')
        if self._query('Choose the operation', 'Please create') == 1:
            self.__param_map.update(input_dict or kwargs)
            self._process_input(deepcopy(self.__param_map))
        else:
            return ldapconfigEditLDAPAccept(self._get_sess())

    def ldaprouting(self, input_dict = None, **kwargs):
        self._query_response('LDAPROUTING')
        if self._query('Choose the operation', 'Please create') == 1:
            self.__param_map.update(input_dict or kwargs)
            self._process_input(deepcopy(self.__param_map))
        else:
            return ldapconfigEditLDAPRouting(self._get_sess())

    def masquerade(self, input_dict = None, **kwargs):
        self._query_response('MASQUERADE')
        if self._query('Choose the operation', 'Please create') == 1:
            self.__param_map.update(input_dict or kwargs)
            self._process_input(deepcopy(self.__param_map))
        else:
            return ldapconfigEditMasquerade(self._get_sess())

    def ldapgroup(self, input_dict = None, **kwargs):
        self._query_response('LDAPGROUP')
        if self._query('Choose the operation', 'Please create') == 1:
            self.__param_map.update(input_dict or kwargs)
            self._process_input(deepcopy(self.__param_map))
        else:
            return ldapconfigEditLDAPGroup(self._get_sess())

    def smtpauth(self, input_dict = None, **kwargs):
        self._query_response('SMTPAUTH')
        if self._query('Choose the operation', 'Please create') == 1:
            self.__param_map.update(input_dict or kwargs)
            self._process_input(deepcopy(self.__param_map))
        else:
            return ldapconfigEditSMTPAuth(self._get_sess())


class ldapconfigAdvanced(ccb.IafCliConfiguratorBase):

    """ldapconfig -> ADVANCED """
    newlines = 3

    def new(self, input_dict=None, **kwargs):
        param_map = ccb.IafCliParamMap(end_of_command =
                                                    'Choose the operation')
        param_map['name']               = ['a name for this advanced ' \
                                                   'query:', REQUIRED]
        param_map['type']               = ['select an advanced type',
                                                      DEFAULT, True]
        param_map['query_type']         = ['select a query type', DEFAULT,
                                                                    True]
        param_map['domain']             = ['a domain to match addresses',
                                                               REQUIRED]
        param_map['query_domain']       = ['a query to associate with the',
                                                            DEFAULT, True]
        param_map['more_domain']        = ['Add another mapping', DEFAULT]
        param_map['query_chain']        = ['the number of the query to add',
                                                             REQUIRED, True]
        param_map['more_chain']         = ['Add another query to the chain',
                                                                    DEFAULT]
        param_map['use_default_query']  = ['specify a default query ' \
                                                  'to be used ', DEFAULT]
        param_map['activate'] = ['to activate this query', DEFAULT]
        param_map['default_query'] = ['Select a query to use as the default',
                                                                DEFAULT, True]
        self._query_response('NEW')
        param_map.update(input_dict or kwargs)
        self._process_input(param_map)

    def edit(self, name):
        self._query_response('EDIT')
        self._query_response(name)
        return ldapconfigAdvancedEdit(self._get_sess())

    def delete(self, name):
        self._query_response('DELETE')
        self._query_response(name)
        self._to_the_top(self.newlines)

    def print_advanced(self, name):
        self.clearbuf()
        self._query_response('PRINT')
        self._query_response(name)
        out = self._read_until('Currently configured advanced LDAP')
        self._to_the_top(self.newlines)
        return out


class ldapconfigAdvancedEdit(ccb.IafCliConfiguratorBase):

    """ldapconfig -> ADVANCED -> EDIT"""

    newlines = 3
    def new(self, input_dict=None, **kwargs):
        param_map = ccb.IafCliParamMap(end_of_command = 'Choose the operation')
        param_map['domain']        = ['a domain to match addresses', REQUIRED]
        param_map['query']         = ['a query to associate with the',
                                             DEFAULT, True]
        param_map.update(input_dict or kwargs)
        self._query_response('NEW')
        self._process_input(param_map)

    def edit(self, entry=DEFAULT, domain=DEFAULT, query=DEFAULT):
        self._query_response('EDIT')
        self._query_select_list_item(entry)
        self._query_response(domain)
        self._query_select_list_item(query)
        self._to_the_top(self.newlines + 1)

    def delete(self, entry):
        # for domain-based: entry = domain table entry
        # for chain-based:  entry = chain list entry
        self._query_response('DELETE')
        self._query_select_list_item(entry)
        self._to_the_top(self.newlines)

    def default(self, confirm=NO, query=DEFAULT):
        self._query_response('DEFAULT')
        self._query_response(confirm)
        if confirm == YES:
            self._query_select_list_item(query)
        self._to_the_top(self.newlines)

    def insert(self, query=DEFAULT, position=DEFAULT):
        self._query_response('INSERT')
        self._query_select_list_item(query)
        self._query_select_list_item(position)
        self._to_the_top(self.newlines)

    def activate(self, confirm=DEFAULT):
        self._query_response('ACTIVATE')
        self._query_response(confirm)
        self._to_the_top(self.newlines)


class ldapconfigOperation(ldapconfigEdit):
    """ldapconfig -> New->Operations(emulation) """

    __server_name = ['Unknown name']

    def __call__(self):
        self._writeln('ldapconfig')
        self._query_response('EDIT')
        self._query_response(self.__server_name[0])
        return self

    def set_server_name(self,server_name):
        self.__server_name[0]=server_name

    def server(self):
        self._query_response('SERVER')
        return ldapconfigEditServer(self._get_sess(), self.__server_name)


class ldapconfigEditServer(ccb.IafCliConfiguratorBase):
    """ldapconfig->EDIT->SERVER """
    newlines = 3

    def __init__(self,sess,server_name=' '):
        import types
        ccb.IafCliConfiguratorBase.__init__(self, sess)
        self._set_local_err_dict({
            ('The value cannot be blank.', EXACT): ccb.IafCliValueError,
            ('A hostname is a string that must match',
                                           EXACT): ccb.IafCliValueError,
            ('The LDAP Server Port should', EXACT): ccb.IafCliValueError,
            ('Please answer Yes or No', EXACT): ccb.IafCliValueError,
            })
        if type(server_name) == types.ListType:
            self.server_name = server_name

    def name(self, name=DEFAULT):
        self._query_response('NAME')
        self._query_response(name)
        if hasattr(self, 'server_name'):
            self.server_name[0] = name
        self._to_the_top(self.newlines)

    def hostname(self, host=DEFAULT):
        self._query_response('HOSTNAME')
        self._query_response(host)
        self._to_the_top(self.newlines)

    def port(self, port=DEFAULT):
        self._query_response('PORT')
        self._query_response(port)
        self._to_the_top(self.newlines)

    def servertype(self, server_type=DEFAULT):
        self._query_response('SERVERTYPE')
        self._query_select_list_item(server_type)
        self._to_the_top(self.newlines)

    def authtype(self, input_dict=None, **kwargs):
        param_map = ccb.IafCliParamMap(end_of_command = 'Choose the operation')
        param_map['auth_type']  = ['Select the authentication method',
                                   DEFAULT, 1]
        param_map['username']   = ['Please enter the bind username:',
                                   REQUIRED]
        param_map['passphrase']   = ['Press Enter to leave the passphrase unchanged', DEFAULT]
        param_map['retype_passwd'] = ['Please enter the new passphrase again', REQUIRED]
        param_map['ssl_using']  = ['Use SSL to connect', DEFAULT]
        param_map['port']       = ['enter the port number', DEFAULT]
        self._query_response('AUTHTYPE')
        args = input_dict or kwargs

        if args.get('passphrase'):
            args['retype_passwd'] = args['passphrase']
        param_map.update(args)
        self._process_input(param_map)

    def base(self, base=DEFAULT):
        self._query_response('BASE')
        self._query_response(base)
        self._to_the_top(self.newlines)

    def cache(self, input_dict=None, **kwargs):
        param_map = ccb.IafCliParamMap(end_of_command = 'Choose the operation')
        param_map['cache_ttl'] = ['the cache TTL in seconds', DEFAULT]
        param_map['max_entries'] = ['maximum number of cache entries', DEFAULT]
        param_map.update(input_dict or kwargs)
        self._query_response('CACHE')
        self._process_input(param_map)

    def compatibility(self, input_dict=None, **kwargs):
        param_map = ccb.IafCliParamMap(end_of_command = 'Choose the operation')
        param_map['enabling']    = ['to enable Microsoft Exchange', DEFAULT]
        param_map['settings_en'] = ['LDAP compatibility settings?',  DEFAULT]
        param_map['attribute']   = ['Attribute to use for', DEFAULT]
        param_map['search_scope'] = ['LDAP search scope', DEFAULT, 1]
        param_map.update(input_dict or kwargs)
        self._query_response('COMPATIBILITY')
        self._process_input(param_map)

    def connection(self, input_dict=None, **kwargs):
        param_map = ccb.IafCliParamMap(end_of_command = 'Choose the operation')
        param_map['connection']    = ['number of simultaneous connections',
                                      DEFAULT]
        param_map['request'] = ['requests be spread out over', DEFAULT, 1]
        param_map.update(input_dict or kwargs)
        self._query_response('CONNECTION')
        self._process_input(param_map)


class ldapconfigConfiguratorBase(ccb.IafCliConfiguratorBase):
    """ldapconfig->EDIT-> ISQAUTH(base operations)
                          ISQALIAS(base operations)
    """
    newlines = 3

    def __init__(self,sess):
        ccb.IafCliConfiguratorBase.__init__(self, sess)
        self._set_local_err_dict({
            ('Please answer Yes or No', EXACT): ccb.IafCliValueError,
            ('The Query should be the actual text',
                                        EXACT): ccb.IafCliValueError,
            ('The LDAP Query Name should be a string',
                                        EXACT): ccb.IafCliValueError,
            ('The LDAP Query TTL should be the time to live in cache',
                                        EXACT): ccb.IafCliValueError,
            ('The LDAP Query cache size should', EXACT): ccb.IafCliValueError,
            })

    def name(self, name=DEFAULT):
        self._query_response('NAME')
        self._query_response(name)
        self._to_the_top(self.newlines)

    def query(self, query=DEFAULT):
        self._query_response('QUERY')
        self._query_response(query)
        self._to_the_top(self.newlines)

    def cache(self, ttl=DEFAULT, num_entries=DEFAULT):
        self._query_response('CACHE')
        self._query_response(ttl)
        self._query_response(num_entries)
        self._to_the_top(self.newlines)

    def delete(self):
        self._query_response('DELETE')
        self._to_the_top(self.newlines-1)

    def emailattribute(self, email_attrs=''):
        self._query_response('EMAILATTRIBUTE')
        self._query_response(email_attrs)
        self._to_the_top(self.newlines)

    def activate(self, value=DEFAULT):
        self._query_response('ACTIVATE')
        self._query_response(value)
        self._to_the_top(self.newlines)


class ldapconfigEditExternalauth(ccb.IafCliConfiguratorBase):
    """ldapconfig->EDIT->EXTERNALAUTH """
    global ccb
    global DEFAULT, REQUIRED, EXACT
    newlines = 3

    def __init__(self,sess,server_name=' '):
        ccb.IafCliConfiguratorBase.__init__(self, sess)
        self._set_local_err_dict({
            ('Value can not be blank.', EXACT): ccb.IafCliValueError,
            ('Please enter a value.', EXACT): ccb.IafCliValueError,
            ('The Query should be the actual text',
                                           EXACT): ccb.IafCliValueError,
            })

    def name(self, name=DEFAULT):
        self._query_response('NAME')
        self._query_response(name)
        self._to_the_top(self.newlines)

    def user(self, user=DEFAULT):
        self._query_response('USER')
        self._query_response(user)
        self._to_the_top(self.newlines)

    def membership(self, membership=DEFAULT):
        self._query_response('MEMBERSHIP')
        self._query_response(membership)
        self._to_the_top(self.newlines)

    def delete(self,):
        self._query_response('DELETE')
        self._to_the_top(self.newlines - 1)

    def accountbase(self, base_dn=DEFAULT):
        self._query_response('ACCOUNTBASE')
        self._query_response(base_dn)
        self._to_the_top(self.newlines)

    def groupbase(self, base_dn=DEFAULT):
        self._query_response('GROUPBASE')
        self._query_response(base_dn)
        self._to_the_top(self.newlines)

    def fullname(self, attr=DEFAULT):
        self._query_response('FULLNAME')
        self._query_response(attr)
        self._to_the_top(self.newlines)

    def groupname(self, attr=DEFAULT):
        self._query_response('GROUPNAME')
        self._query_response(attr)
        self._to_the_top(self.newlines)

    def groupmember(self, attr=DEFAULT):
        self._query_response('GROUPMEMBER')
        self._query_response(attr)
        self._to_the_top(self.newlines)

    def expiration(self, answer=DEFAULT):
        self._query_response('EXPIRATION')
        self._query_response(answer)
        self._to_the_top(self.newlines)


class ldapconfigEditISQAuth(ldapconfigConfiguratorBase):
    """ldapconfig->EDIT-> ISQAUTH """
    newlines = 3

    def emailattribute(self, attr=DEFAULT):
        self._query_response('EMAILATTRIBUTE')
        self._query_response(attr)
        self._to_the_top(self.newlines)


class ldapconfigEditISQAlias(ldapconfigConfiguratorBase):
    """ldapconfig->EDIT-> ISQALIAS """
    pass


class ldapconfigEditLDAPAccept(ldapconfigConfiguratorBase):
    """ldapconfig->EDIT-> LDAPACCEPT """
    pass


class ldapconfigEditLDAPRouting(ldapconfigConfiguratorBase):
    """ldapconfig->EDIT-> LDAPROUTING """
    newlines = 3

    def attribute(self, sending, attr = DEFAULT, mailhost = DEFAULT):
        self._query_response('ATTRIBUTE')
        self._query_response(sending)
        self._query_response(attr)
        self._query_response(mailhost)
        self._to_the_top(self.newlines)


class ldapconfigEditMasquerade(ldapconfigConfiguratorBase):
    """ldapconfig->EDIT-> MASQUERADE"""
    newlines = 3

    def attribute(self, attribute = DEFAULT):
        self._query_response('MAILLOCALADDRESS')
        self._query_response(attribute)
        self._to_the_top(self.newlines)

    def overwrite(self, overwrite = DEFAULT):
        self._query_response('MAILLOCALADDRESSFRIENDLY')
        self._query_response(overwrite)
        self._to_the_top(self.newlines)


class ldapconfigEditLDAPGroup(ldapconfigConfiguratorBase):
    """ldapconfig->EDIT->LDAPGROUP"""
    newlines = 3

    def attribute(self, grp_member = DEFAULT):
        self._query_response('GROUPMEMBERS')
        self._query_response(grp_member)
        self._to_the_top(self.newlines)


class ldapconfigEditSMTPAuth(ldapconfigConfiguratorBase):
    """ldapconfig->EDIT->SMTPAUTH"""
    newlines = 3

    def smtpauth_type(self, smtpauth_type = DEFAULT):
        self._query_response('AUTHTYPE')
        self._query_select_list_item(smtpauth_type)
        self._to_the_top(self.newlines)

    def maxthreads(self, maxthreads = DEFAULT):
        self._query_response('MAXCONNECTIONS')
        self._query_response(maxthreads)
        self._to_the_top(self.newlines)


if __name__=="__main__":
    # session host defaults to .iafrc.DUT
    # if cli_sess is already defined, we have a CLI session object from
    # the validator we can use; if not, we must create one
    try:
        cli_sess
    except NameError:
        cli_sess = ccb.get_sess()

    ldcfg = ldapconfig(cli_sess)

    ldcfg().new(server_name='PublicLDAP', port='389',
                 host_name='trifolium.ironport.com')
    ldcfg().edit('PublicLDAP').server().name('test')
    ldcfg().edit('test').server().hostname('trifolium.ironport.com')
    ldcfg().edit('test').server().authtype(auth_type='Anonymous',ssl_using=NO)
    ldcfg().edit('test').server().servertype(server_type='OpenLDAP')
    ldcfg().edit('test').server().name('PublicLDAP')
    ldcfg().edit('PublicLDAP').server().compatibility(enabling=YES,
                                                    settings_en=YES,
                                                    attribute='test')
    ldcfg().edit('PublicLDAP').server().connection(connection=5, request=2)
    ldcfg().edit(name='PublicLDAP').externalauth( \
        user_query='(&(objectClass=posixAccount)(uid={u}))',
        grp_query='(&(objectClass=posixGroup)(memberUid={u}))',
        all_users_query='(&(objectClass=posixGroup)(cn={g}))',
        test_user_id='extauth',
        bind_password='bind',
        test_grp_id='foo')
    ldcfg().edit(name='PublicLDAP').externalauth().fullname()
    ldcfg().edit(name='PublicLDAP').externalauth().groupmember()
    ldcfg().edit(name='PublicLDAP').externalauth().expiration()
    ldcfg().edit(name='PublicLDAP').externalauth().delete()
    ldcfg().edit(name='PublicLDAP').isqauth(name='isqauth_test',
                                            query='(mailLocalAddress={a})',
                                            attr_list='mail',
                                            test_user_id='karls01',
                                            isq_passwd='ironport')
    ldcfg().edit(name='PublicLDAP').isqauth().emailattribute('mail')
    ldcfg().edit(name='PublicLDAP').isqauth().name('new_isqauth_name')
    ldcfg().edit(name='PublicLDAP').isqalias(name='isqalias_test',
                                             query='(mailLocalAddress={a})',
                                             attr_list='mail',
                                             test_addr='testuser@mail.qa')
    ldcfg().edit(name='PublicLDAP').isqalias().emailattribute('mail')
    ldcfg().edit(name='PublicLDAP').isqalias().name('new_isqalias_name')
    ldcfg().delete(name='PublicLDAP')
