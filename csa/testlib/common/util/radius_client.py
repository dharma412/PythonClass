#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/common/util/radius_client.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $

import atexit

from common.util.connectioncache import ConnectionCache
from common.util.utilcommon import UtilCommon
from sal.clients.radius import FreeRadiusClient

from sal.clients.radius_def.users_parser.compiler import CompiledUser as AdvancedUser


class BasicUser(object):
    def __init__(self, name, password, group=''):
        self.name = name
        self.password = password
        self.group = group
        self._advanced_user_obj = self._to_advanced_user()

    def _to_advanced_user(self):
        verification_attributes = {}
        if self.password:
            verification_attributes['Cleartext-Password'] = (':=', self.password)
        else:
            verification_attributes['Auth-Type'] = (':=', 'Accept')
        response_attributes = {}
        if self.group:
            response_attributes['Class'] = ('=', self.group)
        return AdvancedUser(self.name, verification_attributes,
                            response_attributes)

    @classmethod
    def from_advanced_user(cls, advanced_user):
        name = advanced_user.name
        password = ''
        group = ''
        verification_attributes = advanced_user.verification_attributes
        response_attributes = advanced_user.response_attributes
        if verification_attributes.has_key('Cleartext-Password'):
            password = verification_attributes['Cleartext-Password'][1]
        if response_attributes.has_key('Class'):
            group = response_attributes['Class'][1]
        return BasicUser(name, password, group)

    def as_string(self):
        return self._advanced_user_obj.as_string()

    def as_advanced_user(self):
        return self._advanced_user_obj


