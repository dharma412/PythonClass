#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1350/cli/ctor/webcacheflush.py#1 $ $DateTime: 2020/01/06 01:25:43 $ $Author: saurgup5 $

import clictorbase
import re
from clictorbase import REQUIRED, DEFAULT, NO_DEFAULT, IafCliParamMap

from sal.containers.yesnodefault import YES, NO

class webcacheflush(clictorbase.IafCliConfiguratorBase):

    def __init__(self, sess):
        clictorbase.IafCliConfiguratorBase.__init__(self, sess)

    def __call__(self):
        self._writeln('webcacheflush')
        webcacheflush_output = ''
        webcacheflush_output = self._wait_for_prompt()
        self.matchObj = re.search(r'Web Security cache has been flushed',webcacheflush_output)
        return self.matchObj.group()