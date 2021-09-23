#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/cli/ctor/userconfig.py#2 $
# $DateTime: 2019/11/20 00:33:52 $
# $Author: uvelayut $

import sys
import re

import clictorbase
import sal.containers.yesnodefault as yesnodefault
from clictorbase import IafCliConfiguratorBase,IafCliError, \
    REQUIRED, DEFAULT
from sal.deprecated.expect import REGEX, EXACT
import sal.containers.yesnodefault as yesnodefault

DEBUG = True

class ValueError(IafCliError): pass
class PasswordError(IafCliError): pass
class UnknownOptionError(IafCliError): pass
class YesNoError(IafCliError): pass

class userconfigExternal(clictorbase.IafCliConfiguratorBase):
    """Setup for External authentication
    """
    newlines = 2

    def __init__(self, sess):
        IafCliConfiguratorBase.__init__(self, sess)
        self._set_local_err_dict(
            {
                ('Unknown option', EXACT) :                         UnknownOptionError,
                ('Please answer Yes or No.', EXACT) :          YesNoError,
                ('The value must be an integer.', EXACT) :  ValueError,
                ('You must enter a value from', EXACT) :    ValueError,
            }
        )

    def setup(self, enable='n', timeout=DEFAULT, mechanism=DEFAULT, auth_mode=DEFAULT):

        auth_mode = auth_mode.lower()

        self._query_response('SETUP')

        if yesnodefault.is_no(enable):
            self._query_response(enable)
            self._to_the_top(self.newlines)

        else:
            self._query_response(enable)

            if auth_mode == 'password':
                self._query_select_list_item('Password Based')
                #self._query_response('2')

            elif auth_mode == 'client':
                self._query_select_list_item('Certificate Based')
                #self._query_response('1')

            else:
                self._query_response('')

            self._query_response(timeout)
            self._query_select_list_item(mechanism)
            return userconfigExternalSetup(self._get_sess())

    def groups(self):
        self._query_response('GROUPS')
        return userconfigExternalGroups(self._get_sess())

