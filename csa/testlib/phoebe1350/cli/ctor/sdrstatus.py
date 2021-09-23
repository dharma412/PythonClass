# $Id: //prod/main/sarf_centos/testlib/phoebe1350/cli/ctor/sdrstatus.py#1 $
# $DateTime: 2020/01/06 01:25:43 $
# $Author: saurgup5 $

import clictorbase

class sdrstatus(clictorbase.IafCliConfiguratorBase):
    def __call__(self):
        cmd = 'sdrstatus'
        self._sess.writeln(cmd)
        sdrstatus = self._read_until()
        print sdrstatus
        return sdrstatus
