#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/cli/ctor/proxystat.py#1 $
# $DateTime: 2019/08/14 09:58:47 $
# $Author: uvelayut $

import clictorbase
import time

class proxystat(clictorbase.IafCliConfiguratorBase):
    """
    Display proxy statistics
    """
    def __call__(self):
        self.clearbuf
        self._writeln("proxystat")
        time.sleep(120)
        self._sess.interrupt()
        result = self._wait_for_prompt()
        return result
