#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/sal/clients/mail_delivery.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $

import os
import functools

from sal.exceptions import ConfigError
from sal.servers.mail_delivery import MailDeliveryServer

from mail_delivery_def.accounts_db import MailAccount, AccountsDB


def verify_client_connection(func):
    @functools.wraps(func)
    def decorator(self, *args, **kwargs):
        if not self.is_connected():
            raise ConfigError('Client should be connected to server ' \
                              'in order to call this keyword')
        return func(self, *args, **kwargs)

    return decorator


DEFAULT_ACCOUNTS_DB_PATH = '/usr/local/etc/mail.passwd'


class MailDeliveryClient(object):
    SERVER_CACHE = {}

    def __init__(self):
        self._server_controller = None
        self._accounts_db_path = None

    def is_connected(self):
        return self._server_controller is not None

    def connect(self, dest_hostname, accounts_db_path=DEFAULT_ACCOUNTS_DB_PATH,
                use_existing_accounts_db=False):
        if dest_hostname not in self.SERVER_CACHE:
            self.SERVER_CACHE[dest_hostname] = (MailDeliveryServer(dest_hostname),
                                                accounts_db_path)
        self._server_controller, self._accounts_db_path = \
            self.SERVER_CACHE[dest_hostname]
        if not self._server_controller.is_running():
            self._server_controller.start()
        if not use_existing_accounts_db:
            self.clear_accounts()

    @verify_client_connection
    def disconnect(self):
        self._server_controller = None
        self._accounts_db_path = None

    def _receive_accounts_db(self, local_path=None):
        config_path = self._server_controller.get_config(self._accounts_db_path,
                                                         local_path)
        with open(config_path, 'r') as config_file:
            accounts_db = AccountsDB(config_file.read())
        return (accounts_db, config_path)

    def _store_accounts_db(self, new_db, local_path):
        with open(local_path, 'w') as config_file:
            config_file.write(new_db.as_string())
        self._server_controller.set_config(local_path, self._accounts_db_path)

    @verify_client_connection
    def add_account(self, name, password):
        accounts_db, local_path = self._receive_accounts_db()
        accounts_db.add_account(MailAccount(name, password))
        self._store_accounts_db(accounts_db, local_path)

    @verify_client_connection
    def is_account_exist(self, name):
        accounts_db, local_path = self._receive_accounts_db()
        is_acc_exist = accounts_db.is_account_exist(name)
        os.unlink(local_path)
        return is_acc_exist

    @verify_client_connection
    def remove_account(self, name):
        accounts_db, local_path = self._receive_accounts_db()
        accounts_db.remove_account(name)
        self._store_accounts_db(accounts_db, local_path)

    @verify_client_connection
    def clear_accounts(self):
        accounts_db, local_path = self._receive_accounts_db()
        map(lambda x: accounts_db.remove_account(x[0]), list(accounts_db))
        self._store_accounts_db(accounts_db, local_path)

    @verify_client_connection
    def get_accounts(self):
        accounts_db, local_path = self._receive_accounts_db()
        result = list(accounts_db)
        os.unlink(local_path)
        return result

    @verify_client_connection
    def update_account(self, old_name, new_name=None, new_password=None):
        accounts_db, local_path = self._receive_accounts_db()
        existing_account = filter(lambda x: x[0] == old_name, accounts_db)
        if not existing_account:
            raise ValueError('There is no account named %s in accounts database' % \
                             (old_name,))
        else:
            existing_account = existing_account[0]
        if new_name is None:
            new_name = existing_account.name
        if new_password is None:
            new_password = existing_account.password
        accounts_db.edit_account(old_name,
                                 MailAccount(new_name, new_password))
        self._store_accounts_db(accounts_db, local_path)


if __name__ == '__main__':
    HOSTNAME = 'qa32.qa'

    mdc = MailDeliveryClient()
    mdc.connect(HOSTNAME)
    try:
        mdc.add_account('Vasya', 'vas1')
        mdc.add_account('Vasya2', 'vas2')
        assert (mdc.is_account_exist('Vasya'))
        assert (not mdc.is_account_exist('Vasya3'))
        mdc.remove_account('Vasya')
        print mdc.get_accounts()
        mdc.clear_accounts()
        assert (len(mdc.get_accounts()) == 0)
    finally:
        mdc.disconnect()
