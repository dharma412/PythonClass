#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1360/cli/ctor/suspendtransfers.py#1 $

"""SARF Command Line Interface (CLI) configurator: suspendtransfers
"""

import clictorbase

from sal.exceptions import ConfigError


class suspendtransfers(clictorbase.IafCliConfiguratorBase):

    def __call__(self):
        self._writeln(self.__class__.__name__)
        self._expect('\n')
        cli_buf = self._wait_for_prompt()

        # verify output of the command
        if 'Transfers suspended' not in cli_buf:
            raise ConfigError('Transfers were not suspended')


if __name__ == '__main__':
    import resumetransfers

    try:
        cli_sess
    except NameError:
        cli_sess = clictorbase.get_sess()

    cli = suspendtransfers(cli_sess)
    # test case
    cli()
    print "Test passed, resuming transfers..."
    resumetransfers.resumetransfers(cli_sess)()
