#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1250/cli/ctor/userconfig.py#3 $
# $DateTime: 2019/06/07 02:45:52 $
# $Author: sarukakk $

from sal.deprecated.expect import REGEX, EXACT
import clictorbase
from clictorbase import IafCliConfiguratorBase, IafCliError, REQUIRED, DEFAULT
from sal.exceptions import ConfigError
from sal.containers.yesnodefault import YES, NO, is_yes,is_no
import time

DEBUG = True

class GroupMapEmptyError(IafCliError): pass


class userconfig(clictorbase.IafCliConfiguratorBase):
    """userconfig
    """
    _new_lines = 1

    class UserRestrictedError(IafCliError): pass
    class DeleteSelfError(IafCliError): pass

    def __init__(self, sess):
        IafCliConfiguratorBase.__init__(self, sess)
        self._set_local_err_dict({
             ('User \S+ cannot be modified', REGEX): self.UserRestrictedError,
             ('User \S+ cannot be deleted', REGEX): self.UserRestrictedError,
             ('You cannot delete yourself', EXACT): self.DeleteSelfError,
             })

    def __call__(self):
        self._restart()
        self._writeln('userconfig')
        return self

    def new(self, input_dict=None, **kwargs):
        param_map = clictorbase.IafCliParamMap(end_of_command='Choose the operation')
        param_map['admin_passphrase']   = ['Enter your Passphrase to make changes',REQUIRED]
        param_map['user_name']   = ['username', REQUIRED]
        param_map['full_name']   = ['full name', REQUIRED]
        param_map['group']       = ['group' ,DEFAULT,True]
        param_map['generate_passwd'] = ['system generated passphrase', DEFAULT]
        param_map['password']    = ['Enter the passphrase', REQUIRED]
        param_map['password1']   = ['enter the new passphrase again', REQUIRED]
        param_map.update(input_dict or kwargs)
        self._query_response('NEW')
        _process_result = self._process_input(param_map)
        self._to_the_top(self._new_lines)
        return _process_result

    def edit(self, user_name=REQUIRED, full_name=DEFAULT,
            password=DEFAULT, group=DEFAULT,admin_passphrase=None):
        self._query_response('EDIT')
        self._query_response(user_name)
        self._read_until('Enter your Passphrase to make changes:')
        self._writeln(admin_passphrase)
        self._query_response(full_name)
        self._query_select_list_item(group)
        self._query_response('') # system generated password
        time.sleep(30)
        self._writeln(password)
        if password:
            time.sleep(30)
            self._writeln(password)
        self._to_the_top(self._new_lines)

    def delete(self, user_name=REQUIRED, confirm=DEFAULT,admin_passphrase=None):
        self._query_response('DELETE')
        self._query_response(user_name)
        self._read_until('Enter your Passphrase to make changes:')
        self._writeln(admin_passphrase)
        self._query_response(confirm)
        self._to_the_top(self._new_lines)

    def password(self):
        self._query_response('PASSPHRASE')
        return userconfigPassword(self._get_sess())

    def external(self):
        self._query_response('EXTERNAL')
        return userconfigExternal(self._get_sess())

    def policy(self):
        self._query_response('POLICY')
        return userconfigPolicy(self._get_sess())

    def role(self):
        self._query_response('ROLE')
        return userconfigRole(self._get_sess())

    def status(self, user_name):
        self._query_response('STATUS')
        return userconfigStatus(self._get_sess(), user_name)

    def _addOrDelete(self,allow=None):
        if is_yes(allow):
            self._query_select_list_item('Add')
        if is_no(allow):
            self._query_select_list_item('Delete')

    def dlptracking(self, user, allow):
        userlist={}
        userlist['admin']= 'Administrators'
        userlist['emailAdmin']= 'Email Administrators'
        userlist['helpDesk']='Help Desk Users'
        userlist['operators']='Operators'
        userlist['readOnlyOperators']='Read-Only Operators'
        userlist['urlFilteringAdmin']='URL Filtering Administrators'
        userlist['webAdmin']= 'Web Administrators'
        userlist['webPolicyAdmin']='Web Policy Administrators'

        predefinedlist = {}
        # Copy the userlist dict, don't assign a pointer to it
        predefinedlist.update(userlist)
        del predefinedlist['urlFilteringAdmin']
        del predefinedlist['webAdmin']
        del predefinedlist['webPolicyAdmin']

        self._query_response('DLPTRACKING')
        self._expect([("Choose the operation you want to perform", EXACT)])

        if user == 'all':
            text_block = self._get_last_matched_text()
            dlp_enabled_list = map(lambda x: x.strip(), text_block.split("\n")[4:-2])
            if is_yes(allow):
                # adding only users that don't have dlp permission yet
                result_list = filter(lambda x: (x not in dlp_enabled_list), predefinedlist.values())
            else:
                # and vice-versa
                result_list = filter(lambda x: (x in dlp_enabled_list), predefinedlist.values())

            # if we dont have to perform add/delete then just return
            if not result_list:
                self._to_the_top(self._new_lines+1)
                return

            response = ','.join(result_list)
        else:
            response = userlist[user]
        self._addOrDelete(allow)
        self._query_response(response)
        self._to_the_top(self._new_lines+1)

    def access(self):
        raise clictorbase.IafCliCtorNotImplementedError


