#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1350/cli/ctor/howtoupdate.py#1 $
# $DateTime: 2020/01/06 01:25:43 $
# $Author: saurgup5 $

"""ESA Command Line Interface (CLI): howtoupdate
"""

import clictorbase

class howtoupdate(clictorbase.IafCliConfiguratorBase):

    def __call__(self):
        self.clearbuf()
        self._sess.writeln(self.__class__.__name__)
        howtoupdate = self._read_until()
        print howtoupdate
        return howtoupdate
