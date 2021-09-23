# $Id: //prod/main/sarf_centos/testlib/phoebe1300/cli/ctor/sdrupdate.py#1 $
# $DateTime: 2019/06/27 23:26:24 $
# $Author: aminath $

import clictorbase


class sdrupdate(clictorbase.IafCliConfiguratorBase):
    def __call__(self, force=False):
        cmd = 'sdrupdate'
        if force:
            cmd += ' force'
        self._sess.writeln(cmd)
        self._wait_for_prompt()