class userconfigExternalSetup(clictorbase.IafCliConfiguratorBase):

    """External authentication
    """
    newlines = 3

    class IpHostnameError(IafCliError): pass

    def __init__(self, sess):
        IafCliConfiguratorBase.__init__(self, sess)
        self._set_local_err_dict(
            {
                ('Unknown option', EXACT) : UnknownOptionError,
                ('Please answer Yes or No.', EXACT) : YesNoError,
                ('The value must be an integer.', EXACT) : ValueError,
                ('You must enter a value from', EXACT) : ValueError,
                ('The address must be a hostname or an IP.', EXACT) : \
                    self.IpHostnameError,
                ('A port must be a number from ', EXACT) : ValueError,
                ('The timeout value should be ', EXACT) : ValueError,
                ('A port must be a number from ', EXACT) : PasswordError,
             }
        )

    def ldap(self,
        query_name=DEFAULT,
        auth_timeout=DEFAULT,
        group_name=REQUIRED,
        group=DEFAULT,
        ):
        self.newlines = 2
        self._query_select_list_item(query_name)
        self._query_response(auth_timeout)
        self._query_response(group_name)
        self._query_select_list_item(group)
        self._to_the_top(self.newlines)

    def new(self, hostname_or_ip=REQUIRED, port=DEFAULT, password=REQUIRED,
            reply_timeout=DEFAULT, auth_type=DEFAULT, create_mapping=DEFAULT,
            delete_mapping=DEFAULT, group_name=REQUIRED, mapping_type=DEFAULT,
            cert_name=DEFAULT, ocsp_validate=DEFAULT, auth_protocol=DEFAULT):

        self.newlines = 2
        auth_protocol = auth_protocol.lower()

        if auth_protocol == 'tls':
            self._query_select_list_item('TLS')
        elif auth_protocol == 'udp':
            self._query_select_list_item('UDP')
        else:
            auth_protocol = 'udp'
            self._query_response('')

        self._query_response('NEW')
        self._query_response(hostname_or_ip)
        self._query_response(port)

        if auth_protocol == 'udp':
            self._query("Please enter the shared password")
            self._writeln(password)
            self._query("Please enter the new password again")
            self._writeln(password)

        self._query_response(reply_timeout)
        self._query_select_list_item(auth_type)
        self._query("Choose the operation you want to perform:")
        self._query_response(DEFAULT)

        if auth_protocol == 'tls':
            self._query_select_list_item(cert_name)
            self._query_response(DEFAULT)

        try:
            self._expect(
                [
                    'Do you want to create mappings',
                    'Do you want to delete all'
                ],
                timeout=3
            )

            if self._expectindex == 0:
                if yesnodefault.is_no(create_mapping):
                    self._query_response(create_mapping)
                else:
                    self._query_response(create_mapping)
                    self._query_response(group_name)
                    self._query_response(mapping_type)
            else:
                self._query_response(delete_mapping)

        except:
            self._info('Mappings were not done. Expect Index: %d' %self._expectindex)

        if auth_protocol == 'tls':
            self._query_response(ocsp_validate)
            if ocsp_validate.lower() == 'y':
                self._query_response(DEFAULT)
                self._query_response(DEFAULT)
                self._query_response(DEFAULT)
                self._query_response(DEFAULT)
                self._query_response(DEFAULT)

        self._to_the_top(self.newlines)

    def edit(self, server=DEFAULT, hostname_or_ip=DEFAULT, port=DEFAULT,
             password=DEFAULT, reply_timeout=DEFAULT, auth_type=DEFAULT,
             create_mapping=DEFAULT, delete_mapping=DEFAULT,
             group_name=REQUIRED, mapping_type=DEFAULT,auth_protocol=DEFAULT):
        self._query("Choose an External Auth Protocol to use:")
        self._query_response(DEFAULT)
        self._query_response('EDIT')
        self._query_select_list_item(server)
        self._query_response(hostname_or_ip)
        self._query_response(port)
        self._query_response(password)
        self._expect(['Please enter the new',
                      'Please enter timeout in seconds'], timeout=3)

        if self._expectindex == 0:
           self._writeln(password)

        self._query_response(reply_timeout)
        self._query_select_list_item(auth_type)
        self._query_response(DEFAULT)
        self._expect(['Do you want to create mappings',
                      'Do you want to delete all'], timeout=3)

        if self._expectindex == 0:

            if yesnodefault.is_no(create_mapping):
                self._query_response(create_mapping)
            else:
                self._query_response(create_mapping)
                self._query_response(group_name)
                self._query_response(mapping_type)
        else:
            self._query_response(delete_mapping)

        self._to_the_top(self.newlines)

    def delete(self, server_to_delete=DEFAULT, delete_mapping=DEFAULT,
               create_mapping=DEFAULT, group_name=REQUIRED,
               mapping_type=DEFAULT):
        self._query("Choose an External Auth Protocol to use:")
        self._query_response(DEFAULT)
        self._query_response('DELETE')
        self._query_select_list_item(server_to_delete)
        self._query_response(DEFAULT)
        self._expect(['Do you want to create mappings',
                      'Do you want to delete all'], timeout=3)
        if self._expectindex == 0:
            if yesnodefault.is_no(create_mapping):
                self._query_response(create_mapping)
            else:
                self._query_response(create_mapping)
                self._query_response(group_name)
                self._query_response(mapping_type)
        else:
            self._query_response(delete_mapping)
        self._to_the_top(self.newlines)

    def move(self, server_to_move=DEFAULT, target_server=DEFAULT,
             delete_mapping=DEFAULT, create_mapping=DEFAULT,
             group_name=REQUIRED, mapping_type=DEFAULT):
        self._query("Choose an External Auth Protocol to use:")
        self._query_response(DEFAULT)
        self._query_response('MOVE')
        self._query_select_list_item(server_to_move)
        self._query_response(target_server)
        self._query_response(DEFAULT)
        self._expect(['Do you want to create mappings',
                      'Do you want to delete all'], timeout=3)
        if self._expectindex == 0:
            if yesnodefault.is_no(create_mapping):
                self._query_response(create_mapping)
            else:
                self._query_response(create_mapping)
                self._query_response(group_name)
                self._query_response(mapping_type)
        else:
            self._query_response(delete_mapping)
        self._to_the_top(self.newlines)

    def clear(self, confirm=DEFAULT):
        self._query("Choose an External Auth Protocol to use:")
        self._query_response(DEFAULT)
        self._query_response('CLEAR')
        self._query_response(confirm)
        self._to_the_top(self.newlines)

