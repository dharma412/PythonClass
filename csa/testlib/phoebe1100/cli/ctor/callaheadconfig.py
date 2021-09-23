#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1100/cli/ctor/callaheadconfig.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $

"""
IAF 2 CLI command: callaheadconfig
"""

# import clictorbase properly depending on automation or dev env
# if automation, import the classes and constants we'll need

import clictorbase as ccb

from sal.containers.yesnodefault import YES, NO
from sal.deprecated.expect import EXACT
from sal.exceptions import TimeoutError

REQUIRED = ccb.REQUIRED
DEFAULT = ccb.DEFAULT
NO_DEFAULT = ccb.NO_DEFAULT

DEBUG = True


class callaheadconfig(ccb.IafCliConfiguratorBase):

    def __call__(self):
        self._writeln('callaheadconfig')
        return self

    def new(self, input_dict=None, **kwargs):
        ''' This code needs to be optimized later'''
        input_dict = input_dict or kwargs
        param_map = ccb.IafCliParamMap(end_of_command='Choose the operation')
        param_map['profile_type'] = ['Select the type of profile', \
                                     DEFAULT, True]
        param_map['profile_name'] = ['Please enter a name for the profile', \
                                     DEFAULT]
        param_map['call_ahead_servers'] = \
            ['Enter one or more Call-Ahead servers hostname', DEFAULT]
        param_map['advanced_settings'] = ['change advanced settings', DEFAULT]
        param_map['mail_from'] = ['Enter MAIL FROM address', DEFAULT]
        param_map['ip_interface'] = ['choose an IP interface for this profile' \
            , DEFAULT]
        param_map['request_timeout'] = ['Specify the validation request timeout', \
                                        DEFAULT]
        param_map['action_for_recipients'] = \
            ['the default action for non-verifiable recipients', DEFAULT, True]
        param_map['action_for_failure'] = ['default action for temporary failure', \
                                           DEFAULT, True]
        param_map['smtp_code'] = ['custom SMTP response code', DEFAULT]
        new_dict = {}
        self._query_response('NEW')
        if input_dict.has_key('smtp_text') \
                and input_dict['action_for_failure'] == '2':
            for param in input_dict.keys():
                if param in param_map._map.keys():
                    new_dict[param] = input_dict[param]
        if not input_dict.has_key('smtp_text'):
            param_map['smtp_text'] = ['custom SMTP response text', DEFAULT]
            param_map['max_rcpt_session'] = \
                ['maximum number of recipients to validate per SMTP session', DEFAULT]
            param_map['max_simultaneous_conn'] = \
                ['maximum number of simultaneous connections', DEFAULT]
            param_map['cache_entries'] = ['Enter cache entries', DEFAULT]
            param_map['cache_ttl'] = ['Enter cache TTL', DEFAULT]
            param_map.update(input_dict or kwargs)
            self._process_input(param_map)

        else:
            param_map.update(new_dict or kwargs)

        if input_dict.has_key('smtp_text') and input_dict['action_for_failure'] == '2':
            param_map.set_ending_string("Enter the custom SMTP response text")
            self._process_input(param_map, do_restart=False)
            self._writeln(input_dict['smtp_text'])
            self._writeln()
            param_map1 = ccb.IafCliParamMap(end_of_command='Choose the operation')
            new_dict1 = {}
            for param in input_dict.keys():
                if param not in param_map._map.keys() and param != 'smtp_text':
                    new_dict1[param] = input_dict[param]
            param_map1['max_rcpt_session'] = \
                ['maximum number of recipients to validate per SMTP session', DEFAULT]
            param_map1['max_simultaneous_conn'] = \
                ['maximum number of simultaneous connections', DEFAULT]
            param_map1['cache_entries'] = ['Enter cache entries', DEFAULT]
            param_map1['cache_ttl'] = ['Enter cache TTL', DEFAULT]
            param_map1.update(new_dict1)
            self._process_input(param_map1)

    def edit(self, input_dict=None, **kwargs):
        input_dict = input_dict or kwargs
        param_map = ccb.IafCliParamMap(end_of_command='Choose the operation')
        param_map['profile_edit'] = ['Select the profile you want to edit', \
                                     DEFAULT]
        param_map['profile_name'] = ['Please enter a name for the profile', \
                                     DEFAULT]
        param_map['profile_type'] = ['Select the type of profile', \
                                     DEFAULT, True]
        param_map['call_ahead_servers'] = \
            ['Enter one or more Call-Ahead servers hostname', DEFAULT]
        param_map['advanced_settings'] = ['change advanced settings', DEFAULT]
        param_map['mail_from'] = ['Enter MAIL FROM address', DEFAULT]
        param_map['ip_interface'] = ['choose an IP interface for this profile', \
                                     DEFAULT]
        param_map['request_timeout'] = \
            ['Specify the validation request timeout', DEFAULT]
        param_map['action_for_recipients'] = \
            ['the default action for non-verifiable recipients', DEFAULT, True]
        param_map['action_for_failure'] = \
            ['default action for temporary failure', DEFAULT, True]
        param_map['smtp_code'] = ['custom SMTP response code', DEFAULT]

        new_dict = {}
        self._query_response('EDIT')
        if input_dict.has_key('smtp_text') \
                and input_dict['action_for_failure'] == '2':
            for param in input_dict.keys():
                if param in param_map._map.keys():
                    new_dict[param] = input_dict[param]
        if not input_dict.has_key('smtp_text'):
            param_map['smtp_text'] = ['custom SMTP response text', DEFAULT]
            param_map['max_rcpt_session'] = \
                ['maximum number of recipients to validate per SMTP session', DEFAULT]
            param_map['max_simultaneous_conn'] = \
                ['maximum number of simultaneous connections', DEFAULT]
            param_map['cache_entries'] = ['Enter cache entries', DEFAULT]
            param_map['cache_ttl'] = ['Enter cache TTL', DEFAULT]
            param_map.update(input_dict or kwargs)
            self._process_input(param_map)

        else:
            param_map.update(new_dict or kwargs)

        if input_dict.has_key('smtp_text') \
                and input_dict['action_for_failure'] == '2':
            param_map.set_ending_string("Enter the custom SMTP response text")
            self._process_input(param_map, do_restart=False)
            self._writeln(input_dict['smtp_text'])
            self._writeln()
            param_map1 = ccb.IafCliParamMap(end_of_command='Choose the operation')
            new_dict1 = {}
            for param in input_dict.keys():
                if param not in param_map._map.keys() and param != 'smtp_text':
                    new_dict1[param] = input_dict[param]
            param_map1['max_rcpt_session'] = \
                ['maximum number of recipients to validate per SMTP session', DEFAULT]
            param_map1['max_simultaneous_conn'] = \
                ['maximum number of simultaneous connections', DEFAULT]
            param_map1['cache_entries'] = ['Enter cache entries', DEFAULT]
            param_map1['cache_ttl'] = ['Enter cache TTL', DEFAULT]
            param_map1.update(new_dict1)
            self._process_input(param_map1)

    def delete(self, profile_name=REQUIRED):
        self.newline = 1
        self._query_response('DELETE')
        self._query_select_list_item(profile_name, exact_match=True)
        self._to_the_top(self.newline)

    def print_method(self, profile_name=DEFAULT):
        self._query_response('PRINT')
        self._query_select_list_item(profile_name)
        self._expect('\n')
        printinfo = self._read_until('Choose the operation')
        self._to_the_top(1)
        return printinfo

    def test(self, profile_name, address, ldap=DEFAULT):
        self.clearbuf()
        self._query_response('TEST')
        self._query_select_list_item(profile_name)
        self._query_response(address)
        try:
            ldapmatch = self._read_until(self._sub_prompt_user_match, timeout=3)
            if ldapmatch.find('LDAP-Routing query') != -1:
                self._sess.writeln(ldap)
        except TimeoutError:
            pass
        self._expect('\n')
        testinfo = self._read_until('test using another recipient address')
        self._query_response('N')
        self._to_the_top(1)
        return testinfo

    def flushcache(self, profile_name='all', confirm=DEFAULT):
        self._query_response('flushcache')
        self._query_select_list_item(profile_name)
        self._query_response(confirm)
        self._to_the_top(1)


