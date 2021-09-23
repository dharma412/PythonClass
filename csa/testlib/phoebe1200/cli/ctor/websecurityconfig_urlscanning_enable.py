#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1200/cli/ctor/websecurityconfig_urlscanning_enable.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $

import clictorbase
from clictorbase import REQUIRED, DEFAULT, NO_DEFAULT, IafCliParamMap
from sal.deprecated.expect import REGEX


class websecurityconfig_urlscanning_enable(clictorbase.IafCliConfiguratorBase):

    def __init__(self, sess):
        clictorbase.IafCliConfiguratorBase.__init__(self, sess)

    def __call__(self):
        self._writeln('websecurityconfig urlscanning enable')
        websecurityconfig_urlscanning_enable = self._wait_for_prompt()
        return self
