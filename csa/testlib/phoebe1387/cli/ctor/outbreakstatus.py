#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1350/cli/ctor/outbreakstatus.py#1 $ $DateTime: 2020/01/06 01:25:43 $ $Author: saurgup5 $

"""
SARF CLI command: outbreakstatus
"""
import clictorbase

class outbreakstatus(clictorbase.IafCliConfiguratorBase):
    def __call__(self):
        self._restart()
        self.clearbuf()
        self._writeln(self.__class__.__name__)
        raw = self._sess.read_until()
        if raw.find('Unknown command') > -1:
            raise clictorbase.IafUnknownCommandError
        return raw

if __name__ == '__main__':
    # session host defaults to .iafrc.DUT
    # use the existing CLI session from the validator, or create a new one
    try:
        cli_sess
    except NameError:
        cli_sess = clictorbase.get_sess()
    cli = outbreakstatus(cli_sess)
    # test case
    print cli()
