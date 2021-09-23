#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1362/cli/ctor/upgradeconfig.py#1 $

"""
IAF 2 CLI command: upgradeconfig
"""

import clictorbase


class upgradeconfig(clictorbase.IafCliConfiguratorBase):

    def __call__(self):
        self._writeln(self.__class__.__name__)
        return self._wait_for_prompt()


if __name__ == '__main__':
    # if cli_sess is already defined, we have a CLI session object from
    # the validator we can use; if not, we must create one
    try:
        cli_sess
    except NameError:
        cli_sess = clictorbase.get_sess()

    cli = upgradeconfig(cli_sess)
    print cli()