class userconfig(clictorbase.IafCliConfiguratorBase):
    """userconfig
    """
    newlines = 1

    class UserRestrictedError(IafCliError): pass
    class DeleteSelfError(IafCliError): pass

    def __init__(self, sess):
        IafCliConfiguratorBase.__init__(self, sess)
        self._set_local_err_dict({
             ('User \S+ cannot be modified', REGEX): self.UserRestrictedError,
             ('User \S+ cannot be deleted', REGEX): self.UserRestrictedError,
             ('You cannot delete yourself', EXACT) : self.DeleteSelfError,
             ('criteria for passphrase are not met', EXACT) : ValueError,
             })

    def __call__(self):
        self._writeln('userconfig')
        return self

    def new(self, user_name=REQUIRED, full_name=REQUIRED, password=REQUIRED,
                                                                group=DEFAULT):
        self._query_response('NEW')
        try:
            self._query_response(user_name)
            self._query_response(full_name)
            self._query_select_list_item(group)
            self._query("Enter the passphrase for")
            self._writeln(password)
            self._query("Please enter the new passphrase again")
            self._writeln(password)
            self._to_the_top(self.newlines)
        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            self.interrupt()
            raise exc_type, exc_value, exc_traceback

    def edit(self, user_name=REQUIRED, full_name=DEFAULT, password=DEFAULT,
                                                                group=DEFAULT):
        self._query_response('EDIT')
        try:
            self._query_response(user_name)
            self._query_response(full_name)
            self._query_select_list_item(group)
            self._query_response(password)
            if password:
                self._query("Please enter the new passphrase again")
                self._writeln(password)
            self._to_the_top(self.newlines)
        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            self.interrupt()
            raise exc_type, exc_value, exc_traceback

    def delete(self, user_name=REQUIRED, confirm=DEFAULT):
        self._query_response('DELETE')
        self._query_response(user_name)
        self._query_response(confirm)
        self._to_the_top(self.newlines)


    def policy_passwdStrength(self, **kwargs):
        self._query_response('POLICY')
        self._query_response('PASSWORDSTRENGTH')
        param_map = \
            clictorbase.IafCliParamMap(end_of_command='Choose the operation')
        param_map['min_num'] = ['Specify the minimum number', DEFAULT]
        param_map['require_one_upper_lower_letter'] = \
            ['Require at least one upper', DEFAULT]
        param_map['require_number'] = \
            ['Require at least one number', DEFAULT]
        param_map['require_special_character'] = \
            ['Require at least one special character', DEFAULT]
        param_map['reject_password_as_username'] = \
            ['Reject passphrases similar to the username', DEFAULT]
        param_map['ban_last_password'] = \
            ['Ban reuse of last passphrases', DEFAULT]
        param_map['no_last_passwords'] = \
            ['Specify the  number of the most recent passphrases', DEFAULT]
        param_map['word_disallow'] = \
            ['Use a list of words to disallow in passphrases', DEFAULT]
        param_map['administrator_entropy'] = \
            ['Assign base entropy value for Administrators', DEFAULT]
        param_map['operators_entropy'] = \
            ['Assign base entropy value for Operators', DEFAULT]
        param_map['guests_entropy'] = \
            ['Assign base entropy value for Guests', DEFAULT]
        param_map['read_only_operator_entropy'] = \
            ['Assign base entropy value for Read-Only Operators', DEFAULT]

        param_map.update(kwargs)
        return self._process_input(param_map, timeout=5)

    def policy_account_expiration(self, **kwargs):
        self._query_response('POLICY')
        self._query_response('ACCOUNT')
        param_map = \
            clictorbase.IafCliParamMap(end_of_command='Choose the operation')
        param_map['lock_account'] = \
            ['Do you want to automatically lock account', 'N']
        param_map['locked_message'] = \
            ['Do you want to display the account locked message', 'N']

        #Enable passpharse expiration
        param_map['enable_passphrase_expiration'] = \
            ['Do you want to enable passphrase expiration', DEFAULT]
        param_map['passpharse_expiration_duration'] = \
            ['Enter the passphrase expiration period in days', DEFAULT]

        #Passphare expiration reminder question
        param_map['passphrase_expiration_reminder'] = \
            ['Do you want to display reminder about passphrase expiration', DEFAULT]
        param_map['passphrase_expiration_reminder_duration'] = \
            ['Enter the period before user\'s passphrase change time', DEFAULT]

        #Passpharse expiration grace period
        param_map['passpharse_expiration_grace_period'] = \
            ['Do you want to enable passphrase grace period', DEFAULT]
        param_map['passphrase_expiration_grace_period_duration'] = \
            ['Enter the period after user\'s passphrase change time', DEFAULT]

        param_map['passphrase_reset'] = \
            ['Do you want to require a passphrase reset', 'N']

        param_map.update(kwargs)
        return self._process_input(param_map, timeout=5)


    def password(self, user_name=DEFAULT, new_password=DEFAULT,
        action='assign',when='instant'):
        self._query_response('PASSWORD')
        self._query('ASSIGN - Manually assign')
        self._query_response(action)
        if action.lower() == 'assign':
            self._query('Enter the username')
            self._query_response(user_name)
            self._query("Enter the new passphrase for")
            self._writeln(new_password)
            self._query("Please enter the new passphrase again")
            self._writeln(new_password)
        else:
            self._query('LATER')
            self._query_response(when)
        self._to_the_top(self.newlines)

    def external(self):
        self._query_response('EXTERNAL')
        return userconfigExternal(self._get_sess())

    def access(self):
        raise clictorbase.IafCliCtorNotImplementedError

