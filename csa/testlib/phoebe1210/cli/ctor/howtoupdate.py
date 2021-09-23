#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1210/cli/ctor/howtoupdate.py#1 $
# $DateTime: 2019/05/07 03:16:10 $
# $Author: bimmanue $

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
