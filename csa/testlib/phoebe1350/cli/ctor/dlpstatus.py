#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1350/cli/ctor/dlpstatus.py#1 $ $DateTime: 2020/01/06 01:25:43 $ $Author: saurgup5 $

"""
CLI command - dlpstatus
"""

import clictorbase as ccb
from sal.deprecated.expect import EXACT,REGEX
from sal.containers.cfgholder import CfgHolder
import re

class dlpstatus(ccb.IafCliConfiguratorBase):

    def __call__(self):
        pat = "DLP should be enabled to run this command"
        self.clearbuf()
        self._sess.writeln('dlpstatus')
        self._wait_for_prompt()
        lines = self.getbuf()
        if lines.find(pat) >= 1:
            return pat
        mo = re.match('.*DLP Engine[\s+](?P<version>[\s\da-z\.]+)[\s+](?P<last_updated>[\w\d\s]+)[\'\r\n|\n\']+',lines,re.DOTALL)
        res = CfgHolder()
        res.version = mo.group('version').strip()
        res.last_updated = mo.group('last_updated').strip().strip('\n')
        return res
