#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1360/cli/ctor/suspend.py#1 $

import clictorbase

class suspend(clictorbase.IafCliConfiguratorBase):
    def __call__(self, delay=''):
        self.clearbuf()
        self._writeln(self.__class__.__name__)
        self._query_response(delay)
        if delay:
            timeout = int(delay) + 5
        else:
            timeout = 35
        return self._wait_for_prompt(timeout=timeout)

if __name__ == '__main__':
    import resume

    # session host defaults to .iafrc.DUT
    # if cli_sess is already defined, we have a CLI session object from
    # the validator we can use; if not, we must create one
    try:
        cli_sess
    except NameError:
        cli_sess = clictorbase.get_sess()

    cli = suspend(cli_sess)
    # test case
    print cli('50')
    print "Test passed, resuming delivery and listeners..."
    resume.resume(cli_sess)()
