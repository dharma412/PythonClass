# $Id: //prod/main/sarf_centos/testlib/phoebe1300/cli/ctor/sdrstatus.py#1 $
# $DateTime: 2019/06/27 23:26:24 $
# $Author: aminath $

import clictorbase


class sdrstatus(clictorbase.IafCliConfiguratorBase):
    def __call__(self):
        cmd = 'sdrstatus'
        self._sess.writeln(cmd)
        sdrstatus = self._read_until()
        print sdrstatus
        return sdrstatus
