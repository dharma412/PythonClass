#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1350/cli/keywords/userconfig.py#1 $
# $DateTime: 2020/01/06 01:25:43 $
# $Author: saurgup5 $

from common.cli.clicommon import CliKeywordBase, DEFAULT

class userconfig(CliKeywordBase):
    """This CLI command is used to  manage user accounts and connections
       to external authentication sources

       CLI -> Userconfig

       The various options are
       - `new` : Create a new account.
       - `edit` : Modify an account.
       - `delete`: Remove an account.
       - `policy` : Change password and account policy settings.
       - `password` : Change the password for a user.
       - `role` : Create/modify user roles.
       - `status`: Change the account status.
       - `external` : Configure external authentication.
       - `twofactorauth`: Configure two factor authentication(2FA)
       - `dlptracking` : Configure DLP tracking privileges.
    """

    def get_keyword_names(self):
        return ['userconfig_new',
                'userconfig_batch_add',
                'userconfig_edit',
                'userconfig_delete',
                'userconfig_password',
                'userconfig_password_force_instant',
                'userconfig_password_force_later',
                'userconfig_status',
                'userconfig_external_radius_new',
                'userconfig_external_radius_edit',
                'userconfig_external_radius_move',
                'userconfig_external_radius_delete',
                'userconfig_external_radius_clear',
                'userconfig_role_new',
                'userconfig_role_edit',
                'userconfig_role_delete',
                'userconfig_policy_passwordstrength',
                'userconfig_policy_account',
                'userconfig_external_setup_disable',
                'userconfig_external_setup_ldap',
                'userconfig_external_groups_new',
                'userconfig_external_groups_edit',
                'userconfig_external_groups_delete',
                'userconfig_external_groups_print',
                'userconfig_external_groups_clear',
                'userconfig_dlptracking_add',
                'userconfig_dlptracking_delete',
                'userconfig_urltracking_add',
                'userconfig_urltracking_delete',
                'userconfig_two_factor_disable',
                'userconfig_two_factor_radius_new',
                'userconfig_two_factor_radius_edit',
                'userconfig_two_factor_radius_delete',
                'userconfig_two_factor_status',
                'userconfig_two_factor_radius_clear',
                'userconfig_two_factor_privilege_add',
                'userconfig_two_factor_privilege_delete',
                'userconfig_external_setup_saml',
                'userconfig_external_devopssetup',
                'userconfig_external_devopsgroups_new',
                'userconfig_external_devopsgroups_edit',
                'userconfig_external_devopsgroups_delete',
                'userconfig_external_devopsgroups_clear',
                'userconfig_external_devopsgroups_print',]

    def userconfig_new(self, *args):
        """This option helps in Creating a new user account.

        *Parameters*
        - `user_name` : The name of the external user.
        - `full_name` : The full name for the user.
	- `system_generate_password` : Whether you want system to generate a
           password. 'yes' or 'no'. Default is 'no'
        - `password` : The password for the user.
        - `confirm_password` : Confirm the password again.
        - ` group` : The role for the user. The various values are
            | Key | Value |
            | 1 | Administrators |
            | 2 | Operators |
            | 3 | Read-Only Operators |
            | 4 | Guests |
            | 5 | Technicians |
            | 6 | Help Desk Users |

         *Return:*
           Returns the system generated password if a true value is
           passed for system_generate_password param, else returns None.

         *Example*
         | UserConfig New | user_name=operator1 | full_name=abc |
         | ... | password=12345678 |
         | ... | confirm_password=12345678 | group=1 |

         | UserConfig New | user_name=operator1 | full_name=abc |
         | ... | system_generate_pass=yes |
         """

        kwargs = self._convert_to_dict(args)
        return self._cli.userconfig().new(**kwargs)

    def userconfig_batch_add(self, *args):
        """ This option is used to add user through batch command

        *Parameters*
        - `user_name` : The name of the external user.
        - `full_name` : The full name for the user.
        - `password` : The password for the user.
        - ` group` : The role for the user. The various values are
            | Key | Value |
            | 1 | Administrators |
            | 2 | Operators |
            | 3 | Read-Only Operators |
            | 4 | Guests |
            | 5 | Technicians |
            | 6 | Help Desk Users |

         *Return:*
           Adds user through the bactch command

         *Examples*
         | UserConfig Add user_name=operator1 | full_name=abc |
         | ... | password=Test@1256 | group=1 |
        """

        kwargs = self._convert_to_dict(args)
        return self._cli.userconfig().batch_add(**kwargs)

    def userconfig_edit(self, *args):
        """ This option is used to modify a user account.

        *Parameters*
        - `user_name` : The name of the external user.
        - `full_name` : The full name for the user.
        - `system_generate_password` : Whether you want system to generate a
           password. 'yes' or 'no'. Default is 'no'
        - `password` : The password for the user.
        - `confirm_password` : Confirm the password again.
        - ` group` : The role for the user. The various values are
            | Key | Value |
            | 1 | Administrators |
            | 2 | Operators |
            | 3 | Read-Only Operators |
            | 4 | Guests |
            | 5 | Technicians |
            | 6 | Help Desk Users |

         *Return:*
           Returns the system generated password if a true value is
           passed for system_generate_password param, else returns None.

         *Examples*
         | UserConfig Edit | user_name=operator1 | full_name=abc |
         | ... | password=abcdefgh |
         | ... | confirm_password=abcdefgh | group=1 |

         | UserConfig Edit | user_name=operator1 | full_name=abc |
         | ... | system_generate_pass=yes |
         """
        kwargs = self._convert_to_dict(args)
        return self._cli.userconfig().edit(**kwargs)

    def userconfig_delete(self, *args):
        """This option is used to delete the selected user.

        *Parameters*
        - `user_name` : Name of the user to be deleted.
        - `confirm` : Takes values of YES or NO.

        *Examples*
        | UserConfig Delete | user_name=operator1 | confirm=YES |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.userconfig().delete(**kwargs)

    def userconfig_password(self, *args):
        """This option is used to change the password for a user.

        *Parameters*
        - `operation` : Choosing the operation to perform.
                        The options are assign and force.
                        The default option is assign.
        - `user_name` : The name of the user to be changed.
        - `system_generate_password` : Whether you want system to generate a
	   password. 'yes' or 'no'. Default is 'no'
        - `new_password` : The new password to be changed.
        - `confirm_new_password` : The new password entered again to confirm.

        *Return:*
          Returns the system generated password if a true value is
          passed for system_generate_password param, else returns None.

        *Examples*
        | UserConfig Password | operation=assign | user_name=operator1 |
        | ... | new_password=13456789 | confirm_new_password=13456789 |

        | UserConfig Password | operation=assign | user_name=operator1 |
        | ... | system_generate_pass=yes |
        """
        kwargs = self._convert_to_dict(args)
        return self._cli.userconfig().password(**kwargs)

    def userconfig_password_force_instant(self, user_name=None):
        """This option is used to force the password change for a user.

        userconfig -> password -> force -> instant

        *Parameters*
        - `user_name` : The name of the user to be changed.

        *Examples*
        | UserConfig Password Force Instant | user_name=operator1 |

        """
        self._cli.userconfig().password_force().instant(user_name=user_name)

    def userconfig_password_force_later(self, *args):
        """This option is used to force the password change for a user.

        userconfig -> password -> force -> later

        *Parameters*
        - `user_name` : The name of the user to be changed.
        - `password_exp_time` : password expiration period in days.
        - `enable_grace_period` : Whether to use grace period
        - `password_grace_period` : period after user's password change time during
           which the user will be forced to change her/his password (in days)
           If global grace period is set, then this will be set to global period.

        *Examples*
        | UserConfig Password Force | user_name=operator1 |
        | ... | password_exp_time=3 | enable_grace_period=yes |

        """
        kwargs = self._convert_to_dict(args)
        self._cli.userconfig().password_force().later(**kwargs)

    def userconfig_status(self, *args):
        """Run userconfig -> status command. Using this keyword you're able to
        read current status or lock/unlock user.

        *Parameters:*
        - `user_name`: the user name to work with.
        - `switch`: optional, boolean. Indicates whether to lock/unlock user.

        *Return:*
        string containing user status after command finished. Can be one of:
        'available', 'locked', 'pending' (without quotes).

        *Examples:*
        | ${status} | Userconfig Status | user_name=user1 |
        | ${status} | Userconfig Status | user_name=user1 | switch=${True} |
        """
        kwargs = self._convert_to_dict(args)
        return self._cli.userconfig().status(**kwargs)

    def userconfig_external_radius_new(self, host, password, port=DEFAULT,
        cache_time=DEFAULT, auth_type=DEFAULT, timeout=DEFAULT):
        """This option is used to configure an external authentication server.

        *Parameters*
        - `cache_time` : the timeout in seconds for how long the external
        authentication credentials will be cached. Values - Positive integer.
        - `host` : host name or IP address of the RADIUS server.
        - `port`: Port number of the RADIUS server.
        - `password`: Shared Password of the Server.
        - `auth_type`: the authentication type. 1 - CHAP
        2 - PAP
        - `timeout` : timeout in seconds for receiving a valid reply from
        the server

        *Examples*
        | UserConfig External Radius New | 1.1.1.1 | ironport | port=1812 |
        | ... | cache_time=10 |
        | ... | timeout=10 | auth_type=2 |

        """
        kwargs_setup = {
            'use_ext_auth': 'y',
            'cache_time': cache_time,
            'mechanism': 'radius',
        }
        kwargs = {
            'host': host,
            'port': port,
            'password': password,
            'pass_again': password,
            'timeout': timeout,
            'auth_type': auth_type,
        }
        self._cli.userconfig().external().setup(**kwargs_setup).new(**kwargs)

    def userconfig_external_radius_edit(self, host, host_name=DEFAULT,
         password=DEFAULT, port=DEFAULT, cache_time=DEFAULT, auth_type=DEFAULT
         , timeout=DEFAULT):
        """This option is used to edit a RADIUS server.

        *Parameters*
        - `cache_time` : the timeout in seconds for how long the external
        authentication credentials will be cached. Values - Positive integer.
        - `host` : Choose the host to edit.
        - `host_name` : host name or IP address of the RADIUS server.
           Old value is present by default.
        - `port`: Port number of the RADIUS server.
        - `password`: Shared Password of the Server.
        - `auth_type`: the authentication type. 1 - CHAP
        2 - PAP
        - `timeout` : timeout in seconds for receiving a valid reply from
        the server

        *Examples*
        | UserConfig External Radius Edit | 1.1.1.1 | host_name=1.2.2.2 |
        | ... | password=ironport | timeout=15 | cache_time=30 | auth_type=1 |

        """
        kwargs_setup = {
            'use_ext_auth': 'y',
            'cache_time': cache_time,
            'mechanism': 'radius',
        }
        kwargs = {
            'host': host,
            'host_name': host_name,
            'port': port,
            'password': password,
            'pass_again': password,
            'timeout': timeout,
            'auth_type': auth_type,
        }

        self._cli.userconfig().external().setup(**kwargs_setup).edit(**kwargs)

    def userconfig_external_radius_move(self, host_to_move=DEFAULT,
         position=DEFAULT, cache_time=DEFAULT):

        """Moves external auth server to a different postion.
        Note that this option is only available when there are 2 or more auth
        servers already configured.

            userconfig -> external -> setup -> move.

        Parameters:
        - `cache_time` : the timeout in seconds for how long the external
        authentication credentials will be cached. Values - Positive integer.
        - `host_to_move `: hostname or IP address of server to move.
                            Required parameters.
        - `position`: target position to move to. Current position is
                            indicated by default.

        *Examples*
        | UserConfig External Radius Move | host_to_move=1.2.2.2 | position=2 |
        """
        kwargs_setup = {
            'use_ext_auth': 'y',
            'cache_time': cache_time,
            'mechanism': 'radius',
        }
        kwargs = {
            'host_to_move': host_to_move,
            'position': position,
        }

        self._cli.userconfig().external().setup(**kwargs_setup).move(**kwargs)

    def userconfig_external_radius_delete(self, host=DEFAULT,
    cache_time=DEFAULT):
        """This option is used to delete a RADIUS server.

        *Parameters*
        - `cache_time` : the timeout in seconds for how long the external
        authentication credentials will be cached. Values - Positive integer.
        - `mechanism`: LDAP or Radius.
        - `host`: Choose the host to delete.

        *Examples*
        | UserConfig External Radius Delete | host=1.1.1.2 |
        """
        kwargs_setup = {
            'use_ext_auth': 'y',
            'cache_time': cache_time,
            'mechanism': 'radius',
        }
        kwargs = {
            'host': host,
        }

        self._cli.userconfig().external().setup(**kwargs_setup).delete(**kwargs)


    def userconfig_external_radius_clear(self, confirm_delete=DEFAULT,
    cache_time=DEFAULT):
        """This option is used to clear all the RADIUS Servers.

        *Parameters*
        - `cache_time` : the timeout in seconds for how long the external
        authentication credentials will be cached. Values - Positive integer.
        - `confirm_delete`: confirm whether to clear all existing external
           auth server  configuration.
            Either 'Yes' or 'No'. 'No' is present by default.

        *Examples*
        | UserConfig External Radius Clear | confirm_delete=y |

        """
        kwargs_setup = {
            'use_ext_auth': 'y',
            'cache_time': cache_time,
            'mechanism': 'radius',
        }
        kwargs = {
            'confirm_delete':confirm_delete,
        }
        self._cli.userconfig().external().setup(**kwargs_setup).clear(**kwargs)


    def userconfig_role_new(self, *args):
        """ This option is used to create new user roles.

        The various parameters are:
        - `name` : The name of the user role.
        - `short_name` : a short description for user role.
        - `mailpolicies` : Used to Select type of access to mailpolicies and
           content filters
           The various options and the corresponding options are:
           | Value | Option |
           | 1 |  No access |
           | 2 | View assigned, edit assigned |
           | 3 | View all, edit assigned |
           | 4 | View all, edit all (full access) |
        - `dlp` : Used to select type of access to DLP policies
           | Value | Option |
           | 1 |  No access |
           | 2 | View assigned, edit assigned |
           | 3 | View all, edit assigned |
           | 4 | View all, edit all (full access) |
        - `tracking` : Used to select type of access to Tracking.
           The various options and the corresponding options are:
           | Value | Option |
           | 1 |  No access |
           | 2 | Message Tracking access |
        - `reports` : Used to select the type of access to Reporting.
           The various options and the corresponding options are:
           | Value | Option |
           | 1 |  No access |
           | 2 | View relevant reports |
           | 3 | View all reports |
        - `trace` : Used to select the type of access to trace.
           The various options and the corresponding options are:
           | Value | Option |
           | 1 |  No access |
           | 2 | Trace Access |
        - `quarantines`: Used to select the type of access tp quarantines.
           The various options and the corresponding options are:
           | Value | Option |
           | 1 |  No access |
           | 2 | Allow Assignment |

        *Examples*
        | USerConfig Role New | name=admin1 | short_name=administrator1 |
        | ... | mailpolicies=4 |
        | ... | dlp=4 | tracking=2 | reports=2 | trace=2 | quarantines=2 |

        """

        kwargs = self._convert_to_dict(args)
        self._cli.userconfig().role().new(**kwargs)


    def userconfig_role_edit(self, *args):
        """ This option is used to edit user roles.
        - `role_name` : the role name or number to edit.
        - `new_name` : a new name for the user role.
        - `short_name` : a short description for user role.
        - `mailpolicies` : Used to Select type of access to mailpolicies and
           content filters
           The various options and the corresponding options are:
           | Value | Option |
           | 1 |  No access |
           | 2 | View assigned, edit assigned |
           | 3 | View all, edit assigned |
           | 4 | View all, edit all (full access) |
        - `dlp` : Used to select type of access to DLP policies
           | Value | Option |
           | 1 |  No access |
           | 2 | View assigned, edit assigned |
           | 3 | View all, edit assigned |
           | 4 | View all, edit all (full access) |
        - `tracking` : Used to select type of access to Tracking.
           The various options and the corresponding options are:
           | Value | Option |
           | 1 |  No access |
           | 2 | Message Tracking access |
        - `reports` : Used to select the type of access to Reporting.
           The various options and the corresponding options are:
           | Value | Option |
           | 1 |  No access |
           | 2 | View relevant reports |
           | 3 | View all reports |
        - `trace` : Used to select the type of access to trace.
           The various options and the corresponding options are:
           | Value | Option |
           | 1 |  No access |
           | 2 | Trace Access |
        - `quarantines`: Used to select the type of access tp quarantines.
           The various options and the corresponding options are:
           | Value | Option |
           | 1 |  No access |
           | 2 | Allow Assignment |

        *Examples*
        | UserConfig Role Edit | role_name=admin1 | new_name=new_admin |
        | ... | short_name=administrator1 | mailpolicies=3 | dlp=3 |
        | ... | tracking=1 | reports=2 |
        | ... | quarantines=1 |


        """
        kwargs = self._convert_to_dict(args)
        self._cli.userconfig().role().edit(**kwargs)


    def userconfig_role_delete(self, *args):
        """ This option is used to delete user roles.

        Parameters:
        - `role_name` : The role name or number to delete.

        Example:
        | UserConfig Role Delete | role_name=new_admin |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.userconfig().role().delete(**kwargs)

    def userconfig_policy_passwordstrength(self, *args):

        """Change password policy.

            userconfig -> policy -> passwordstrength.

        Parameters:
        - `min_length` :  minimum number of characters required in the password
           (6 characters is the lowest number possible).
           '6' or last specified number is present by default.
        - `req_alphabets`: requires at least one upper (A-Z) and one lower
           (a-z) case letter. Either 'Yes' or 'No'.
           'No' or last specified option is present by default.
        - `req_number` : requires at least one number (0-9) for passswords.
           Either 'Yes' or 'No'.
           'No' or last specified option is present by default.
        - `req_special_chars` : requires at least one special character. Either
           'Yes' or 'No'. No or last specified option is present.
        - `ban_username`: Reject passwords similar to the username.  Either
           'Yes' or 'No'. No or last specified option is present.
        - `sequential_characters` : Reject passphrases that contain three or more. 
           Either 'Yes' or 'No'.'No' or last specified option is present by default.
        - `ban_reuse` : Block reuse of last passwords. Either 'Yes' or 'No'.
           'No' or last specified option is present by default.
        - `times_ban_reuse` : number of the most recent passwords not allowed
           to re-use. The param is used only if 'Yes' was specified for previous
           Parameter. 3' or last specified number is present by default.
        - `words_to_disallow` : list of words to disallow. Default 'No'
        - `entropy_guests` : entropy value for Guests. Default 'No'
        - `entropy_admin` : entropy value for Administrators. Default 'No'
        - `entropy_cloudadmin` : entropy value for Cloud Administrators. Default 'No'
        - `entropy_readonly` : entropy value for Read-Only Operators. Default 'No'
        - `entropy_customroles` : entropy value for Custom Roles. Default 'No'
        - `entropy_technicians` : entropy value for Technicians. Default 'No'
        - `entropy_operators` : entropy value for Operators. Default 'No'
        - `entropy_helpdesk` : entropy value for Help Desk Users. Default 'No'

        *Example*
         | UserConfig Policy PasswordStrength | min_length=7 |
         | ... | req_alphabets=yes |
         | ... | req_number=yes | req_special_chars=yes | ban_username=no |
         | ... | sequential_characters=yes | ban_reuse=yes |
         | ... | times_ban_reuse=3 |

        """
        kwargs = self._convert_to_dict(args)
        self._cli.userconfig().policy().passwordstrength(**kwargs)

    def userconfig_policy_account(self, *args):

        """Change account policy.

            userconfig -> policy -> account.

       Parameters:
       - `lock_account` : automatically lock account after unsuccessful login
          attempts.  Either 'Yes' or 'No'. 'No' or last selected option is
          present by default.
       - `attempts` : How many consecutive unsuccessful login attempts
          will lock the account. '5' or last specified number is present by
          default.
       - `display_lock_mesg` :  display an account locked message to users if
          the Administrator manually locks their account. Either 'Yes' or 'No'.
          'No' or last specified option is present by default.
       - `change_locked_mesg` : change the account locked message. Either
          'Yes' or 'No'.
          'No' or last specified option is present by default.
       - `lock_message_medium` : The medium to change the lock message.
          The various values and parameters are
          | Value | Option |
          | 1 | Load the lock message from a file. |
          | 2 | Pasting via CLI. |
          | 3 | Use the default lock message. |
       - `mesg_file` : name of a file on the machine to load as lock message.
          The param is used only if 'Load' method was selected.
       - `mesg_cli` : lock message. The param is used only if 'Pasting' method
          was selected.
       - `enable_pass_expire` : enable password expiration. Either 'Yes' or 'No'
          'No' or last selected option is present by default.
       - `expire_time` :  password expiration period in days.
          The param is used only if
          'Yes' was specified for previous option 'pwd_exp'.
          '90' or last specified number is present by default.
       - `display_reminder` : display reminder about password expiration.
          The param is used only if 'Yes' was specified for option
          'pwd_exp'. Either 'Yes' or 'No'.
          'No' or last selected option is present by default.
       - `notification_time` : period before user's password change time during
          which a notification will be
          printed to the user that her/his password will expire.
          The param is used only if 'Yes' was specified for previous
          param 'rem_display'.'14' or last specified number is default.
       - `enable_password_grace` : whether to enable grace period. Default is 'YES'.
       - `password_grace_period` : period after user's password change time during which
          the user will be forced to change her/his password (in days). Applicable if
	  'enable_password_grace' is 'YES'.
       - `force_password` : require a password reset whenever a user's password
          is set or changed by an administrator.
          Either 'Yes' or 'No'. 'No' or last selected option is
          present by default.

       Example:
       | UserConfig Policy Account | lock_account=yes | attempts=15 |
       | ... | display_lock_mesg=yes | change_locked_mesg=yes |
       | ... | lock_message_medium=2 | mesg_cli=Custom |
       | ... | enable_pass_expire=yes | expire_time=150 |
       | ... | display_reminder=yes | notification_time=10 |
       | ... | enable_password_grace=yes | password_grace_period=3 |
       | ... | force_password=yes |

      """
        kwargs = self._convert_to_dict(args)
        self._cli.userconfig().policy().account(**kwargs)


    def userconfig_external_setup_disable(self):
        """Disables external authentication.

            userconfig -> external -> setup.

        Examples:
        | User Config External Setup Disable |
        """
        self._cli.userconfig().external().setup(use_ext_auth='n')


    def userconfig_external_setup_ldap(self, cache_time=DEFAULT,
         ext_auth_query=DEFAULT , timeout=DEFAULT,
          ext_group=DEFAULT, role=DEFAULT):

        """Add external LDAP authentication.

            userconfig -> external -> setup.

        Parameters:
        - `cache_time`: timeout in seconds for how long the external authentication
           credentials will be cached. (Enter '0' to disable expiration of authentication
           credentials altogether when using one time passwords.) '0' or last specified
           number is present by default.
        - `ext_auth_query`: Available LDAP external authentication query.
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

        Examples:
        | UserConfig External Setup Ldap |
        | ... | ext_auth_query=OpenLDAP.externalauth |
        | ... | timeout=30 |
        | ... | ext_group=test |
        | ... | role=Administrators |
        | UserConfig External Setup Ldap |
        | ... | ext_auth_query=SecondLDAP.externalauth |
        | ... | cache_time=10 |
        """
        cache_time = cache_time
        ldap_input_dict = {
            'ext_auth_query':ext_auth_query,
            'timeout':timeout,
            'ext_group':ext_group,
            'role':role,
        }
        self._cli.userconfig().external().setup(use_ext_auth='y', mechanism=
        'ldap', cache_time='5', ldap_input_dict=ldap_input_dict)


    def userconfig_external_groups_new(self, *args):
        """Adds new group mapping.

            userconfig -> external -> groups -> new.

        Parameters:
        - `group_name`: name of external group to map.
        - `role`: map type. First is selected by default.
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

        Examples:
       | UserConfig External Groups New | group_name=testname | role=Operators |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.userconfig().external().groups().new(**kwargs)


    def userconfig_external_groups_edit(self, *args):
        """Edits existing group mapping.

            userconfig -> external -> groups -> edit.

        Parameters:
        - `group_name`: name of existing group mapping to edit.
        - `role` : map type. See list of available types in keyword for
           group creation. Old selection is present by default.

        Example:
        | UserConfig External Groups Edit | group_name=testname | role=1 |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.userconfig().external().groups().edit(**kwargs)

    def userconfig_external_groups_delete(self, *args):
        """Deletes existing group mapping.

            userconfig -> external -> groups -> delete.

        Parameters:
        - `group_name`: name of existing group mapping to delete.

        Example:
        | UserConfig External Groups Delete | group_name=testname |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.userconfig().external().groups().delete(**kwargs)

    def userconfig_external_groups_print(self):
        """Displays all currently configured group mapping.

            userconfig -> external -> groups -> print.

        Examples:
        | ${out}= | UserConfig External Groups Print |
        | Log | ${out} |
        """
        return str(self._cli.userconfig().external().groups().print_groups())

    def userconfig_external_groups_clear(self):
        """ Clears all the mappings.

            userconfig -> external -> groups -> clear.
        Note : We can use this keyword for RADIUS only
        Examples:
        | UserConfig External Groups Clear |

        """
        self._cli.userconfig().external().groups().clear()

    def userconfig_dlptracking_add(self, *args):
        """Add the DLP tracking privilege for the
        particular default or custom role. This option may not exists
        if all roles are already added

        *Parameters:*
        - `role`: the name of the particular existing custom or predefined
        role to which the DLP tracking privilege is going to be
        assigned.

        *Examples:*
        | Userconfig DLPTracking Add | role=Operators |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.userconfig().dlptracking().add(**kwargs)

    def userconfig_dlptracking_delete(self, *args):
        """Delete the DLP tracking privilege for the
        particular default or custom role. This option may not exists
        if all roles are already deleted

        *Parameters:*
        - `role`: the name of the particular existing custom or predefined
        role from which the DLP tracking privilege is going to be
        deleted.

        *Examples:*
        | Userconfig DLPTracking Delete | role=Operators |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.userconfig().dlptracking().delete(**kwargs)

    def userconfig_urltracking_add(self, *args):
        """Add the URL tracking privilege for the
        particular default or custom role. This option may not exist
        if all roles are already added

        *Parameters:*
        - `role`: the name of the particular existing custom or predefined
        role to which the URL tracking privilege is going to be
        assigned.

        *Examples:*
        | Userconfig URLTracking Add | role=Operators |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.userconfig().urltracking().add(**kwargs)

    def userconfig_urltracking_delete(self, *args):
        """Delete the URL tracking privilege for the
        particular default or custom role. This option may not exist
        if all roles are already deleted

        *Parameters:*
        - `role`: the name of the particular existing custom or predefined
        role from which the URL tracking privilege is going to be
        deleted.

        *Examples:*
        | Userconfig URLTracking Delete | role=Operators |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.userconfig().urltracking().delete(**kwargs)

    def userconfig_two_factor_disable(self):
        """Disables twofactor authentication.

            userconfig -> twofactorauth -> setup.

        Examples:
        | User Config Two Factor Setup Disable |
        """
        self._cli.userconfig().twofactor().setup(use_2fa_auth='n')

    def userconfig_two_factor_radius_new(self, host, password, port=DEFAULT,
        auth_type=DEFAULT, timeout=DEFAULT):
        """This option is used to configure an external authentication server.

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

    def userconfig_two_factor_radius_edit(self, host, host_name=DEFAULT,
         password=DEFAULT, port=DEFAULT, auth_type=DEFAULT
         , timeout=DEFAULT):
        """This option is used to edit a RADIUS server.

        *Parameters*
        - `host` : Choose the host to edit.
        - `host_name` : host name or IP address of the RADIUS server.
           Old value is present by default.
        - `port`: Port number of the RADIUS server.
        - `password`: Shared Password of the Server.
        - `auth_type`: the authentication type.
        1 - CHAP
        2 - PAP
        - `timeout` : timeout in seconds for receiving a valid reply from
        the server

        *Examples*
        | UserConfig Two Factor Radius Edit | 1.1.1.1 | host_name=1.2.2.2 |
        | ... | password=ironport | timeout=15 | auth_type=1 |

        """
        kwargs_setup = {
            'use_2fa_auth': 'y',
        }
        kwargs = {
            'host': host,
            'host_name': host_name,
            'port': port,
            'password': password,
            'pass_again': password,
            'timeout': timeout,
            'auth_type': auth_type,
        }

        self._cli.userconfig().twofactor().setup(**kwargs_setup).edit(**kwargs)

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
            'confirm_delete':confirm_delete,
        }
        self._cli.userconfig().twofactor().setup(**kwargs_setup).clear(**kwargs)

    def userconfig_two_factor_status(self, *args):
        """Run userconfig -> twofactorauth command. Using this keyword you're able to
        read current status of 2 factor auth.

        *Parameters:*

        *Return:*
        string containing user status after command finished. Can be one of:
        'disabled' or 'radius' (without quotes).

        *Examples:*
        | ${status} | Userconfig Two Factor Status |
        """
        return self._cli.userconfig().two_factor_status()

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

    def userconfig_external_setup_saml(self, cache_time=DEFAULT, group_name=DEFAULT,
                                       role=DEFAULT, group_attribute=DEFAULT,):
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
        | ... | use_ext_auth=Yes                |
        | ... | cache_time=5                    |
        | ... | group_name=${SAML_GROUP1}       |
        | ... | role=${SAML_GROUP1_ROLE}        |
        | ... | group_attribute = ${GRP_ATTRIB} |
        """
        kwargs_setup = {
            'use_ext_auth': 'Y',
            'cache_time': cache_time,
            'mechanism': 'saml',
        }
        kwargs = {
            'group_name': group_name,
            'role': role,
            'group_attribute' : group_attribute
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
        NOTE : We can use this keyword for RADIUS only
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

