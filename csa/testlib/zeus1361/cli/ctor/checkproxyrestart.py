#!/usr/bin/python
# $Id: //prod/main/sarf_centos/testlib/zeus1360/cli/ctor/checkproxyrestart.py#1 $ $DateTime: 2020/03/05 19:45:32 $ $Author: sarukakk $

import clictorbase


class checkproxyrestart(clictorbase.IafCliConfiguratorBase):

    def __call__(self, cm_version):
        cmd = 'checkproxyrestart %s' % (cm_version,)
        self.clearbuf()
        self._writeln(cmd)
        return self._wait_for_prompt()


