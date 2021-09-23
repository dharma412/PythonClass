#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/phoebe1200/cli/ctor/ipcheck.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $

import clictorbase


class ipcheck(clictorbase.IafCliConfiguratorBase):
    def __call__(self):
        self.clearbuf()
        self._writeln(self.__class__.__name__)
        return self._wait_for_prompt()
