#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/cli/ctor/intrelay.py#1 $

"""
IAF 2 CLI command: intrelay
"""

import re
import clictorbase
from clictorbase import REQUIRED, DEFAULT, NO_DEFAULT
from sal.containers.yesnodefault import YES, NO, is_yes
from sal.deprecated.expect import REGEX
import clictorbase as ccb

class intrelay(clictorbase.IafCliConfiguratorBase):
    """intrelay
        - Update the internal SMTP relay hosts
    """

    class IntRelayError(ccb.IafCliError):
        pass

    def __init__(self, sess):
        ccb.IafCliConfiguratorBase.__init__(self, sess)
        self._set_local_err_dict(
            {
                ('is not configured', REGEX): self.IntRelayError,

            }
        )

    def __call__(self):
        self._writeln('intrelay')
        return self

    def new(self, host=None):
        self._query_response('NEW')
        self._query_response(host)
        self._to_the_top(1)

    def edit(self, old_host=None, new_host=''):
        self._query_response('EDIT')
        self._query_response(old_host)
        self._query_response(new_host)
        self._to_the_top(1)

    def delete(self, host=None):
        self._query_response('DELETE')
        self._query_response(host)
        self._to_the_top(1)

    def routing_table(self, table='Management'):
        self._query_response('ROUTING TABLE')
        self._query_select_list_item(table)
        self._to_the_top(1)

    def auth(self, use_auth=NO, username=None, password=None):
        self._query_response('AUTH')
        self._query_response(use_auth)
        if is_yes(use_auth):
            self._query_response(username)
            self._query_response(password)
            if password:
                self._writeln(password)
        self._to_the_top(1)

if __name__ == '__main__':
    # if cli_sess is already defined, we have a CLI session object from
    # the validator we can use; if not, we must create one
    try:
        cli_sess
    except NameError:
        cli_sess = clictorbase.get_sess()

    ir = intrelay(cli_sess)
    ir().new(host='foo.bar')
    ir().edit(old_host='foo.bar', new_host='bar.foo')
    ir().delete(host='bar.foo')
    ir().routing_table(table='Management')
    ir().auth()
    ir().auth(use_auth=YES)
    ir().auth(use_auth=YES, username='foo', password='bar')

