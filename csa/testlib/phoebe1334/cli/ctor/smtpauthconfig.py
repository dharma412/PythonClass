#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1350/cli/ctor/smtpauthconfig.py#1 $ $DateTime: 2020/01/06 01:25:43 $ $Author: saurgup5 $

"""
SARF CLI command: smtpauthconfig
"""
import clictorbase as ccb
import types
from sal.containers.yesnodefault import NO, YES, is_yes
from sal.exceptions import ConfigError

DEBUG = True
REQUIRED = ccb.REQUIRED
DEFAULT = ccb.DEFAULT

class smtpauthconfig(ccb.IafCliConfiguratorBase):


    def __call__(self):
        self._writeln(self.__class__.__name__)
        return self

    def new(self):
        self._query_response('NEW')
        return smtpauthconfigNew(self._get_sess())

    def edit_forward(self,
             name=DEFAULT,
             new_name=DEFAULT,
             confirm_in_use_delete=DEFAULT):
        self._query_response('EDIT')
        self._query_select_list_item(name)
        self._query_response(new_name)
        lines = self._read_until(self._sub_prompt_user_match)
        if lines.find('listener') >= 0:
            self._writeln(confirm_in_use_delete)
            lines = self._read_until(self._sub_prompt_user_match)
        return smtpauthconfigEditForward(self._get_sess())

    def edit_ldap(self,
             name=DEFAULT,
             new_name=DEFAULT,
             confirm_in_use_delete=DEFAULT,
             query_name=DEFAULT):
        self._query_response('EDIT')
        self._query_select_list_item(name)
        self._query_response(new_name)
        lines = self._read_until(self._sub_prompt_user_match)
        if lines.find('listener') >= 0:
            self._writeln(confirm_in_use_delete)
            lines = self._read_until(self._sub_prompt_user_match)
        self._select_list_item(query_name, lines)
        self._query_response(NO)
        self._query_response(NO)
        self._to_the_top(1)

    def edit_outgoing(self, input_dict=None, **kwargs):
        param_map = ccb.IafCliParamMap(end_of_command='Choose the operation')
        param_map['name'] = ['Select the profile', DEFAULT, 1]
        param_map['new_name'] = ['name for this profile', DEFAULT]
        param_map['confirm_in_use_delete'] = ['listener', DEFAULT]
        param_map['username'] = ['the SMTP authentication username', DEFAULT]
        param_map['password'] = ['the SMTP authentication passphrase', DEFAULT]
        param_map.update(input_dict or kwargs)
        self._query_response('EDIT')
        self._process_input(param_map)

    def print_all(self):
        self._query_response('PRINT')
        self._expect('SMTP Authentication Profiles')
        raw = self._read_until('Choose the operation')
        lst = (raw.split('Name: '))[1:]
        self._restart()
        return lst

    def delete(self, input_dict=None, **kwargs):
        param_map = ccb.IafCliParamMap(end_of_command='Choose the operation')
        param_map['name'] = ['Select the profile', DEFAULT, 1]
        param_map['confirm_delete'] = ['delete this SMTP Auth profile', 'y']
        param_map['confirm_in_use_delete'] = ['listener', DEFAULT]
        param_map.update(input_dict or kwargs)

        self._query_response('DELETE')
        return self._process_input(param_map)

    def clear(self, input_dict=None, **kwargs):
        param_map = ccb.IafCliParamMap(end_of_command='Choose the operation')
        param_map['confirm_clear']        = ['want to erase', DEFAULT]
        param_map['confirm_in_use_clear'] = ['invalidate your config', DEFAULT]
        param_map.update(input_dict or kwargs)

        self._query_response('CLEAR')
        return self._process_input(param_map)

    def clusterset(self):
        raise ccb.IafCliCtorNotImplementedError

    def clustershow(self):
        raise ccb.IafCliCtorNotImplementedError

