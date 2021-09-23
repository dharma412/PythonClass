#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1210/cli/ctor/userconfig.py#1 $

import clictorbase
from clictorbase import IafCliConfiguratorBase, IafCliError, \
    REQUIRED, DEFAULT

from sal.deprecated.expect import REGEX, EXACT
from sal.exceptions import ConfigError
from sal.containers.yesnodefault import YES, NO, is_no
from credentials import *
import re

DEBUG = True


class userconfig(clictorbase.IafCliConfiguratorBase):
    """userconfig
    """

    newlines = 1

    class UserRestrictedError(IafCliError):
        pass

    class DeleteSelfError(IafCliError):
        pass

    def __init__(self, sess):
        IafCliConfiguratorBase.__init__(self, sess)

        self._set_local_err_dict({
            ('User \S+ cannot be modified', REGEX): self.UserRestrictedError,
            ('User \S+ cannot be deleted', REGEX): self.UserRestrictedError,
            ('You cannot delete yourself', EXACT): self.DeleteSelfError,
        })

    def __call__(self):
        self._writeln('userconfig')
        return self

    def new(self, admin_passphrase=None, user_name=REQUIRED, full_name=REQUIRED, system_generate_password=NO,
            password=REQUIRED, confirm_password=None, group=DEFAULT):
        confirm_password = confirm_password or password
        admin_passphrase = admin_passphrase or DUT_ADMIN_SSW_PASSWORD

        self._query_response('NEW')
        self._expect(['Enter your Passphrase to make changes:', ], timeout=5)
        self._writeln(admin_passphrase)
        self._query_response(user_name)
        self._query_response(full_name)
        self._query_select_list_item(group)
        sys_gen_passwd = ''
        self._query_response(system_generate_password)
        if re.match(r'yes|y', str(system_generate_password), re.I):
            sys_gen_passwd_output = \
                self._read_until('want to proceed with this')
            self._info(sys_gen_passwd_output)
            self._query_response(YES)
            sys_gen_passwd = re.search( \
                r'your system generated passphrase:\s+(.*)\n', \
                sys_gen_passwd_output, re.I | re.M)
            sys_gen_passwd = sys_gen_passwd.group(1).strip()
        else:
            self._query_response(password)
            self._writeln(confirm_password)
        self._to_the_top(self.newlines)

        return sys_gen_passwd

    def edit(self, admin_passphrase=None, user_name=REQUIRED, full_name=DEFAULT, system_generate_password=NO,
             password=DEFAULT, confirm_password=None, group=DEFAULT):
        confirm_password = confirm_password or password
        admin_passphrase = admin_passphrase or DUT_ADMIN_SSW_PASSWORD

        self._query_response('EDIT')
        self._query_response(user_name)
        self._expect(['Enter your Passphrase to make changes:', ], timeout=5)
        self._writeln(admin_passphrase)
        self._query_response(full_name)
        self._query_select_list_item(group)
        sys_gen_passwd = ''
        self._query_response(system_generate_password)
        if re.match(r'yes|y', str(system_generate_password), re.I):
            sys_gen_passwd_output = \
                self._read_until('want to proceed with this')
            self._info(sys_gen_passwd_output)
            self._query_response(YES)
            sys_gen_passwd = re.search( \
                r'your system generated passphrase:\s+(.*)\n', \
                sys_gen_passwd_output, re.I | re.M)
            sys_gen_passwd = sys_gen_passwd.group(1).strip()
        else:
            self._query_response(password)
            if confirm_password:
                self._writeln(confirm_password)

        self._to_the_top(self.newlines)

        return sys_gen_passwd

    def delete(self, admin_passphrase=None, user_name=REQUIRED, confirm=DEFAULT):
        admin_passphrase = admin_passphrase or DUT_ADMIN_SSW_PASSWORD
        self._query_response('DELETE')
        self._query_response(user_name)
        self._expect(['Enter your Passphrase to make changes:', ], timeout=5)
        self._writeln(admin_passphrase)
        self._query_response(confirm)
        self._to_the_top(self.newlines)

    def password(self, admin_passphrase=None, operation="assign", user_name=REQUIRED, system_generate_password=NO,
                 new_password=REQUIRED, confirm_new_password=None):
        confirm_new_password = confirm_new_password or new_password
        admin_passphrase = admin_passphrase or DUT_ADMIN_SSW_PASSWORD
        self._query_response('PASSPHRASE')
        self._query_response(operation)
        self._query_response(user_name)
        self._expect(['Enter your Passphrase to make changes:', ], timeout=5)
        self._writeln(admin_passphrase)
        sys_gen_passwd = ''
        if 'assign' in operation.lower():
            self._query_response(system_generate_password)
            if re.match(r'yes|y', str(system_generate_password), re.I):
                sys_gen_passwd_output = \
                    self._read_until('want to proceed with this')
                self._info(sys_gen_passwd_output)
                self._query_response(YES)
                sys_gen_passwd = re.search( \
                    r'your system generated passphrase:\s+(.*)\n', \
                    sys_gen_passwd_output, re.I | re.M)
                sys_gen_passwd = sys_gen_passwd.group(1).strip()
            else:
                self._query_response(new_password)
                self._writeln(confirm_new_password)
        self._to_the_top(self.newlines)

        return sys_gen_passwd

    def password_force(self):
        self._query_response('PASSPHRASE')
        self._query_response('FORCE')
        return userconfigForcepassword(self._get_sess())

    def external(self):
        self._query_response('EXTERNAL')
        return userconfigExternal(self._get_sess())

    def twofactor(self):
        self._query_response('TWOFACTORAUTH')
        return userconfigTwoFactor(self._get_sess())

    def role(self):
        self._query_response('ROLE')
        return userconfigRole(self._get_sess())

    def policy(self):
        self._query_response('POLICY')
        return userconfigPolicy(self._get_sess())

    def dlptracking(self):
        self._query_response('DLPTRACKING')
        return userconfigDLPTracking(self._get_sess())

    def urltracking(self):
        self._query_response('URLTRACKING')
        return userconfigURLTracking(self._get_sess())

    def status(self, admin_passphrase=None, user_name=REQUIRED, switch=False):
        ACTIVE = 'available'
        LOCKED = 'locked'
        PENDING = 'pending'
        options = (ACTIVE, LOCKED, PENDING)

        admin_passphrase = admin_passphrase or DUT_ADMIN_SSW_PASSWORD
        self._query_response('STATUS')
        self._expect(['Enter your Passphrase to make changes:', ], timeout=5)
        self._writeln(admin_passphrase)
        self._query_response(user_name)
        state = options[self._query(*options)]
        if state != PENDING:
            if switch:
                self._writeln('yes')
                state = options[self._query(*options)]
            else:
                self._writeln('no')
        self._to_the_top(self.newlines)
        return state

    def defaultaccess(self, group):
        self._query_response('defaultaccess')
        return userconfigDefaultaccess(self._get_sess(), group)

    def two_factor_status(self, ):
        state = "UNKNOWN"
        ENABLED = 'Two-Factor Authentication: RADIUS'
        DISABLED = 'Two-Factor Authentication: Disabled'
        options = (ENABLED, DISABLED)

        state = options[self._query(*options)]
        self._to_the_top(1)
        if state == "UNKNOWN":
            return state.upper()
        state = state.split(":")[1].strip()
        if state == "RADIUS":
            state = "enabled"
        return state.upper()


