#!/usr/bin/python
# $Id: //prod/main/sarf_centos/testlib/zeus1380/cli/ctor/checkproxyrestart.py#1 $ $DateTime: 2020/05/25 00:19:30 $ $Author: sarukakk $

import clictorbase


class checkproxyrestart(clictorbase.IafCliConfiguratorBase):

    def __call__(self, cm_version):
        cmd = 'checkproxyrestart %s' % (cm_version,)
        self.clearbuf()
        self._writeln(cmd)
        return self._wait_for_prompt()


