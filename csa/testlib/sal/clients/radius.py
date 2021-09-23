#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/sal/clients/radius.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $

import functools
import socket

from sal.exceptions import ConfigError
from sal.servers.radius import BaseRadiusServer, FreeRadiusServer

from radius_def.clients_parser.compiler import ClientsConfCompiler, \
    CompiledClient
from radius_def.clients_parser.tokenizer import ClientsConfTokenizer
from radius_def.users_parser.compiler import UsersCompiler, \
    CompiledUser
from radius_def.users_parser.tokenizer import UsersTokenizer


def verify_client_connection(func):
    @functools.wraps(func)
    def decorator(self, *args, **kwargs):
        if self._server_controller is None:
            raise ConfigError('Client should be connected to server ' \
                              'in order to call this method')

        return func(self, *args, **kwargs)

    return decorator


class BaseRadiusClient(object):
    SERVER_CACHE = {}

    def __init__(self):
        self._server_controller = None
        self._shared_secret = None

    @classmethod
    def _get_radius_server_class(cls):
        # This method should be overriden in subclasses
        return BaseRadiusServer

    @verify_client_connection
    def get_shared_secret(self):
        return self._shared_secret

    def _establish_shared_secret(self, default_secret_str, use_existing_config):
        raise NotImplementedError('Should be implemented in subclasses')

    def _clear_user_config(self):
        raise NotImplementedError('Should be implemented in subclasses')

    def is_connected(self):
        return self._shared_secret is not None

    def connect(self, dest_hostname, default_secret_str='ironport',
                should_preserve_server_config=True,
                use_existing_config=False):
        if self._server_controller is not None:
            self.disconnect()
        self.__should_preserve_server_config = should_preserve_server_config
        self.__preserved_radius_config_path = None
        self.__is_radius_in_running_state = True

        if not self.SERVER_CACHE.has_key(dest_hostname):
            self.SERVER_CACHE[dest_hostname] = \
                self._get_radius_server_class()(dest_hostname)
        self._server_controller = self.SERVER_CACHE[dest_hostname]
        if self.__should_preserve_server_config:
            self.__preserved_radius_config_path = \
                self._server_controller.preserve_settings()

        self._establish_shared_secret(default_secret_str, use_existing_config)
        if not use_existing_config:
            self._clear_user_config()
        if not self._server_controller.is_running():
            self.__is_radius_in_running_state = False
            self._server_controller.start()

    @verify_client_connection
    def disconnect(self):
        if self.__should_preserve_server_config:
            self._server_controller.restore_settings(self.__preserved_radius_config_path)
        if not self.__is_radius_in_running_state:
            self._server_controller.stop()
        self._shared_secret = None
        self._server_controller = None


