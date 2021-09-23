#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1200/cli/ctor/howtostatus.py#1 $
# $DateTime: 2019/03/22 01:36:06 $
# $Author: aminath $

"""ESA Command Line Interface (CLI): howtostatus
"""

import clictorbase


class howtostatus(clictorbase.IafCliConfiguratorBase):

    def __call__(self):
        self.clearbuf()
        self._sess.writeln(self.__class__.__name__)
        howtostatus = self._read_until()
        print howtostatus
        return howtostatus
