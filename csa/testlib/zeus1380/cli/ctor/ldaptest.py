#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1380/cli/ctor/ldaptest.py#1 $ $DateTime: 2020/05/25 00:19:30 $ $Author: sarukakk $

"""
CLI command: ldaptest
"""

import re

import clictorbase

from sal.containers.yesnodefault import YES, NO
from sal.exceptions import ConfigError

DEFAULT = clictorbase.DEFAULT


class ldaptest(clictorbase.IafCliConfiguratorBase):

    def __call__(self, input_dict=None, **kwargs):
        self._sess.writeln('ldaptest')
        mo = self._query('no LDAP queries configured', 'Select which')
        if mo == 0:
            return ["No LDAP queries configured"]
        param_map = clictorbase.IafCliParamMap(
            end_of_command='query test finished')

        param_map['query_to_test'] = ['query to test', DEFAULT, 1]
        # ldapaccept, ldapgroup, ldaprouting, masquerade, isqalias
        param_map['email_addr'] = ['Address to use in query', DEFAULT]
        # ldapgroup query
        param_map['group'] = ['Group name to use in query', DEFAULT]
        # isqauth and smtpauth
        param_map['uid'] = ['User identity to use in query', DEFAULT]
        # isqauth and smtpauth
        param_map['passwd'] = [
            re.compile('Password (to use in query)|(for testing LDAP bind)'),
            DEFAULT]
        param_map.update(input_dict or kwargs)

        sess = self._get_sess()
        sess.clearbuf()
        self._process_input(param_map)

        buf = sess.getbuf()
        patt = r'(.*query test results(?:.|\n)*query test finished\.)'
        mo = re.search(patt, buf)

        if not mo:
            raise ConfigError, 'Can not parse ldaptest output'

        return mo.group(1)


if __name__ == '__main__':
    # if cli_sess is already defined, we have a CLI session object from
    # the validator we can use; if not, we must create one
    # also import ldapconfig to set up a test server
    try:
        cli_sess
    except NameError:
        cli_sess = clictorbase.get_sess()
    import ldapconfig

    lt = ldaptest(cli_sess)
    # check negative case first
    result = lt(uid='admin')
    print result

    # set up ldap and test again
    lc = ldapconfig.ldapconfig(cli_sess)
    lc().new(server_name='PublicLDAP', port='389',
             host_name='trifolium.ironport.com')().ldapaccept(testing=NO)
    result = lt(uid='admin')
    print result

    # delete ldap setup before closing down
    lc().delete(name='PublicLDAP')