class FreeRadiusClient(BaseRadiusClient):
    USERS_CONFIG_NAME = 'users'
    CLIENTS_CONFIG_NAME = 'clients.conf'

    def __init__(self):
        super(FreeRadiusClient, self).__init__()
        self._clients_compiler = ClientsConfCompiler(ClientsConfTokenizer)
        self._users_compiler = UsersCompiler(UsersTokenizer)

    @classmethod
    def _get_radius_server_class(cls):
        return FreeRadiusServer

    def _establish_shared_secret(self, default_secret_str, use_existing_config):
        """Currently this method adds the whole ironport network to
        the list of allowed clients.
        """
        clients_content = self._server_controller.get_config(self.CLIENTS_CONFIG_NAME)
        clients = self._clients_compiler.get_compiled_content(clients_content)
        ironport_net = CompiledClient('10.0.0.0/8', {'secret': default_secret_str,
                                                     'shortname': 'ironportnet'})
        new_content = ironport_net.as_string()
        if use_existing_config:
            clients_content += new_content
        else:
            clients_content = new_content
        self._shared_secret = default_secret_str
        self._server_controller.set_config(self.CLIENTS_CONFIG_NAME,
                                           clients_content)

    @verify_client_connection
    def _clear_user_config(self):
        self._server_controller.set_config(self.USERS_CONFIG_NAME,
                                           '# Empty config\n')

    @verify_client_connection
    def get_all_users(self):
        users_content = self._server_controller.get_config(self.USERS_CONFIG_NAME)
        return self._users_compiler.get_compiled_content(users_content)

    @verify_client_connection
    def is_user_exist(self, name):
        users_content = self._server_controller.get_config(self.USERS_CONFIG_NAME)
        all_users = self._users_compiler.get_compiled_content(users_content)
        return bool(filter(lambda x: x.name == name, all_users))

    @verify_client_connection
    def get_user(self, name):
        users_content = self._server_controller.get_config(self.USERS_CONFIG_NAME)
        all_users = self._users_compiler.get_compiled_content(users_content)
        dest_users = filter(lambda x: x.name == name, all_users)
        if dest_users:
            return dest_users[0]
        else:
            raise ValueError('User named %s does not exist in Radius config' % \
                             (name,))

    @verify_client_connection
    def update_user(self, name, verification_attributes, response_attributes={}):
        all_users = self.get_all_users()
        dest_users = filter(lambda x: x.name == name, all_users)
        if dest_users:
            dest_user = dest_users[0]
            dest_user.verification_attributes.update(verification_attributes)
            dest_user.response_attributes.update(response_attributes)
        else:
            dest_user = CompiledUser(name, verification_attributes, response_attributes)
            all_users.insert(0, dest_user)
        final_content = '\n'.join(map(lambda x: x.as_string(), all_users))
        self._server_controller.set_config(self.USERS_CONFIG_NAME, final_content)

    @verify_client_connection
    def edit_user(self, name, verification_attributes, response_attributes={}):
        users_content = self._server_controller.get_config(self.USERS_CONFIG_NAME)
        all_users = self._users_compiler.get_compiled_content(users_content)
        dest_users = filter(lambda x: x.name == name, all_users)
        if dest_users:
            dest_users[0].verification_attributes = verification_attributes
            dest_users[0].response_attributes = response_attributes
            final_content = '\n'.join(map(lambda x: x.as_string(), all_users))
            self._server_controller.set_config(self.USERS_CONFIG_NAME, final_content)
        else:
            raise ValueError('User named %s does not exist in Radius config' % \
                             (name,))

    @verify_client_connection
    def delete_user(self, name):
        users_content = self._server_controller.get_config(self.USERS_CONFIG_NAME)
        all_users = self._users_compiler.get_compiled_content(users_content)
        dest_users = filter(lambda x: x.name == name, all_users)
        if dest_users:
            for user in dest_users:
                all_users.remove(user)
            final_content = '\n'.join(map(lambda x: x.as_string(), all_users))
            self._server_controller.set_config(self.USERS_CONFIG_NAME, final_content)
        else:
            raise ValueError('User named %s does not exist in Radius config' % \
                             (name,))


if __name__ == '__main__':
    client = FreeRadiusClient()
    client.connect('localhost')
    try:
        print 'Shared secret value: %s ' % (client.get_shared_secret(),)

        users = client.get_all_users()
        for user in users:
            print '*******'
            print '%s\n%s\n%s' % (user.name, user.verification_attributes,
                                  user.response_attributes)
            print '*******'

        USER_NICK = 'dummy'
        client.update_user(USER_NICK, {'Group': ('==', 'disabled'),
                                       'Auth-Type': (':=', 'Reject')},
                           {'Reply-Message': ('=',
                                              'Your account has been disabled.')})
        print client.get_user(USER_NICK)
        client.edit_user(USER_NICK, {'Group': ('==', 'enabled')})
        client.delete_user(USER_NICK)
        assert (not client.is_user_exist(USER_NICK))
    finally:
        raw_input('Press ENTER to continue restore...')
        client.disconnect()

    print 'Press Ctrl+Z to exit...'
