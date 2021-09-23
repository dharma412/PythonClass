#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1350/cli/ctor/showmessage.py#1 $ $DateTime: 2020/01/06 01:25:43 $ $Author: saurgup5 $

"""
IAF2 CLI command showmessage
"""

import clictorbase

class showmessage(clictorbase.IafCliConfiguratorBase):
    def __call__(self, mid=''):
        self.clearbuf()
        self._writeln(self.__class__.__name__)
        self._writeln(mid)
        return self._parse_lines(self._wait_for_prompt())

    def _parse_lines(self, raw):
        return '\n'.join(raw.splitlines()[2:-1])

if __name__ == '__main__':
    try:
        cli_sess
    except NameError:
        cli_sess = clictorbase.get_sess()

    print showmessage(cli_sess)(MID='1')

