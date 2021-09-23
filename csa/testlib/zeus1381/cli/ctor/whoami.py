#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1380/cli/ctor/whoami.py#1 $

"""
IAF Command Line Interface (CLI)

command:
    - whoami
"""

import clictorbase

class whoami(clictorbase.IafCliConfiguratorBase):
    def __call__(self):
        self.clearbuf()
        self._writeln(self.__class__.__name__)
        raw = ''
        tries = 1
        # look for prompt up to five times
        # if we can't find whoami info the first time
        while raw.lower().find('username') == -1 and tries <= 5:
            raw += self._sess.read_until()
            tries += 1

        return raw