#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/cli/ctor/smtprelay.py#1 $

"""
    smtprelay
"""

import clictorbase
from clictorbase import IafCliConfiguratorBase, IafCliError, \
                        REQUIRED, DEFAULT
from sal.deprecated.expect import REGEX, EXACT
import sal.containers.yesnodefault as yesnodefault

DEBUG = True

class smtprelay(clictorbase.IafCliConfiguratorBase):

    newlines = 1

    class HostConfiguredError(IafCliError): pass
    class AuthConfigureError(IafCliError): pass

    def __init__(self, sess):
        IafCliConfiguratorBase.__init__(self, sess)
        self._set_local_err_dict({
             ('The host \S+ is already configured.', REGEX): \
                  self.HostConfiguredError,
             ('The host \S+ is not configured.', REGEX): \
                  self.HostConfiguredError,
             ('The passwords did not match.', EXACT) : \
                  self.AuthConfigureError,
             })

    def __call__(self):
        self._writeln('smtprelay')
        return self

    def new(self, host=REQUIRED):
        self._query_response('NEW')
        self._query_response(host)
        self._to_the_top(self.newlines)

    def edit(self, old_host=REQUIRED, new_host=DEFAULT):
        self._query_response('EDIT')
        self._query_response(old_host)
        self._query_response(new_host)
        self._to_the_top(self.newlines)

    def delete(self, host=REQUIRED):
        self._query_response('DELETE')
        self._query_response(host)
        self._to_the_top(self.newlines)

    def routingtable(self, table=DEFAULT):
        self._query_response('ROUTING TABLE')
        self._query_select_list_item(table)
        self._to_the_top(self.newlines)

    def auth(self, use_auth=DEFAULT, user=DEFAULT, password=DEFAULT):
        self._query_response('AUTH')
        self._query_response(use_auth)
        if yesnodefault.is_yes(use_auth):
            self._query_response(user)
            self._query_response(password)
            self._writeln(password)
        self._to_the_top(self.newlines)

if __name__ == '__main__':

    try:
        cli_sess
    except NameError:
        cli_sess = clictorbase.get_sess()

    sr = smtprelay(cli_sess)
    sr().new(host='foo.com')
    sr().edit(old_host='foo.com', new_host='bar.com')
    sr().delete(host='bar.com')
    sr().routingtable()
    sr().routingtable(table='Data')
    sr().routingtable(table='Management')
    sr().auth()
    sr().auth(use_auth=yesnodefault.YES, user='foo', password='bar')
