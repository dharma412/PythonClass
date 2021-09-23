#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1360/cli/ctor/resumetransfers.py#1 $

"""SARF Command Line Interface (CLI) configurator: resumetransfers
"""

import clictorbase

from sal.exceptions import ConfigError


class resumetransfers(clictorbase.IafCliConfiguratorBase):

    def __call__(self):
        self._writeln(self.__class__.__name__)
        self._expect('\n')
        cli_buf = self._wait_for_prompt()

        # verify output of the command
        if 'Transfers resumed' not in cli_buf:
            raise ConfigError('Transfers were not resumed')


if __name__ == '__main__':
    import suspendtransfers

    try:
        cli_sess
    except NameError:
        cli_sess = clictorbase.get_sess()

    suspendtransfers.suspendtransfers(cli_sess)()

    cli = resumetransfers(cli_sess)
    # test case
    cli()

