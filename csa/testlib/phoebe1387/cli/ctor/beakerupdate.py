# $Id: //prod/main/sarf_centos/testlib/phoebe1350/cli/ctor/beakerupdate.py#1 $
# $ $DateTime: 2020/01/17 04:04:23 $
# $Author: aminath $

import clictorbase


class beakerupdate(clictorbase.IafCliConfiguratorBase):
    def __call__(self, force=False):
        cmd = self.__class__.__name__
        if force:
            cmd += ' force'
        self._sess.writeln(cmd)
        self._wait_for_prompt()
