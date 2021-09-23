#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/common/util/mail_delivery_client.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $

import atexit

from common.util.connectioncache import ConnectionCache
from common.util.utilcommon import UtilCommon

import sal.clients.mail_delivery as mail_delivery


class MailAccount(object):
    def __init__(self, name, password):
        self.name = name
        self.password = password


class MailDeliveryClient(UtilCommon):
    """Keywords for interacting with Dovecot2 mail delivery server. See
    http://wikicentral.cisco.com/display/GROUP/How+to+Configure+Dovecot+Mail+Delivery+Server+for+RF+Tests
    for more details about how to configure the server on FreeBSD machine
    """
    CLIENTS_CACHE = ConnectionCache(no_current_msg='You should connect at least ' \
                                                   'one host running Dovecot Mail Delivery server')

    def get_keyword_names(self):
        return ['mail_delivery_client_connect',
                'mail_delivery_client_disconnect',
                'mail_delivery_client_switch',

                'mail_delivery_client_add_account',
                'mail_delivery_client_update_account',
                'mail_delivery_client_is_account_exist',
                'mail_delivery_client_get_account',
                'mail_delivery_client_get_all_accounts',
                'mail_delivery_client_delete_account',
                'mail_delivery_client_clear_accounts']

    def _get_client_obj(self):
        return self.CLIENTS_CACHE.current

    def mail_delivery_client_connect(self, host, *args):
        """Connect to Dovecot Mail Delivery server. It is mandatory
        to call this keyword before any client operations.
        Otherwise you'll get ConfigError exception. It is
        recommended to call it in test/suite Setup section.

        *Parameters:*
        - `host`: existing FreeBSD host running Dovecot daemon
        - `accounts_db_path`: path to mail accounts database on
        remote host. "/usr/local/etc/mail.passwd" by default
        - `use_existing_accounts_db`: whether to use existing
        mail accounts database. If ${False} (default behavior)
        then all current email accounts will be cleaned on connect.

        *Examples:*
        | Mail Delivery Client Connect | qa32.qa |
        | ... | accounts_db_path=/etc/mail.passwd |
        | ... | use_existing_accounts_db=${True} |
        """
        try:
            self.mail_delivery_client_switch(host)
        except ValueError:
            self.CLIENTS_CACHE.register(mail_delivery.MailDeliveryClient(),
                                        host)
        dest_obj = self._get_client_obj()
        kwargs = self._parse_args(args)
        dest_obj.connect(host, **kwargs)

    def mail_delivery_client_switch(self, host):
        """Switch current client connection.
        Connection to the host should be previously created by
        `Mail Delivery Client Connect` keyword.

        *Parameters:*
        - `host`: existing FreeBSD host running Dovecot daemon

        *Exceptions:*
        - `ValueError`: if there is no connection to host in cache

        *Examples:*
        | Mail Delivery Client Connect | sma19.sma |
        | Mail Delivery Client Connect | qa24.sma |
        | Mail Delivery Client Switch | sma19.sma |
        """
        self.CLIENTS_CACHE.switch(host)

    def mail_delivery_client_disconnect(self):
        """Terminate current connection to Dovecot server.
        It is recommended to call this keyword in suite/testcase
        Teardown section to be sure that all connections are properly
        closed (and configs are restored).

        *Exceptions:*
        - `ValueError`: if there is no opened connections
        - `ConfigError`: if current connection was closed

        *Examples:*
        | Mail Delivery Client Connect | sma19.sma |
        | Mail Delivery Client Connect | qa24.sma |
        | Mail Delivery Client Switch | sma19.sma |
        | Mail Delivery Client Disconnect |
        | Mail Delivery Client Switch | qa24.qa |
        | Mail Delivery Client Disconnect |
        """
        self._get_client_obj().disconnect()

    def mail_delivery_client_add_account(self, name, password):
        """Add new mail delivery account. If account with same name
        already exists then this keyword will pass silently

        *Parameters:*
        - `name`: new account name
        - `password`: new account password

        *Exceptions:*
        - `ValueError`: if there is no opened connections
        - `ConfigError`: if current connection was closed

        *Examples:*
        | Mail Delivery Client Add Account | vasya | securepass |
        """
        self._get_client_obj().add_account(name, password)

    def mail_delivery_client_update_account(self, old_name,
                                            new_name=None, new_password=None):
        """Update properties for existing mail delivery account

        *Parameters:*
        - `old_name`: account name to be updated. Mandatory
        - `new_name`: new account name. Will be the same as old one if omitted
        - `new_password`: new account password. Will be the same as old one if
        omitted

        *Exceptions:*
        - `ValueError`: if there are no opened connections or there are no account
        with given `old_name`
        - `ConfigError`: if current connection was closed

        *Examples:*
        | Mail Delivery Client Update Account | vasya | new_password=123456 |
        """
        self._get_client_obj().update_account(old_name, new_name, new_password)

    def mail_delivery_client_get_account(self, name):
        """Return properties for account named `name`

        *Parameters:*
        - `name`: account name whose properties are returned

        *Exceptions:*
        - `ValueError`: if there is no opened connections or
        there is no account with given name
        - `ConfigError`: if current connection was closed

        *Return:*
        object with two properties: name and password

        *Examples:*
        | ${acc}= | Mail Delivery Client Get Account | vasya |
        | Log | ${acc.name} |
        | Log | ${acc.password} |
        """
        dest_account = filter(lambda x: x[0] == name,
                              self._get_client_obj().get_accounts())
        if dest_account:
            name, password = dest_account[0]
            return MailAccount(name, password)
        else:
            raise ValueError('There is no mail delivery account named %s' % \
                             (name,))

    def mail_delivery_client_get_all_accounts(self):
        """Return all accounts defined in current mail delivery server config

        *Return:*
        List of users defined in current mail delivery server config.
        Each item of this list is an object having the following
        properties:
        | `name` | account name |
        | `password` | account password |

        *Exceptions:*
        - `ValueError`: if there is no opened connections
        - `ConfigError`: if current connection was closed

        *Examples:*
        | @{accounts}= | Mail Delivery Client Get All Accounts |
        | :FOR | ${acc} | IN | @{accounts} |
        | \ | Log | ${acc.name} |
        | \ | Log | ${acc.password} |
        """
        result = []
        for name, password in self._get_client_obj().get_accounts():
            result.append(MailAccount(name, password))
        return result

    def mail_delivery_client_is_account_exist(self, name):
        """Return True if account with given name exists in
        current Dovecot config

        *Parameters:*
        - `name`: account name to be checked for existence

        *Exceptions:*
        - `ValueError`: if there is no opened connections
        - `ConfigError`: if current connection was closed

        *Return:*
        Either ${True} or ${False}

        *Examples:*
        | ${is_user_exist}= | Mail Delivery Client Is Account Exist | vasya |
        | Should Be True | ${is_user_exist} |
        """
        return self._get_client_obj().is_account_exist(name)

    def mail_delivery_client_delete_account(self, name):
        """Delete existing Dovecot account.

        *Parameters:*
        - `name`: account name to be deleted. Mandatory

        *Exceptions:*
        - `ValueError`: if there is no account with given name
        - `ConfigError`: if current connection was closed

        *Examples:*
        | Mail Delivery Client Delete Account | vasya |
        """
        self._get_client_obj().remove_account(name)

    def mail_delivery_client_clear_accounts(self):
        """Clear all existing Dovecot accounts.

        *Exceptions:*
        - `ValueError`: if there is no opened connections
        - `ConfigError`: if current connection was closed

        *Examples:*
        | Mail Delivery Client Clear Accounts |
        """
        self._get_client_obj().clear_accounts()


@atexit.register
def close_pending_connections():
    all_connections = MailDeliveryClient.CLIENTS_CACHE.get_all_current()
    connections_to_close = filter(lambda x: x.is_connected(), all_connections)
    map(lambda x: x.disconnect(), connections_to_close)