if __name__ == '__main__':
    # if cli_sess is already defined, we have a CLI session object from
    # the validator we can use; if not, we must create one
    try:
        cli_sess
    except NameError:
        cli_sess = ccb.get_sess()
    ca = callaheadconfig(cli_sess)
    input_dict = {'profile_type': 1, 'profile_name': 'test', \
                  'advanced_settings': 'y', 'max_rcpt_session': 2}
    ca().new(input_dict)
    input_dict = {'profile_edit': '1', 'profile_type': 2, \
                  'profile_name': 'test', 'call_ahead_servers': 'ss.com', \
                  'advanced_settings': 'y', \
                  'max_rcpt_session': 3, 'action_for_failure': '2', \
                  'smtp_code': 460, 'smtp_text': 'smtp fail'}
    ca().edit(input_dict)
    input_dict1 = {'profile_edit': '1', 'profile_type': 2, \
                   'profile_name': 'test', 'call_ahead_servers': 'ss.com', \
                   'advanced_settings': 'y', \
                   'max_rcpt_session': 3, 'action_for_failure': '1'}
    ca().edit(input_dict1)
    print ca().print_method(profile_name='1')
    print ca().test(profile_name='1', address='ss@ss.com')
    input_dict2 = {'profile_type': 1, 'profile_name': 'test1', \
                   'advanced_settings': 'y', 'max_rcpt_session': 3, \
                   'action_for_failure': '2', 'smtp_code': 460, 'smtp_text': 'smtp fail'}
    ca().new(input_dict2)
    print ca().test(profile_name='2', address='ss@ss.com', ldap='1')
    ca().flushcache(profile_name='2', confirm='y')
    ca().delete(profile_name='1')
