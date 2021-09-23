#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1250/cli/ctor/resetconfig.py#3 $ $DateTime: 2019/06/07 02:45:52 $ $Author: sarukakk $

"""
CLI ctor - resetconfig
"""

import clictorbase

from sal.exceptions import ConfigError
from sal.containers.yesnodefault import YES, NO


class resetconfig(clictorbase.IafCliConfiguratorBase):

    def __call__(self, confirm=YES):
        """Resets the DUT configuration to a default set."""
        self._writeln('resetconfig')

        idx = self._query('only works in the offline state',
                          'Are you sure you want to reset')

        if idx == 0:
            raise ConfigError('DUT must be suspended first')
        elif idx == 1:
            self._query_response(confirm)
        else:
            raise ConfigError('resetconfig: unexpected response')

        self._wait_for_prompt(60)


if __name__ == '__main__':
    import suspend

    # session host defaults to .iafrc.DUT
    # if cli_sess is already defined, we have a CLI session object from
    # the validator we can use; if not, we must create one
    try:
        cli_sess
    except NameError:
        cli_sess = clictorbase.get_sess()

    reset_cfg = resetconfig(cli_sess)

    print 'resetconfig test before suspend '
    try:
        reset_cfg()
    except ConfigError, ce:
        if (str(ce).find('not offline') == 0):
            print 'Config error found, as expected in negative test case'
        else:
           raise

    print 'DONE!'

    suspend.suspend(cli_sess)()

    print 'resetconfig test after suspend'
    reset_cfg()
    print 'resetconfig DONE!'

    #  restore to a configured MGA
    from iafframework import iafcfg
    iafcfg.get_cfg().dut.configure()