class userconfigPassword(clictorbase.IafCliConfiguratorBase):
    _new_lines = 1

    def assign(self, user_name=REQUIRED, new_password=REQUIRED):
        self._query_response('ASSIGN')
        self._query_response(user_name)
        self._query_response('') # system generated password
        time.sleep(30)
        self._writeln(new_password)
        time.sleep(30)
        self._writeln(new_password)
        self._to_the_top(self._new_lines)

    def force(self, user_name=REQUIRED):
        self._query_response('FORCE')
        self._query_response('INSTANT')
        self._query_select_list_item(user_name)
        curr_status = self._read_until('Choose the operation')
        self._to_the_top(self._new_lines)
        return curr_status


class userconfigExternal(clictorbase.IafCliConfiguratorBase):
    _new_lines = 2

    def setup(self, use_ext_auth=DEFAULT, cred_timeout=DEFAULT, mechanism=DEFAULT,ldap_input_dict=None, **kwargs):
        """
            userconfig -> external -> setup
        """
        self._query_response('SETUP')
        self._query_response(use_ext_auth)
        if use_ext_auth == 'y':
            self._query_response(cred_timeout)
            self._query_select_list_item(mechanism)
            if mechanism.lower() == 'radius':
                return userconfigExternalRadius(self._get_sess())
            elif mechanism.lower() == 'ldap':
                return userconfigExternalLdap(self._get_sess(),ldap_input_dict, **kwargs)
            else:
                raise ConfigError('Unknown auth mechanism')
        self._to_the_top(self._new_lines)

    def groups(self):
        self._query_response('GROUPS')
        return userconfigExternalGroups(self._get_sess())


class userconfigExternalGroups(clictorbase.IafCliConfiguratorBase):
    """
       userconfig -> external -> groups
    """
    _new_lines = 1

    def new(self, input_dict=None, **kwargs):
        param_map = clictorbase.IafCliParamMap(end_of_command='Choose the operation')
        param_map['group_name']  = ['external group name to map', REQUIRED]
        param_map['role']        = ['Choose the group' ,DEFAULT,True]
        param_map.update(input_dict or kwargs)
        self._query_response('NEW')
        _process_result = self._process_input(param_map)
        self._to_the_top(self._new_lines)
        return _process_result

    def edit(self, input_dict=None, **kwargs):
        param_map = clictorbase.IafCliParamMap(end_of_command='Choose the operation')
        param_map['group_name']  = ['mapping to edit', DEFAULT,True]
        param_map['role']        = ['Choose the group', DEFAULT,True]
        param_map.update(input_dict or kwargs)
        self._query_response('EDIT')
        _process_result = self._process_input(param_map)
        self._to_the_top(self._new_lines)
        return _process_result

    def delete(self, input_dict=None, **kwargs):
        param_map = clictorbase.IafCliParamMap(end_of_command='Choose the operation')
        param_map['group_name']  = ['mapping to delete', DEFAULT,True]
        param_map.update(input_dict or kwargs)
        self._query_response('DELETE')
        _process_result = self._process_input(param_map)
        self._to_the_top(self._new_lines)
        return _process_result

    def clear(self):
        self._query_response('CLEAR')
        curr_status = self._read_until('Choose the operation')
        self._to_the_top(self._new_lines+2)
        return curr_status

    def print_groups(self):
        self._query_response('PRINT')
        res = self._read_until('Choose the operation')
        self._to_the_top(self._new_lines+2)
        return res