class userconfigForcepassword(clictorbase.IafCliConfiguratorBase):

    def instant(self, user_name=REQUIRED):
        self._new_lines = 1
        self._query_response('INSTANT')
        self._query_select_list_item(user_name)
        self._to_the_top(self._new_lines)

    def later(self, input_dict=None, **kwargs):
        param_map = clictorbase.IafCliParamMap(end_of_command='Choose the operation')
        param_map['user_name'] = ['Enter the username', REQUIRED]
        param_map['password_exp_time'] = ['passphrase expiration period', DEFAULT]
        param_map['enable_grace_period'] = ['Do you want to ', DEFAULT]
        param_map['password_grace_period'] = ['passphrase grace period', DEFAULT]
        param_map.update(input_dict or kwargs)
        self._query_response('LATER')
        return self._process_input(param_map)


class userconfigExternal(clictorbase.IafCliConfiguratorBase):
    _new_lines = 2

    def setup(self, use_ext_auth=DEFAULT, cache_time=DEFAULT, mechanism=DEFAULT, ldap_input_dict=None, **kwargs):
        self._query_response('SETUP')
        self._query_response(use_ext_auth)
        if is_no(use_ext_auth):
            self._to_the_top(self._new_lines)
            return
        self._query_response(cache_time)
        self._query_select_list_item(mechanism)
        if mechanism.lower() == 'radius':
            return userconfigExternalRadius(self._get_sess())
        elif mechanism.lower() == 'ldap':
            return userconfigExternalLdap(self._get_sess(), ldap_input_dict, **kwargs)
        else:
            raise ConfigError('Unknown auth mechanism')

    def groups(self):
        self._query_response('GROUPS')
        return userconfigExternalGroups(self._get_sess())


