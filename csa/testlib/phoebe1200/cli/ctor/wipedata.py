#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1200/cli/ctor/wipedata.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $

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
        output = [y for y in (x.strip() for x in wipedatastatus_output.splitlines()) if y]
        return output[1]

    def coredump(self):
        self._query_response('coredump')
        wipedatacore_output = self._wait_for_prompt()
        self.matchObj = re.search(r'wipedata: In progress', wipedatacore_output)
        return self.matchObj.group()
