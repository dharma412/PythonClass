# $Id: //prod/main/sarf_centos/testlib/phoebe1200/cli/ctor/sdrupdate.py#1 $
# $DateTime: 2019/03/22 01:36:06 $
# $Author: aminath $

import clictorbase


class sdrupdate(clictorbase.IafCliConfiguratorBase):
    def __call__(self, force=False):
        cmd = 'sdrupdate'
        if force:
            cmd += ' force'
        self._sess.writeln(cmd)
        self._wait_for_prompt()
