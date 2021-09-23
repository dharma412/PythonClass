#!/usr/bin/python
# $Id: //prod/main/sarf_centos/testlib/zeus1362/cli/ctor/checkproxyrestart.py#1 $ $DateTime: 2020/06/10 22:29:20 $ $Author: sarukakk $

import clictorbase


class checkproxyrestart(clictorbase.IafCliConfiguratorBase):

    def __call__(self, cm_version):
        cmd = 'checkproxyrestart %s' % (cm_version,)
        self.clearbuf()
        self._writeln(cmd)
        return self._wait_for_prompt()