class userconfigExternalRadius(clictorbase.IafCliConfiguratorBase):
    _new_lines = 1

    def new(self, input_dict=None, **kwargs):
        param_map = clictorbase.IafCliParamMap(end_of_command=' SETUP ')
        param_map['host']                = ['host name', REQUIRED]
        param_map['port']                = ['port number', DEFAULT]
        param_map['password']            = ['shared passphrase', REQUIRED]
        param_map['password1']           = ['passphrase again', REQUIRED]
        param_map['timeout']             = ['timeout in seconds', DEFAULT]
        param_map['auth_type']           = ['authentication type', DEFAULT, 1]
        param_map['operation']           = ['the operation', DEFAULT]
        if 'delete_mapping' in (input_dict or kwargs):
            param_map['delete_mapping']      = ['delete all the RADIUS CLASS attribute', DEFAULT]
        if 'create_mapping' in (input_dict or kwargs):
            param_map['create_mapping']      = ['create mappings', DEFAULT]
        if 'group_name' in (input_dict or kwargs):
            param_map['group_name']          = ['group name', DEFAULT]
        if 'role' in (input_dict or kwargs):
            param_map['role']                = ['group', DEFAULT, 1]

        param_map.update(input_dict or kwargs)

        self._query_response('NEW')
        _process_result = self._process_input(param_map)
        self._to_the_top(self._new_lines)
        return _process_result

    def edit(self, input_dict=None, **kwargs):
        param_map = clictorbase.IafCliParamMap(end_of_command=' SETUP ')
        param_map['host']                = ['server', DEFAULT, True]
        param_map['host_name']           = ['host name or IP address', DEFAULT]
        param_map['port']                = ['port number', DEFAULT]
        param_map['password']            = ['shared password', DEFAULT]
        param_map['password1']           = ['password again', DEFAULT]
        param_map['timeout']             = ['timeout in seconds', DEFAULT]
        param_map['auth_type']           = ['authentication type', DEFAULT, 1]
        param_map['operation']           = ['the operation', DEFAULT]
        if 'delete_mapping' in (input_dict or kwargs):
            param_map['delete_mapping']      = ['delete all the RADIUS CLASS attribute', DEFAULT]
        if 'create_mapping' in (input_dict or kwargs):
            param_map['create_mapping']      = ['create mappings', DEFAULT]
        if 'group_name' in (input_dict or kwargs):
            param_map['group_name']          = ['group name', DEFAULT]
        if 'role' in (input_dict or kwargs):
            param_map['role']                = ['group', DEFAULT, 1]

        param_map.update(input_dict or kwargs)

        if (param_map['password'])['answer'] == DEFAULT:
            (param_map['password1'])['must_answer']=0

        self._query_response('EDIT')
        _process_result = self._process_input(param_map)
        self._to_the_top(self._new_lines)
        return _process_result

    def move(self, input_dict=None, **kwargs):
        param_map = clictorbase.IafCliParamMap(end_of_command=' SETUP ')
        param_map['host']                = ['server', DEFAULT, True]
        param_map['position']            = ['position', DEFAULT]
        param_map['operation']           = ['the operation', DEFAULT]
        if 'delete_mapping' in (input_dict or kwargs):
            param_map['delete_mapping']      = ['delete all the RADIUS CLASS attribute', DEFAULT]
        if 'create_mapping' in (input_dict or kwargs):
            param_map['create_mapping']      = ['create mappings', DEFAULT]
        if 'group_name' in (input_dict or kwargs):
            param_map['group_name']          = ['group name', DEFAULT]
        if 'role' in (input_dict or kwargs):
            param_map['role']                = ['group', DEFAULT, 1]

        param_map.update(input_dict or kwargs)

        self._query_response('MOVE')
        _process_result = self._process_input(param_map)
        self._to_the_top(self._new_lines)
        return _process_result

    def delete(self, input_dict=None, **kwargs):

        param_map = clictorbase.IafCliParamMap(end_of_command=' SETUP ')
        param_map['host']                = ['server', DEFAULT, True]
        param_map['operation']           = ['the operation', DEFAULT]
        if 'delete_mapping' in (input_dict or kwargs):
            param_map['delete_mapping']      = ['delete all the RADIUS CLASS attribute', DEFAULT]
        if 'create_mapping' in (input_dict or kwargs):
            param_map['create_mapping']      = ['create mappings', DEFAULT]
        if 'group_name' in (input_dict or kwargs):
            param_map['group_name']          = ['group name', DEFAULT]
        if 'role' in (input_dict or kwargs):
            param_map['role']                = ['group', DEFAULT, 1]

        param_map.update(input_dict or kwargs)

        self._query_response('DELETE')
        _process_result = self._process_input(param_map)
        self._to_the_top(self._new_lines)
        return _process_result

    def clear(self,confirm=DEFAULT):
        self._query_response('CLEAR')
        self._query_response(confirm)
        self._to_the_top(self._new_lines+2)


