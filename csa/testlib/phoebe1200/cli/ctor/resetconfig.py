#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1200/cli/ctor/resetconfig.py#1 $
# $DateTime: 2019/03/22 01:36:06 $
# $Author: aminath $

"""
CLI command - resetconfig
"""

import clictorbase

from sal.exceptions import ConfigError
from common.util.systools import SysTools
from sal.containers.yesnodefault import YES


class resetconfig(clictorbase.IafCliConfiguratorBase):
    def __call__(self, dut, dut_version, timeout=900):
        """
        Resets the DUT configuration to a default set.
        """
        self.clearbuf()
        self._writeln('fipsconfig')
        self._to_the_top(1)
        buf = self.getbuf()
        self._writeln('resetconfig')
        idx = self._query('only works in the offline state',
                          'Are you sure you want to reset')
        if idx == 0:
            raise ConfigError, "not offline"
        elif idx == 1:
            self._query_response(YES)
            if buf.find("enabled") >= 1:
                self._writeln(YES)
                return SysTools(dut, dut_version).wait_until_dut_reboots(timeout)
        else:
            raise ConfigError, "resetconfig: unexpected response"
        self._wait_for_prompt(300)

    def DisableClusterMode(self):
        raise NotImplementedError


if __name__ == '__main__':
    dev_mode = False
    import suspend

    # session host defaults to .iafrc.DUT
    # if cli_sess is already defined, we have a CLI session object from
    # the validator we can use; if not, we must create one
    try:
        cli_sess
        dev_mode = True
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

    #  restore to a configured MGA if this isn't in dev mode
    if not dev_mode:
        from iafframework import iafcfg

        iafcfg.get_cfg().dut.configure()
