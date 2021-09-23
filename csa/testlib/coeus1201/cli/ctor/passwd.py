#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/cli/ctor/passwd.py#2 $
# $DateTime: 2019/11/20 00:33:52 $
# $Author: uvelayut $

"""
    IAF 2 CLI ctor - passwd
"""
import sys
import re

import clictorbase
from clictorbase import IafCliConfiguratorBase, IafCliError, REQUIRED
from sal.deprecated.expect import EXACT

TIMEOUT=10
DEBUG = True

class passwd(clictorbase.IafCliConfiguratorBase):

    class OldPwdWrongError(IafCliError): pass
    class WeakPwdError(IafCliError): pass
    newlines = 1

    def __init__(self, sess):
        IafCliConfiguratorBase.__init__(self, sess)
        self._set_local_err_dict({
             ('Old passphrase did not match', EXACT) : self.OldPwdWrongError,
             ('Following criteria for passphrase are not met:', EXACT) : self.WeakPwdError,
             })

    def __call__(self, old_pwd=REQUIRED, new_pwd=REQUIRED, abbrev=True):
        self.clearbuf()
        if abbrev:
            self._writeln('passwd')
        else:
            self._writeln('password')
        try:
            self._query("Old passphrase", timeout=TIMEOUT)
            self._writeln(old_pwd)
            self._query("New Passphrase", timeout=TIMEOUT)
            self._writeln(new_pwd)
            self._query("Please enter the new passphrase again", timeout=TIMEOUT)
            self._writeln(new_pwd)
            return self.getbuf()
        except:
            self.interrupt()
            exc_type, exc_value, exc_traceback = sys.exc_info()
            raise exc_type, exc_value, exc_traceback

if __name__ == '__main__':
    # if cli_sess is already defined, we have a CLI session object from
    # the validator we can use; if not, we must create one
    try:
        cli_sess
    except NameError:
        cli_sess = clictorbase.get_sess()

    pw = passwd(cli_sess)
    print pw(old_pwd='ironport', new_pwd='123456')
    print pw(old_pwd='123456', new_pwd='ironport', abbrev=False)
