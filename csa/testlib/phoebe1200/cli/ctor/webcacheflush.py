#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1200/cli/ctor/webcacheflush.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $

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
        self.matchObj = re.search(r'Web Security cache has been flushed', webcacheflush_output)
        return self.matchObj.group()
