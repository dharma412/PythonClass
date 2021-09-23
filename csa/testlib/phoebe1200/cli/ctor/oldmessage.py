#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1200/cli/ctor/oldmessage.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $

"""
SARF CLI command: oldmessage
"""

import clictorbase


class oldmessage(clictorbase.IafCliConfiguratorBase):
    def __call__(self):
        self.clearbuf()
        self._writeln(self.__class__.__name__)
        return self._parse_lines(self._wait_for_prompt())

    def _parse_lines(self, raw):
        return '\n'.join(raw.splitlines()[2:-1])


if __name__ == '__main__':
    try:
        cli_sess
    except NameError:
        cli_sess = clictorbase.get_sess()

    print oldmessage(cli_sess)()
