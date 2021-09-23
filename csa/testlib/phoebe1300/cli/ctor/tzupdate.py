#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1300/cli/ctor/tzupdate.py#1 $

"""
IAF Command Line Interface (CLI)

command:
    - tzupdate
"""

import clictorbase


class tzupdate(clictorbase.IafCliConfiguratorBase):

    def __call__(self, force=False):
        cmd = self.__class__.__name__
        if force:
            cmd += ' force'
        self._writeln(cmd)

        return self._wait_for_prompt()


if __name__ == '__main__':
    try:
        cli_sess
    except NameError:
        cli_sess = clictorbase.get_sess()

    cli = tzupdate(cli_sess)

    # test case
    print cli()
    print cli(True)
