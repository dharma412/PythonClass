# $Id: //prod/main/sarf_centos/testlib/phoebe1350/cli/ctor/sdrupdate.py#1 $
# $DateTime: 2020/01/06 01:25:43 $
# $Author: saurgup5 $

import clictorbase

class sdrupdate(clictorbase.IafCliConfiguratorBase):
    def __call__(self, force=False):
        cmd = 'sdrupdate'
        if force:
            cmd += ' force'
        self._sess.writeln(cmd)
        self._wait_for_prompt()