class userconfigExternalLdap(clictorbase.IafCliConfiguratorBase):
    _new_lines = 1

    def __init__(self, sess,input_dict=None,**kwargs):
        try:
            IafCliConfiguratorBase.__init__(self, sess)
        except NameError:
            self.IafCliConfiguratorBase.__init__(self, sess)
        self._set_local_err_dict({
          ('External group name should be a string',
                                      EXACT) : GroupMapEmptyError,
                 })

        param_map = clictorbase.IafCliParamMap(end_of_command='Choose the operation')
        param_map['ldap_query'] = ['LDAP external authentication queries', DEFAULT, True]
        param_map['timeout']        = ['seconds for entire LDAP authentication', DEFAULT]
        param_map['ext_group']      = ['external group name', DEFAULT]
        param_map['role']           = ['Choose the group for',DEFAULT, True]
        param_map.update(input_dict or kwargs)
        _process_result = self._process_input(param_map)
        self._to_the_top(self._new_lines)
        return _process_result


class userconfigPolicy(clictorbase.IafCliConfiguratorBase):
    _new_lines = 1

    def account(self, input_dict=None, **kwargs):
        param_map = clictorbase.IafCliParamMap(end_of_command='Choose the operation')
        param_map['autolock']            = ['lock account after unsuccessful login', DEFAULT]
        param_map['attempts']            = ['unsuccessful login attempts', DEFAULT]
        param_map['lm_display']          = ['display an account locked message', DEFAULT]
        param_map['lm_change']           = ['change the account locked message', DEFAULT]
        param_map['lm_method']           = ['lock message', DEFAULT, 1]
        param_map['lm_file']             = ['name of the file', DEFAULT]
        param_map['lm_input']            = ['locked message', DEFAULT]
        param_map['pwd_exp']             = ['password expiration', DEFAULT]
        param_map['pwd_exp_period']      = ['expiration period', DEFAULT]
        param_map['pwd_rem_display']         = ['display reminder', DEFAULT]
        param_map['pwd_rem_period']          = ['the period', DEFAULT]
        param_map['pwd_reset']           = ['require a password reset', DEFAULT]
        param_map['grace_period']        = ['enable password grace period', DEFAULT]

        param_map.update(input_dict or kwargs)

        self._query_response('ACCOUNT')
        _process_result = self._process_input(param_map)
        self._to_the_top(self._new_lines)
        return _process_result

    def passwordstrength(self, input_dict=None, **kwargs):
        param_map = clictorbase.IafCliParamMap(end_of_command='Choose the operation')
        param_map['min_chars']           = ['minimum number of characters', DEFAULT]
        param_map['case_letters']        = ['case letter', DEFAULT]
        param_map['numbers']             = ['at least one number', DEFAULT]
        param_map['spec_chars']          = ['special character', DEFAULT]
        param_map['sim_name']            = ['similar to the username', DEFAULT]
        param_map['reuse']               = ['reuse', DEFAULT]
        param_map['num_recent']          = ['number of the most recent passwords', DEFAULT]
        param_map['word_list']           = ['list of words to disallow in passwords', DEFAULT]
        param_map['guest_entropy']       = ['entropy value for Guests', DEFAULT]
        param_map['admin_entropy']       = ['entropy value for Administrators', DEFAULT]
        param_map['cloud_entropy']       = ['entropy value for Cloud Administrators', DEFAULT]
        param_map['email_entropy']       = ['entropy value for Email Administrators', DEFAULT]
        param_map['url_entropy']         = ['entropy value for URL Filtering Administrators', DEFAULT]
        param_map['readonly_entropy']    = ['entropy value for Read-Only Operators', DEFAULT]
        param_map['customrole_entropy']  = ['entropy value for Custom Roles', DEFAULT]
        param_map['tech_entropy']        = ['entropy value for Technicians', DEFAULT]
        param_map['webpolicy_entropy']   = ['entropy value for Web Policy Administrators', DEFAULT]
        param_map['oper_entropy']        = ['entropy value for Operators', DEFAULT]
        param_map['helpdesk_entropy']    = ['entropy value for Help Desk Users', DEFAULT]
        param_map['webadmin_entropy']    = ['entropy value for Web Administrators', DEFAULT]

        param_map.update(input_dict or kwargs)

        self._query_response('PASSWORDSTRENGTH')
        _process_result = self._process_input(param_map)
        self._to_the_top(self._new_lines)
        return _process_result


