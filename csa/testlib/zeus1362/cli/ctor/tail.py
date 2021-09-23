#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1362/cli/ctor/tail.py#1 $ $DateTime: 2020/06/10 22:29:20 $ $Author: sarukakk $

"""
    tail IAF 2 configurator
"""
import clictorbase
from clictorbase import IafCliConfiguratorBase, IafCliError, REQUIRED
from sal.deprecated.expect import EXACT

DEBUG = True


class tail(clictorbase.IafCliConfiguratorBase):

    class UnableToTailError(IafCliError): pass

    def __init__(self, sess):
        # use the correct scoping for IafCliConfiguratorBase
        # if NameError is thrown EXACT will need to be defined as well
        try:
            IafCliConfiguratorBase.__init__(self, sess)
        except NameError:
            self.IafCliConfiguratorBase.__init__(self, sess)

        self._set_local_err_dict({
             ('Unable to tail', EXACT) : self.UnableToTailError,
             })

    def __call__(self, log_name=REQUIRED,timeout=5):
        import time

        self._writeln('tail')
        self._query_select_list_item(log_name)
        time.sleep(timeout)
        self._sess.interrupt()
        out = self._read_until('^C')
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
    print tl(log_name='mail')

