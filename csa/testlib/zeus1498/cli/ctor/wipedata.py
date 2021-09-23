#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1350/cli/keywords/wipedata.py
# $DateTime: 2020/05/28 03:18:30 $ $Author: mrmohank $

import clictorbase
from clictorbase import REQUIRED, DEFAULT, NO_DEFAULT, IafCliParamMap
import re

class wipedata(clictorbase.IafCliConfiguratorBase):

    def __init__(self, sess):
        clictorbase.IafCliConfiguratorBase.__init__(self, sess)

    def __call__(self):
        """Wipedata cli command"""
        self._writeln(self.__class__.__name__)
        return self

    def status(self):
        self._query_response('status')
        wipedatastatus_output = self._wait_for_prompt()
        output= [y for y in (x.strip() for x in wipedatastatus_output.splitlines()) if y]
        return output[1]

    def coredump(self):
        self._query_response('coredump')
        wipedatacore_output = self._wait_for_prompt()
        self.matchObj = re.search(r'wipedata: In progress',wipedatacore_output)
        return self.matchObj.group()
