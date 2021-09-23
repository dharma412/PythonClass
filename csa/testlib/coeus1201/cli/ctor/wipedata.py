#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/cli/ctor/wipedata.py#1 $ 
# $DateTime: 2019/08/14 09:58:47 $ 
# $Author: uvelayut $

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
        #iRetruning actual out put since its return different value
        #self.matchObj = re.search(r'wipedata: In progress',wipedatacore_output)
        #return self.matchObj.group()
	return wipedatacore_output

if __name__ == '__main__':
    cli_sess = clictorbase.get_sess()
    wdata=wipedata(cli_sess)

    wdata().status()
    wdata().coredump()