class userconfigExternalGroups(clictorbase.IafCliConfiguratorBase):
    """Configure external group mapping:
       userconfig -> external -> groups
    """
    newlines = 3

    def __init__(self, sess):
        IafCliConfiguratorBase.__init__(self, sess)

    def new(self, group_name=REQUIRED, mapping_type=DEFAULT):
        self._query_response('NEW')
        self._query_response(group_name)
        self._query_select_list_item(mapping_type)
        self._to_the_top(self.newlines)

    def edit(self, group_name=DEFAULT, mapping_type=DEFAULT):
        self._query_response('EDIT')
        self._query_select_list_item(group_name)
        self._query_select_list_item(mapping_type)
        self._to_the_top(self.newlines)

    def delete(self, group_name=DEFAULT):
        self._query_response('DELETE')
        self._query_select_list_item(group_name)
        self._to_the_top(self.newlines)

    def clear(self):
        self._query_response('CLEAR')
        self._to_the_top(self.newlines)

    def print_mappings(self):
        self.clearbuf()
        self._query_response('PRINT')
        self._expect(['-Press Any Key For More-', 'Choose the operation'],
                     timeout=3)
        raw = self.getbuf()
        while self._expectindex == 0:
            self._writeln('')
            self._expect(['-Press Any Key For More-', 'Choose the operation'],
                         timeout=3)
            raw = self.getbuf()
        self._to_the_top(self.newlines)
        return raw