class userconfigRole(clictorbase.IafCliConfiguratorBase):
    """
       userconfig -> role
    """
    _new_lines = 1

    def new(self, input_dict=None, **kwargs):
        param_map = clictorbase.IafCliParamMap(end_of_command='Choose the operation')
        param_map['name']               = ['name', REQUIRED]
        param_map['descr']              = ['short description' ,DEFAULT]
        param_map['type']               = ['type of role', DEFAULT, True]

        # email params
        param_map['access_reports']     = ['type of access to reports', DEFAULT, True]
        param_map['reports_type']       = ['type of reports', DEFAULT, True]
        param_map['access_tracking']    = ['type of access to tracking', DEFAULT, True]
        param_map['access_quarantines'] = ['type of access to quarantines', DEFAULT, True]

        # web params
        param_map['visibility']         = ['Visibility', DEFAULT, True]
        param_map['publish']            = ['Publish Privilege', DEFAULT, True]

        param_map.update(input_dict or kwargs)

        self._query_response('NEW')
        _process_result = self._process_input(param_map)
        self._to_the_top(self._new_lines)
        return _process_result

    def edit(self, input_dict=None, **kwargs):
        param_map = clictorbase.IafCliParamMap(end_of_command='Choose the operation')
        param_map['name']         = ['name', DEFAULT]
        param_map['new_name']     = ['new name', DEFAULT]
        param_map['descr']        = ['short description', DEFAULT]

        # email params
        param_map['access_reports']     = ['type of access to reports', DEFAULT, True]
        param_map['reports_type']       = ['type of reports', DEFAULT, True]
        param_map['access_tracking']    = ['type of access to tracking', DEFAULT, True]
        param_map['access_quarantines'] = ['type of access to quarantines', DEFAULT, True]

        # web params
        param_map['visibility']         = ['Visibility', DEFAULT, True]
        param_map['publish']            = ['Publish Privilege', DEFAULT, True]

        param_map.update(input_dict or kwargs)

        self._query_response('EDIT')
        _process_result = self._process_input(param_map)
        self._to_the_top(self._new_lines)
        return _process_result

    def delete(self, input_dict=None, **kwargs):
        param_map = clictorbase.IafCliParamMap(end_of_command='Choose the operation')
        param_map['name']  = ['name', DEFAULT]
        param_map.update(input_dict or kwargs)
        self._query_response('DELETE')
        try:
            _process_result = self._process_input(param_map)
            self._to_the_top(self._new_lines)
            return _process_result
        except:
            self._restart()