class smtpauthconfigNew(ccb.IafCliConfiguratorBase):
    """smtpauthconfig -> NEW """

    def forward(self, input_dict=None, **kwargs):
        self._query_response('FORWARD')
        param_map = ccb.IafCliParamMap(end_of_command='Choose the operation')
        param_map['name'] = \
        ['Enter a name for this profile', REQUIRED]
        param_map['hostname'] = \
        ['Enter a hostname or an IP address for the forwarding server', REQUIRED]
        param_map['port'] = ['Enter a port', DEFAULT]
        param_map['interface'] = \
        ['Choose the interface to use for forwarding requests', DEFAULT, 1]
        param_map['tls'] = ['Require TLS?', DEFAULT]
        param_map['max_conn'] = \
        ['the maximum number of simultaneous connections allowed', DEFAULT]
        param_map['use_plain'] = \
        ['PLAIN mechanism when contacting forwarding server', DEFAULT]
        param_map['use_login'] = \
        ['LOGIN mechanism when contacting forwarding server', DEFAULT]
        param_map['another_server'] = \
        ['like to enter another forwarding server to this group?', DEFAULT]
        param_map.update(input_dict or kwargs)
        self._process_input(param_map)

    def outgoing(self, name, username, password):
        self._query_response('OUTGOING')
        self._query_response(name)
        self._query_response(username)
        self._writeln(password)
        self._restart()

    def ldap(self, name, query_name=''):
        self._query_response('LDAP')
        self._query_response(name)
        self._query_select_list_item(query_name)
        #Would you like to specify a default encryption
        #method to be assumed by the appliance when making SMTP AUTH queries if
        #the encryption method is not prefixed in the query result? (recommended
        #for OpenWave LDAP servers only
        self._query_response(NO)
        self._query_response(NO)
        self._to_the_top(1)

class smtpauthconfigEditForward(ccb.IafCliConfiguratorBase):
    """smtpauthconfig -> EDIT (forwarding profile)"""

    def new(self, input_dict=None, **kwargs):
        param_map = ccb.IafCliParamMap(end_of_command='Choose the operation')
        param_map['hostname']               = ['Enter a hostname', REQUIRED]
        param_map['port']                   = ['Enter a port', DEFAULT]
        param_map['interface']              = ['Choose the interface', DEFAULT]
        param_map['tls']                    = ['Require TLS', DEFAULT]
        param_map['max_conn']               = ['Enter the maximum', DEFAULT]
        param_map['use_plain']              = ['Use SASL PLAIN', DEFAULT]
        param_map['use_login']              = ['Use SASL LOGIN', DEFAULT]
        param_map.update(input_dict or kwargs)

        self._writeln('NEW')
        return self._process_input(param_map)

    def edit(self, input_dict=None, **kwargs):
        param_map = ccb.IafCliParamMap(end_of_command='Choose the operation')

        param_map['server_name']            = ['Choose the server', DEFAULT, 1]
        param_map['hostname']               = ['Enter a hostname', DEFAULT]
        param_map['port']                   = ['Enter a port', DEFAULT]
        param_map['interface']              = ['Choose the interface', DEFAULT]
        param_map['tls']                    = ['Require TLS', DEFAULT]
        param_map['max_conn']               = ['Enter the maximum', DEFAULT]
        param_map['use_plain']              = ['Use SASL PLAIN', DEFAULT]
        param_map['use_login']              = ['Use SASL LOGIN', DEFAULT]
        param_map.update(input_dict or kwargs)

        self._writeln('EDIT')
        return self._process_input(param_map)

    def delete(self, server_name=DEFAULT):
        self._writeln('DELETE')
        self._expect(['must contain', 'select a server'])
        if self._expectindex == 0:
            raise ConfigError
        if self._expectindex == 1:
            self._query_select_list_item(server_name)
            self._restart()

    def print_all(self):
        self._writeln('PRINT')
        lines = self._read_until('Choose the operation')
        lst = (lines.split('\r\n'))[4:-2]
        for i in range(len(lst)/2):
            lst[i] = lst[i*2] + ' ' + lst[i*2+1]
        lst = lst[0:len(lst)/2]
        self._restart()
        return lst