class userconfigExternalGroups(clictorbase.IafCliConfiguratorBase):
    """
       userconfig -> external -> groups
    """
    _new_lines = 3

    def new(self, input_dict=None, **kwargs):
        global DEFAULT, REQUIRED

        param_map = clictorbase.IafCliParamMap(end_of_command='Choose the operation')
        param_map['group_name'] = ['external group name to map', REQUIRED]
        param_map['role'] = ['Assign a role', DEFAULT, True]
        param_map.update(input_dict or kwargs)
        self._query_response('NEW')
        return self._process_input(param_map)

    def edit(self, input_dict=None, **kwargs):
        global DEFAULT, REQUIRED

        param_map = clictorbase.IafCliParamMap(end_of_command='Choose the operation')
        param_map['group_name'] = ['mapping to edit', DEFAULT, True]
        param_map['role'] = ['Assign a role', DEFAULT, True]
        param_map.update(input_dict or kwargs)
        self._query_response('EDIT')
        return self._process_input(param_map)

    def delete(self, input_dict=None, **kwargs):
        global DEFAULT, REQUIRED

        param_map = clictorbase.IafCliParamMap(end_of_command='Choose the operation')
        param_map['group_name'] = ['mapping to delete', DEFAULT, True]
        param_map.update(input_dict or kwargs)
        self._query_response('DELETE')
        return self._process_input(param_map)

    def print_groups(self):
        self._query_response('PRINT')
        self._to_the_top(self._new_lines)

    def clear(self):
        self._query_response('CLEAR')
        self._to_the_top(self._new_lines)


class userconfigExternalRadius(clictorbase.IafCliConfiguratorBase):
    _new_lines = 4

    def __init__(self, sess, input_dict=None, **kwargs):
        try:
            IafCliConfiguratorBase.__init__(self, sess)
        except NameError:
            self.IafCliConfiguratorBase.__init__(self, sess)

    def new(self, input_dict=None, **kwargs):

        param_map = clictorbase.IafCliParamMap(end_of_command='Choose the operation')
        param_map['host'] = ['host name', REQUIRED]
        param_map['port'] = ['port number', DEFAULT]
        param_map['password'] = ['shared passphrase', REQUIRED]
        param_map['pass_again'] = ['new passphrase', REQUIRED]
        param_map['auth_type'] = ['authentication type', DEFAULT, True]
        param_map['timeout'] = ['timeout in seconds', DEFAULT]
        param_map.update(input_dict or kwargs)
        # if 'pass_again' is not passed, it will be same as password
        param_map['pass_again']['answer'] = param_map['password']['answer']

        self._query_response('NEW')
        return self._process_input(param_map)

    def edit(self, input_dict=None, **kwargs):

        param_map = clictorbase.IafCliParamMap(end_of_command='Choose the operation')
        param_map['host'] = ['server', DEFAULT, True]
        param_map['host_name'] = ['host name or IP address', DEFAULT]
        param_map['port'] = ['port number', DEFAULT]
        param_map['password'] = ['shared passphrase', DEFAULT]
        param_map['pass_again'] = ['new passphrase', REQUIRED]
        param_map['timeout'] = ['timeout in seconds', DEFAULT]
        param_map['auth_type'] = ['authentication type', DEFAULT, True]
        param_map.update(input_dict or kwargs)
        # if 'pass_again' is not passed, it will be same as password
        param_map['pass_again']['answer'] = param_map['password']['answer']

        self._query_response('EDIT')
        return self._process_input(param_map)

    def delete(self, host=DEFAULT):

        self._query_response('DELETE')
        self._query_select_list_item(host)
        self._to_the_top(self._new_lines)

    def clear(self, confirm_delete=DEFAULT):
        self._query_response('CLEAR')
        self._query_response(confirm_delete)
        self._to_the_top(self._new_lines)

    def move(self, input_dict=None, **kwargs):

        param_map = clictorbase.IafCliParamMap(end_of_command='Choose the operation')
        param_map['host_to_move'] = ['server', DEFAULT, True]
        param_map['position'] = ['target server', DEFAULT]
        param_map.update(input_dict or kwargs)

        self._query_response('MOVE')
        return self._process_input(param_map)


