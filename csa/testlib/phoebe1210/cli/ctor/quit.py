#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1210/cli/ctor/quit.py#1 $
""" IAF Command Line Interface (CLI) configurator: quit
"""

import clictorbase
from sal.exceptions import ExpectError
from sal.containers.yesnodefault import YES, NO


class quit(clictorbase.IafCliConfiguratorBase):
    def __call__(self, yes_or_no=YES):
        self.clearbuf()
        self._writeln(self.__class__.__name__)
        try:
            idx = self._query('Are you sure you wish to exit?',
                              'Connection closed by foreign host',
                              'Connection to %s closed' \
                              % self._get_prompt().hostname)
        except ExpectError, e:
            if str(e).find('EOF during expect') >= 0:
                del self._sess
                return True
            raise

        if idx == 0:
            self._writeln(yes_or_no)
            try:
                self._query(self._get_prompt().single,
                            'Connection closed by foreign host',
                            'Connection to %s closed' \
                            % self._get_prompt().hostname)
            except ExpectError, e:
                if str(e).find('EOF during expect') >= 0:
                    del self._sess
                    return True
                raise

        return False


if __name__ == '__main__':
    import sethostname

    # session host defaults to .iafrc.DUT
    # DO NOT USE the CLI session object from the validator here
    # since we kill the session at the end of the test
    sess = clictorbase.get_sess()
    # test case
    sethostname.sethostname(sess)('bogushostname.com')
    cli = quit(sess)
    print 'do quit?', cli(NO)
    print 'do quit?', cli(YES)
