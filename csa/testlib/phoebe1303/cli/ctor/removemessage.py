#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/phoebe1350/cli/ctor/removemessage.py#1 $ $DateTime: 2020/01/06 01:25:43 $ $Author: saurgup5 $

import clictorbase
from sal.containers.yesnodefault import YES, NO, is_yes, is_no

class removemessage(clictorbase.IafCliConfiguratorBase):
    def __call__(self, confirm=YES, MID=''):
        self.clearbuf()
        self._writeln(self.__class__.__name__)
        self._query_response(MID)
        notfoundstr = "MID %s not found." % MID
        idx = self._query(self._sub_prompt, notfoundstr)

        if idx == 0:
            self._writeln(confirm)
            return self._parse_lines(self._wait_for_prompt())
        elif idx == 1:
            self._wait_for_prompt()
            return notfoundstr

    def _parse_lines(self, raw):
        return '\n'.join(raw.splitlines()[2:-1])