class userconfigStatus(clictorbase.IafCliConfiguratorBase):
    """
       userconfig -> status
    """
    _new_lines = 1
    __username = ''
    __user_status = ''

    def __init__(self, sess, user_name):
        try:
            IafCliConfiguratorBase.__init__(self, sess)
        except NameError:
            self.IafCliConfiguratorBase.__init__(self, sess)

        self.__username = user_name

    def status(self):
        self._query_response(self.__username)

        _curr_status = self._read_until('Do you want')
        self.__user_status = "User %s had status: %s" % (self.__username, _curr_status)

        # Skip locking/unlocking by remaining default value
        self._query_response('')
        self._to_the_top(self._new_lines)
        return self.__user_status

    def lock(self, admin_passphrase=None):
        param_map = clictorbase.IafCliParamMap(end_of_command='Choose the operation')
        param_map['lock']                = ['lock this account', YES]
        param_map['unlock']              = ['make this account available', NO]

        self._read_until('Enter your Passphrase to make changes:')
        self._writeln(admin_passphrase)
        self._query_response(self.__username)
        _process_result = self._process_input(param_map)
        assert param_map.has_been_answered('lock'), "User %s was not locked." % self.__username
        assert (not param_map.has_been_answered('unlock')), "User %s was already locked." % self.__username
        self._to_the_top(self._new_lines)
        return _process_result

    def unlock(self, admin_passphrase=None):
        param_map = clictorbase.IafCliParamMap(end_of_command='Choose the operation')
        param_map['lock']                = ['lock this account', NO]
        param_map['unlock']              = ['make this account available', YES]

        self.__username
        self._read_until('Enter your Passphrase to make changes:')
        self._writeln(admin_passphrase)
        self._query_response(self.__username)
        _process_result = self._process_input(param_map)
        assert param_map.has_been_answered('unlock'), "User %s was not unlocked." % self.__username
        assert (not param_map.has_been_answered('lock')), "User %s was already unlocked." % self.__username
        self._to_the_top(self._new_lines)
        return _process_result

if __name__ == '__main__':
    # if cli_sess is already defined, we have a CLI session object from
    # the validator we can use; if not, we must create one
    try:
        cli_sess
    except NameError:
        cli_sess = clictorbase.get_sess()

    uc = userconfig(cli_sess)
    uc().new(
                   user_name='new',
                   full_name='abc',
                   password='123456',
                     )
    uc().edit(user_name='new')
    uc().password(user_name='new', new_password='zxcvbn')
    uc().delete(user_name='new', confirm='y')

    uc().external().setup(use_ext_auth=YES, mechanism='RADIUS').\
            new(host='1.2.3.4', password='qwe')

    uc().external().setup(use_ext_auth=YES, mechanism='RADIUS').\
            new(host='4.3.2.1', password='qwe', timeout=60)

    uc().external().setup(use_ext_auth=YES, mechanism='RADIUS').\
            edit(host='1.2.3.4', port='1234', password='abc', timeout=5)

    uc().external().setup(use_ext_auth=YES, mechanism='RADIUS').\
            delete(host='4.3.2.1')

    uc().external().setup(use_ext_auth=YES, mechanism='RADIUS').clear()

    ldap_input_dict={'ext_auth_query':1,'timeout':10, 'ext_group':'mygroup','role':3}
    uc().external().setup(use_ext_auth=YES, mechanism='ldap', ldap_input_dict=ldap_input_dict)

    uc().external().groups().new(group_name='mygroup2',role=3)
    uc().external().groups().edit(group_name='mygroup2',role=2)
    uc().external().groups().print_groups()
    uc().external().groups().new(group_name='mygroup3')
    uc().external().groups().new(group_name='mygroup4')
    uc().external().groups().delete()