class GroupMapEmptyError(IafCliError): pass


class userconfigExternalLdap(clictorbase.IafCliConfiguratorBase):
    _new_lines = 3

    def __init__(self, sess, input_dict=None, **kwargs):
        print "input dict %s " % (input_dict)
        print "kwargs dict %s " % (input_dict)
        try:
            IafCliConfiguratorBase.__init__(self, sess)
        except NameError:
            self.IafCliConfiguratorBase.__init__(self, sess)
        self._set_local_err_dict({
            ('Group mapping cannot be empty if LDAP is being used for external',
             EXACT): GroupMapEmptyError,
        })

        param_map = clictorbase.IafCliParamMap(end_of_command='Choose the operation')
        param_map['ext_auth_query'] = ['external authentication queries', DEFAULT, True]
        param_map['timeout'] = ['seconds for entire LDAP authentication', DEFAULT]
        param_map['ext_group'] = ['external group name', DEFAULT]
        param_map['role'] = ['Assign a role', DEFAULT, True]
        param_map.update(input_dict or kwargs)
        _process_result = self._process_input(param_map)
        return _process_result


class userconfigRole(clictorbase.IafCliConfiguratorBase):
    _new_lines = 2

    def new(self, input_dict=None, **kwargs):
        param_map = clictorbase.IafCliParamMap(end_of_command='Choose the operation')
        param_map['name'] = ['name for the role', REQUIRED]
        param_map['short_name'] = ['short description', DEFAULT]
        param_map['mailpolicies'] = ['mailpolicies and content filters', DEFAULT]
        param_map['dlp'] = ['DLP', DEFAULT, True]
        param_map['tracking'] = ['tracking', DEFAULT, True]
        param_map['reports'] = ['reports', DEFAULT, True]
        param_map['trace'] = ['trace', DEFAULT, True]
        param_map['quarantines'] = ['quarantines', DEFAULT, True]
        param_map.update(input_dict or kwargs)
        self._query_response('NEW')
        return self._process_input(param_map)

    def edit(self, input_dict=None, **kwargs):
        param_map = clictorbase.IafCliParamMap(end_of_command='Choose the operation')
        param_map['role_name'] = ['role name or number', REQUIRED]
        param_map['new_name'] = ['new name for the user', DEFAULT]
        param_map['short_name'] = ['short description', DEFAULT]
        param_map['mailpolicies'] = ['mailpolicies and content filters', DEFAULT]
        param_map['dlp'] = ['DLP', DEFAULT, True]
        param_map['tracking'] = ['tracking', DEFAULT, True]
        param_map['reports'] = ['reports', DEFAULT, True]
        param_map['trace'] = ['trace', DEFAULT, True]
        param_map['quarantines'] = ['quarantines', DEFAULT, True]
        param_map.update(input_dict or kwargs)
        self._query_response('EDIT')
        return self._process_input(param_map)

    def delete(self, role_name=REQUIRED):
        self._query_response('DELETE')
        self._query_response(role_name)
        self._to_the_top(self._new_lines)


