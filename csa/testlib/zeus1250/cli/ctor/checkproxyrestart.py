#!/usr/bin/python
# $Id: //prod/main/sarf_centos/testlib/zeus1250/cli/ctor/checkproxyrestart.py#3 $ $DateTime: 2019/06/07 02:45:52 $ $Author: sarukakk $

import clictorbase


class checkproxyrestart(clictorbase.IafCliConfiguratorBase):

    def __call__(self, cm_version):
        cmd = 'checkproxyrestart %s' % (cm_version,)
        self.clearbuf()
        self._writeln(cmd)
        return self._wait_for_prompt()


