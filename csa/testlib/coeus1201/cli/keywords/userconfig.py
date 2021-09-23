#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/cli/keywords/userconfig.py#1 $
# $DateTime: 2019/08/14 09:58:47 $
# $Author: uvelayut $

from common.cli.clicommon import CliKeywordBase, DEFAULT

class UserConfig(CliKeywordBase):
    """Configure local users that are allowed to use the system.
    """

    def get_keyword_names(self):
        return [
                'user_config_new',
                'user_config_edit',
                'user_config_password',
                'user_config_delete',
                'user_config_policy_passwd_strength',
                'user_config_policy_account_expiration',
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
                'user_config_external_setup_ldap',
               ]

    def user_config_new(self, user_name, full_name, password, group=DEFAULT):
        """Adds new user.

           userconfig -> new

        Parameters:
           - `user_name`: username for new user.
           - `full_name`: full name of new user.
           - `password`: password for new user.
           - `group`: group new user belong to.  Either 'Administrators'
                      'Operators', 'Read-Only', or 'Guests'.  Defaulted to
                      'Administrators'.

        Examples:
        | User Config New | foo | Foo Foo | foofoo | group=Operators |
        | User Config New | bar | Bar Bar | barbar | group=Guests |
        """
        self._cli.userconfig().new(user_name=user_name, full_name=full_name,
                                   password=password, group=group.title())

    def user_config_edit(self, user_name, full_name=DEFAULT,
                         password=DEFAULT, group=DEFAULT):
        """Edits existing user.

           userconfig -> edit

        Parameters:
           - `user_name`: username of existing user to be edited.
           - `full_name`: new full name for existing user.  Defaulted to old
                          full name if not specified.
           - `password`: new password for existing user.  Defaulted to old
                         password if not specified.
           - `group`: new group for existing user.  Either 'Administrators'
                      'Operators', 'Read-Only', or 'Guests'.  Defaulted to old
                      group if not specified.

        Examples:
        | User Config Edit | foo | Bar Bar | barbar | group=Read-Only |
        | User Config Edit | bar | Foo Foo | foofoo | group=Administrators |
        """
        self._cli.userconfig().edit(user_name=user_name, full_name=full_name,
                                    password=password, group=group.title())

    def user_config_delete(self, user_name, confirm=DEFAULT):
        """Deletes existing user.

           userconfig -> delete

        Parameters:
           - `user_name`: username of existing user to be deleted.
           - `confirm`: confirmation of delete existing user.  Either 'Yes' or
                        'No'.

        Example:
        | User Config Delete | foo |
        """
        self._cli.userconfig().delete(user_name=user_name, confirm=confirm)


    def user_config_policy_passwd_strength(self, *args):
        """Edits password of existing user.

           userconfig -> policy -> passwordstrength

        Parameters:
           - min_num: Password Length
           - require_one_upper_lower_letter: Answers yes or no if required one
             upper case letter and a lower letter
           - require_number: Answers yes or no if required numeric character in
             password
           - require_special_character: Answers yes or no if required special
             character in password
           - reject_password_as_username: Answers yes or no if you want to reject
             password same as username
           - ban_last_password: Answers yes or no if want to ban reusing last password
           - no_last_passwords: enter number of password you dont want to reuse
           - word_disallow: Answers yes or no for words not use is password
           - administrator_entropy: Answers yes or no if administrator entropy
             is required
           - operators_entropy: Answers yes or no if operators entropy is required
           - guests_entropy: Answers yes or no if guest entropy is required
           - read_only_operator_entropy: Answers yes or no if read only operators
             entropy is required

        Example:
        | User Config Policy Passwd Strength | min_num=8 | require_one_upper_lower_letter=Y|
        |...    require_number=Y | require_special_character=Y|
        |...    reject_password_as_username=Y | ban_last_password=Y|
        |...    no_last_passwords=3 | word_disallow=N|
        |...    administrator_entropy=N | operators_entropy=N|
        |...    guests_entropy=N | read_only_operator_entropy=N|
        """
        kwargs = self._convert_to_dict(args)
        self._cli.userconfig().policy_passwdStrength(**kwargs)

    def user_config_policy_account_expiration(self, *args):
        """Configures user account expiration

           userconfig -> policy -> account -> enable passphrase expiration?

        Parameters:
           - enable_passphrase_expiration: Answers yes or no for passphrase expiration
           - passpharse_expiration_duration: Sets the duration for passphrase expiration
           - passphrase_expiration_reminder: Anwsers yes or for passpharse expiration reminder
           - passphrase_expiration_reminder_duration: Sets duration for passphrase expiration reminder
           - passpharse_expiration_grace_period: Answers yes or no for passphrase expiration grace period
           - passphrase_expiration_grace_period_duration: Sets duration for passphrase expiration grace period

        Example:
        | User Config Policy Account Expiration
        |...  enable_passphrase_expiration=Y| passpharse_expiration_duration=1
        |...  passphrase_expiration_reminder=Y | passphrase_expiration_reminder_duration=3
        |...  passpharse_expiration_grace_period=Y | passphrase_expiration_grace_period_duration=2
        """
        kwargs = self._convert_to_dict(args)
        self._cli.userconfig().policy_account_expiration(**kwargs)

    def user_config_password(self,
        user_name=None,
        new_password=None,
        action=None,
        when=None,
        ):
        """Edits password of existing user.

           userconfig -> password

        Parameters:
           - `user_name`: username of existing user to be edited.
           - `new_password`: new password to replace existing one.
           - `action`: 'assign' or 'force'
            ASSIGN - Manually assign a new account password.
            FORCE - Force a user to change the account password.
           - `when`: `instant' or 'later`:
            INSTANT - Force changing password on next login
            LATER - Force changing password after a certain period.

        Example:
        | User Config Password | foo | newpasswd | assign |
        | User Config Password | action=force | when=later |
        """
        self._cli.userconfig().password(
            user_name=user_name,
            new_password=new_password,
            action=action,
            when=when,
        )

    def user_config_external_setup_new(self,
        server,
        password,
        group_name,
        port=DEFAULT,
        reply_timeout=DEFAULT,
        auth_type=DEFAULT,
        delete_mapping=DEFAULT,
        create_mapping=DEFAULT,
        mapping_type=DEFAULT,
        cert_name=DEFAULT,
        ocsp_validate=DEFAULT,
        auth_mode=DEFAULT,
        auth_protocol=DEFAULT,
        ):
        """Adds new external auth server configuration.

           userconfig -> external -> setup -> new.

        Parameters:
        -  `server`: hostname or IP address of new server.
        -  `port`: port number of new server.
        -  `password`: shared password.
        -  `reply_timeout`: timeout in seconds for receiving a valid reply
                              from the server
        -  `auth_type`: authentication type.  Either 'CHAP' or 'PAP'.
        -  `delete_mapping`: specify whether to delete group mapping.  This
            parameter is only valid when there is existing group mapping.
            Either 'Yes' or 'No'.
        -  `create_mapping`: specify whether to create group mapping.  This
            parameter is only valid when there is no group mapping.
            Either 'Yes' or 'No'.
        -  `group_name`: group name to map when `create_mapping` above is
            set to 'Yes'.
        -  `mapping_type`: map type when `create_mapping` above is set to 'Yes'.
            Either 'Administrators', 'Operators', 'Read_Only', or 'Guests'.

        Example:
        | User Config External Setup New | 1.1.1.1 | ironport | foo |
        | | reply_timeout=15 | create_mapping=Yes | auth_mech=RADIUS |
        """
        self._cli.userconfig().external().\
            setup(enable='y',auth_mode=auth_mode).new(
            hostname_or_ip=server,
            port=port,
            password=password,
            reply_timeout=reply_timeout,
            auth_type=auth_type,
            delete_mapping=delete_mapping,
            create_mapping=create_mapping,
            group_name=group_name,
            mapping_type=mapping_type.title(),
            cert_name=cert_name,
            ocsp_validate=ocsp_validate,
            auth_protocol=auth_protocol,
            )

    def user_config_external_setup_edit(self, server=DEFAULT,
                  hostname_or_ip=DEFAULT, port=DEFAULT, password=DEFAULT,
                  reply_timeout=DEFAULT, auth_type=DEFAULT,
                  delete_mapping=DEFAULT, create_mapping=DEFAULT,
                  group_name=DEFAULT, mapping_type=DEFAULT,cert_name=DEFAULT, ocsp_validate=DEFAULT,auth_protocol=DEFAULT):
        """Edits existing external server configuration.

           userconfig -> external -> setup -> edit.

        Parameters:
           - `server`: hostname or IP address of existing server to edit.
           - `hostname_or_ip`: new hostname or IP address for edited server.
           - `port`: new port number for edited server
           - `password`: new shared password.
           - `reply_timeout`: new timeout in seconds for receiving a valid reply
                              from the server
           - `auth_type`: new authentication type.  Either 'CHAP' or 'PAP'.
           - `delete_mapping`: specify whether to delete group mapping.  This
                               parameter is only valid when there is existing
                               group mapping.  Either 'Yes' or 'No'.
           - `create_mapping`: specify whether to create group mapping.  This
                               parameter is only valid when there is no group
                               mapping.  Either 'Yes' or 'No'.
           - `group_name`: group name to map when `create_mapping` above is
                           set to 'Yes'.
           - `mapping_type`: map type when `create_mapping` above is
                             set to 'Yes'.  Either 'Administrators',
                             'Operators', 'Read_Only', or 'Guests'.

        Example:
        | User Config External Setup Edit | server=1.1.1.1 | hostname_or_ip=2.2.2.2 |
        | | auth_type=CHAP |
        """
        self._cli.userconfig().external().setup(enable='y').edit(
            server=server, hostname_or_ip=hostname_or_ip, port=port,
            password=password, reply_timeout=reply_timeout, auth_type=auth_type,auth_protocol=auth_protocol,
            delete_mapping=delete_mapping, create_mapping=create_mapping,
            group_name=group_name, mapping_type=mapping_type.title())

    def user_config_external_setup_move(self, server=DEFAULT, position=DEFAULT,
        delete_mapping=DEFAULT, create_mapping=DEFAULT, group_name=DEFAULT,
        mapping_type=DEFAULT):
        """Moves external auth server to a different position.  Note that this
           option is only available when there are 2 or more auth servers
           already configured.

           userconfig -> external -> setup -> move.

        Parameters:
           - `server`: hostname or IP address of server to move.
           - `position`: target position to move to.
           - `delete_mapping`: specify whether to delete group mapping.  This
                               parameter is only valid when there is existing
                               group mapping.  Either 'Yes' or 'No'.
           - `create_mapping`: specify whether to create group mapping.  This
                               parameter is only valid when there is no group
                               mapping.  Either 'Yes' or 'No'.
           - `group_name`: group name to map when `create_mapping` above is
                           set to 'Yes'.
           - `mapping_type`: map type when `create_mapping` above is
                             set to 'Yes'.  Either 'Administrators',
                             'Operators', 'Read_Only', or 'Guests'.

        Examples:
        | User Config External Setup Move | server=1.1.1.1 | position=1 |
        """
        self._cli.userconfig().external().setup(enable='y').move(
            server_to_move=server, target_server=position,
            delete_mapping=delete_mapping, create_mapping=create_mapping,
            group_name=group_name, mapping_type=mapping_type.title())

    def user_config_external_setup_delete(self, server=DEFAULT,
        delete_mapping=DEFAULT, create_mapping=DEFAULT, group_name=DEFAULT,
        mapping_type=DEFAULT):
        """Deletes existing external auth server.

           userconfig -> external -> setup -> delete.

        Parameters:
           - `server`: hostname or IP address of server to delete.
           - `delete_mapping`: specify whether to delete group mapping.  This
                               parameter is only valid when there is existing
                               group mapping.  Either 'Yes' or 'No'.
           - `create_mapping`: specify whether to create group mapping.  This
                               parameter is only valid when there is no group
                               mapping.  Either 'Yes' or 'No'.
           - `group_name`: group name to map when `create_mapping` above is
                           set to 'Yes'.
           - `mapping_type`: map type when `create_mapping` above is
                             set to 'Yes'.  Either 'Administrators',

        Example:
        | User Config External Setup Delete | server=1.1.1.1 |
        """
        self._cli.userconfig().external().setup(enable='y').delete(
            server_to_delete=server, delete_mapping=delete_mapping,
            create_mapping=create_mapping, group_name=group_name,
            mapping_type=mapping_type.title())

    def user_config_external_setup_clear(self, confirm=DEFAULT):
        """Clears all existing external auth server.

           userconfig -> external -> setup -> clear.

        Parameters:
           - `confirm`: confirm whether to clear all existing external auth
                        server configuration.  Either 'Yes' or 'No'.

        Example:
        | User Config External Setup Clear |
        """
        self._cli.userconfig().external().setup(enable='y').clear(
                                                               confirm=confirm)

    def user_config_external_setup_disable(self):
        """Disables external authentication.

           userconfig -> external -> setup.

        Example:
        | User Config External Setup Disable |
        """
        self._cli.userconfig().external().setup(enable='n')

    def user_config_external_groups_new(self, group_name, mapping_type=DEFAULT):
        """Adds new group mapping.

           userconfig -> external -> groups -> new.

        Parameters:
           - `group_name`: name of external group to map.
           - `mapping_type`: map type.  Either 'Administrators', 'Operators',
                             'Read_Only', or 'Guests'.

        Example:
        | User Config External Groups New | bar | mapping_type=Operators |
        """
        self._cli.userconfig().external().groups().new(
            group_name=group_name, mapping_type=mapping_type.title())

    def user_config_external_groups_edit(self, group_name=DEFAULT,
                                         mapping_type=DEFAULT):
        """Edits existing group mapping.

           userconfig -> external -> groups -> edit.

        Parameters:
           - `group_name`: name of existing group mapping to edit.
           - `mapping_type`: map type.  Either 'Administrators', 'Operators',
                             'Read_Only', or 'Guests'.

        Example:
        | User Config External Groups Edit | group_name=foo | mapping_type=Guests |
        """
        self._cli.userconfig().external().groups().edit(
            group_name=group_name, mapping_type=mapping_type.title())

    def user_config_external_groups_delete(self, group_name=DEFAULT):
        """Deletes existing group mapping.

           userconfig -> external -> groups -> delete.

        Parameters:
           - `group_name`: name of existing group mapping to delete.

        Example:
        | User Config External Groups Delete | group_name=bar |
        """
        self._cli.userconfig().external().groups().delete(group_name=group_name)

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
        return self._cli.userconfig().external().groups().print_mappings()

    def user_config_external_setup_ldap(self,
        query_name=DEFAULT,
        auth_timeout=DEFAULT,
        group_name=DEFAULT,
        group=DEFAULT,
        ):
        """Adds new external auth server configuration.

           userconfig -> external -> setup -> new.

        Parameters:
        - `query_name`: LDAP external authentication query
        - `auth_timeout`: timeout in seconds for authentication request
        - `group_name`: external group name to map
        - `group`: Choose the group:
           . Administrators
           . Operators
           . Read-Only Operators
           . Guests

        Example:
        User Config External Setup LDAP
        ...    query_name=a
        ...    auth_timeout=2
        ...    group_name=foo
        ...    group=Guests
        """
        self._cli.userconfig().external().\
            setup(enable='y', mechanism='LDAP').ldap(
            query_name=query_name,
            auth_timeout=auth_timeout,
            group_name=group_name,
            group=group,
            )


