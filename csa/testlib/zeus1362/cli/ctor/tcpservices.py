#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1361/cli/ctor/tcpservices.py#1
# $ $DateTime: 2020/06/10 22:29:20 $ $Author: sarukakk $

import clictorbase
from clictorbase import REQUIRED, DEFAULT, NO_DEFAULT, IafCliParamMap
import re

class tcpservices(clictorbase.IafCliConfiguratorBase):

    def __init__(self, sess):
        clictorbase.IafCliConfiguratorBase.__init__(self, sess)

    def __call__(self):
        """tcpservices cli command"""
        self._writeln(self.__class__.__name__)
        tcpservices = self._wait_for_prompt()
        return tcpservices