class userconfigPolicy(clictorbase.IafCliConfiguratorBase):
    _new_lines = 2

    def passwordstrength(self, input_dict=None, **kwargs):
        param_map = clictorbase.IafCliParamMap(end_of_command='Choose the operation')
        param_map['min_length'] = ['minimum number of characters required', DEFAULT]
        param_map['req_alphabets'] = ['one upper', DEFAULT]
        param_map['req_number'] = ['one number', DEFAULT]
        param_map['req_special_chars'] = ['one special character', DEFAULT]
        param_map['ban_username'] = ['Reject passphrases', DEFAULT]
        param_map['ban_reuse'] = ['Ban reuse', DEFAULT]
        param_map['times_ban_reuse'] = ['most recent passphrases not allowed', DEFAULT]
        param_map['words_to_disallow'] = ['list of words to disallow', DEFAULT]
        param_map['entropy_guests'] = ['entropy value for Guests', DEFAULT]
        param_map['entropy_admin'] = ['entropy value for Administrators', DEFAULT]
        param_map['entropy_cloudadmin'] = ['entropy value for Cloud Administrators', DEFAULT]
        param_map['entropy_readonly'] = ['entropy value for Read-Only Operators', DEFAULT]
        param_map['entropy_customroles'] = ['entropy value for Custom Roles', DEFAULT]
        param_map['entropy_technicians'] = ['entropy value for Technicians', DEFAULT]
        param_map['entropy_operators'] = ['entropy value for Operators', DEFAULT]
        param_map['entropy_helpdesk'] = ['entropy value for Help Desk Users', DEFAULT]
        param_map.update(input_dict or kwargs)
        self._query_response('PASSWORDSTRENGTH')
        return self._process_input(param_map)

    def account(self, input_dict=None, **kwargs):
        param_map = clictorbase.IafCliParamMap(end_of_command='Choose the operation')
        param_map['lock_account'] = ['automatically lock account', DEFAULT]
        param_map['attempts'] = ['unsuccessful login attempts', DEFAULT]
        param_map['login_attempts_minute'] = ['login attempts can be done in a minute', DEFAULT]
        param_map['display_lock_mesg'] = ['display an account locked message', DEFAULT]
        param_map['change_locked_mesg'] = ['change the account locked message', DEFAULT]
        param_map['lock_message_medium'] = ['default lock message', DEFAULT, True]
        param_map['mesg_file'] = ['Enter the name of the file', DEFAULT, True]
        param_map['mesg_cli'] = ['Enter or paste the account locked', DEFAULT]
        param_map['enable_pass_expire'] = ['enable passphrase expiration', DEFAULT]
        param_map['expire_time'] = ['passphrase expiration period', DEFAULT]
        param_map['display_reminder'] = ['display reminder', DEFAULT]
        param_map['notification_time'] = ['notification will be  printed', DEFAULT]
        param_map['enable_password_grace'] = ['enable passphrase grace period?', DEFAULT]
        param_map['password_grace_period'] = ['period after users passphrase change time', DEFAULT]
        param_map['force_password'] = ['require a passphrase reset', DEFAULT]
        param_map.update(input_dict or kwargs)
        if param_map['mesg_cli']['answer']:
            param_map['mesg_cli']['answer'] = param_map['mesg_cli']['answer'] + '\n.'
        self._query_response('ACCOUNT')
        return self._process_input(param_map)


class userconfigDefaultaccess(clictorbase.IafCliConfiguratorBase):

    def __init__(self, sess, group=REQUIRED):
        self._new_lines = 2
        try:
            IafCliConfiguratorBase.__init__(self, sess)
            self.group = group
            self._query_select_list_item(self.group)
        except NameError:
            self.IafCliConfiguratorBase.__init__(self, sess)
        except clictorbase.IafUnknownOptionError, e:
            print e
            self._to_the_top(1)

    def _select_or_enter(self, modes):
        if isinstance(modes, (tuple, list)):
            self._query_response(','.join(str(s) for s in modes))
        else:
            self._query_select_list_item(modes)

    def add(self, modes=DEFAULT, access=DEFAULT):
        self._query_response('ADD')
        self._select_or_enter(modes)
        self._query_select_list_item(access)
        self._to_the_top(self._new_lines)

    def edit(self, modes=DEFAULT, access=DEFAULT):
        self._query_response('EDIT')
        self._select_or_enter(modes)
        self._query_select_list_item(access)
        self._to_the_top(self._new_lines)

    def delete(self, modes=DEFAULT):
        self._query_response('DELETE')
        self._select_or_enter(modes)
        self._to_the_top(self._new_lines)

    def clear(self):
        self._query_response('CLEAR')
        self._to_the_top(self._new_lines)

    def get_access_table(self):
        # return {level:access_mode}
        modes_map = {}
        self._sess.clearbuf()
        self._query_response('ADD')
        buf = self._sess.getbuf()
        res = re.findall(r"(.*): (.*)", buf)
        for k, v in dict(res[1:]).items():
            modes_map[k.strip(' \t\n\r')] = v.strip(' \t\n\r')
        self._sess.clearbuf()
        self._restart_nosave()
        return modes_map


