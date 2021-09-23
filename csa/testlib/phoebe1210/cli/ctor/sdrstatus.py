# $Id: //prod/main/sarf_centos/testlib/phoebe1210/cli/ctor/sdrstatus.py#1 $
# $DateTime: 2019/05/07 03:16:10 $
# $Author: bimmanue $

import clictorbase


class sdrstatus(clictorbase.IafCliConfiguratorBase):
    def __call__(self):
        cmd = 'sdrstatus'
        self._sess.writeln(cmd)
        sdrstatus = self._read_until()
        print sdrstatus
        return sdrstatus
