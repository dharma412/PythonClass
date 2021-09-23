#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/phoebe1200/cli/ctor/ldaptest.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $

from sal.exceptions import ConfigError
import re

import clictorbase

from sal.containers.yesnodefault import YES, NO

REQUIRED = clictorbase.REQUIRED
DEFAULT = clictorbase.DEFAULT


class ldaptest(clictorbase.IafCliConfiguratorBase):

    def __call__(self, input_dict=None, **kwargs):
        self._sess.writeln('ldaptest')
        mo = self._query('no LDAP queries configured', 'Select which')
        if mo == 0:
            raise ConfigError('No LDAP queries configured')

        param_map = clictorbase.IafCliParamMap(end_of_command='query test finished')
        param_map['query_to_test'] = ['query to test', DEFAULT, 1]
        # ldapaccept, ldapgroup, ldaprouting, masquerade, isqalias
        param_map['email_addr'] = ['Address to use in query', REQUIRED]
        # ldapgroup query
        param_map['group'] = ['Group name to use in query', REQUIRED]
        # isqauth and smtpauth
        param_map['uid'] = ['User identity to use in query', REQUIRED]
        # isqauth and smtpauth
        param_map['passwd'] = ['Passphrase to use in query', REQUIRED]
        # external auth
        param_map['bind_passwd'] = ['Passphrase for testing LDAP bind', REQUIRED]
        param_map.update(input_dict or kwargs)

        sess = self._get_sess()
        sess.clearbuf()
        self._process_input(param_map)

        buf = sess.getbuf()
        patt = r'(.*query test results(?:.|\n)*query test finished\.)'
        mo = re.search(patt, buf)
        if not mo:
            raise ConfigError('Can not parse ldaptest output')
        return mo.group(1)