class userconfigDLPTracking(clictorbase.IafCliConfiguratorBase):
    _new_lines = 3

    def _select_or_enter(self, roles):
        if isinstance(roles, (tuple, list)):
            self._query_response(','.join(str(s) for s in roles))
        else:
            self._query_select_list_item(roles)

    def delete(self, role=DEFAULT):
        self._query_select_list_item('Delete')
        self._select_or_enter(role)
        self._to_the_top(self._new_lines)

    def add(self, role=DEFAULT):
        self._query_select_list_item('Add')
        self._select_or_enter(role)
        self._to_the_top(self._new_lines)


class userconfigURLTracking(clictorbase.IafCliConfiguratorBase):
    _new_lines = 3

    def _select_or_enter(self, roles):
        if isinstance(roles, (tuple, list)):
            self._query_response(','.join(str(s) for s in roles))
        else:
            self._query_select_list_item(roles)

    def delete(self, role=DEFAULT):
        self._query_select_list_item('Delete')
        self._select_or_enter(role)
        self._to_the_top(self._new_lines)

    def add(self, role=DEFAULT):
        self._query_select_list_item('Add')
        self._select_or_enter(role)
        self._to_the_top(self._new_lines)


class userconfigTwoFactor(clictorbase.IafCliConfiguratorBase):
    _new_lines = 2

    def setup(self, use_2fa_auth=DEFAULT, **kwargs):
        self._query_response('SETUP')
        self._query_response(use_2fa_auth)
        if is_no(use_2fa_auth):
            self._to_the_top(self._new_lines)
            return
        return userconfigTwoFactorRadius(self._get_sess())

    def privilege(self, **kwargs):
        self._query_response('PRIVILEGES')
        return userconfigTwoFactorPrivilege(self._get_sess())


class userconfigTwoFactorRadius(clictorbase.IafCliConfiguratorBase):
    _new_lines = 2

    def __init__(self, sess, **kwargs):
        try:
            IafCliConfiguratorBase.__init__(self, sess)
        except NameError:
            self.IafCliConfiguratorBase.__init__(self, sess)

    def new(self, **kwargs):

        param_map = clictorbase.IafCliParamMap(end_of_command='Choose the operation')
        param_map['host'] = ['host name', REQUIRED]
        param_map['port'] = ['port number', DEFAULT]
        param_map['password'] = ['shared passphrase', REQUIRED]
        param_map['pass_again'] = ['new passphrase', REQUIRED]
        param_map['auth_type'] = ['authentication type', DEFAULT, True]
        param_map['timeout'] = ['timeout in seconds', DEFAULT]
        param_map.update(kwargs)
        # if 'pass_again' is not passed, it will be same as password
        param_map['pass_again']['answer'] = param_map['password']['answer']

        self._query_response('NEW')
        return self._process_input(param_map)

    def edit(self, input_dict=None, **kwargs):

        param_map = clictorbase.IafCliParamMap(end_of_command='Choose the operation')
        param_map['host'] = ['server', DEFAULT, True]
        param_map['host_name'] = ['host name or IP address', DEFAULT]
        param_map['port'] = ['port number', DEFAULT]
        param_map['password'] = ['shared passphrase', DEFAULT]
        param_map['pass_again'] = ['new passphrase', REQUIRED]
        param_map['timeout'] = ['timeout in seconds', DEFAULT]
        param_map['auth_type'] = ['authentication type', DEFAULT, True]
        param_map.update(kwargs)
        # if 'pass_again' is not passed, it will be same as password
        param_map['pass_again']['answer'] = param_map['password']['answer']

        self._query_response('EDIT')
        return self._process_input(param_map)

    def delete(self, host=DEFAULT):

        self._query_response('DELETE')
        self._query_select_list_item(host)
        self._to_the_top(self._new_lines)

    def clear(self, confirm_delete=DEFAULT):
        self._query_response('CLEAR')
        self._query_response(confirm_delete)
        self._to_the_top(self._new_lines)


class userconfigTwoFactorPrivilege(clictorbase.IafCliConfiguratorBase):
    _new_lines = 4

    def _select_or_enter(self, roles):
        self._query_response(','.join(str(s) for s in roles.split(" ")))

    def delete(self, role=REQUIRED, cust_role=None):
        self._writeln('2')
        self._select_or_enter(role)
        if cust_role != None:
            self._select_or_enter(cust_role)
        self._to_the_top(self._new_lines)

    def add(self, role=REQUIRED, cust_role=None):
        self._writeln('1')
        self._select_or_enter(role)
        if cust_role != None:
            self._select_or_enter(cust_role)
        self._to_the_top(self._new_lines)
