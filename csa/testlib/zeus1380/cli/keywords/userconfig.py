# $Id: //prod/main/sarf_centos/testlib/zeus1380/cli/keywords/userconfig.py#1 $
# $DateTime: 2020/05/25 00:19:30 $
# $Author: sarukakk $

from common.cli.clicommon import CliKeywordBase, DEFAULT
import common.Variables

class UserConfig(CliKeywordBase):
    """Configure local users that are allowed to use the system.
    """

    def get_keyword_names(self):
        return [
                'user_config_new',
                'user_config_edit',
                'user_config_password_assign',
                'user_config_password_force',
                'user_config_policy_account',
                'user_config_policy_passwordstrength',
                'user_config_delete',
                'user_config_status',
                'user_config_status_lock',
                'user_config_status_unlock',
                'user_config_role_email_new',
                'user_config_role_email_edit',
                'user_config_role_web_new',
                'user_config_role_web_edit',
                'user_config_role_delete',
                'user_config_external_setup_ldap',
                'user_config_external_setup_disable',
                'user_config_external_setup_new',
                'user_config_external_setup_edit',
                'user_config_external_setup_move',
                'user_config_external_setup_delete',
                'user_config_external_setup_clear',
                'user_config_external_groups_new',
                'user_config_external_groups_edit',
                'user_config_external_groups_delete',
                'user_config_external_groups_clear',
                'user_config_external_groups_print',
                'user_config_dlptracking',
                'userconfig_two_factor_disable',
                'userconfig_two_factor_radius_new',
                'userconfig_two_factor_radius_clear',
                'userconfig_two_factor_radius_delete',
                'userconfig_two_factor_privilege_add',
                'userconfig_two_factor_privilege_delete',
                'userconfig_external_setup_saml',
                'userconfig_external_devopssetup',
                'userconfig_external_devopsgroups_new',
                'userconfig_external_devopsgroups_edit',
                'userconfig_external_devopsgroups_delete',
                'userconfig_external_devopsgroups_clear',
                'userconfig_external_devopsgroups_print',
                'user_config_print_options',
               ]

    def user_config_new(self,user_name, full_name, password, group=DEFAULT,admin_passphrase=None):
        """Adds new user.

            userconfig -> new

        Parameters:
        - `user_name`:    username for new user.
        - `full_name`:    full name of new user.
        - `password`:    password for new user.
        - `group`:         group new user belong to.
                    Either 'Administrators', 'Operators', 'Read-Only', or 'Guests'.
                    ('Administrators' is selected by default.)

        Examples:
        | User Config New | foo | Full Name | somepassword | group=Operators |
        | User Config New | bar | Bar Bar | barbar | group=Guests |
        """
        variables = common.Variables.get_variables()
        admin_passphrase = admin_passphrase or variables["${DUT_ADMIN_SSW_PASSWORD}"]
        kwargs = {
            'admin_passphrase': admin_passphrase,
            'user_name': user_name,
            'full_name': full_name,
            'password': password,
            'password1': password,
            'group': group.title()
        }
        self._cli.userconfig().new(**kwargs)

    def user_config_edit(self, user_name, full_name=DEFAULT,
                         password=DEFAULT, group=DEFAULT,admin_passphrase=None):
        """Edits existing user.

            userconfig -> edit

        Parameters:
        - `user_name`: username of existing user to be edited.
        - `full_name`: new full name for existing user.
                    Defaulted to old full name if not specified.
        - `password`: new password for existing user.
                    Defaulted to old password if not specified.
        - `group`: new group for existing user. Either 'Administrators',
                    'Operators', 'Read-Only', or 'Guests'.
                    Defaulted to old group if not specified.

        Examples:
        | User Config Edit | foo |
        | ... | full_name=Foo1 Foo2 |
        | ... | group=Read-Only |
        | User Config Edit | bar |
        | ... | password=barbar1 |
        | ... | group=Administrators |
        """
        variables = common.Variables.get_variables()
        admin_passphrase = admin_passphrase or variables["${DUT_ADMIN_SSW_PASSWORD}"]
        kwargs = {
            'user_name': user_name,
            'full_name': full_name,
            'password': password,
            'group': group.title(),
            'admin_passphrase':admin_passphrase
        }

        self._cli.userconfig().edit(**kwargs)

    def user_config_delete(self, user_name, confirm=DEFAULT,admin_passphrase=None):
        """Deletes existing user.

            userconfig -> delete

        Parameters:
        - `user_name`: username of existing user to be deleted.
        - `confirm`: confirmation of delete existing user.
                     Either 'Yes' or 'No'.
                     'No' is present by default.

        Example:
        | User Config Delete | foo |
        | User Config Delete | foo | confirm=yes |
        """
        variables = common.Variables.get_variables()
        admin_passphrase = admin_passphrase or variables["${DUT_ADMIN_SSW_PASSWORD}"]
        kwargs = {
            'user_name': user_name,
            'confirm': self._process_yes_no(confirm),
            'admin_passphrase':admin_passphrase
        }
        self._cli.userconfig().delete(**kwargs)

    def user_config_password_assign(self, user_name, new_password):
        """Edits password of existing user.

            userconfig -> password -> assign

        Parameters:
        - `user_name`:        username of existing user to be edited.
        - `new_password`:    new password to replace existing one.

        Example:
        | User Config Password Assign | foo | newpasswd |
        """
        kwargs = {
            'user_name': user_name,
            'new_password': new_password,
        }
        self._cli.userconfig().password().assign(**kwargs)

    def user_config_password_force(self, user_name):
        """Force a user to change the account password on next login.

            userconfig -> password -> force

        Parameters:
        - `user_name`: username of existing user to be edited.

        Example:
        | User Config Password Force | foo |
        """
        kwargs = {
            'user_name': user_name
        }
        self._cli.userconfig().password().force(**kwargs)

    def user_config_policy_account(self, autolock=DEFAULT, attempts=DEFAULT, lm_display=DEFAULT,
            lm_change=DEFAULT, lm_method=DEFAULT, lm_file=DEFAULT, lm_input=DEFAULT,login_attempts_minute=DEFAULT,
            pwd_exp=DEFAULT, pwd_exp_period=DEFAULT, pwd_rem_display=DEFAULT, pwd_rem_period=DEFAULT,
            pwd_reset=DEFAULT):

        """Change account policy.

            userconfig -> policy -> account.

        Parameters:
        - `autolock`: automatically lock account after unsuccessful login attempts.
                    Either 'Yes' or 'No'. 'No' or last selected option is present by default.
        - `attempts`: How many consecutive unsuccessful login attempts will lock the account.
                    '5' or last specified number is present by default.
        - `lm_display`: display an account locked message to users if the Administrator manually
                    locks their account. Either 'Yes' or 'No'.
                    'No' or last selected option is present by default.
        - `lm_change`: change the account locked message. Either 'Yes' or 'No'.
                    'No' or last selected option is present by default.
        - `lm_method`: method to change lock message. Either 'Load', 'Pasting', or 'default'.
                    'Load' is selected by default.
        - `lm_file`: name of a file on the machine to load as lock message.
                    The param is used only if 'Load' method was selected.
        - `lm_input`: lock message. The param is used only if 'Pasting' method was selected.
        - `pwd_exp`: enable password expiration. Either 'Yes' or 'No'.
                    'No' or last selected option is present by default.
        - `pwd_exp_period`: password expiration period in days. The param is used only if
                    'Yes' was specified for previous option 'pwd_exp'.
                    '90' or last specified number is present by default.
        - `pwd_rem_display`: display reminder about password expiration.
                    The param is used only if 'Yes' was specified for option 'pwd_exp'. Either 'Yes' or 'No'.
                    'No' or last selected option is present by default.
        - `pwd_rem_period`: period before user's password change time during which a notification will be
                    printed to the user that her/his password will expire.
                    The param is used only if 'Yes' was specified for previous param 'rem_display'.
                    '14' or last specified number is present by default.
        - `pwd_reset`: require a password reset whenever a user's password is set or changed by an administrator.
                    Either 'Yes' or 'No'. 'No' or last selected option is present by default.

        Examples:
        | [Documentation] | Lock account after several attempts to guess the password |
        | User Config Policy Account |
        | ... | autolock=yes |
        | ... | attempts=10 |
        | [Documentation] | Display specified message to users if the Administrator manually locks their account. |
        | User Config Policy Account |
        | ... | lm_display=yes |
        | ... | lm_change=yes |
        | ... | lm_method=Pasting |
        | ... | lm_input=Custom Lock Message. |
        | [Documentation] | Display a message from a file to users if the Administrator manually locks their account. |
        | User Config Policy Account |
        | ... | lm_display=yes |
        | ... | lm_change=yes |
        | ... | lm_method=Load |
        | ... | lm_file=mymessage.txt |
        | [Documentation] | Display default message to users if the Administrator manually locks their account. |
        | User Config Policy Account |
        | ... | lm_display=yes |
        | ... | lm_change=yes |
        | ... | lm_method=default |
        | [Documentation] | Enable password expiration with displaying reminder about password expiration |
        | User Config Policy Account |
        | ... | pwd_exp=yes |
        | ... | pwd_exp_period=30 |
        | ... | pwd_rem_display=yes |
        | ... | pwd_rem_period=7 |
        | [Documentation] | Require a password reset whenever a user's password is set or changed by an administrator. |
        | User Config Policy Account |
        | ... | pwd_reset=yes |
        """
        kwargs = {
            'autolock': self._process_yes_no(autolock),
            'lm_display': self._process_yes_no(lm_display),
            'pwd_exp': self._process_yes_no(pwd_exp),
            'pwd_reset': self._process_yes_no(pwd_reset)
        }

        if kwargs['autolock'] == 'Y':
            kwargs['attempts'] = attempts

        if kwargs['lm_display'] == 'Y':
            kwargs['lm_change'] = self._process_yes_no(lm_change)
            if kwargs['lm_change'] == 'Y':
                kwargs['lm_method'] = lm_method
                if lm_method.strip().lower() == 'load':
                    kwargs['lm_file'] = lm_file
                elif lm_method.strip().lower() == 'pasting':
                    kwargs['lm_input'] = str(lm_input)+'\r\n.'

        kwargs['login_attempts_minute'] = login_attempts_minute

        if kwargs['pwd_exp'] == 'Y':
            kwargs['pwd_exp_period'] = pwd_exp_period
            kwargs['pwd_rem_display'] = self._process_yes_no(pwd_rem_display)
            if kwargs['pwd_rem_display'] == 'Y':
                kwargs['pwd_rem_period'] = pwd_rem_period

        self._cli.userconfig().policy().account(**kwargs)




    def user_config_policy_passwordstrength(self, min_chars=DEFAULT, case_letters=DEFAULT, numbers=DEFAULT,
                                            spec_chars=DEFAULT, sim_name=DEFAULT, reuse=DEFAULT,
                                            num_recent=DEFAULT, word_list=DEFAULT,
                                            guest_entropy=DEFAULT, admin_entropy=DEFAULT,
                                            cloud_entropy=DEFAULT, email_entropy=DEFAULT,
                                            url_entropy=DEFAULT, readonly_entropy=DEFAULT,
                                            customrole_entropy=DEFAULT, tech_entropy=DEFAULT,
                                            webpolicy_entropy=DEFAULT, oper_entropy=DEFAULT,
                                            helpdesk_entropy=DEFAULT, webadmin_entropy=DEFAULT):
        """Change password policy.

            userconfig -> policy -> passwordstrength.

        Parameters:
        - `min_chars`: minimum number of characters required in the password
                (6 characters is the lowest number possible).
                '6' or last specified number is present by default.
        - `case_letters`: requires at least one upper (A-Z) and one lower (a-z) case letter.
                Either 'Yes' or 'No'. 'No' or last specified option is present by default.
        - `numbers`: requires at least one number (0-9) for passswords. Either 'Yes' or 'No'.
                'No' or last specified option is present by default.
        - `spec_chars`: requires at least one special character. Either 'Yes' or 'No'.
                'No' or last specified option is present.
        - `sim_name`: Reject passwords similar to the username. Either 'Yes' or 'No'.
                'No' or last specified option is present by default.
        - `reuse`: Block reuse of last passwords. Either 'Yes' or 'No'.
                'No' or last specified option is present by default.
        - `num_recent`: number of the most recent passwords not allowed to re-use.
                The param is used only if 'Yes' was specified for previous param 'reuse'.
                '3' or last specified number is present by default.
        - `word_list`: list of words to disallow in passwords.
                'No'
        - `guest_entropy`: assign base entropy to use for Guests
                'No'
        - `admin_entropy`: assign base entropy to use for Administrators.
                'No'
        - `cloud_entropy`: assign base entropy to use for Cloud Administrators
                'No'
        - `email_entropy`: assign base entropy to use for Email Administrators
                'No'
        - `url_entropy`: assign base entropy to use for URL Filtering Administrators
                'No'
        - `readonly_entropy`: assign base entropy to use for Read-Only Operators
                'No'
        - `customrole_entropy`: assign base entropy to use for Custom Roles
                'No'
        - `tech_entropy`: assign base entropy to use for Technicians
                'No'
        - `webpolicy_entropy`: assign base entropy to use for Web Policy Administrators
                'No'
        - `oper_entropy`: assign base entropy to use for Operators
                'No'
        - `helpdesk_entropy`: assign base entropy to use for Help Desk Users
                'No'
        - `webadmin_entropy`: assign base entropy to use for Web Administrators
                'No'

        Examples:
        | [Documentation] | Allow simple passwords |
        | User Config Policy Passwordstrength |
        | ... | min_chars=6 |
        | ... | case_letters=no |
        | ... | numbers=no |
        | ... | spec_chars=no |
        | ... | sim_name=no |
        | ... | reuse=no |
        | [Documentation] | Allow only strong passwords |
        | User Config Policy Passwordstrength |
        | ... | min_chars=16 |
        | ... | case_letters=yes |
        | ... | numbers=yes |
        | ... | spec_chars=yes |
        | ... | sim_name=yes |
        | ... | reuse=yes |
        | ... | num_recent=10 |
        | ... | word_list=N |
        | ... | guest_entropy=N |
        | ... | admin_entropy=N |
        | ... | cloud_entropy=N |
        | ... | email_entropy=N |
        | ... | url_entropy=N |
        | ... | readonly_entropy=N |
        | ... | customrole_entropy=N |
        | ... | tech_entropy=N |
        | ... | webpolicy_entropy=N |
        | ... | oper_entropy=N |
        | ... | helpdesk_entropy=N |
        | ... | webadmin_entropy=N |
        """
        kwargs = {
            'min_chars': min_chars,
            'case_letters': self._process_yes_no(case_letters),
            'numbers': self._process_yes_no(numbers),
            'spec_chars': self._process_yes_no(spec_chars),
            'sim_name': self._process_yes_no(sim_name),
            'reuse': self._process_yes_no(reuse)
        }

        if kwargs['reuse'] == 'Y':
            kwargs['num_recent'] = num_recent

        self._cli.userconfig().policy().passwordstrength(**kwargs)

    def user_config_external_setup_new(self, server, password, port=DEFAULT,
                        reply_timeout=DEFAULT, auth_type=DEFAULT,
                        cred_timeout=DEFAULT,
                        delete_mapping=DEFAULT, create_mapping=DEFAULT,
                        group_name=DEFAULT, role=DEFAULT):
        """Adds new external RADIUS authentication server configuration.

            userconfig -> external -> setup -> new.

        Parameters:
        - `server`: hostname or IP address of an authentication server.
        - `password`: RADIUS shared password.
        - `port`: port number of the authentication server. '1812' is present by default.
        - `reply_timeout`: timeout in seconds for receiving a valid reply from the server.
                '5' is present by default.
        - `auth_type`: authentication type.  Either 'CHAP' or 'PAP'. 'PAP' is selected by default.
        - `cred_timeout`: timeout in seconds for how long the external authentication credentials
                will be cached. (Enter '0' to disable expiration of authentication credentials
                altogether when using one time passwords.) '0' or last specified number is present by default.
        - `delete_mapping`: specify whether to delete group mapping.
                This parameter is only valid when there is existing group mapping.
                Either 'Yes' or 'No'. 'No' is selected by default.
        - `create_mapping`: specify whether to create group mapping.
                This parameter is only valid when there is no group mapping.
                Either 'Yes' or 'No'. 'Yes' is present by default for first auth server,
                'No' is present by default in other cases.
        - `group_name`: group name to map when create_mapping above is set to 'Yes'.
        - `role`: role for created group. It is available when create_mapping is set to
                'Yes' and 'group_name' specified.

        Examples:
        | User Config External Setup New | 1.1.1.1 |
        | ... | ironport |
        | ... | reply_timeout=15 |
        | ... | create_mapping=yes |
        | ... | group_name=test |
        | ... | role=Guests |
        | User Config External Setup New | 192.168.1.3 |
        | ... | 123456 |
        | ... | port=1813 |
        | ... | auth_type=CHAP |
        | ... | cred_timeout=10 |
        | ... | delete_mapping=no |
        | User Config External Setup New | auth.server.com |
        | ... | 111111 |
        | ... | auth_type=PAP |
        | ... | cred_timeout=0 |
        | ... | delete_mapping=yes |
        """
        kwargs_setup = {
            'use_ext_auth': 'y',
            'cred_timeout': cred_timeout,
            'mechanism': 'radius',
        }
        kwargs = {
            'host': server,
            'port': port,
            'password': password,
            'password1': password,
            'timeout': reply_timeout,
            'auth_type': auth_type,
        }
        if delete_mapping != DEFAULT:
            kwargs['delete_mapping'] = delete_mapping
        if create_mapping != DEFAULT:
            kwargs['create_mapping'] = create_mapping
        if group_name != DEFAULT:
            kwargs['group_name'] = group_name
        if role != DEFAULT:
            kwargs['role'] = role
        self._cli.userconfig().external().setup(**kwargs_setup).new(**kwargs)

    def user_config_external_setup_edit(self, server=DEFAULT,
                  hostname_or_ip=DEFAULT, port=DEFAULT, password=DEFAULT,
                  reply_timeout=DEFAULT, auth_type=DEFAULT,
                  cred_timeout=DEFAULT,
                  delete_mapping=DEFAULT, create_mapping=DEFAULT,
                  group_name=DEFAULT, role=DEFAULT):
        """Edits existing external server configuration.

            userconfig -> external -> setup -> edit.

        Parameters:
        - `server`: hostname or IP address of existing server to edit. Required parameter.
        - `hostname_or_ip`: new hostname or IP address for edited server.
                Old value is present by default.
        - `password`: new shared password. Old password is used by default.
        - `port`: new port number for edited server. Old value is used by default.
        - `reply_timeout`: new timeout in seconds for receiving a valid reply from the server.
                Old value is present by default.
        - `auth_type`: new authentication type.  Either 'CHAP' or 'PAP'.
                Old selection is present by default.
        - `cred_timeout`: timeout in seconds for how long the external authentication credentials
                will be cached. (Enter '0' to disable expiration of authentication credentials
                altogether when using one time passwords.) '0'
                or last specified number is present by default.
        - `delete_mapping`: specify whether to delete group mapping.
                This parameter is only valid when there is existing group mapping.
                Either 'Yes' or 'No'. 'No' is selected by default.
        - `create_mapping`: specify whether to create group mapping.
                This parameter is only valid when there is no group mapping.  Either 'Yes' or 'No'.
                'Yes' is present by default for first auth server,
                'No' is present by default in other cases.
        - `group_name`: group name to map when create_mapping above is set to 'Yes'.
        - `role`: role for created group. It is available when create_mapping is set to
                'Yes' and 'group_name' specified.

        Examples:
        | User Config External Setup Edit |1.1.1.1 |
        | ... | hostname_or_ip=1.1.1.1 |
        | ... | password=123456 |
        | ... | reply_timeout=15 |
        | ... | create_mapping=yes |
        | ... | group_name=test1 |
        | ... | role=Guests |
        | User Config External Setup Edit | 1.1.1.1 |
        | ... | port=1813 |
        | ... | auth_type=CHAP |
        | ... | cred_timeout=10 |
        | ... | delete_mapping=no |
        | User Config External Setup New | auth.server.com |
        | ... | auth_type=PAP |
        | ... | cred_timeout=0 |
        | ... | delete_mapping=yes |
        """
        kwargs_setup = {
            'use_ext_auth': 'y',
            'cred_timeout': cred_timeout,
            'mechanism': 'radius',
        }
        kwargs = {
            'host': server,
            'host_name': hostname_or_ip,
            'port': port,
            'password': password,
            'password1': password,
            'timeout': reply_timeout,
            'auth_type': auth_type,
        }
        if delete_mapping != DEFAULT:
            kwargs['delete_mapping'] = delete_mapping
        if create_mapping != DEFAULT:
            kwargs['create_mapping'] = create_mapping
        if group_name != DEFAULT:
            kwargs['group_name'] = group_name
        if role != DEFAULT:
            kwargs['role'] = role
        self._cli.userconfig().external().setup(**kwargs_setup).edit(**kwargs)

    def user_config_external_setup_move(self, server=DEFAULT, position=DEFAULT,
            cred_timeout=DEFAULT,
            delete_mapping=DEFAULT, create_mapping=DEFAULT, group_name=DEFAULT, role=DEFAULT):
        """Moves external auth server to a different postion.
        Note that this option is only available when there are 2 or more auth servers already configured.

            userconfig -> external -> setup -> move.

        Parameters:
        - `server`:         hostname or IP address of server to move.
                            Required parameters.
        - `position`:         target position to move to. Current position is
                            indicated by default.
        - `cred_timeout`:     timeout in seconds for how long the external
                            authentication credentials will be cached.
                            (Enter '0' to disable expiration of authentication
                            credentials altogether when using one time passwords.)
                            '0' or last specified number is present by default.
        - `delete_mapping`: specify whether to delete group mapping.
                            This parameter is only valid when there is existing
                            group mapping.  Either 'Yes' or 'No'.
                            'No' is selected by default.
        - `create_mapping`: specify whether to create group mapping.
                            This parameter is only valid when there is no group mapping.
                            Either 'Yes' or 'No'.
                            'Yes' is present by default for first auth server,
                            'No' is present by default in other cases.
        - `group_name`:     group name to map when create_mapping above is set to 'Yes'.
        - `role`:             role for created group. It is available when create_mapping
                            is set to 'Yes' and 'group_name' specified.

        Examples:
        | User Config External Setup Move | 1.1.1.1 |
        | ... | position=2 |
        | User Config External Setup Move | 1.1.1.1 |
        | ... | position=1 |
        | ... | create_mapping=yes |
        | ... | group_name=test1 |
        | ... | role=Guests |
        | User Config External Setup Edit | 1.1.1.1 |
        | ... | position=2 |
        | ... | cred_timeout=10 |
        """
        kwargs_setup = {
            'use_ext_auth': 'y',
            'cred_timeout': cred_timeout,
            'mechanism': 'radius',
        }
        kwargs = {
            'host': server,
            'position': position,
        }
        if delete_mapping != DEFAULT:
            kwargs['delete_mapping'] = delete_mapping
        if create_mapping != DEFAULT:
            kwargs['create_mapping'] = create_mapping
        if group_name != DEFAULT:
            kwargs['group_name'] = group_name
        if role != DEFAULT:
            kwargs['role'] = role
        self._cli.userconfig().external().setup(**kwargs_setup).move(**kwargs)

    def user_config_external_setup_delete(self, server=DEFAULT,
            cred_timeout=DEFAULT,
            delete_mapping=DEFAULT, create_mapping=DEFAULT, group_name=DEFAULT,
            role=DEFAULT):
        """Deletes existing external auth server.

            userconfig -> external -> setup -> delete.

        Parameters:
        - `server`: hostname or IP address of server to delete.
        - `cred_timeout`: timeout in seconds for how long the external authentication
            credentials will be cached. (Enter '0' to disable expiration of authentication
            credentials altogether when using one time passwords.) '0'
            or last specified number is present by default.
        - `delete_mapping`: specify whether to delete group mapping.
            This parameter is only valid when there is existing group mapping.
            Either 'Yes' or 'No'. 'No' is selected by default.
        - `create_mapping`: specify whether to create group mapping.
            This parameter is only valid when there is no group mapping. Either 'Yes' or 'No'.
            'Yes' is present by default for first auth server, 'No' is present by default in other cases.
        - `group_name`: group name to map when create_mapping above is set to 'Yes'.
        - `role`: role for created group. It is available when create_mapping is set to
            'Yes' and 'group_name' specified.

        Examples:
        | User Config External Setup Delete | 1.1.1.1 |
        | User Config External Setup Delete | 192.168.1.3 |
        | ... | create_mapping=yes |
        | ... | group_name=test |
        | ... | role=Guests |
        """
        kwargs_setup = {
            'use_ext_auth': 'y',
            'cred_timeout': cred_timeout,
            'mechanism': 'radius',
        }
        kwargs = {
            'host': server,
        }
        if delete_mapping != DEFAULT:
            kwargs['delete_mapping'] = delete_mapping
        if create_mapping != DEFAULT:
            kwargs['create_mapping'] = create_mapping
        if group_name != DEFAULT:
            kwargs['group_name'] = group_name
        if role != DEFAULT:
            kwargs['role'] = role
        self._cli.userconfig().external().setup(**kwargs_setup).delete(**kwargs)

    def user_config_external_setup_clear(self, confirm=DEFAULT, cred_timeout=DEFAULT):
        """Clears all existing external auth server.

            userconfig -> external -> setup -> clear.

        Parameters:
        - `confirm`: confirm whether to clear all existing external auth server configuration.
            Either 'Yes' or 'No'. 'No' is present by default.

        Examples:
        | User Config External Setup Clear |
        | User Config External Setup Clear | confirm=yes |
        """
        kwargs_setup = {
            'use_ext_auth': 'y',
            'cred_timeout': cred_timeout,
            'mechanism': 'radius',
        }
        self._cli.userconfig().external().setup(**kwargs_setup).clear(self._process_yes_no(confirm))

    def user_config_external_setup_disable(self):
        """Disables external authentication.

            userconfig -> external -> setup.

        Examples:
        | User Config External Setup Disable |
        """
        self._cli.userconfig().external().setup(use_ext_auth='n')

    def user_config_external_setup_ldap(self, cred_timeout=DEFAULT, ldap_query=DEFAULT, timeout=DEFAULT,
            ext_group=DEFAULT, role=DEFAULT):
        """Add external LDAP authentication.

            userconfig -> external -> setup.

        Parameters:
        - `cred_timeout`: timeout in seconds for how long the external authentication credentials
            will be cached. (Enter '0' to disable expiration of authentication credentials altogether
            when using one time passwords.) '0' or last specified number is present by default.
        - `ldap_query`: Available LDAP external authentication query.
            First available LDAP query is selected by default.
        - `timeout`: timeout in seconds for entire LDAP authentication request.
            '10' or last specified number is present by default.
        - `ext_group`: external group name to map.
        - `role`: role for mapping group:
            1. Administrators
            - Administrators have full access to all settings of the system.
            2. Operators
            - Operators are restricted from creating new user accounts.
            3. Read-Only Operators
            - Read-Only operators may only view settings and status information.
            4. Guests
            - Guest users may only view status information.
            5. Technicians
            - Technician can only manage upgrades and feature keys.
            6. Help Desk Users
            - Help Desk users have access only to ISQ and Message Tracking.
            7. Web Administrators
            - Web Admins are restricted to Web menus only.
            8. Email Administrators
            - Email Admins are restricted to Email menus only, ISQ and system quarantine rights.
            9. URL Filtering Administrators
            - URL Filtering Admins are restricted to Custom URL Categories pages in a sandbox.
            10. Web Policy Administrators
            - Web Policy Admins are restricted to policy and URL pages in a sandbox.

        Examples:
        | User Config External Setup Ldap |
        | ... | ldap_query=OpenLDAP.externalauth |
        | ... | timeout=30 |
        | ... | ext_group=test |
        | ... | role=Administrators |
        | User Config External Setup Ldap |
        | ... | ldap_query=SecondLDAP.externalauth |
        | ... | cred_timeout=10 |
        """
        kwargs_setup = {
            'use_ext_auth': 'y',
            'cred_timeout': cred_timeout,
            'mechanism': 'ldap',
            'ldap_query':ldap_query,
            'timeout':timeout,
            'ext_group':ext_group,
        }
        if ext_group!=DEFAULT:
            kwargs_setup['role']=role

        self._cli.userconfig().external().setup(**kwargs_setup)

    def user_config_external_groups_new(self, group_name, mapping_type=DEFAULT):
        """Adds new group mapping.

            userconfig -> external -> groups -> new.

        Parameters:
        - `group_name`: name of external group to map.
        - `mapping_type`: map type. First is selected by default.
            1. Administrators
                - Administrators have full access to all
                settings of the system.
            2. Operators
                - Operators are restricted from creating new
                user accounts.
            3. Read-Only Operators
                - Read-Only operators may only view settings
                and status information.
            4. Guests
                - Guest users may only view status information.
            5. Technicians
                - Technician can only manage upgrades and feature keys.
            6. Help Desk Users
                - Help Desk users have access only to ISQ and
                Message Tracking.
            7. Web Administrators
                - Web Admins are restricted to Web menus only.
            8. Email Administrators
                - Email Admins are restricted to Email menus only,
                ISQ and system quarantine rights.
            9. URL Filtering Administrators
                - URL Filtering Admins are restricted to Custom URL
                Categories pages in a sandbox.
            10. Web Policy Administrators
                - Web Policy Admins are restricted to policy and URL
                pages in a sandbox.

        Examples:
        | User Config External Groups New | testname | mapping_type=Operators |
        """
        kwargs = {
            'group_name': group_name,
            'role': mapping_type.title(),
        }
        self._cli.userconfig().external().groups().new(**kwargs)

    def user_config_external_groups_edit(self, group_name=DEFAULT,
                                         mapping_type=DEFAULT):
        """Edits existing group mapping.

            userconfig -> external -> groups -> edit.

        Parameters:
        - `group_name`: name of existing group mapping to edit.
        - `mapping_type`: map type. See list of available types in keyword for group creation.
            Old selection is present by default.

        Example:
        | User Config External Groups Edit | testname | mapping_type=Guests |
        """
        kwargs = {
            'group_name': group_name,
            'role': mapping_type.title(),
        }
        self._cli.userconfig().external().groups().edit(**kwargs)

    def user_config_external_groups_delete(self, group_name=DEFAULT):
        """Deletes existing group mapping.

            userconfig -> external -> groups -> delete.

        Parameters:
        - `group_name`: name of existing group mapping to delete.

        Example:
        | User Config External Groups Delete | test |
        """
        kwargs = {
            'group_name': group_name,
        }
        self._cli.userconfig().external().groups().delete(**kwargs)

    def user_config_external_groups_clear(self):
        """Clears all existing group mapping.

            userconfig -> external -> groups -> clear.

        Example:
        | User Config External Groups Clear |
        """
        self._cli.userconfig().external().groups().clear()

    def user_config_external_groups_print(self):
        """Displays all currently configured group mapping.

            userconfig -> external -> groups -> print.

        Examples:
        | ${out}= | User Config External Groups Print |
        | Log | ${out} |
        """
        return self._cli.userconfig().external().groups().print_groups()

    def user_config_role_email_new(self,
        name,
        descr=DEFAULT,
        access_reports=None,
        reports_type=None,
        access_tracking=None,
        access_quarantines=None,
        ):
        """Define a new Email role.
            userconfig -> role -> new.

        Parameters:
        - `name`: name for the role.
        - `descr`: short description for the role.
        - `access_reports`: answer to question: Select type of access to reports?
          This question will be asked if Centralized Email Reporting is enabled.
          Possible answers:
            1. No access
            2. Access to reports by Reporting Group
            3. Access to reports From All Email Appliances
        - `reports_type`: answer to question: Select type of reports to be given access:
          This question will be asked if type of access to reports is not equal 'No access'.
          Possible answers:
            1. All Reports
            2. Mail Policy Reports
            3. DLP Reports
        - `access_tracking`: answer to question: Select type of access to tracking?
          This question will be asked if Centralized Email Message Tracking is enabled.
          Possible answers:
            1. No access
            2. Message Tracking access
        - `access_quarantines`: answer to question: Select type of access to quarantines?
          This question will be asked if either Spam Quarantine or
          Policy, Virus and Outbreak Quarantines is enabled. Possible answers:
            1. No access
            2. Allow assignment

        Example:
        | User Config Role Email New | test | descr=Testing role |
        | User Config Role Email New | test2 | descr=Another testing role |
        | ... | access_reports=by Reporting Group |
        | ... | reports_type=DLP Reports |
        | ... | access_tracking=Message Tracking access |
        | ... | access_quarantines=Allow assignment |
        """

        kwargs = {
            'type': 'Email',
            'name': name,
            'descr': descr,
        }

        if access_reports is not None:
            kwargs['access_reports'] = access_reports
            if reports_type is not None:
                kwargs['reports_type'] = reports_type

        if access_tracking is not None:
            kwargs['access_tracking'] = access_tracking

        if access_quarantines is not None:
            kwargs['access_quarantines'] = access_quarantines

        self._cli.userconfig().role().new(**kwargs)

    def user_config_role_email_edit(self,
        name=DEFAULT,
        new_name=DEFAULT,
        descr=DEFAULT,
        access_reports=None,
        reports_type=None,
        access_tracking=None,
        access_quarantines=None,
        ):
        """Edits existing Email role.
            userconfig -> role -> edit.

        Parameters:
        - `name`: name or number of a role to edit.
        - `new_name`: new name for the user role.
        - `descr`: short description for the role.
       - `access_reports`: answer to question: Select type of access to reports?
          This question will be asked if Centralized Email Reporting is enabled.
          Possible answers:
            1. No access
            2. Access to reports by Reporting Group
            3. Access to reports From All Email Appliances
        - `reports_type`: answer to question: Select type of reports to be given access:
          This question will be asked if type of access to reports is not equal 'No access'.
          Possible answers:
            1. All Reports
            2. Mail Policy Reports
            3. DLP Reports
        - `track_reports`: answer to question: Select type of access to tracking?
          This question will be asked if Centralized Email Message Tracking is enabled.
          Possible answers:
            1. No access
            2. Message Tracking access
        - `access_quarantines`: answer to question: Select type of access to quarantines?
          This question will be asked if either Spam Quarantine or
          Policy, Virus and Outbreak Quarantines is enabled.
          Possible answers:
            1. No access
            2. Allow assignment

        Examples:
        | User Config Role Email Edit | test | new_name=test1 |
        | User Config Role Email Edit | test1 | access_quarantines=Allow assignment |
        """

        kwargs = {
            'name': name,
            'new_name': new_name,
            'descr': descr,
        }

        if access_reports is not None:
            kwargs['access_reports'] = access_reports
            if reports_type is not None:
                kwargs['reports_type'] = reports_type

        if access_tracking is not None:
            kwargs['access_tracking'] = access_tracking

        if access_quarantines is not None:
            kwargs['access_quarantines'] = access_quarantines

        self._cli.userconfig().role().edit(**kwargs)

    def user_config_role_web_new(self, name, descr=DEFAULT,
                                visibility=DEFAULT, publish=DEFAULT):
        """Define a new Web role.

            userconfig -> role -> new.

        Parameters:
        - `name`: name for the role.
        - `descr`: short description for the role.
        - `visibility`: Visibility of Policies and Categories. Either 'Visible' or 'Hidden'.
            Visible by default.
        - `publish`: Publish Privilege. Either 'On' or 'Off'.
            Off by default.

        Example:
        | User Config Role Web New | test |
        | User Config Role Web New | test1 |
        | ... | descr=Testing role |
        | ... | visibility=Visible |
        | ... | publish=On |
        """
        kwargs = {
            'type': 'Web',
            'name': name,
            'descr': descr,
            'visibility': visibility,
            'publish': publish,
        }

        self._cli.userconfig().role().new(**kwargs)

    def user_config_role_web_edit(self, name=DEFAULT, new_name=DEFAULT,
                            descr=DEFAULT, visibility=DEFAULT, publish=DEFAULT):
        """Edits existing Web role.

            userconfig -> role -> edit.

        Parameters:
        - `name`: name or number to edit.
        - `new_name`: new name for the user role. Old value is present by default.
        - `descr`: short description for the role. Old value is present by default.
        - `visibility`: Visibility of Policies and Categories. Either 'Visible' or 'Hidden'.
            Visible by default.
        - `publish`: Publish Privilege. Either 'On' or 'Off'. Old selection is present by default.

        Examples:
        | User Config Role Edit | test |
        | ... | new_name=test1 |
        | ... | descr=New Description |
        | User Config Role Edit | test1 |
        | ... | visible=Hidden |
        | ... | publish=Off |
        """
        kwargs = {
            'name': name,
            'new_name': new_name,
            'descr': descr,
            'visibility': visibility,
            'publish': publish,
        }

        self._cli.userconfig().role().edit(**kwargs)

    def user_config_role_delete(self, name=DEFAULT):
        """Deletes existing role.

            userconfig -> role -> delete.

        Parameters:
        - `name`: role name or number to delete.

        Example:
        | User Config Role Delete | test |
        """
        self._cli.userconfig().role().delete(name=name)

    def user_config_status(self, name):
        """Report status of an account.

            userconfig -> status.

        Parameters:
        - `name`: username to check status.

        Examples:
        | ${user_status}= | User Config Status     test |
        | Log | ${user_status} |
        """
        return self._cli.userconfig().status(name).status()

    def user_config_status_lock(self, name, admin_passphrase=None):
        """Lock an account.

            userconfig -> status.

        Parameters:
        - `name`: username to edit.

        Examples:
        | User Config Status Lock | test |
        """
        variables = common.Variables.get_variables()
        admin_passphrase = admin_passphrase or variables["${DUT_ADMIN_SSW_PASSWORD}"]
        return self._cli.userconfig().status(name).lock(admin_passphrase)

    def user_config_status_unlock(self, name, admin_passphrase=None):
        """Unlock an account.

            userconfig -> status.

        Parameters:
        - `name`: username to edit.

        Examples:
        | User Config Status Unlock | test |
        """
        variables = common.Variables.get_variables()
        admin_passphrase = admin_passphrase or variables["${DUT_ADMIN_SSW_PASSWORD}"]
        return self._cli.userconfig().status(name).unlock(admin_passphrase)

    def user_config_dlptracking(self, allow=DEFAULT,user=None):
        """Configure DLP tracking privileges.

            userconfig -> dlptracking.

        Parameters:
        - `allow`: Should a UserType specified by user parameter be allowed to view
        DLP Matched Content in Message Tracking results?.
        Either 'Yes' or 'No'.
         'Yes' or last selected option is present by default.


        - `user`: User type in one of the following - admin or emailAdmin or helpDesk or
        operators or readOnlyOperators or urlFilteringAdmin or webAdmin or webPolicyAdmin or all

         where  -`admin`: corresponds to `Administrators`
                -`emailAdmin`: corresponds to `Email Administrators`
                -`helpDesk`: corresponds to `Help Desk Users`
                -`readOnlyOperators`: corresponds to `Read-Only Operators`
                -`urlFilteringAdmin`: corresponds to  `URL Filtering Administrators`
                -`webAdmin`: corresponds to  `Web Administrators`
                -`webPolicyAdmin`: corresponds to `Web Policy Administrators`
                -'all': for all user types in the *Predefined* list Only

        Examples:
        | User Config Dlptracking | allow=yes | user=emailAdmin
        | User Config Dlptracking | allow=no | user=all
        """

        userlist= ['admin','emailAdmin','helpDesk','operators',\
                   'readOnlyOperators','urlFilteringAdmin','webAdmin','webPolicyAdmin','all']
        if user not in userlist:
            raise ValueError("user argument - %s is not valid - Acceptable values are admin or \
            emailAdmin or helpDesk or operators or readOnlyOperators \
            or urlFilteringAdmin or webAdmin or webPolicyAdmin or all" %user)

        self._cli.userconfig().dlptracking(user=user,allow=self._process_yes_no(allow))

    def userconfig_two_factor_disable(self):
        """Disables twofactor authentication.

            userconfig -> twofactorauth -> setup.

        Examples:
        | User Config Two Factor Disable |
        """
        self._cli.userconfig().twofactor().setup(use_2fa_auth='n')

    def userconfig_two_factor_radius_new(self, host, password, port=DEFAULT,
                                         auth_type=DEFAULT, timeout=DEFAULT):
        """This option is used to configure two factor authentication

        *Parameters*
        - `host` : host name or IP address of the RADIUS server.
        - `port`: Port number of the RADIUS server.
        - `password`: Shared Password of the Server.
        - `auth_type`: the authentication type.
        1 - CHAP
        2 - PAP
        - `timeout` : timeout in seconds for receiving a valid reply from
        the server

        *Examples*
        | UserConfig Two Factor Radius New | 1.1.1.1 | ironport | port=1812 |
        | ... | timeout=10 | auth_type=2 |

        """
        kwargs_setup = {
            'use_2fa_auth': 'y',
        }
        kwargs = {
            'host': host,
            'port': port,
            'password': password,
            'pass_again': password,
            'timeout': timeout,
            'auth_type': auth_type,
        }
        self._cli.userconfig().twofactor().setup(**kwargs_setup).new(**kwargs)

    def userconfig_two_factor_radius_clear(self, confirm_delete=DEFAULT):
        """This option is used to clear all the RADIUS Servers.

        *Parameters*
        - `confirm_delete`: confirm whether to clear all existing external
           auth server  configuration.
            Either 'Yes' or 'No'. 'No' is present by default.

        *Examples*
        | UserConfig Two Factor Radius Clear | confirm_delete=y |

        """
        kwargs_setup = {
            'use_2fa_auth': 'y',
        }
        kwargs = {
            'confirm_delete': confirm_delete,
        }
        self._cli.userconfig().twofactor().setup(**kwargs_setup).clear(**kwargs)

    def userconfig_two_factor_radius_delete(self, host=DEFAULT):
        """This option is used to delete a RADIUS server.

        *Parameters*
        - `host`: Choose the host to delete.

        *Examples*
        | UserConfig Two Factor Radius Delete | host=1.1.1.2 |
        """
        kwargs_setup = {
            'use_2fa_auth': 'y',
        }
        kwargs = {
            'host': host,
        }

        self._cli.userconfig().twofactor().setup(**kwargs_setup).delete(**kwargs)

    def userconfig_two_factor_privilege_add(self, *args):
        """Add the two factor privilege for the
        particular default or custom role.

        *Parameters:*
        - `role`: the name of the particular existing custom or predefined
        role from which the second factor privilege is going to be
        added.

        *Examples:*
        | UserConfig Two Factor Privilege Add | role=operator |
        """

        kwargs = self._convert_to_dict(args)
        self._cli.userconfig().twofactor().privilege().add(**kwargs)

    def userconfig_two_factor_privilege_delete(self, *args):
        """Delete the two factor privilege for the
        particular default or custom role. This option may not exist
        if all roles are already deleted

        *Parameters:*
        - `role`: the name of the particular existing custom or predefined
        role from which the second factor privilege is going to be
        deleted.

        *Examples:*
        | UserConfig Two Factor Privilege Delete | role=operator |
        """

        kwargs = self._convert_to_dict(args)
        self._cli.userconfig().twofactor().privilege().delete(**kwargs)

    def userconfig_external_setup_saml(self, *args):
        """
        Keyword to enable SAML authentication for external users

        *Parameters:*
        - `cache_time`: Please enter the timeout in seconds for how long the
                        external authentication credentials will be cached.
                        Enter '0' to disable expiration of authentication
                        credentials altogether when using one time passphrases.
        - `group_name`: Please enter the external group name to map (group
                        names are case-sensitive)
        - `role`: Assign a role to "testG":
                1. Administrators - Administrators have full access to all
                                    settings of the system.
                2. Operators - Operators are restricted from creating new user
                               accounts.
                3. Cloud Administrators - Cloud Administrators have restrictions
                               on access to network and data-center related
                               configuration.
                4. Read-Only Operators - Read-Only operators may only view
                               settings and status information.
                5. Guests - Guest users may only view status information.
                6. Technicians - Technician can only manage upgrades and feature keys.
                7. Help Desk Users - Help Desk users have access only to ISQ
                               and Message Tracking.
        - `group_attribute` : group attribute to be matched in saml attributes

        *Examples:*
        | Userconfig External Setup Saml        |
        | ... | cache_time=5                    |
        | ... | group_name=${SAML_GROUP1}       |
        | ... | role=${SAML_GROUP1_ROLE}        |
        | ... | group_attribute = ${GRP_ATTRIB} |
        """
        kwargs = self._convert_to_dict(args)
        kwargs_setup = {
            'use_ext_auth': 'y',
            'cred_timeout': kwargs.pop('cache_time',0),
            'mechanism': 'saml',
        }
        self._cli.userconfig().external().setup(**kwargs_setup).saml(**kwargs)

    def userconfig_external_devopssetup(self, *args):
        """
        Keyword to setup devops for external users authentication.

        *Parameters:*
        - `use_ext_auth`: Do you want to enable Dev Ops external authentication (Yes | No)
        - `cache_time`: Please enter the timeout in seconds for how long the external
                        authentication credentials will be cached. (Enter '0' to
                        disable expiration of authentication credentials altogether
                        when using one time passphrases.)
        - `mechanism`: Select authentication type.
                        1. SAML
        - `group_name`: Please enter the external group name to map (group names
                        are case-sensitive)
        - `role`: Assign a role to "testG":
                1. Administrators - Administrators have full access to all
                                    settings of the system.
                2. Operators - Operators are restricted from creating new user
                               accounts.
                3. Cloud Administrators - Cloud Administrators have restrictions
                               on access to network and data-center related
                               configuration.
                4. Read-Only Operators - Read-Only operators may only view
                               settings and status information.
                5. Guests - Guest users may only view status information.
                6. Technicians - Technician can only manage upgrades and feature keys.
                7. Help Desk Users - Help Desk users have access only to ISQ
                               and Message Tracking.
        - `group_attribute` : group attribute to be matched in saml
        - `sso_string` : toggle string for Dev Ops SSO

        *Examples:*
        | Userconfig External Devopssetup    |
        | ... | use_ext_auth=YES             |
        | ... | cache_time=10                |
        | ... | mechanism=saml               |
        | ... | group_name=${SAML_GROUP2}    |
        | ... | role=${SAML_GROUP2_ROLE}     |
        | ... | group_attribute=${GRP_ATTR}  |
        | ... | sso_string=samluser,testuser |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.userconfig().external().devopssetup(**kwargs)

    def userconfig_external_devopsgroups_new(self, *args):
        """
        Keyword to create new devops group for external users authentication.

        *Parameters:*
        - `group_name`: Please enter the external group name to map (group
                        names are case-sensitive)
        - `role`: Assign a role to "testG":
                1. Administrators - Administrators have full access to all
                                    settings of the system.
                2. Operators - Operators are restricted from creating new user
                               accounts.
                3. Cloud Administrators - Cloud Administrators have restrictions
                               on access to network and data-center related
                               configuration.
                4. Read-Only Operators - Read-Only operators may only view
                               settings and status information.
                5. Guests - Guest users may only view status information.
                6. Technicians - Technician can only manage upgrades and feature keys.
                7. Help Desk Users - Help Desk users have access only to ISQ
                               and Message Tracking.

        *Examples:*
        | Userconfig External Devopsgroups New  |
        | ... | group_name=${SAML_GROUP3}       |
        | ... | role=${SAML_GROUP3_ROLE}        |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.userconfig().external().devopsgroups().new(**kwargs)

    def userconfig_external_devopsgroups_edit(self, *args):
        """
        Keyword to edit devops group for external users authentication.

        *Parameters:*
        - `group_name`: Please enter the external group name to map (group
                        names are case-sensitive)
        - `role`: Assign a role to "testG":
                1. Administrators - Administrators have full access to all
                                    settings of the system.
                2. Operators - Operators are restricted from creating new user
                               accounts.
                3. Cloud Administrators - Cloud Administrators have restrictions
                               on access to network and data-center related
                               configuration.
                4. Read-Only Operators - Read-Only operators may only view
                               settings and status information.
                5. Guests - Guest users may only view status information.
                6. Technicians - Technician can only manage upgrades and feature keys.
                7. Help Desk Users - Help Desk users have access only to ISQ
                               and Message Tracking.

        *Examples:*
        | Userconfig External Devopsgroups Edit     |
        | ... | group_name=${SAML_GROUP3}           |
        | ... | role=${SAML_GROUP1_ROLE}            |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.userconfig().external().devopsgroups().edit(**kwargs)

    def userconfig_external_devopsgroups_delete(self, *args):
        """
        Keyword to delete devops group for external users authentication.

        *Parameters:*
        - `group_name`: Choose a mapping to delete

        *Examples:*
        | Userconfig External Devopsgroups Delete   |
        | ... | group_name=${SAML_GROUP3}           |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.userconfig().external().devopsgroups().delete(**kwargs)

    def userconfig_external_devopsgroups_clear(self):
        """
        Keyword to remove all devops group for external users authentication.

        *Parameters:*
        None

        *Examples:*
        | Userconfig External Devopsgroups Clear |
        """
        self._cli.userconfig().external().devopsgroups().clear()

    def userconfig_external_devopsgroups_print(self):
        """
        Keyword to print configured devops group for external users authentication.

        *Parameters:*
        None

        *Examples:*
        | ${devops_groups}= | Userconfig External Devopsgroups Print    |
        | Log               | ${devops_groups} |                        |
        | Should Contain    | ${devops_groups} | ${SAML_GROUP3}         |
        | Should Contain    | ${devops_groups} | ${SAML_GROUP4}         |
        """
        return self._cli.userconfig().external().devopsgroups().print_groups()


    def user_config_print_options(self):
        """To view configured users list

        Examples:
        | User Config Print Options  |

        | ${users}= | Users Config Print Options |
        | Log | ${users} |
        """

        output = self._cli.userconfig().print_options()
        self._info(output)
        return output