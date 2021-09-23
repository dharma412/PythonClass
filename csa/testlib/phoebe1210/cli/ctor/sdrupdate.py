# $Id: //prod/main/sarf_centos/testlib/phoebe1210/cli/ctor/sdrupdate.py#1 $
# $DateTime: 2019/05/07 03:16:10 $
# $Author: bimmanue $

import clictorbase


class sdrupdate(clictorbase.IafCliConfiguratorBase):
    def __call__(self, force=False):
        cmd = 'sdrupdate'
        if force:
            cmd += ' force'
        self._sess.writeln(cmd)
        self._wait_for_prompt()