class RadiusClient(UtilCommon):
    """Keywords for interacting with FreeRadius daemon.
    """
    CLIENTS_CACHE = ConnectionCache(no_current_msg='You should connect at least ' \
                                                   'one host running Radius daemon')

    def get_keyword_names(self):
        return ['radius_client_connect',
                'radius_client_disconnect',
                'radius_client_switch',

                'radius_client_get_shared_secret',
                'radius_client_get_all_users',
                'radius_client_is_user_exist',
                'radius_client_get_user',
                'radius_client_update_basic_user',
                'radius_client_update_advanced_user',
                'radius_client_edit_basic_user',
                'radius_client_edit_advanced_user',
                'radius_client_delete_user']

    def _get_client_obj(self):
        return self.CLIENTS_CACHE.current

    def radius_client_connect(self, host, *args):
        """Connect to Radius server. It is mandatory
        to call this keyword before any client operations.
        Otherwise you'll get ConfigError exception. It is
        recommended to call it in test/suite Setup section.
        In case you already have opened connection to particular
        host then it will be reopened with given parameters.

        *Parameters:*
        - `host`: existing FreeBSD host running Radius daemon
        - `default_secret_str`: string, that may be used as Radius shared key
        in case your host does not exist in Radius clients config. If this host
        is already present in clients.conf then you can get shared key via
        `Radius Client Get Shared Secret` keyword that should be called AFTER
        connect. 'ironport' by default
        - `should_preserve_server_config`: whether to preserve existing Radius
        on connect and restore it on disconnect. ${True} by default
        - `use_existing_config`: whether to update existing Radius config (clients
        and users), that already exists on server (${True}) or clear it completely
        before use (${False}). ${False} by default

        *Examples:*
        | Radius Client Connect | sma19.sma | default_secret_str=ironport1 |
        | ... | should_preserve_server_config=${True} |
        | ... | use_existing_config=${False} |
        """
        try:
            self.radius_client_switch(host)
        except ValueError:
            self.CLIENTS_CACHE.register(FreeRadiusClient(), host)
        dest_obj = self._get_client_obj()
        if dest_obj.is_connected():
            dest_obj.disconnect()
        kwargs = self._parse_args(args)
        dest_obj.connect(host, **kwargs)

    def radius_client_switch(self, host):
        """Switch current client connection.
        Connection to the host should be previously created by
        `Radius Client Connect` keyword.

        *Parameters:*
        - `host`: existing FreeBSD host running Radius daemon

        *Exceptions:*
        - `ValueError`: if there is no connection to host in cache

        *Examples:*
        | Radius Client Connect | sma19.sma |
        | Radius Client Connect | qa24.sma |
        | Radius Client Switch | sma19.sma |
        """
        self.CLIENTS_CACHE.switch(host)

    def radius_client_disconnect(self):
        """Terminate current connection to Radius server.
        It is recommended to call this keyword in suite/testcase
        Teardown section to be sure that all connections are properly
        closed (and configs are restored).

        *Exceptions:*
        - `ValueError`: if there is no opened connections
        - `ConfigError`: if current connection was closed

        *Examples:*
        | Radius Client Connect | sma19.sma |
        | Radius Client Connect | qa24.sma |
        | Radius Client Switch | sma19.sma |
        | Radius Client Disconnect |
        | Radius Client Switch | qa24.qa |
        | Radius Client Disconnect |
        """
        self._get_client_obj().disconnect()

    def radius_client_get_shared_secret(self):
        """Return Radius shared secret string for current connection. Read
        http://technet.microsoft.com/en-us/library/cc740124%28v=ws.10%29.aspx
        for more details.

        *Exceptions:*
        - `ValueError`: if there is no opened connections
        - `ConfigError`: if current connection was closed

        *Return:*
        String containing Radius shared secret string for current connection

        *Examples:*
        | ${shared_secret}= | Radius Client Get Shared Secret |
        """
        return self._get_client_obj().get_shared_secret()

    def radius_client_get_all_users(self, use_basic_model=True):
        """Return all users defined in current Radius config

        *Parameters:*
        - `use_basic_model`: whether to use simple presentation
        for resulting list items. Either ${True} or ${False}. ${True}
        by default

        *Return:*
        List of users defined in current Radius config. In case
        `use_basic_model` is set to ${True} each item will be BasicUser
        class instance having next properties:
        | `name` | user name |
        | `password` | user password, either Cleartext-Password
        attribute value in config file. Can be ${EMPTY} if no
        password is defined |
        | `group` | user group, either Class attribute value in
        config file. Can be ${EMPTY} if no group is defined |
        If `use_basic_model` is set to ${False} then each item will be
        AdvancedUser class instance having next properties:
        | `name` | user name |
        | `verification_attributes` | dictionary containing user verification
        attributes. Should contain at least one item. Keys are attribute names
        and values are 2-element tuples containing operator and value, for example:
        {'Cleartext-Password': (':=', 'ironport')}. See the FreeRadius man pages
        for more detailed information about possible attributes |
        | `response_attributes` | dictionary containing user response
        attributes. Can be empty. Keys are attribute names
        and values are 2-element tuples containing operator and value, for example:
        {'Group': ('=', 'Operators')}. See the FreeRadius man pages
        for more detailed information about possible attributes |

        *Exceptions:*
        - `ValueError`: if there is no opened connections
        - `ConfigError`: if current connection was closed

        *Examples:*
        | @{radius_users}= | Radius Client Get All Users |
        | :FOR | ${user} | IN | @{radius_users} |
        | \ | Log | ${user.name} |
        | \ | Log | ${user.password} |
        | \ | Log | ${user.group} |
        # Advanced users example
        | @{radius_users}= | Radius Client Get All Users | ${False} |
        | :FOR | ${user} | IN | @{radius_users} |
        | \ | Log | ${user.name} |
        | \ | Log Dictionary | ${user.verification_attributes} |
        | \ | Log Dictionary | ${user.response_attributes} |
        """
        all_users = self._get_client_obj().get_all_users()
        if use_basic_model:
            return map(lambda x: BasicUser.from_advanced_user(x), all_users)
        else:
            return all_users

    def radius_client_is_user_exist(self, name):
        """Return True if user with given name exists in
        current Radius config

        *Parameters:*
        - `name`: user name to be checked for existence

        *Exceptions:*
        - `ValueError`: if there is no opened connections
        - `ConfigError`: if current connection was closed

        *Return:*
        Either ${True} or ${False}

        *Examples:*
        | ${is_user_exist}= | Radius Client Is User Exist | vasya |
        """
        return self._get_client_obj().is_user_exist(name)

    def radius_client_get_user(self, name, use_basic_model=True):
        """Return properties for user named `name`

        *Parameters:*
        - `name`: user name whose properties are returned
        - `use_basic_model`: whether to return keyword result
        in simple (basic) or advanced form. Either ${True} (default)
        to use basic view or ${False} to use advanced one.

        *Exceptions:*
        - `ValueError`: if there is no opened connections or
        there is no user with given name
        - `ConfigError`: if current connection was closed

        *Return:*
        See returned item description for *Radius Client Get All Users*
        keyword

        *Examples:*
        | ${basic_user}= | Radius Client Get User | vasya |
        | Log | ${basic_user.name} |
        | Log | ${basic_user.password} |
        | Log | ${basic_user.group} |
        # Advanced users example
        | ${advanced_user}= | Radius Client Get User | vasya |
        | Log | ${advanced_user.name} |
        | Log Dictionary | ${advanced_user.verification_attributes} |
        | Log Dictionary | ${advanced_user.response_attributes} |
        """
        user = self._get_client_obj().get_user(name)
        if use_basic_model:
            return BasicUser.from_advanced_user(user)
        else:
            return user

    def radius_client_update_basic_user(self, name, password, group=''):
        """Update properties for basic Radius user. In user with given name
        already exists in Radius config then it will be updated with
        given parameter otherwise he will be added to current config

        *Parameters:*
        - `name`: user name to be updated. Mandatory
        - `password`: user password string. Mandatory
        - `group`: user group. Can be empty which means that this user
        does not belong to any group

        *Exceptions:*
        - `ValueError`: if there is no opened connections
        - `ConfigError`: if current connection was closed

        *Examples:*
        | Radius Client Update Basic User | vasya | 123456 | Guests |
        """
        user = BasicUser(name, password, group).as_advanced_user()
        self._get_client_obj().update_user(user.name,
                                           user.verification_attributes,
                                           user.response_attributes)

    def radius_client_update_advanced_user(self, name, verification_attributes,
                                           response_attributes={}):
        """Update properties for advanced Radius user. In user with given name
        already exists in Radius config then it will be updated with
        given parameter otherwise he will be added to current config

        *Parameters:*
        - `name`: user name to be updated. Mandatory
        - `verification_attributes`: user verification attributes dictionary.
        Mandatory. See corresponding parameter description in
        *Radius Client Get All Users* keyword documentation for more details
        - `response_attributes`: user response attributes dictionary. See
        corresponding parameter description in
        *Radius Client Get All Users* keyword documentation for more details

        *Exceptions:*
        - `ValueError`: if there is no opened connections
        - `ConfigError`: if current connection was closed

        *Examples:*
        | ${verification_attributes}= | Evaluate | {'Cleartext-Password': (':=', 'testing')} |
        | ${response_attributes}= | Catenate |
        | ... | {'Service-Type', ('=', 'Framed-User'), |
        | ... |  'Framed-Protocol', ('=', 'PPP')} |
        | ${response_attributes}= | Evaluate | '''${response_attributes}''' |
        | Radius Client Update Advanced User | vasya |
        | ... | ${verification_attributes} | ${response_attributes} |
        """
        self._get_client_obj().update_user(name,
                                           verification_attributes,
                                           response_attributes)

    def radius_client_edit_basic_user(self, name, password, group=''):
        """Edit properties for basic Radius user.

        *Parameters:*
        - `name`: user name to be updated. Mandatory
        - `password`: user password string. Mandatory
        - `group`: user group. Can be empty which means that this user
        does not belong to any group

        *Exceptions:*
        - `ValueError`: if there is no opened connections or
        there is no user with given name
        - `ConfigError`: if current connection was closed

        *Examples:*
        | Radius Client Edit Basic User | vasya | 123456 | Guests |
        """
        user = BasicUser(name, password, group).as_advanced_user()
        self._get_client_obj().edit_user(user.name,
                                         user.verification_attributes,
                                         user.response_attributes)

    def radius_client_edit_advanced_user(self, name, verification_attributes,
                                         response_attributes={}):
        """Edit properties for advanced Radius user.

        *Parameters:*
        - `name`: user name to be updated. Mandatory
        - `verification_attributes`: user verification attributes dictionary.
        Mandatory. See corresponding parameter description in
        *Radius Client Get All Users* keyword documentation for more details
        - `response_attributes`: user response attributes dictionary. See
        corresponding parameter description in
        *Radius Client Get All Users* keyword documentation for more details

        *Exceptions:*
        - `ValueError`: if there is no opened connections or there is no
        user with given name in current Radius config
        - `ConfigError`: if current connection was closed

        *Examples:*
        | ${verification_attributes}= | Evaluate | {'Cleartext-Password': (':=', 'testing')} |
        | ${response_attributes}= | Catenate |
        | ... | {'Service-Type', ('=', 'Framed-User'), |
        | ... |  'Framed-Protocol', ('=', 'PPP')} |
        | ${response_attributes}= | Evaluate | '''${response_attributes}''' |
        | Radius Client Edit Advanced User | vasya |
        | ... | ${verification_attributes} | ${response_attributes} |
        """
        self._get_client_obj().edit_user(name,
                                         verification_attributes,
                                         response_attributes)

    def radius_client_delete_user(self, name):
        """Remove existing Radius user.

        *Parameters:*
        - `name`: user name to be deleted. Mandatory

        *Exceptions:*
        - `ValueError`: if there is no opened connections or
        there is no user with given name
        - `ConfigError`: if current connection was closed

        *Examples:*
        | Radius Client Delete User | vasya |
        """
        self._get_client_obj().delete_user(name)


def close_pending_connections():
    all_connections = RadiusClient.CLIENTS_CACHE.get_all_current()
    connections_to_close = filter(lambda x: x.is_connected(), all_connections)
    map(lambda x: x.disconnect(), connections_to_close)


atexit.register(close_pending_connections)
