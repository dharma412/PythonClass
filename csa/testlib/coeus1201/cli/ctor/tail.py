#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/cli/ctor/tail.py#1 $

"""
    tail IAF 2 configurator
"""

import clictorbase
from clictorbase import IafCliConfiguratorBase, IafCliError, REQUIRED
from sal.deprecated.expect import EXACT
import time

DEBUG = True


class tail(clictorbase.IafCliConfiguratorBase):

    class UnableToTailError(IafCliError): pass

    def __init__(self, sess):
        IafCliConfiguratorBase.__init__(self, sess)
        self._set_local_err_dict({
             ('Unable to tail', EXACT) : self.UnableToTailError,
             })

    def __call__(self, log_name=REQUIRED, timeout=5):
        self._writeln('tail')
        self._query_select_list_item(log_name)
        time.sleep(timeout)
        ##New change in tail command needs CTRL+c and then q to get the DUT prompt
        self._sess.write('\x03')
        self._sess.write('q')
        out = self._read_until('>')
        self._wait_for_prompt()
        return out

if __name__ == '__main__':
    # if cli_sess is already defined, we have a CLI session object from
    # the validator we can use; if not, we must create one
    try:
        cli_sess
    except NameError:
        cli_sess = clictorbase.get_sess()

    tl = tail(cli_sess)
    for log in ('accesslogs', 'authlogs', 'bypasslogs', 'cli_logs', 'gui_logs',
                'status', 'system_logs', 'webrootlogs'):
        print tl(log_name='status')

