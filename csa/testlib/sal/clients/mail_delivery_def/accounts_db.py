#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/sal/clients/mail_delivery_def/accounts_db.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $

import re


class AccountParseError(Exception): pass


PASSWORD_SCHEME_PLAIN = 'PLAIN'


class MailAccount(object):
    """The class implements Python wrapper for one password database
    record
    """
    # http://wiki2.dovecot.org/Authentication/PasswordSchemes
    SUPPORTED_PASSWORD_SCHEMES = (PASSWORD_SCHEME_PLAIN,)

    def __init__(self, name, password, password_scheme=PASSWORD_SCHEME_PLAIN):
        self._name = name
        self._password = password
        self._password_scheme = password_scheme

    @property
    def name(self):
        return self._name

    @property
    def password(self):
        return self._password

    @property
    def password_scheme(self):
        return self._password_scheme

    @classmethod
    def create_from_string(cls, string):
        PATTERN = r'(?P<name>\w+):\{(?P<password_scheme>\w+)\}(?P<password>\S+)'
        match = re.search(PATTERN, string)
        if match:
            if match.group('password_scheme') not in MailAccount.SUPPORTED_PASSWORD_SCHEMES:
                raise AccountParseError('Failed to parse mail account from string ' \
                                        '"%s". Unsupported password scheme "%s". ' \
                                        'Only %s schemes are supported.' % \
                                        (string, match.group('password_scheme'),
                                         MailAccount.SUPPORTED_PASSWORD_SCHEMES))
            return cls(match.group('name'), match.group('password'),
                       match.group('password_scheme'))
        else:
            raise AccountParseError('Failed to parse mail account from string ' \
                                    '"%s"' % (string,))

    def as_string(self):
        return '%s:{%s}%s' % (self._name, self._password_scheme, self._password)


class DBParsingError(Exception): pass


class AccountsDB(object):
    """Simple wrapper for passwd-file format supported by
    Dovecot Mail Delivery server
    http://wiki2.dovecot.org/AuthDatabase/PasswdFile
    """

    def __init__(self, content):
        self._accounts = self._parse(content)

    def _parse(self, content):
        parsed_accounts = []
        for row_num, line in enumerate(content.splitlines()):
            if len(line.strip()) > 0:
                try:
                    parsed_accounts.append(MailAccount.create_from_string(line))
                except AccountParseError as e:
                    raise DBParsingError('Failed to parse mail accounts database.\n' \
                                         'Line %d; Error:\n' % (row_num + 1, unicode(e)))
        return parsed_accounts

    def as_string(self):
        return '\n'.join(map(lambda x: x.as_string(), self._accounts))

    def add_account(self, new_account):
        assert (isinstance(new_account, MailAccount))
        if not self.is_account_exist(new_account.name):
            self._accounts.append(new_account)

    def edit_account(self, name, new_account):
        assert (isinstance(new_account, MailAccount))
        dest_account_params = None
        for idx, item in enumerate(self._accounts):
            if item.name == name:
                dest_account_params = (idx, item)
                break
        if dest_account_params is None:
            raise ValueError('There is no account named %s inside ' \
                             'mail accounts database' % (name,))
        else:
            dest_idx, dest_item = dest_account_params
            del self._accounts[dest_idx]
            if not self.is_account_exist(new_account.name):
                self._accounts.insert(dest_idx, new_account)

    def is_account_exist(self, name):
        return bool(filter(lambda x: x.name == name, self._accounts))

    def remove_account(self, name):
        dest_account = filter(lambda x: x.name == name, self._accounts)
        if dest_account:
            self._accounts.remove(dest_account[0])
        else:
            raise ValueError('There is no account named %s inside mail ' \
                             'accounts database' % (name,))

    def __iter__(self):
        for account in self._accounts:
            yield (account.name, account.password)

    def __len__(self):
        return len(self._accounts)
