#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/phoebe1300/cli/ctor/ipcheck.py#1 $ $DateTime: 2019/06/27 23:26:24 $ $Author: aminath $

import clictorbase


class ipcheck(clictorbase.IafCliConfiguratorBase):
    def __call__(self):
        self.clearbuf()
        self._writeln(self.__class__.__name__)
        return self._wait_for_prompt()
