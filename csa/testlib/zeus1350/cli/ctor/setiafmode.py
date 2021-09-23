#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1350/cli/ctor/setiafmode.py#1 $

# import clictorbase properly depending on automation or dev env
# if automation, import the classes and constants we'll need
import clictorbase as ccb

from sal.containers.yesnodefault import YES, NO


class setiafmode(ccb.IafCliConfiguratorBase):
    """setiafmode - enable or disable iaf mode
    """

    def __call__(self, enable):
        if enable:
            self._writeln('setiafmode 1')
        else:
            self._writeln('setiafmode 0')
        self._wait_for_prompt()


if __name__ == '__main__':
    # if cli_sess is already defined, we have a CLI session object from
    # the validator we can use; if not, we must create one
    try:
        cli_sess
    except NameError:
        cli_sess = ccb.get_sess()

    sim = setiafmode(cli_sess)
    sim(YES)
    sim(NO)
