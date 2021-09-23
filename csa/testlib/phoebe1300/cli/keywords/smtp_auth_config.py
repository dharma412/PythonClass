#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1300/cli/keywords/smtp_auth_config.py#1 $ $DateTime: 2019/06/27 23:26:24 $ $Author: aminath $

from common.cli.clicommon import CliKeywordBase, DEFAULT


class SmtpAuthConfig(CliKeywordBase):
    """
    CLI command: smtpauthconfig
    """

    def get_keyword_names(self):
        return ['smtp_auth_config_new_forward',
                'smtp_auth_config_new_outgoing',
                'smtp_auth_config_new_ldap',
                'smtp_auth_config_edit_forward_new',
                'smtp_auth_config_edit_forward_edit',
                'smtp_auth_config_edit_forward_delete',
                'smtp_auth_config_edit_forward_print',
                'smtp_auth_config_edit_ldap',
                'smtp_auth_config_edit_outgoing',
                'smtp_auth_config_print',
                'smtp_auth_config_clear',
                'smtp_auth_config_delete', ]

    def smtp_auth_config_new_forward(self, *args):
        """Create a new SMTP Auth profile.
        Create an SMTP Auth forwarding server group profile.

        CLI command: smtpauthconfig > new > forward

        *Parameters:*
        - `name`: A name for the profile.
        - `hostname`: A hostname or an IP address for the forwarding server.
        - `port`: A port for the forwarding server.
        - `interface`: The interface to use for forwarding requests.
        - `tls`: Require TLS. YES or NO.
        - `max_conn`: The maximum number of simultaneous connections allowed.
        - `use_plain`: PLAIN mechanism when contacting forwarding server YES or NO.
        - `use_login`: Use LOGIN mechanism when contacting forwarding server. YES or NO.
        - `another_server`: Enter another forwarding server to this group. YES or NO.

        *Return:*
        None

        *Examples:*
        | Smtp Auth Config New Forward |
        | ... | name=forward |
        | ... | hostname=host.qa |
        | ... | port=333 |
        | ... | interface=auto |
        | ... | tls=yes |
        | ... | max_conn=1000 |
        | ... | use_plain=yes |
        | ... | another_server=no |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.smtpauthconfig().new().forward(**kwargs)

    def smtp_auth_config_new_outgoing(self, *args):
        """Create a new SMTP Auth profile.
        Create an outgoing SMTP Auth profile.

        CLI command: smtpauthconfig > new > outgoing

        *Parameters:*
        - `name`: A name for this profile.
        - `username`: The SMTP authentication username.
        - `password`: The SMTP authentication password.

        *Return:*
        None

        *Examples:*
        | Smtp Auth Config New Outgoing |
        | ... | name=out.qa |
        | ... | username=admin |
        | ... | password=ironport |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.smtpauthconfig().new().outgoing(**kwargs)

    def smtp_auth_config_new_ldap(self, *args):
        """Create a new SMTP Auth profile.
        Create an LDAP based profile.

        CLI command: smtpauthconfig > new > outgoing

        *Parameters:*
        - `name`: A name for this profile.
        - `query_name`: The LDAP query to use when authenticating SMTP.

        *Return:*
        None

        *Examples:*
        | Smtp Auth Config New LDAP |
        | ... | name=sully |
        | ... | query_name=sully.auth |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.smtpauthconfig().new().ldap(**kwargs)

    def smtp_auth_config_edit_forward_new(self, *args):
        """Edit Forward SMTP Auth profile.
        Add a server to this group.

        CLI command: smtpauthconfig > edit > SOME_FORWARD_PROFILE > new

        *Parameters:*
        - `name`: A name of the profile.
        - `hostname`: A hostname or an IP address for the forwarding server.
        - `port`: A port for the forwarding server.
        - `interface`: The interface to use for forwarding requests.
        - `tls`: Require TLS. YES or NO.
        - `max_conn`: The maximum number of simultaneous connections allowed.
        - `use_plain`: PLAIN mechanism when contacting forwarding server YES or NO.
        - `use_login`: Use LOGIN mechanism when contacting forwarding server. YES or NO.
        - `another_server`: Enter another forwarding server to this group. YES or NO.

        *Return:*
        None

        *Examples:*
        | Smtp Auth Config Edit Forward New |
        | ... | name=${forward} |
        | ... | new_name=${forward}_renamed |
        | ... | hostname=${h2} |
        | ... | interface=Management |
        | ... | tls=no |
        | ... | max_conn=88 |
        | ... | use_login=yes |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.smtpauthconfig(). \
            edit_forward(name=kwargs.pop('name', DEFAULT),
                         new_name=kwargs.pop('new_name', DEFAULT),
                         confirm_in_use_delete=kwargs.pop('confirm_in_use_delete', DEFAULT)). \
            new(**kwargs)

    def smtp_auth_config_edit_forward_edit(self, *args):
        """Edit Forward SMTP Auth profile.
        Modify a server in this group.

        CLI command: smtpauthconfig > edit > SOME_FORWARD_PROFILE > edit

        *Parameters:*
        - `name`: A name of the profile.
        - `server_name`: The server to edit.
        - `hostname`: A hostname or an IP address for the forwarding server.
        - `port`: A port for the forwarding server.
        - `interface`: The interface to use for forwarding requests.
        - `tls`: Require TLS. YES or NO.
        - `max_conn`: The maximum number of simultaneous connections allowed.
        - `use_plain`: PLAIN mechanism when contacting forwarding server YES or NO.
        - `use_login`: Use LOGIN mechanism when contacting forwarding server. YES or NO.
        - `another_server`: Enter another forwarding server to this group. YES or NO.

        *Return:*
        None

        *Examples:*
        | Smtp Auth Config Edit Forward Edit |
        | ... | name=forward |
        | ... | server_name=serv1 |
        | ... | hostname=serv2.qa |
        | ... | interface=auto |
        | ... | tls=yes |
        | ... | max_conn=200 |
        | ... | use_login=no |
        | ... | use_plain=yes |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.smtpauthconfig(). \
            edit_forward(name=kwargs.pop('name', DEFAULT),
                         new_name=kwargs.pop('new_name', DEFAULT),
                         confirm_in_use_delete=kwargs.pop('confirm_in_use_delete', DEFAULT)). \
            edit(**kwargs)

    def smtp_auth_config_edit_forward_delete(self, *args):
        """Edit Forward SMTP Auth profile.
        Remove a server from this group.

        CLI command: smtpauthconfig > edit > SOME_FORWARD_PROFILE > delete

        *Parameters:*
        - `name`: A name of the profile.
        - `server_name`: The name of the server in profile to delete.

        *Return:*
        None

        *Examples:*
        | Smtp Auth Config Edit Forward Delete |
        | ... | name=forward |
        | ... | server_name=serv2.qa |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.smtpauthconfig(). \
            edit_forward(name=kwargs.pop('name', DEFAULT),
                         new_name=kwargs.pop('new_name', DEFAULT),
                         confirm_in_use_delete=kwargs.pop('confirm_in_use_delete', DEFAULT)). \
            delete(**kwargs)

    def smtp_auth_config_edit_forward_print(self, *args):
        """Edit Forward SMTP Auth profile.
        List servers in this group.

        CLI command: smtpauthconfig > edit > SOME_FORWARD_PROFILE > print

        *Parameters:*
        - `name`: A name of the profile.

        *Return:*
        List.

        *Examples:*
        | ${hosts}= | Smtp Auth Config Edit Forward Print name=forward |
        | Log List | ${hosts} |
        """
        kwargs = self._convert_to_dict(args)
        return self._cli.smtpauthconfig().edit_forward(**kwargs).print_all()

    def smtp_auth_config_edit_ldap(self, *args):
        """Edit LDAP Auth profile.

        CLI command: smtpauthconfig > edit > SOME_LDAP_PROFILE

        *Parameters:*
        `name`: A name of the profile.
        `new_name`: The new name for this profile.
        `confirm_in_use_delete`: Confirm edit if this profile is in use by listener.
        `query_name`: The LDAP query to use when authenticating SMTP.

        *Return:*
        None

        *Examples:*
        | Smtp Auth Config Edit Ldap |
        | ... | name=${ldap} |
        | ... | new_name=ldap1 |
        | ... | query_name=ldap1.auth |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.smtpauthconfig().edit_ldap(**kwargs)

    def smtp_auth_config_edit_outgoing(self, *args):
        """Edit LDAP Auth profile.

        CLI command: smtpauthconfig > edit > SOME_OUTGOING_PROFILE

        *Parameters:*
        - `name`: A name of the profile.
        - `username`: The SMTP authentication username.
        - `password`: The SMTP authentication password.

        *Return:*
        None

        *Examples:*
        | Smtp Auth Config Edit Outgoing |
        | ... | name=${out} |
        | ... | username=anotheruser |
        | ... | password=anotherpassword |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.smtpauthconfig().edit_outgoing(**kwargs)

    def smtp_auth_config_delete(self, *args):
        """Remove SMTP Auth profile.

        CLI command: smtpauthconfig > delete

        *Parameters:*
        - `name`: A name of the profile to delete.

        *Return:*
        None

        *Examples:*
        | Smtp Auth Config Delete | name=${out} |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.smtpauthconfig().delete(**kwargs)

    def smtp_auth_config_clear(self, *args):
        """Clear all SMTP Auth profiles.

        CLI command: smtpauthconfig > clear

        *Parameters:*
        None

        *Return:*
        None

        *Examples:*
        | Smtp Auth Config Clear |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.smtpauthconfig().clear(**kwargs)

    def smtp_auth_config_print(self):
        """Clear all SMTP Auth profiles.

        CLI command: smtpauthconfig > print

        *Parameters:*
        None

        *Return:*
        List

        *Examples:*
        | ${profiles}= | Smtp Auth Config Print |
        | Log List | ${profiles} |
        | ${first}= | Get From List | ${profiles} | 0 |
        | Should Contain | ${first} | ${forward} |
        """
        return self._cli.smtpauthconfig().print_all()
